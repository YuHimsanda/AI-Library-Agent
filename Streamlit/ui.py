import sys
import uuid
import sqlite3
import pandas as pd
from pathlib import Path
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agent import agent_executor

st.set_page_config(
    page_title="AI Library Assistant",
    page_icon="📚",
    layout="centered",
)

def reset_chat() -> None:
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    reset_chat()

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

st.title("AI Library Assistant")
st.caption("Search the catalogue, check availability, and reserve books.")

with st.sidebar:
    st.header("Library Assistant")
    st.write("Ask about books or request a reservation. A Student ID is required to reserve a book.")
    if st.button("Start new chat", use_container_width=True):
        reset_chat()
        st.rerun()
        
    st.divider()
    
    st.header("Admin Settings")
    if not st.session_state.admin_logged_in:
        admin_pass = st.text_input("Enter Password", type="password")
        if st.button("Log In"):
            if admin_pass == "kdu123":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Incorrect password!")
    else:
        st.success("Admin logged in.")
        if st.button("View All Reservations"):
            try:
                conn = sqlite3.connect("library.db")
                df = pd.read_sql_query("SELECT * FROM reservations", conn)
                conn.close()
                st.dataframe(df)
            except Exception as e:
                st.error("Error retrieving data.")
        if st.button("Log Out"):
            st.session_state.admin_logged_in = False
            st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about a book..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Checking the library..."):
            try:
                result = agent_executor.invoke(
                    {"messages": [("user", prompt)]},
                    config={
                        "configurable": {
                            "thread_id": st.session_state.thread_id
                        }
                    },
                )
                response = result["messages"][-1].content
                if isinstance(response, list):
                    response = "\n".join(
                        item.get("text", str(item))
                        if isinstance(item, dict)
                        else str(item)
                        for item in response
                    )
            except Exception as error:
                response = f"I couldn't reach the library assistant: {error}"

        st.markdown(response)
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )