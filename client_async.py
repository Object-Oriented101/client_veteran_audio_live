import asyncio
import websockets
import json

async def transcribe_audio(websocket_uri, file_path):
    async with websockets.connect(websocket_uri) as websocket:
        # Open the audio file in binary mode and send its content
        with open(file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            await websocket.send(audio_data)
            print("Audio data sent, waiting for transcription...")

        # Wait for the transcription result from the server
        transcription = await websocket.recv()
        return transcription

def main():
    pod_id = "xo3hx076k8dcke"
    websocket_uri = f"wss://{pod_id}-8888.proxy.runpod.net/ws"  # Change this to your WebSocket server URI
    file_path = 'sample_audio.mp3'  # Path to the audio file you want to transcribe

    # Run the async function in an event loop
    loop = asyncio.get_event_loop()
    transcription_result = loop.run_until_complete(transcribe_audio(websocket_uri, file_path))
    print(f"Transcription Result:\n{transcription_result}")

if __name__ == "__main__":
    main()
