from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#loading google model to give question and prompt as input
# 
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text


def read_sql_query(sql,db):
    conn=sqlite3.connect(db) 
    qry=conn.cursor()
    qry.execute(sql)
    rows=qry.fetchall()
    conn.commit()
    conn.close()

    for row in rows:
        print(row)
    return rows

# it defines the gemini ai that how u want to create the sql query
# by giving the example u are teaching it

# promt=[
#     """
#     you are expert in converting English question to SQL Query.
#     The Sql database haf the name CMS and the table as STUDENT and has the following columns-
#     s_name`, `s_reg`, `s_phno`, `s_sem`, `s_comb`, `s_pass`, `s_fees`, `s_balance` \n\n
#     for example 1: How many entires of records are present?
#     Then the sql comand will something like this " SELECT * FROM student;"
#     \nEXample 2: Tell me all the students who are studying in 1st sem ?
#     then the sql command will we be something like " SELECT * FROM student WHERE s_sem='1 SEM';"
#     and also code should not have ''' in the beginning and end and "sql" word in output \n
#     if empty question is asked just show all data in database
# """
# ]

promt=["""
       
you are expert in converting English question to SQL Query.The code should not have ''' in the beginning and end and "sql" word in output \n
if empty question is asked just show all data in database
You are an expert in managing databases using SQL commands. The SQL database named 'medical' consists of several tables, including 'Patients', 'Doctors', 'Appointments', 'Diagnosis', 'Treatments', and 'Billing', each with specific columns. 
Here's an example of the 'medical' table contains:
       
this is what my database consits of :
       



CREATE TABLE IF NOT EXISTS Patients (
    patient_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(10),
    address VARCHAR(255),
    phone_number VARCHAR(20),
    email VARCHAR(100)
)

CREATE TABLE IF NOT EXISTS Doctors (
    doctor_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    specialization VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100)
)

CREATE TABLE IF NOT EXISTS Appointments (
    appointment_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATE,
    appointment_time TIME,
    status VARCHAR(50),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
)

CREATE TABLE IF NOT EXISTS Diagnosis (
    diagnosis_id INTEGER PRIMARY KEY,
    appointment_id INTEGER,
    diagnosis_description VARCHAR(255),
    date_diagnosed DATE,
    FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id)
)

CREATE TABLE IF NOT EXISTS Treatments (
    treatment_id INTEGER PRIMARY KEY,
    diagnosis_id INTEGER,
    treatment_description VARCHAR(255),
    treatment_date DATE,
    cost DECIMAL(10, 2),
    FOREIGN KEY (diagnosis_id) REFERENCES Diagnosis(diagnosis_id)
)

CREATE TABLE IF NOT EXISTS Billing (
    billing_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    total_amount DECIMAL(10, 2),
    amount_paid DECIMAL(10, 2),
    billing_date DATE,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
)



    Example 1: How many records are present in the 'medical' table?
    The SQL command would look like this: "SELECT COUNT(*) FROM student;"

    Example 2: Show all the records in the 'notification' table.
    The SQL command would be something like: "SELECT * FROM notification;"


    Example 6: Find the total number of entries in the 'contact' table.
    The SQL query could be: "SELECT COUNT(*) FROM contact;"


"""]

# front end



st.set_page_config(page_title="Retrive Any Query From Database")
st.header("My App To Retrive Medical Data ")

question=st.text_input("Input:",key="input")

submit=st.button("Get Query")
# st.subheader()
# st.header("Gemini App To Retrive SQL Data")

if submit:
    response=get_gemini_response(question,promt)
    print(response)
    st.text(f"The Query is : {response}")
    # st.markdown(response)


    data=read_sql_query(response,"medical.db")
    st.subheader("The response Is : ")
    for row in data:
        print(row)
        # st.markdown(row)
        st.markdown(row)



st.markdown("""
<style>
.custom-text{
    color: black;
    font-size: 20px;
    font-family:Garamond;
}
st.text{
    color: red;
    font-size: 20px;
    font-family:Garamond;
}
</style>
""", unsafe_allow_html=True)