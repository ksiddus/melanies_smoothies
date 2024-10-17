# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie.
    """
)

#option = st.selectbox(
    #"What is your favorite fruit?",
   # ("Banana", "Strawberry", "Peaches"),
  #  index=None,
 #   placeholder="You selected ",
#)

#st.write("You selected:", option)
#
from snowflake.snowpark.functions import col
name_on_order = st.text_input("Name on Smoothie", "")
st.write("The name on your Smoothie will be : ", name_on_order)

session = get_active_session()
#cnx = st.connection("snowflake")
#session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))

#my_dataframe = session.table("smoothies.public.fruit_options")
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    'Choose upto 5 ingredients:'
    , my_dataframe
    ,max_selections = 5
    
)
if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredients_string  = ''
    for fruit_chosen in ingredient_list:
        ingredients_string  = ingredients_string +fruit_chosen + ' '

   # st.write(ingredients_string )
my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Great ' + name_on_order +   '! Your Smoothie is ordered!', icon="✅")

