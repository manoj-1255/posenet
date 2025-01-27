import streamlit as st
from users import authenticate_user, register_user
from plans import *
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

def register_page():
    st.title("Register")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", min_value=50, max_value=250)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=200)
    age = st.number_input("Age", min_value=10, max_value=100)

    if st.button("Register"):
        register_user(username, password, gender, height, weight, age)
        st.success("Registration successful! Please login.")
