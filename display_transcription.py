import streamlit as st
import json
import time

file_path = "json_files/database.json"

def load_transcriptions():
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def display_messages(message_container, messages):
    message_container.empty()
    with message_container:
        for item in messages:
            st.text(item["message"])
def app():
    st.title("Live Transcriptions")
    data = load_transcriptions()
     # Display initial messages
    for item in data:
        st.text(item["message"])
    
    # Track the last known state of the data
    last_known_length = len(data)
    
    # Loop to refresh data
    while True:
        new_data = load_transcriptions()
        new_data_length = len(new_data)
        
        # Check if there are new messages
        if new_data_length > last_known_length:
            # Display only new messages
            for item in new_data[last_known_length:]:
                st.text(item["message"])
                
            # Update the last known data length
            last_known_length = new_data_length
        
        time.sleep(1)  # Wait for 1 second before checking for updates again

 
if __name__ == "__main__":
    app()