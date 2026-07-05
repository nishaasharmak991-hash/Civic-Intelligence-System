import streamlit as st
import os

st.title("🔐 Admin Login")

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_pass = os.getenv("ADMIN_PASSWORD", "admin123")

    if username == admin_user and password == admin_pass:

        st.session_state.admin_logged_in = True

        st.success("Login Successful")

        st.switch_page("pages/Admin.py")

    else:

        st.error("Invalid Username or Password")