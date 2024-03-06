#!/bin/bash

# Update system package lists
sudo apt-get update

# Install Vim, portaudio19-dev, ffmpeg, and netcat
sudo apt-get install -y vim portaudio19-dev ffmpeg netcat

# Create and activate a Python virtual environment
python3 -m venv env
source env/bin/activate

# Install Python packages from requirements.txt
pip install -r requirements.txt