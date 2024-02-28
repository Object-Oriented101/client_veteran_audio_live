import speech_recognition as sr
import websocket
import threading
import sys

try:
    import thread
except ImportError:
    import _thread as thread

pod_id = "a8gonqdtokxxyb"
#SERVER_URL = f"https://{pod_id}-8888.proxy.runpod.net/transcribe" 
SERVER_WS_URL = "wss://a8gonqdtokxxyb-8888.proxy.runpod.net/ws"  # Use wss:// for secure WebSocket connections


def on_message(ws, message):
    print("Received Transcription:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
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
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(SERVER_WS_URL,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
