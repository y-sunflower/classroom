import streamlit as st

st.title("My first app")
st.write("Welcome to my app!")

name = st.number_input("Your name")

if st.button("Submit"):
    if name:
        st.success(f"Hello, {name}!")
    else:
        st.warning("Please enter your name.")
