#!/bin/bash

# Update system package lists
sudo apt-get update

# Install Vim, portaudio19-dev, ffmpeg, and netcat
sudo apt-get install -y vim portaudio19-dev ffmpeg netcat

# Clone the Git repository
git clone https://github.com/Object-Oriented101/client_veteran_audio_live.git

# Create and activate a Python virtual environment
python3 -m venv env
source env/bin/activate

# Change directory to the cloned repository
cd client_veteran_audio_live

# Install Python packages from requirements.txt
pip install -r requirements.txt