import streamlit as st
import json
import time

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        return {"error": str(e)}

def main():
    st.set_page_config(layout="wide")

    pause_transcription, live_transcription = st.columns(2)

    with pause_transcription:
        st.header("Transcription by Pause")
        pause_content = st.empty()

    with live_transcription:
        st.header("Transcription Live")
        live_content = st.empty()

    while True:
        content1 = load_json_file("json_files/history_pause.json")
        pause_content.json(content1)

        content2 = load_json_file("json_files/history_live.json")
        live_content.json(content2)

        time.sleep(0.1)

  

if __name__ == "__main__":
    main()
