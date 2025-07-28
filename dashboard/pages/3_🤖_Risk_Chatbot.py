
import streamlit as st
import requests

st.set_page_config(
    page_title="SmartRxHub-Insights: Risk Chatbot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 SmartRxHub Chatbot")
st.markdown("##")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask the chatbot about patient data..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send message to FastAPI chatbot endpoint
    try:
        response = requests.post("http://127.0.0.1:8000/chat", params={"query": prompt})
        response.raise_for_status() # Raise an exception for HTTP errors
        chatbot_response = response.json().get("response", "Error: Could not get response from chatbot.")
    except requests.exceptions.RequestException as e:
        chatbot_response = f"Error connecting to chatbot: {e}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(chatbot_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
