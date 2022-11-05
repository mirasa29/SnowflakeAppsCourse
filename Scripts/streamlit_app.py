import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parent New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boilded Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.title('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# use remote csv file as fruit list
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# pick list for users to choose fruit/s
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruit_to_show = my_fruit_list.loc[fruit_selected]

# display the table on the page
streamlit.dataframe(fruit_to_show)

# function to get fruit data
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

    return fruityvice_normalized

# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
            streamlit.error('Please select a fruit to get information.')
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)

except URLError as error:
    streamlit.error()

streamlit.header("The fruit load list contains:")
# SF connection
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select fruit_name from pc_rivery_db.public.fruit_load_list")
         return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

# New section to accept input fruit to add
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
         return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

