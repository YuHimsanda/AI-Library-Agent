import sys
import uuid
from pathlib import Path

import streamlit as st


# Make imports work when Streamlit launches this file from its subdirectory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

from agent import agent_executor


st.set_page_config(
	page_title="AI Library Assistant",
	page_icon="",
	layout="centered",
)


def reset_chat() -> None:
	st.session_state.thread_id = str(uuid.uuid4())
	st.session_state.messages = []


if "thread_id" not in st.session_state:
	reset_chat()

st.title(" AI Library Assistant")
st.caption("Search the catalogue, check availability, and reserve books.")

with st.sidebar:
	st.header("Library assistant")
	st.write("Ask about books or request a reservation. A Student ID is required to reserve a book.")
	if st.button("Start new chat", use_container_width=True):
		reset_chat()
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
