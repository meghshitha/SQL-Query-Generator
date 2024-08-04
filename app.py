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
 You are an expert in converting English questions to SQL queries. The code should not have ''' in the beginning and end and the word "sql" should not be included in the output. If an empty question is asked, just show all data in the database.

You are an expert in managing databases using SQL commands. The SQL database named 'medical' consists of several tables, including 'Patients', 'Doctors', 'Appointments', 'Diagnosis', 'Treatments', and 'Billing', each with specific columns.

Here's an example of the 'Patients' table contains:
1. Patients Table:
   - `patient_id`: Patient ID
   - `first_name`: First Name
   - `last_name`: Last Name
   - `date_of_birth`: Date of Birth
   - `gender`: Gender
   - `address`: Address
   - `phone_number`: Phone Number
   - `email`: Email

Here's an example of the 'Doctors' table contains:
2. Doctors Table:
   - `doctor_id`: Doctor ID
   - `first_name`: First Name
   - `last_name`: Last Name
   - `specialization`: Specialization
   - `phone_number`: Phone Number
   - `email`: Email

Here's an example of the 'Appointments' table contains:
3. Appointments Table:
   - `appointment_id`: Appointment ID
   - `patient_id`: Patient ID
   - `doctor_id`: Doctor ID
   - `appointment_date`: Appointment Date
   - `appointment_time`: Appointment Time
   - `status`: Status

Here's an example of the 'Diagnosis' table contains:
4. Diagnosis Table:
   - `diagnosis_id`: Diagnosis ID
   - `appointment_id`: Appointment ID
   - `diagnosis_description`: Diagnosis Description
   - `date_diagnosed`: Date Diagnosed

Here's an example of the 'Treatments' table contains:
5. Treatments Table:
   - `treatment_id`: Treatment ID
   - `diagnosis_id`: Diagnosis ID
   - `treatment_description`: Treatment Description
   - `treatment_date`: Treatment Date
   - `cost`: Cost

Here's an example of the 'Billing' table contains:
6. Billing Table:
   - `billing_id`: Billing ID
   - `patient_id`: Patient ID
   - `total_amount`: Total Amount
   - `amount_paid`: Amount Paid
   - `billing_date`: Billing Date

    Example 1: How many records are present in the 'Patients' table?
    The SQL command would look like this: "SELECT COUNT(*) FROM Patients;"

    Example 2: Show all the records in the 'Doctors' table.
    The SQL command would be something like: "SELECT * FROM Doctors;"

    Example 3: Retrieve the details of the 'Appointment' with ID 1113.
    The SQL command could be: "SELECT * FROM Appointments WHERE appointment_id=1113;"

    Example 4: List all the unique diagnosis descriptions in the 'Diagnosis' table.
    The SQL query might look like: "SELECT DISTINCT diagnosis_description FROM Diagnosis;"

    Example 5: Display the treatment descriptions and their costs from the 'Treatments' table.
    The SQL query would be: "SELECT treatment_description, cost FROM Treatments;"

    Example 6: Find the total amount billed and the amount paid for patient with ID 263.
    The SQL query could be: "SELECT total_amount, amount_paid FROM Billing WHERE patient_id=263;"


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