# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd



# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

import streamlit as st
name_on_order = st.text_input("Name on smoothie:")
st.write("The name on smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_List = st.multiselect(
'Choose up to 5 ingresients',my_dataframe,max_selections=5)

if ingredients_List:
    if len(ingredients_List)<7:
        ingredients_string = ''
        for fruit_chosen in ingredients_List:
            ingredients_string += fruit_chosen+" "
            # st.write(pd_df['FRUIT_NAME'],fruit_chosen)
            search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
            st.subheader(fruit_chosen + ' Nutrition Information' )
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)    
    
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string +"""','""" +name_on_order+ """')"""
        # st.write(my_insert_stmt)
        # st.stop()
        time_to_insert = st.button("submit")
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
    else:
        st.error("Ingredients van not be more than 5")
