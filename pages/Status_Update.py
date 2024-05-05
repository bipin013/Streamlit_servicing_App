import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect(r"mechanics.db")
cursor = conn.cursor()

st.header("Update Mechanic Status")

# Mechanic selection
mechanic_options = ['Select Mechanic'] + [mechanic[1] for mechanic in cursor.execute("SELECT * FROM mechanics").fetchall()]
selected_mechanic = st.selectbox("Select Mechanic", mechanic_options,key="Mech_status_mechanic")

if selected_mechanic != 'Select Mechanic':
    mechanic_id = cursor.execute("SELECT ID FROM mechanics WHERE NAME = ?", (selected_mechanic,)).fetchone()[0]

    if st.button("Set Mechanic Status to Free"):
        cursor.execute("UPDATE mechanics SET STATUS = ?,EVENT_TIME = strftime('%H:%M', 'now', 'localtime') WHERE ID = ?", ('Free', mechanic_id))
        cursor.execute("UPDATE jobs SET job_status = ? WHERE mechanic_id = ?", ('Completed', mechanic_id))

        conn.commit()
        st.success(f"{selected_mechanic}'s status updated to 'Free'.")
    if st.button("Set Mechanic Status to 'On leave'"):
        cursor.execute("UPDATE mechanics SET STATUS = ?,EVENT_TIME = strftime('%H:%M', 'now', 'localtime') WHERE ID = ?", ('On leave', mechanic_id))
        conn.commit()
        st.success(f"{selected_mechanic}'s status updated to 'On leave'.")

st.header("Reassign Work")

job_options = ['Select Vehicle'] + [job[1] for job in cursor.execute("SELECT * FROM jobs WHERE job_status=='Pending'").fetchall()]
selected_job = st.selectbox("Select Vehicle", job_options,key="Reassign_work_Vehicle") 
#print(selected_job)

if selected_job != 'Select Vehicle':
    query = "SELECT id FROM jobs WHERE vehicle_number = '"+selected_job+"' AND job_status='Pending'"
    job_id = cursor.execute(query).fetchone()[0]
    selected_mech_id = cursor.execute("SELECT mechanic_id FROM jobs WHERE vehicle_number = ? AND job_status='Pending'", (selected_job,)).fetchone()[0]
    mechanic_reassign_opt = [mechanic[1] for mechanic in cursor.execute("SELECT * FROM mechanics WHERE STATUS=='Free'").fetchall()]
    reassign_mechanic = st.selectbox("Select Mechanic", mechanic_options,key="Reassign_work_mechanic")
    if reassign_mechanic != 'Select Mechanic':
        query = "SELECT ID FROM mechanics WHERE NAME = '"+reassign_mechanic+"'"
        reassign_mechanic_id = cursor.execute(query).fetchone()[0]
        if st.button("Reassign job"):
            cursor.execute("UPDATE mechanics SET STATUS = 'Free',EVENT_DATE = DATE('now'),EVENT_TIME = strftime('%H:%M', 'now', 'localtime') WHERE ID = ?", (selected_mech_id,))
            cursor.execute("UPDATE jobs SET mechanic_allocated = ?,mechanic_id = ? WHERE id = ?", (reassign_mechanic,reassign_mechanic_id,job_id,))
            cursor.execute("UPDATE mechanics SET STATUS = 'engaged',EVENT_DATE = DATE('now'),EVENT_TIME = strftime('%H:%M', 'now', 'localtime') WHERE ID = ?", (reassign_mechanic_id,))
            conn.commit()
            st.success("Job successfully reassigned")

