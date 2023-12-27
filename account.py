import streamlit as st
import firebase_admin
from PIL import Image
from firebase_admin import credentials, auth

if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/Dinesh M/Desktop/front end/ids-fyp24-0985061c728c.json")
    firebase_admin.initialize_app(cred)
img_login = Image.open("images/bg.jpg").resize((300, 300))
def login():
    # Initialize session state if not present
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
            st.subheader("Login Section")
            email = st.text_input("Email")
            password = st.text_input("Password", type='password')

            if st.button("Login"):
                try:
                    user = auth.get_user_by_email(email)
                    #signed_in_user = auth.sign_in_with_email_and_password(email, password)
                    st.success("Login successful")
                    st.session_state.username = user.uid
                    st.session_state.useremail = user.email
                    st.session_state.signedout = True
                    st.session_state.signout = True
                except Exception as e:
                    st.warning("Login failed. Incorrect email or password.")
                    st.error(f"Error: {e}")
        else:
            st.subheader("Create New Account")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type='password')
            new_username = st.text_input("Unique Username")

            if st.button("Register"):
                try:
                    user = auth.create_user(email=new_email, password=new_password, uid=new_username)
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
