import pyaudio
import websocket
import _thread as thread
import time
import json

# just figure out to send the audio bytes as they come....use the bytes
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

def audio_stream_callback(in_data, frame_count, time_info, status):
    ws.send(in_data, opcode=websocket.ABNF.OPCODE_BINARY)
    return (None, pyaudio.paContinue)

def run(*args):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024,
                    stream_callback=audio_stream_callback)
    stream.start_stream()

    while stream.is_active():
        # Keep the main thread alive.
        time.sleep(1)

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