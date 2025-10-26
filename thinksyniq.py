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

