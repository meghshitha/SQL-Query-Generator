import sqlite3

##connect to sqlite
connection =sqlite3.connect("medical.db")

##create a cursor object to insert record ,create table and retrive
cursor=connection.cursor()

#create the table
table_info = """
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
"""
cursor.execute(table_info)

# Create Doctors table
table_info = """
CREATE TABLE IF NOT EXISTS Doctors (
    doctor_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    specialization VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100)
)
"""
cursor.execute(table_info)

# Create Appointments table
table_info = """
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
"""
cursor.execute(table_info)

# Create Diagnosis table
table_info = """
CREATE TABLE IF NOT EXISTS Diagnosis (
    diagnosis_id INTEGER PRIMARY KEY,
    appointment_id INTEGER,
    diagnosis_description VARCHAR(255),
    date_diagnosed DATE,
    FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id)
)
"""
cursor.execute(table_info)

# Create Treatments table
table_info = """
CREATE TABLE IF NOT EXISTS Treatments (
    treatment_id INTEGER PRIMARY KEY,
    diagnosis_id INTEGER,
    treatment_description VARCHAR(255),
    treatment_date DATE,
    cost DECIMAL(10, 2),
    FOREIGN KEY (diagnosis_id) REFERENCES Diagnosis(diagnosis_id)
)
"""
cursor.execute(table_info)

# Create Billing table
table_info = """
CREATE TABLE IF NOT EXISTS Billing (
    billing_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    total_amount DECIMAL(10, 2),
    amount_paid DECIMAL(10, 2),
    billing_date DATE,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
)
"""
cursor.execute(table_info)
 
 ##insert some more records
# Insert data into Doctors table
cursor.execute("INSERT INTO Doctors VALUES(101,'Dr.Rishab','Shetty','Cardiologist',8567493043,'rishab@email.com')")
cursor.execute("INSERT INTO Doctors VALUES(102,'Dr.Riya','Sharma','Neurologist',9972674512,'riya@email.com')")
cursor.execute("INSERT INTO Doctors VALUES(103,'Dr.Anushka','Sharma','Pediatrician',663321232,'asharma@email.com')")
cursor.execute("INSERT INTO Doctors VALUES(104,'Dr.Stephen','Joe','Orthopedic Surgeon',1234567890,'stephen@email.com')")
cursor.execute("INSERT INTO Doctors VALUES(105,'Dr.Joe','Fernandies','Dermatologist',5432167890,'fernandies@email.com')")

# Insert data into Patients table
cursor.execute("INSERT INTO Patients VALUES(261,'carry','N','1963-02-02','female','888 Whimsical Willow Lane, Willowville, IL 60001',5647382901,'carry@email.com')")
cursor.execute("INSERT INTO Patients VALUES(262,'Nick','carry','1965-05-13','male','666 Silent Brook Lane, Tranquil Town, IA 50301',6754893211,'nick@email.com')")
cursor.execute("INSERT INTO Patients VALUES(263,'John','clar','1961-10-20','male','777 Mystic Oak Grove, Oakwood, MA 02101',2314341546,'clar@email.com')")
cursor.execute("INSERT INTO Patients VALUES(264,'Natella','paul','1962-12-25','female','Amarvathi Nagar,Manglore',5682901473,'natella@email.com')")
cursor.execute("INSERT INTO Patients VALUES(265,'Guru','Kiran','1999-02-02','male','123,Gandhinagar,Benglore',3895546713,'guru@email.com')")

# Insert data into Appointments table
cursor.execute("INSERT INTO Appointments VALUES(1111,261, 101, '2024-07-03', '13:00:00', 'Scheduled')")
cursor.execute("INSERT INTO Appointments VALUES(1112,262, 106, '2024-07-12', '08:30:00', 'Scheduled')")
cursor.execute("INSERT INTO Appointments VALUES(1113,263, 103, '2024-06-28', '11:30:00', 'Completed')")
cursor.execute("INSERT INTO Appointments VALUES(1114,264, 105, '2024-06-29', '13:00:00', 'Scheduled')")
cursor.execute("INSERT INTO Appointments VALUES(1115,265, 106, '2024-07-08', '13:00:00', 'Scheduled')")

# Insert data into Diagnosis table
cursor.execute("INSERT INTO Diagnosis VALUES(111, 1113, 'Influenza (Flu),Fever', '2024-06-28')")
cursor.execute("INSERT INTO Diagnosis VALUES(112, 1114, 'Psoriasis,Red patches of skin', '2024-06-28')")
cursor.execute("INSERT INTO Diagnosis VALUES(113, 1116, 'Epilepsy,Recurrent seizures', '2024-06-26')")
cursor.execute("INSERT INTO Diagnosis VALUES(114, 1117, 'Influenza (Flu),Fever', '2024-06-08')")
cursor.execute("INSERT INTO Diagnosis VALUES(115, 1122, 'Angina Pectoris,Chest pain', '2024-06-20')")

# Insert data into Treatments table
cursor.execute("INSERT INTO Treatments VALUES(501,111,'Rehydration therapy','2024-06-29',15000)")
cursor.execute("INSERT INTO Treatments VALUES(502,112,'Topical treatments','2024-06-28',7000)")
cursor.execute("INSERT INTO Treatments VALUES(503,113,'Antiepileptic drugs (AEDs)','2024-06-27',25000)")
cursor.execute("INSERT INTO Treatments VALUES(504,114,'Antiviral medications,Rest and hydration','2024-06-12',5000)")
cursor.execute("INSERT INTO Treatments VALUES(505,115,'Nitroglycerin (to relieve chest pain)','2024-06-22',10000)")

# Insert data into Billing table
cursor.execute("INSERT INTO Billing VALUES(2001,263,15000,11000,'2024-06-29')")
cursor.execute("INSERT INTO Billing VALUES(2002,264,7000,7000,'2024-06-28')")
cursor.execute("INSERT INTO Billing VALUES(2003,266,25000,23000,'2024-06-27')")
cursor.execute("INSERT INTO Billing VALUES(2004,267,5000,5000,'2024-06-12')")
cursor.execute("INSERT INTO Billing VALUES(2005,272,10000,9500,'2024-06-22')")

##display all the records

print("the inserted records are")

data1=cursor.execute("select * from doctors")

for row in data1:
    print(row)
    
print("the inserted records are")

data2=cursor.execute("select * from patients")

for row in data2:
    print(row)
    
print("the inserted records are")

data3=cursor.execute("select * from appointments")

for row in data3:
    print(row)

print("the inserted records are")

data4=cursor.execute("select * from treatments")

for row in data4:
    print(row)
    
print("the inserted records are")

data5=cursor.execute("select * from diagnosis")

for row in data5:
    print(row)
    
print("the inserted records are")

data6=cursor.execute("select * from billing")

for row in data6:
    print(row)

connection.commit()

connection.close()

