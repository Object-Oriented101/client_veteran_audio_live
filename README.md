## Overview

Purpose of project is to transcribe audio using an local embedding model. Server should be run on a high VRAM compute to account for Whisper (voice-to-text model). There are two client files to account for two use-cases. Use client_live to transcribe audio by the second (aka live). Client pause sends voice data after there is a pause...allowing for more accurate but slower transcription.

### Server (server_socket.py)

Run this file on the server. Use the setup_script.sh to install all necessary dependencies. Accepts socket connections from either client file.

### Client Live (client_live.py, process_messages_live.py, message_queue_live.json, history_live.json)

Use when you want to transcribe client's voice within a second or two (essentially live).

Key Parameters to adjust in client_live.py:
buffer_duration_ms = duration of audio data to fill up before sending to server. Lower buffer means faster (but less) accurate transcription
overlap_buffer = duration of previous buffer to include for better performance
silence_threshold_seconds = how long to wait before sending audio data to server if the buffer duration is not met
rms_threshold = value from ~0-500 that determines the threshold to determine silence vs non-silence. The purpose of this parameter is to filter out background noise. You will need to adjust this based on your mic

The client_live.py file saves data recieved from the server to a message queue (message_queue_live.json). The reason we are storing data in a queue is to process repeated data (previous second from the overlap buffer and the current second from buffer may cause same word to be transcribed twice).

We want to cut off any words that are repeated when the user sees the transcription. Hence, data saved in the message queue is checked with the previous 10 words (arbitrary choice based on personal testing) and any repeated words are cut off. This process happens inside process_messages_live.py. From there, data is saved to history_live.json, which is updated and displayed to the user.

### Client Pause (client_pause.py)

Implementation of voice-to-text with the assistance of the speech_recognition library. When a pause is detected, data is automatically send to the server. Recieving data is stored in history_pause.json (what the user sees)


### Streamlit App (streamlit_app.py)

streamlit_app.py is used for internal testing to compare the two transcription methods side by side. It is not needed to run the program.

### http
Kept the http files for client and server as a reference



