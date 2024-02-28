import asyncio
import websockets
from pydub import AudioSegment
import io
import time

async def send_audio(file_path):
    pod_id = "xo3hx076k8dcke"
    uri = f"wss://{pod_id}-8888.proxy.runpod.net/ws"  # WebSocket server URI
    chunk_size = 1024 * 4  # 4KB chunk size, adjust as necessary

    # Convert mp3 file to wav
    audio = AudioSegment.from_file(file_path, format="wav")
    # Export as wav and read bytes
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    wav_bytes = buffer.read()

    async with websockets.connect(uri) as websocket:
        # Stream audio in chunks
        for i in range(0, len(wav_bytes), chunk_size):
            await websocket.send(wav_bytes[i:i+chunk_size])
            transcription = await websocket.recv()
            print(f"Transcription: {transcription}")  # Print live transcription
            time.sleep(2)

# Replace 'sample_audio.mp3' with the path to your audio file
asyncio.run(send_audio("sample_audio.wav"))