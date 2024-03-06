import pyaudio
import websocket
import _thread as thread
import time
import json
import numpy as np

# just figure out to send the audio bytes as they come....use the bytes
pod_id = "sjz61aho9p5lyj"
SERVER_WS_URL = f"wss://{pod_id}-8888.proxy.runpod.net/ws"

buffer = bytearray()
overlap_buffer = bytearray()
buffer_duration_ms = 1000  # Target duration for each buffer in milliseconds
samples_per_frame = 1024
sample_rate = 16000
buffer_size = int((sample_rate / 1000) * buffer_duration_ms) * 2  # 2 bytes per sample for paInt16
overlap_size = buffer_size  # Overlap is the same size as the buffer
silence_threshold_seconds = 1.5  # How long to wait in silence before sending the buffer
last_send_time = time.time()  # Initialization of the global variable


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

def calculate_rms(audio_data):
    """Calculate the Root Mean Square of the audio data, safely handling edge cases."""
    # Ensure audio_data is not empty
    if not audio_data:
        return 0

    # Convert audio_data to a numpy array of int16
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # Ensure the array is not empty
    if audio_array.size == 0:
        return 0
    
    # Calculate the squared values to ensure non-negativity
    squared_audio = audio_array.astype(np.float32) ** 2
    
    # Calculate mean safely, ensuring the array contains finite numbers
    mean_squared = np.mean(squared_audio[np.isfinite(squared_audio)])
    
    # Calculate RMS, handling edge cases
    rms = 0
    if mean_squared > 0 and np.isfinite(mean_squared):
        rms = np.sqrt(mean_squared)
    
    return rms

def audio_stream_callback(in_data, frame_count, time_info, status):
    global buffer, overlap_buffer, last_send_time  # Declare as global inside the function
    rms_threshold = 200  # Adjust the RMS threshold based on your needs

    current_time = time.time()  # Get the current time

    # Your logic to calculate RMS and handle voice activity
    if calculate_rms(in_data) > rms_threshold:
        buffer.extend(in_data)
        
        # Logic to send data when the buffer is full or based on activity
        if len(buffer) >= buffer_size:
            send_buffer = overlap_buffer + buffer[:buffer_size]  # Combine overlap buffer and current buffer
            ws.send(send_buffer, opcode=websocket.ABNF.OPCODE_BINARY)
            
            # Update overlap buffer with the second half of the current buffer for the next overlap
            overlap_buffer = buffer[:buffer_size]  # Keep the first second as overlap
            buffer = buffer[buffer_size:]  # Remove the first second that was already included in send_buffer
            last_send_time = current_time  # Update the last send time

    # Additional condition to handle silence and send accumulated data
    elif current_time - last_send_time >= silence_threshold_seconds and len(buffer) > 0:
        send_buffer = overlap_buffer + buffer  # Send whatever is in the buffer
        ws.send(send_buffer, opcode=websocket.ABNF.OPCODE_BINARY)
        buffer = bytearray()  # Clear the main buffer
        overlap_buffer = bytearray()  # Clear the overlap buffer
        last_send_time = current_time  # Reset the last send time

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
        time.sleep(0.1)

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