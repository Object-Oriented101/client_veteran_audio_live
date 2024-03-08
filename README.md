## Overview

Purpose of project is to transcribe audio using an local embedding model. Server should be run on a high VRAM compute to account for Whisper (voice-to-text model). There are two client files to account for two use-cases. Use client_live to transcribe audio by the second (aka live). Client pause sends voice data after there is a pause...allowing for more accurate but slower transcription.

### server_socket.py

Run this file on the server. Use the setup_script.sh to install all necessary dependencies. 

## Client Live

Use when you want to transcribe client's voice within a second or two.

Key Parameters to adjust:
buffer_duration_ms = duration of buffer to fill up before sending to server
silence_threshold_seconds = how long to wait before sending audio data to server if the buffer duration is not met
rms_threshold = value from ~0-500 that determines the threshold to determine silence vs non-silence. The purpose of this parameter is to filter out background noise. You will need to adjust this based on your mic



