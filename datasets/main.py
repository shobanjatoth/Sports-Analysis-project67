import streamlit as st
from app import app_main  # Importing the main app logic from app.py
from cricket import cricket_main  # Importing the cricket app logic from cricket.py

# Initialize session state for navigation
if "current_app" not in st.session_state:
    st.session_state.current_app = "Home"

# Function to navigate between apps
def navigate_to(app_name):
    st.session_state.current_app = app_name

# App navigation buttons
st.title("Multi-App Navigation")
col1, col2 = st.columns(2)

with col1:
    if st.button("Go to Olympic"):
        navigate_to("Home")
with col2:
    if st.button("Go to Cricket"):
        navigate_to("Cricket")

# Display the selected app
if st.session_state.current_app == "Home":
    st.title("Welcome to the Main App")
    app_main()  # Call the app logic from app.py
elif st.session_state.current_app == "Cricket":
    st.title("Welcome to the Cricket App")
    cricket_main()  # Call the app logic from cricket.py
        
         