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

# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
            streamlit.error('Please select a fruit to get information.')
    else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruityvice_normalized)

except URLError as error:
    streamlit.error()

# stop here
streamlit.stop()

# SF connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# New section to accept input fruit to add
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')

streamlit.write('Thanks for adding ', add_my_fruit)

# This will not work correctly, but just go with it for now
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")