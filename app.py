import streamlit as st
import sqlite3

# Database setup
DATABASE = "data.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Creates the student data table if it does not exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student_Data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            title TEXT,
            age INTEGER,
            nationality TEXT,
            registration_status TEXT,
            num_courses INTEGER,
            num_semesters INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Ensure DB is initialized
initialize_db()

# Streamlit UI
st.title("📋 Student Data Entry Form")

with st.form("student_form"):
    st.subheader("User Information")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    title = st.selectbox("Title", ["", "Mr.", "Ms.", "Dr."])
    age = st.number_input("Age", min_value=18, max_value=110, step=1)
    nationality = st.selectbox("Nationality", 
                               ["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America"])

    st.subheader("Course Information")
    registration_status = st.checkbox("Currently Registered")
    num_courses = st.number_input("Number of Completed Courses", min_value=0, step=1)
    num_semesters = st.number_input("Number of Semesters", min_value=0, step=1)

    st.subheader("Terms & Conditions")
    accepted = st.checkbox("I accept the terms and conditions.")

    submit_button = st.form_submit_button("Submit Data")

if submit_button:
    if not accepted:
        st.warning("⚠️ You must accept the terms and conditions.")
    elif not first_name or not last_name:
        st.warning("⚠️ First Name and Last Name are required.")
    else:
        # Convert registration status to string
        registration_status = "Registered" if registration_status else "Not Registered"

        # Insert into database
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Student_Data (firstname, lastname, title, age, nationality, 
            registration_status, num_courses, num_semesters) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, title, age, nationality, registration_status, num_courses, num_semesters))
        conn.commit()
        conn.close()

        st.success(f"✅ Student {first_name} {last_name} has been successfully added!")

# Display the data table
st.subheader("📜 Student Data Records")
conn = get_db_connection()
students = conn.execute("SELECT * FROM Student_Data").fetchall()
conn.close()

if students:
    st.write("### Registered Students")
    st.table(students)
else:
    st.info("No student records found.")
