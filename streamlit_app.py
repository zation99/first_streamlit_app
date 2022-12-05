import streamlit

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
code = '''def hello():
    print("Hello, Streamlit!")'''
streamlit.code(code, language='python')
