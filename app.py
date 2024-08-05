from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import sqlite3
import pandas as pd

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#loading google model to give question and prompt as input
# 
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text


def read_sql_query(sql,db):
    try:
        conn = sqlite3.connect(db)
        qry = conn.cursor()
        qry.execute(sql)
        rows = qry.fetchall()
        conn.commit()
        conn.close()
        for row in rows:
            return rows
        
    except sqlite3.Error as e:
        st.text(f"Sorry {e} ")
        return 0
            #  return f"SQL error: {e}"
    except Exception as e:
        st.text(f"Sorry  {e}")
        return 0



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
st.markdown('<h1 class="main-header">&emsp;My App To Retrive Medical Data</h1>', unsafe_allow_html=True)
# st.header("My App To Retrive Medical Data ")

data = {
    "Table Name": ["Patients", "Doctors", "Appointments", "Diagnosis", "Treatments", "Billing"],
    "Description": [
        "Stores patient details: ID, name, DOB, gender, address, phone, email",
        "Stores doctor details: ID, name, specialization, phone, email",
        "Stores appointment details: ID, patient ID, doctor ID, date, time, status",
        "Stores diagnosis details: ID, appointment ID, description, date diagnosed",
        "Stores treatment details: ID, diagnosis ID, description, date, cost",
        "Stores billing details: ID, patient ID, total amount, amount paid, billing date"
    ]
}

# Convert the data to a DataFrame
df = pd.DataFrame(data)
st.markdown("")
# Create the Streamlit app
st.text("Database Table Descriptions")

# Styling the DataFrame with CSS
styled_df = df.style.set_table_styles({
    'Table Name': [{'selector': 'td:hover', 'props': 'background-color: #f1f1f1;'}],
    'Description': [{'selector': 'td:hover', 'props': 'background-color: #f1f1f1;'}]
}).set_properties(**{
    'background-color': 'transparent',
    'color': 'white',
    'border-color': 'grey'
}).set_caption("Overview of Database Tables").set_table_attributes('style="width:100%; font-size:14px;"')

# Display the styled table
st.write(styled_df, unsafe_allow_html=True)



question=st.text_input("Input:",key="input",placeholder="Enter the Question")

submit=st.button("Get Query")
# st.subheader()
# st.header("Gemini App To Retrive SQL Data")

if submit:
    response=get_gemini_response(question,promt)
 
    data=read_sql_query(response,"medical.db")
    if(data==None):
            st.markdown(" SORRY NO DATA")  
    elif(data!=0):
        # st.text(f"The Query is : {response}")
        st.markdown(f'<p class="response-text">The Query is : *** {response}  ***</p>', unsafe_allow_html=True)
        st.subheader("The response Is : ")
        for row in data:
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
.response-text {
        font-size: 18px;
        color: white;
        font-family: Arial, sans-serif;
        background: rgb(91,12,238);
        background: linear-gradient(297deg, rgba(190,181,219,100) 27%, rgba(232,175,204,100) 100%);
        border-radius:30px;
            padding-left:30px;
    }

.main-header {
        font-size: 36px;
        color: white;
        # background-image: linear-gradient(#fe667, #ffa375);
        # background-color: rgba(201, 76, 76, 0.3);
        background: linear-gradient(297deg, rgba(190,181,219,100) 27%, rgba(232,175,204,100) 100%);
            border-radius:30px;

    }
</style>
""", unsafe_allow_html=True)
