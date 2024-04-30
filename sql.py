from dotenv import load_dotenv
load_dotenv()

import streamlit as st 
import os 
import psycopg2

import google.generativeai as genai 

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))
db_user ="postgres"
db = "hr"
hostname  = 'localhost'
pwd ='1234'
port_id = 5432

def get_gemini_response(question,prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0],question])
    return response.text


def read_sql_query(sql,db):
    connection  = psycopg2.connect(host = hostname,
                dbname =db,
                user = db_user,
                password=pwd,
                port=port_id)
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return rows
def add(x,y):
    z = x+y
    return


## define your prompt 

prompt =[
    """
    you are in expert in converting English Question to SQL Query
    The sql database has the name hr and has the folowing tables name - countries ,
    departments , employees , job_history , jobs , locations , regions 
    \n\n for example ,\nExample 1 - how many countries in there in the countries table ?
     The SQL Command will be SELECT DISTINCT(country_name) FROM countries;
     also the sql code shoild not have ''' in beginning or end and sql word in output
     
     """
]

st.set_page_config(page_title = 'I can Retrive any sql query')
st.header('gemini-App to retrieve SQL Data From Postgresql')
question = st.text_input("Input: " ,key = "input")

submit = st.button('Ask the Question')


if submit:
    response = get_gemini_response(question , prompt)
    response = read_sql_query(response,'hr')
    st.subheader('The response is')
    for row in response:
        print(row)
        st.header(row)