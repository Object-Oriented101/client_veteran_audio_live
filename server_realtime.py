import whisper
import numpy as np
from fastapi import FastAPI, WebSocket
import uvicorn
import torch

app = FastAPI()

# Load Whisper model
model = whisper.load_model("tiny")  # Use a smaller model for potentially faster processing

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    audio_buffer = np.array([], dtype=np.float32)  # Initialize an empty buffer for audio
    expected_sample_rate = 16000  # Whisper expects 16 kHz sample rate
    chunk_duration = 0.5  # Duration of audio to process at once, in seconds
    chunk_size = int(expected_sample_rate * chunk_duration)  # Number of samples to process at once

    try:
        while True:
            # Receive audio data from client
            audio_data = await websocket.receive_bytes()

            # Convert audio bytes to NumPy array
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

            # Append to buffer
            audio_buffer = np.concatenate((audio_buffer, audio_np))

            # Process audio in chunks
            while len(audio_buffer) >= chunk_size:
                audio_chunk = audio_buffer[:chunk_size]
                audio_buffer = audio_buffer[chunk_size:]

                # Whisper expects audio as np.float32 in -1.0 to 1.0 range
                result = model.transcribe(audio_chunk, fp16=torch.cuda.is_available(), verbose=False)
                text = result['text'].strip()

                # Send transcription back to client
                await websocket.send_text(text)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8888)
