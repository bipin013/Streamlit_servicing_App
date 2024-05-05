import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta


# Function to mark rows as red if more than 2 hours have passed since making the job entry
def mark_red(row):
    entry_date = row['entry_date']
    entry_time = row['entry_time']
    entry_datetime = datetime.strptime(entry_date + ' ' + entry_time, "%Y-%m-%d %H:%M")
    if (datetime.now() - entry_datetime > timedelta(hours=2)) & (row['Job Status']!='Completed'):
        return ['background-color: red'] * len(row)
    elif row['Job Status']=='Completed':
        return ['background-color: lightgreen'] * len(row)
    else:
        return [''] * len(row)

# Retrieve job data from the database

conn = sqlite3.connect(r"mechanics.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM jobs")
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=["ID", "Vehicle Number", "Owner Name", "entry_date", "entry_time", "Owner Phone", "Owner Email", "Skills Required", "Remarks", "Job Status","Mechanic Allocated","Mechanic ID"])
df = df.loc[:,["Vehicle Number", "entry_date", "entry_time", "Owner Phone", "Skills Required", "Remarks", "Job Status","Mechanic Allocated"]]
# Apply conditional formatting to the DataFrame
styled_df = df.style.apply(mark_red, axis=1)
st.dataframe(styled_df,hide_index=True)

