import speech_recognition as sr
import requests
import sys

pod_id = "c78v86pkys859d"
SERVER_URL = f"https://{pod_id}-8888.proxy.runpod.net/transcribe" 

def record_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        
    return audio

def send_audio_to_server(audio):
    audio_data = audio.get_wav_data()
    files = {'file': audio_data}
    response = requests.post(SERVER_URL, files=files)
    return response.json()

def main():
    try:
        while True:
            audio = record_audio()
            transcription = send_audio_to_server(audio)
            print(transcription)
            print(transcription['transcription'])
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
