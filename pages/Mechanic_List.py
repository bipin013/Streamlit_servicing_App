import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect(r"mechanics.db")
cursor = conn.cursor()

# Create mechanics table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS mechanics
                  (ID INTEGER PRIMARY KEY,
                   NAME TEXT,
                   SKILLS TEXT,
                   STATUS TEXT DEFAULT 'Free',
               EVENT_DATE TEXT DEFAULT (date('now')),
    EVENT_TIME TEXT DEFAULT (time('now', 'localtime')))''')
conn.commit()

# Function to add mechanic to database
def add_mechanic(name, skills):
    skills_str = ','.join(skills)
    # Get today's date
    today_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("INSERT INTO mechanics (NAME, SKILLS, STATUS, EVENT_DATE, EVENT_TIME) VALUES (?, ?, ?, ?, ?)",
                   (name, skills_str, 'Free', today_date, '00:00:00'))
    conn.commit()
    st.success("Mechanic added successfully!")
def display_mechanics_table():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mechanics")
    rows = cursor.fetchall()
    print(rows)
    df = pd.DataFrame(rows, columns=["ID", "NAME", "SKILLS", "STATUS","EVENT_DATE","EVENT_TIME"])
    #df = df.loc[:,["ID", "NAME", "SKILLS", "STATUS","EVENT_TIME"]]
    
    # Apply conditional formatting to status column
    def highlight_status(status):
        if status == 'Free':
            return 'background-color: lightgreen'
        else:
            return 'background-color: red'
    
    styled_df = df.style.applymap(lambda x: highlight_status(x), subset=['STATUS'])
    st.dataframe(styled_df,hide_index=True)



# Streamlit UI
st.title("Worker Grid")

if st.button("Display Mechanics Table"):
    display_mechanics_table()

# Mechanic name input
name = st.text_input("Mechanic Name")

# Skills selection
selected_skills = st.multiselect("Select Skills", ['Engine Repair', 'Electrical', 'Tire Change', 'Brake Service', 'Tune-up'])

# Add mechanic button
if st.button("Add Mechanic"):
    if name == "":
        st.error("Please enter a mechanic name.")
    elif len(selected_skills) == 0:
        st.error("Please select at least one skill.")
    else:
        add_mechanic(name, selected_skills)

