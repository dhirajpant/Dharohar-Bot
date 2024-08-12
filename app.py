import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Dharohar Bot: An AI Chatbot",
    page_icon=":tourist:",
    layout="centered"
)

# Get the Google API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Function to get a time-based greeting
def get_time_based_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning!"
    elif 12 <= current_hour < 18:
        return "Good afternoon!"
    elif 18 <= current_hour < 22:
        return "Good evening!"
    else:
        return "Hello!"

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("Dharohar Bot")
st.subheader("A travelling guide chatbot")

# Sidebar inputs for user to provide location and type of places
st.sidebar.markdown('Fill these fields')
location = st.sidebar.text_input('Enter your location')
categories = [
    "Religious Destinations",
    "Cultural Destinations",
    "Amusement and Theme Parks",
    "Natural Destinations",
    "Adventure Destinations",
    "Wellness and Spa Destinations",
    "Casino and Bars"
]

# Create a multiselect box
place_type = st.sidebar.multiselect(
    "Select Travel Destination Categories:",
    categories
)
if st.sidebar.button("Suggest"):
    with st.spinner("Suggesting"):
        prompt = f"Suggest {place_type} places in {location}"
        gemini_response = st.session_state.chat_session.send_message(prompt)

        # Display Gemini-Pro's response in the main area
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


# Input field for user's message
user_prompt = st.chat_input("Ask me...")
initial_prompt = ("Imagine yourself as a traveling guide who will help people or tourists find various historical and natural places to visit nearby their locations in Nepal only. Remember to only answer questions related to tourism and natural places.Reply I dont know in case of other inputs and answer with just 4-5 places only.")

# Initial greeting message based on time
if not st.session_state.get('greeted', False):
    with st.chat_message("assistant"):
        st.markdown(f"{get_time_based_greeting()} Where can I guide you?")
    st.session_state.greeted = True

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    with st.spinner("Generating answers"):
        # Send the initial prompt to ensure context
        st.session_state.chat_session.send_message(initial_prompt)
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
st.write("© 2024 Dharohar.All rights reserved")