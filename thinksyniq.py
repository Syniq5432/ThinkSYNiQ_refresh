import streamlit as st
import pandas as pd

st.set_page_config(page_title="ThinkSYNiQ Dashboard", layout="wide")

st.markdown("<h1 style='text-align:center;color:#1E3A8A;'>ThinkSYNiQ</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#3B82F6;'>AI for Bosses</h3>", unsafe_allow_html=True)

tabs = st.tabs(["Customers", "Products", "Transactions", "Reports"])

with tabs[0]:
    st.subheader("Customer Management")
    st.write("Add, edit, or delete customer info here.")

with tabs[1]:
    st.subheader("Product Management")
    st.write("Manage your product catalog here.")

with tabs[2]:
    st.subheader("Transactions")
    st.write("Log and view transactions.")

with tabs[3]:
    st.subheader("Reports")
    st.write("Analytics and performance reports will appear here.")
