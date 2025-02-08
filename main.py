import os
import json
import streamlit as st
from groq import Groq

# Streamlit page configuration
st.set_page_config(
    page_title="CHATBOT",
    page_icon="💫",
    layout="centered"
)

# Load configuration data
working_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(working_dir, "config.json")

# Check if config file exists
if not os.path.exists(config_file_path):
    st.error("Configuration file not found. Please create a config.json file with your API key.")
    st.stop()

# Load the API key from the config file
with open(config_file_path) as config_file:
    config_data = json.load(config_file)

GROQ_API_KEY = config_data.get("GROQ_API_KEY")

# Check if the API key is present
if not GROQ_API_KEY:
    st.error("API key not found in config.json. Please ensure it is set correctly.")
    st.stop()

# Initialize the Groq client
try:
    client = Groq(api_key=GROQ_API_KEY)
except TypeError as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

# Initialize chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("ChatBot 💫✨")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask AI...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Prepare messages for the model
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        *st.session_state.chat_history
    ]

    # Get response from the model
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        assistant_response = response.choices[0].message.content
    except Exception as e:
        st.error(f"Error while getting response from the model: {e}")
        assistant_response = "Sorry, I couldn't process your request."

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
