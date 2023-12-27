import streamlit as st
import mysql.connector
from PIL import Image

# Establish connection to your local MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ids"
)
mycursor = mydb.cursor()
img_login = Image.open("images/bg.jpg").resize((300, 300))

def creation():
    def create_user_table():
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS ACCOUNT (
                email VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                phone VARCHAR(25) NOT NULL
            )
        """)
        mydb.commit()

    create_user_table()

    if 'username' not in st.session_state:
        st.session_state.username = ''

    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    if 'signedout' not in st.session_state:
        st.session_state.signedout = False

    if 'signout' not in st.session_state:
        st.session_state.signout = False

    if not st.session_state.signedout:
        st.title("User Authentication")
        choice = st.selectbox("Login/Signup", ["Login", "Register"])
        if choice == "Login":
            # Login Section
            st.subheader("Login Section")
            email = st.text_input("Email")
            password = st.text_input("Password", type='password')

            if st.button("Login"):
                try:
                    query = "SELECT * FROM ACCOUNT WHERE email = %s"
                    values = (email,)
                    mycursor.execute(query, values)
                    user = mycursor.fetchone()

                    if user:
                        if user[1] == password:  # Check if fetched password matches input password
                            st.success("Login successful")
                            st.session_state.username = user[2]  # Assuming username is at index 3
                            st.session_state.useremail = user[0]  # Assuming email is at index 1
                            st.session_state.signedout = True
                            st.session_state.signout = True
                        else:
                            st.warning("Login failed. Incorrect password.")
                    else:
                        st.warning("Login failed. Incorrect email.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            # Create New Account Section
            st.subheader("Create New Account")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type='password')
            new_username = st.text_input("Unique Username")
            new_name = st.text_input("Full Name")
            new_phone = st.text_input("Phone Number")

            if st.button("Register"):
                mycursor.execute(f"SELECT * FROM ACCOUNT WHERE username='{new_username}'")
                existing_user = mycursor.fetchone()
                if existing_user:
                    st.warning("Username already exists! Try a different one.")
                else:
                    try:
                        query = "INSERT INTO ACCOUNT (email, password, username, name, phone) VALUES (%s, %s, %s, %s, %s)"
                        values = (new_email, new_password, new_username, new_name, new_phone)
                        mycursor.execute(query, values)
                        mydb.commit()
                        st.success('Account created successfully!')
                        st.markdown("Login using your email and password")
                        st.balloons()
                    except Exception as e:
                        st.warning("Account creation failed.")
                        st.error(f"Error: {e}")

    if st.session_state.signout:
        st.image(img_login)
        st.subheader("Name: " + st.session_state.username)
        st.text("Email id:" + st.session_state.useremail)
        if st.button("Sign out"):
            st.session_state.signedout = False
            st.session_state.signout = False
            st.session_state.username = ''
            st.session_state.useremail = ''

