import streamlit as st
import sqlite3
import pandas as pd

st.title("Raviram Motors")

# Connect to SQLite database
#conn = sqlite3.connect(r"C:/Bipin/Streamlit_App/mechanics.db")
conn = sqlite3.connect(r"mechanics.db")


# Function to fetch skills from mechanics table
def fetch_skills():
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT skills FROM mechanics")
    rows = cursor.fetchall()
    skills = [skill for row in rows for skill in row[0].split(',')]
    skills = list(set(skills))

    return skills

# Function to create jobs table if it doesn't exist
def create_jobs_table():
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
                      (id INTEGER PRIMARY KEY,
                       vehicle_number TEXT,
                       owner_name TEXT,
                       entry_date TEXT,
                       entry_time TEXT,
                       owner_phone TEXT,
                       owner_email TEXT,
                       skills_required TEXT,
                       remarks TEXT,
                    job_status TEXT DEFAULT 'Pending',
                   mechanic_allocated TEXT DEFAULT 'Not allocated',
                   mechanic_id INTEGER DEFAULT 999)''')
    conn.commit()

# Streamlit UI
st.header("New Job Entry")

# Create jobs table if it doesn't exist
create_jobs_table()

# Function to add new job details to database
def add_job(vehicle_number, owner_name, entry_date, entry_time, owner_phone, owner_email, skills_required, remarks):
    cursor = conn.cursor()

    fetch_query = "SELECT ID, NAME, STATUS,EVENT_TIME FROM mechanics WHERE CONCAT(',', skills, ',') LIKE '%,"+",%' AND CONCAT(',', skills, ',') LIKE '%,".join(skills_required)+",%'"
    cursor.execute(fetch_query)
    mechanics = cursor.fetchall()

    free_mechanics = [mechanic for mechanic in mechanics if mechanic[2] == 'Free']

    free_mechanics.sort(key=lambda x: x[3])

    if free_mechanics:
        # Allocate job to the first mechanic in the sorted list
        allocated_mechanic = free_mechanics[0]
        mechanic_id = allocated_mechanic[0]
        mechanic_name = allocated_mechanic[1]

        # Update mechanic status to "engaged"
        cursor.execute("UPDATE mechanics SET status = ?,EVENT_DATE = DATE('now'),EVENT_TIME = strftime('%H:%M', 'now', 'localtime') WHERE id = ?", ('engaged', mechanic_id))
        cursor.execute("INSERT INTO jobs (vehicle_number, owner_name, entry_date, entry_time, owner_phone, owner_email, skills_required, remarks,mechanic_allocated,mechanic_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?)",
                   (vehicle_number, owner_name, entry_date, entry_time, owner_phone, owner_email, ", ".join(skills_required), remarks,mechanic_name,mechanic_id))
    
        conn.commit()
    else:
        cursor.execute("INSERT INTO jobs (vehicle_number, owner_name, entry_date, entry_time, owner_phone, owner_email, skills_required, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (vehicle_number, owner_name, entry_date, entry_time, owner_phone, owner_email, ", ".join(skills_required), remarks))
        conn.commit()
    st.success("Job details added successfully!")

# Job details input
vehicle_number = st.text_input("Vehicle Number")
owner_name = st.text_input("Owner Name")
entry_date = st.date_input("Date of Entry")
entry_time = st.time_input("Time of Entry")
owner_phone = st.text_input("Owner Phone Number")
owner_email = st.text_input("Owner Email")
skills = fetch_skills()
skills_required = st.multiselect("Skills Required", skills)
remarks = st.text_area("Remarks")

# Add job button
if st.button("Add Job"):
    if vehicle_number == "":
        st.error("Please enter the vehicle number.")
    elif owner_name == "":
        st.error("Please enter the owner name.")
    else:
        add_job(vehicle_number, owner_name, entry_date, entry_time.strftime("%H:%M"), owner_phone, owner_email, skills_required, remarks)

