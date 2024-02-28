import asyncio
import websockets
from pydub import AudioSegment
import io
import time

async def send_audio(file_path):
    uri = "ws://localhost:8888/ws"  # WebSocket server URI
    chunk_size = 1024 * 4  # 4KB chunk size, adjust as necessary

    # Convert mp3 file to wav
    audio = AudioSegment.from_file(file_path, format="mp3")
    # Export as wav and read bytes
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    print("Exported to wav")
    buffer.seek(0)
    wav_bytes = buffer.read()
    print("Read bytes")

    async with websockets.connect(uri) as websocket:
        print("Inside for loop")
        # Stream audio in chunks
        for i in range(0, len(wav_bytes), chunk_size):
            print("Sending audio packet")
            await websocket.send(wav_bytes[i:i+chunk_size])
            print("In between")
            transcription = await websocket.recv()
            print(f"Transcription: {transcription}")  # Print live transcription
            time.sleep(2)

# Replace 'sample_audio.mp3' with the path to your audio file
asyncio.run(send_audio("sample_audio.mp3"))
