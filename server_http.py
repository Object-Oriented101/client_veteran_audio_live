from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import whisper
import numpy as np
import torch
import uvicorn

app = FastAPI()

# Load Whisper model
model = whisper.load_model("base")

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    audio_data = await file.read()

    # Convert audio bytes to NumPy array
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    # Transcribe audio
    result = model.transcribe(audio_np, fp16=torch.cuda.is_available())
    text = result['text'].strip()

    return JSONResponse(content={'transcription': text})

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8888)