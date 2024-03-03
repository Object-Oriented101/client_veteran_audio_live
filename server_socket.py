import whisper
import numpy as np
import torch
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

# Load Whisper model
model = whisper.load_model("base.en")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive audio data from client
            audio_data = await websocket.receive_bytes()

            # Convert audio bytes to NumPy array and transcribe
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            result = model.transcribe(audio_np, fp16=torch.cuda.is_available())
            text = result['text'].strip()

            # Send transcription back to client
            await websocket.send_text(text)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8888)
