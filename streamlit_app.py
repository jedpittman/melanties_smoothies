# Import python packages
import requests
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be', name_on_order)

#option = st.selectbox('What is your favorite fruit?', ('Banana', 'Strawberries', 'Peaches'))
#st.write('Your favorite fruit is:', option)

cnx=st.connection('snowflake')
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)



ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon").json()
    fv_df = st.dataframe(fruityvice_response.json(), use_container_width=true)
    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)
    my_insert_stmt = """insert into 
    smoothies.public.orders(ingredients, name_on_order) 
    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #SMOOTHIES.PUBLIC.MY_INTERNAL_STAGEst.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order + '!', icon="✅")




