import streamlit
import pandas

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
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# display the table on the page
streamlit.dataframe(my_fruit_list)

