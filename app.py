import streamlit as st
import requests
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# get webhook URL from .env
WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# create the title for the page
st.title("🤝 Your Personal Assistant")

# add subheader
st.subheader("What can your personal assistant do?")

st.markdown("""
1. Answer questions on various topics.  
2. Arrange Calendar events and meetings.  
3. Read your emails and send replies, can even summarize them for you.  
4. Manage your tasks and to-do lists.  
5. Take quick notes for you.  
6. Track your expenses and budgeting.  
""")

st.subheader("💬 Chat with your assistant")

# session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# input
user_message = st.chat_input()

if user_message:
    with st.chat_message("user"):
        st.markdown(user_message)
        st.session_state.messages.append({"role": "user", "content": user_message})

    # 🔥 check if webhook exists
    if not WEBHOOK_URL:
        st.error("Webhook URL not found. Please check your .env file.")
    else:
        try:
            response = requests.post(
                WEBHOOK_URL,
                json={"message": user_message}
            )

            res_json = response.json()

            # 🔥 safer parsing (fix your previous bug)
            if isinstance(res_json, list):
                ai_response = res_json[0].get("output", "No response")
            elif isinstance(res_json, dict):
                ai_response = res_json.get("output", str(res_json))
            else:
                ai_response = str(res_json)

        except Exception as e:
            ai_response = f"Error: {str(e)}"

        with st.chat_message("assistant"):
            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})