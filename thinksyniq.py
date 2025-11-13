# ThinkSYNiQ main app - refreshed
import streamlit as st
import pandas as pd

st.title("DEBUG BUILD - IF YOU SEE THIS, MAIN IS LIVE")

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

    # Auto-generate next Customer ID
    if not customers_df.empty and "Customer_ID" in customers_df.columns:
        last_id = customers_df["Customer_ID"].iloc[-1]
        try:
            last_num = int(last_id.replace("CUST", ""))
        except:
            last_num = len(customers_df)
        next_customer_id = f"CUST{last_num + 1:03d}"
    else:
        next_customer_id = "CUST001"

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

        if "Name" in customers_df.columns:
            customers_df = customers_df.drop(columns=["Name"])

        customers_df = pd.concat([customers_df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(customers_df, "data/customers.csv")
        st.success(f"Customer {customer_name} added successfully!")
        st.rerun()



# PRODUCTS TAB
with tabs[1]:
    st.subheader("Product Management")

    # Load product data
    products_df = pd.read_csv("data/products.csv")

    st.write("### Existing Products")
    st.dataframe(products_df)

    st.write("### Add or Edit Product")

    # Auto-generate next Product ID
    if not products_df.empty and "Product_ID" in products_df.columns:
        last_id = products_df["Product_ID"].iloc[-1]
        try:
            last_num = int(last_id.replace("PROD", ""))
        except:
            last_num = len(products_df)
        next_product_id = f"PROD{last_num + 1:03d}"
    else:
        next_product_id = "PROD001"

    # Input fields
    product_name = st.text_input("Product Name")
    product_description = st.text_area("Description", placeholder="Enter a short product description...")
    product_price = st.number_input("Price ($)", min_value=0.0, step=0.01)
    product_stock = st.number_input("Stock Quantity", min_value=0, step=1)

    if st.button("Add / Update Product"):
        new_row = {
            "Product_ID": next_product_id,
            "Product_Name": product_name,
            "Description": product_description,
            "Price": product_price,
            "Stock": product_stock
        }

        if "Name" in products_df.columns:
            products_df = products_df.drop(columns=["Name"])

        products_df = pd.concat([products_df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(products_df, "data/products.csv")
        st.success(f"Product '{product_name}' added successfully!")

# Clear input fields after submission
st.session_state["product_name"] = ""
st.session_state["product_description"] = ""
st.session_state["product_price"] = 0.0
st.session_state["product_stock"] = 0

st.rerun()



# --- TRANSACTIONS TAB ---
with tabs[2]:
    st.header("Add or Edit Transaction")

    customers = pd.read_csv("data/customers.csv")
    products = pd.read_csv("data/products.csv")
    transactions = pd.read_csv("data/transactions.csv")

    customer_names = customers["Customer Name"].tolist()
    product_names = products["Product Name"].tolist()

    # Form for adding a new transaction
    with st.form("add_transaction_form"):
        transaction_id = st.text_input("Transaction ID", f"TXN{len(transactions)+1:03d}")
        date = st.date_input("Date")
        customer = st.selectbox("Customer", customer_names)
        product = st.selectbox("Product", product_names)
        quantity = st.number_input("Quantity", min_value=1, value=1)

        if st.form_submit_button("Add Transaction"):
            product_price = float(products.loc[products["Product Name"] == product, "Price"].values[0])
            total = quantity * product_price

            new_txn = pd.DataFrame(
                [[transaction_id, date, customer, product, product_price, quantity, total]],
                columns=["Transaction ID", "Date", "Customer Name", "Product Name", "Price", "Quantity", "Total"]
            )
            transactions = pd.concat([transactions, new_txn], ignore_index=True)
            transactions.to_csv("data/Transactions.csv", index=False)
            st.success("Transaction added successfully!")

            # Clear input fields after submission
            st.session_state["Transaction ID"] = ""
            st.session_state["Date"] = None
            st.session_state["Customer"] = ""
            st.session_state["Product"] = ""
            st.session_state["Quantity"] = 1

    # Display Transaction History
    st.subheader("Transaction History")
    st.dataframe(transactions)


# --- REPORTS TAB ---
with tabs[3]:
    st.header("Reports Overview")

    # Load necessary data
    customers_df = pd.read_csv("data/customers.csv")
    transactions_df = pd.read_csv("data/transactions.csv")

    # Calculate totals safely
    total_revenue = transactions_df["Total"].sum() if "Total" in transactions_df.columns else 0
    total_customers = len(customers_df)
    total_transactions = len(transactions_df)

    # Display metrics
    st.metric("Total Revenue", f"${total_revenue:,.2f}")
    st.metric("Total Customers", total_customers)
    st.metric("Total Transactions", total_transactions)



# --- ThinkSYNiQ Customer Chatbot (Floating, Navy Theme) ---
import streamlit as st

# Only show chatbot on Customer tab
with tabs[0]:
    st.markdown(
        """
        <style>
        /* Floating chat button */
        #chat-button {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background-color: #0b1d39; /* Deep navy */
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 28px;
            cursor: pointer;
            box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.3);
            transition: 0.3s ease;
        }
        #chat-button:hover {
            background-color: #153061; /* Slightly lighter navy */
        }

        /* Chat window styling */
        .chat-window {
            position: fixed;
            bottom: 100px;
            right: 25px;
            background-color: #0b1d39;
            color: white;
            width: 320px;
            border-radius: 12px;
            box-shadow: 0px 3px 15px rgba(0, 0, 0, 0.4);
            padding: 15px;
            display: none;
        }
        .chat-window.show {
            display: block;
        }
        .chat-header {
            font-weight: bold;
            color: #f7c948; /* Gold accent */
            margin-bottom: 8px;
            text-align: center;
        }
        .chat-input {
            width: 100%;
            padding: 8px;
            border-radius: 8px;
            border: none;
            margin-top: 10px;
        }
        </style>

        <button id="chat-button">💬</button>
        <div class="chat-window" id="chat-window">
            <div class="chat-header">ThinkSYNiQ Support</div>
            <div id="chat-content">Hi there 👋<br>I'm still learning from Boss Lady Christie, but I'm ready to help!</div>
            <input class="chat-input" id="chat-input" placeholder="Type your question here..."/>
        </div>

        <script>
        const chatButton = document.getElementById("chat-button");
        const chatWindow = document.getElementById("chat-window");

        chatButton.addEventListener("click", function() {
            chatWindow.classList.toggle("show");
        });
        </script>
        """,
        unsafe_allow_html=True,
    )
