import streamlit as st
import pandas as pd

# ===================== MODE TOGGLE =====================
mode = st.radio("Select Mode", ["Admin", "Customer"], horizontal=True)

if mode == "Admin":
    st.title("👑 ThinkSYNiQ Admin Dashboard")
else:
    st.markdown("<h1 style='text-align:center; color:#1E3A8A;'>💼 Welcome to ThinkSYNiQ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px; color:#555;'>AI for Bosses — Smart Tools for Smarter Business</p>", unsafe_allow_html=True)
    st.markdown("---")

    cols = st.columns(3)
    products = [
        {"name": "AI Chat Assistant", "price": "$49.99/mo", "desc": "Automate your customer service 24/7."},
        {"name": "Analytics Dashboard", "price": "$79.99/mo", "desc": "Real-time data tracking and insights."},
        {"name": "Smart Scheduler", "price": "$39.99/mo", "desc": "Streamline appointments with AI reminders."},
    ]

    for i, col in enumerate(cols):
        with col:
            st.markdown(f"<div style='background-color:#f3f4f6; border-radius:12px; padding:20px; text-align:center; box-shadow:0 2px 10px rgba(0,0,0,0.1);'>"
                        f"<h3 style='color:#1E3A8A;'>{products[i]['name']}</h3>"
                        f"<p style='font-size:18px; color:#333;'>{products[i]['price']}</p>"
                        f"<p style='color:#555;'>{products[i]['desc']}</p>"
                        f"<button style='background-color:#1E3A8A; color:white; border:none; border-radius:8px; padding:10px 20px;'>Learn More</button>"
                        f"</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='text-align:center; color:#999;'>© 2025 ThinkSYNiQ — Built with 💙 by Boss Lady Christie</p>", unsafe_allow_html=True)
    st.stop()

# =======================================================


st.set_page_config(page_title="ThinkSYNiQ Dashboard", layout="wide")

st.markdown("<h1 style='text-align:center;color:#1E3A8A;'>ThinkSYNiQ</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#3B82F6;'>AI for Bosses</h3>", unsafe_allow_html=True)

import pandas as pd
from datetime import datetime

# ======== LOAD DATA FROM CSV FILES ========
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame()

customers_df = load_data("data/customers.csv")
products_df = load_data("data/products.csv")
transactions_df = load_data("data/transactions.csv")

# ======== SAVE UPDATED DATA BACK TO CSV ========
def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# ======== ADMIN TABS ========
st.sidebar.title("ThinkSYNiQ Admin Panel")
tabs = st.tabs(["Customers", "Products", "Transactions", "Reports"])

with tabs[0]:
    st.subheader("Customer Management")

    # Load customer data
    customers_df = pd.read_csv("data/customers.csv")

    st.write("### Existing Customers")
    st.dataframe(customers_df)

    st.write("### Add or Edit Customer")

# --- Add or Edit Customer ---

# Auto-generate next Customer ID
if not customers_df.empty and "Customer_ID" in customers_df.columns:
    # Extract numeric part safely
    last_id = customers_df["Customer_ID"].iloc[-1]
    try:
        last_num = int(last_id.replace("CUST", ""))
    except:
        last_num = len(customers_df)
    next_customer_id = f"CUST{last_num + 1:03d}"
else:
    next_customer_id = "CUST001"

st.text_input("Customer ID", value=next_customer_id, disabled=True, key="cust_id_auto")
customer_name = st.text_input("Customer Name")
email = st.text_input("Email")
phone = st.text_input("Phone")

if st.button("Add / Update Customer"):
    new_row = {
        "Customer_ID": next_customer_id,
        "Customer_Name": customer_name,
        "Email": email,
        "Phone": phone
    }

    # Drop any stray "Name" column before saving
    if "Name" in customers_df.columns:
        customers_df = customers_df.drop(columns=["Name"])

    customers_df = pd.concat([customers_df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(customers_df, "data/customers.csv")
    st.success(f"Customer {customer_name} added successfully!")


# PRODUCTS TAB
with tabs[1]:
    st.subheader("Manage Products")
    st.dataframe(products_df)

# TRANSACTIONS TAB
with tabs[2]:
    st.subheader("Transaction History")
    st.dataframe(transactions_df)

# REPORTS TAB
with tabs[3]:
    st.subheader("Reports Overview")
    total_revenue = transactions_df["Total"].sum() if "Total" in transactions_df.columns and not transactions_df.empty else 0
    st.metric("Total Revenue", f"${total_revenue:,.2f}")
    st.metric("Total Customers", len(customers_df))
    st.metric("Total Transactions", len(transactions_df))


# ===================== FLOATING CHATBOT =====================
import streamlit.components.v1 as components

chatbot_html = """
<style>
#chatbox {
  position: fixed;
  bottom: 25px;
  right: 25px;
  width: 320px;
  height: 420px;
  background-color: #111827;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(0,0,0,0.3);
  overflow: hidden;
  font-family: 'Arial';
}
#chatheader {
  background-color: #1E3A8A;
  color: white;
  text-align: center;
  padding: 10px;
  font-weight: bold;
}
#chatbody {
  height: 330px;
  overflow-y: auto;
  padding: 10px;
  color: white;
}
#chatinput {
  width: 100%;
  border: none;
  outline: none;
  padding: 10px;
  box-sizing: border-box;
  background-color: #f3f4f6;
}
</style>

<div id="chatbox">
  <div id="chatheader">💬 ThinkSYNiQ Assistant</div>
  <div id="chatbody"></div>
  <input id="chatinput" placeholder="Type your message..." />
</div>

<script>
const input = document.getElementById("chatinput");
const body = document.getElementById("chatbody");
input.addEventListener("keypress", async function(e){
  if(e.key === "Enter" && input.value.trim() !== ""){
    const userMsg = input.value;
    body.innerHTML += `<p><b>You:</b> ${userMsg}</p>`;
    input.value = "";
    setTimeout(() => {
      body.innerHTML += `<p><b>ThinkSYNiQ:</b> I'm still learning from Boss Lady Christie — but I'm ready to help!</p>`;
      body.scrollTop = body.scrollHeight;
    }, 600);
  }
});
</script>
"""

components.html(chatbot_html, height=500)
# ===========================================================

