import speech_recognition as sr
import websocket
import _thread as thread
import json
import time

# just figure out to send the audio bytes as they come


pod_id = "sjz61aho9p5lyj"
SERVER_WS_URL = f"wss://{pod_id}-8888.proxy.runpod.net/ws"

def save_message(message):
    file_path = "database.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append({"message": message})

    with open(file_path, "w") as file:
        json.dump(data, file)

def on_message(ws, message):
    print("Received Transcription:", message)
    save_message(message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("### CONNECTION CLOSED ###")

def run(*args):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        while True:
            start_time = time.time()
            # Record audio for 3 seconds
            audio = recognizer.record(source, duration=2)
            audio_data = audio.get_wav_data()
            ws.send(audio_data, opcode=websocket.ABNF.OPCODE_BINARY)
            # Adjust for any time taken to process and send the audio
            time_taken = time.time() - start_time
            if time_taken < 2:
                time.sleep(2 - time_taken)

def on_open(ws):
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(SERVER_WS_URL,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
