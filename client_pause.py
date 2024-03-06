import speech_recognition as sr
import websocket
import _thread as thread
import json

pod_id = "28erl462homow7"
SERVER_WS_URL = f"wss://{pod_id}-8888.proxy.runpod.net/ws"

# Have two proccesses: time-based + pause based...
# if no bytes...turn it off

def save_message(message):
    file_path = "json_files/history_pause.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    
    if data == []:
        data = {"history" : message}
    else:
        data = {"history" : data["history"] + message}

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
                try:
                    audio = recognizer.listen(source)
                    audio_data = audio.get_wav_data()
                    ws.send(audio_data, opcode=websocket.ABNF.OPCODE_BINARY)
                except Exception as e:
                    print("Listening stopped:", e)
                    break
        ws.close()
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
