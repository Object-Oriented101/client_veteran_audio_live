import whisper 
import numpy as np 
from fastapi import FastAPI, WebSocket 
import uvicorn 
import torch 
 
app = FastAPI() 
 
# Load Whisper model 
model = whisper.load_model("base") 
 
@app.websocket("/ws") 
async def websocket_endpoint(websocket: WebSocket): 
    await websocket.accept() 
    audio_buffer = np.array([], dtype=np.float32)  # Initialize an empty buffer for audio 
    expected_sample_rate = 44100  # Assuming 16 kHz sample rate 
    buffer_duration = 1  # Buffer audio for 1 second before processing 
    buffer_size = expected_sample_rate * buffer_duration  # Calculate buffer size needed for 1 second of audio 
 
    try: 
        while True: 
            # Receive audio data from client 
            audio_data = await websocket.receive_bytes() 
            # Convert audio bytes to NumPy array 
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0 
            # Append to buffer 
            audio_buffer = np.concatenate((audio_buffer, audio_np)) 
 
            # Check if we have 1 second of audio for processing 
            if len(audio_buffer) >= buffer_size: 
                # Process the first 1 second of buffered audio 
                audio_to_process = audio_buffer[:buffer_size] 
                result = model.transcribe(audio_to_process, fp16=torch.cuda.is_available()) 
                text = result['text'].strip() 
 
                # Send transcription back to client 
                await websocket.send_text(text) 
                 
                # Remove the processed audio from the buffer, keeping any excess for the next batch 
                audio_buffer = audio_buffer[buffer_size:] 
                 
    except Exception as e: 
        print(f"Error: {e}") 
    finally: 
        await websocket.close() 
 
if __name__ == '__main__': 
    uvicorn.run(app, host="0.0.0.0", port=8888) 