import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header("Breakfast favorites")
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruites_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruites_to_show = my_fruit_list.loc[fruites_selected]

# Display the table on the page.
streamlit.dataframe(fruites_to_show)


def get_fruityvice_data(chosen_fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+chosen_fruit)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please choose a fruit")
  else:
    fruityvice_data = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_data)
except URLError as e:
  streamlit.error()
      

streamlit.header("See our fruit list. Add your favorite!")

def get_fruit_load_list(cnx):
  with cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    all_data = my_cur.fetchall()
    return all_data
  
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list(my_cnx)
  my_cnx.close()
  streamlit.header("The fruit load list contains:")
  streamlit.dataframe(my_data_row)


def insert_row_snowflake(new_fruit, cnx):
  with cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list VALUES('%s')"%(new_fruit))
    return "Thanks for adding "+new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  insert_res = insert_row_snowflake(add_my_fruit, my_cnx)
  my_cnx.close()
  streamlit.write(insert_res)


