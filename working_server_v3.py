from fastapi import FastAPI, WebSocket
import numpy as np
import whisper
import torch
import asyncio

app = FastAPI()

model_name = "base"  # Adjust as necessary
audio_model = whisper.load_model(model_name)

async def transcribe_audio(audio_np, model):
    # This function runs the blocking transcription operation in a separate thread
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, lambda: model.transcribe(audio_np, fp16=torch.cuda.is_available()))
    print("transcription completed in function")
    return result

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    transcription = []

    try:
        while True:
            print("Beg of loop")
            audio_data = await websocket.receive_bytes()
            print("Bytes recieved")
            if len(audio_data) % 2 != 0:
                audio_data += b'\x00'  # Ensure buffer size is a multiple of element size
            print("Bytes is multiple of 2")

            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            print("Converted to np")

            # Use asyncio.to_thread or run_in_executor to run transcription asynchronously
            result = await transcribe_audio(audio_np, audio_model)
            print(f"Result recieved: {result}")

            text = result['text'].strip()

            transcription.append(text)
            await safe_send_text(websocket, '\n'.join(transcription))
            print("Result sent")
    except asyncio.CancelledError:
        print("WebSocket connection cancelled.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if transcription:
            await safe_send_text(websocket, "Final Transcription:\n" + '\n'.join(transcription))
        await websocket.close()

async def safe_send_text(websocket: WebSocket, text: str):
    try:
        await websocket.send_text(text)
    except RuntimeError as e:
        print(f"Failed to send message: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)