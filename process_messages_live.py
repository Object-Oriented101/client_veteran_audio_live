import json
import time
import re  # Import the regular expressions library for removing punctuation

def load_messages(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    return data

def save_messages(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file)

def remove_punctuation(text):
    # Remove punctuation using regex
    return re.sub(r'[^\w\s]', '', text)

def append_new_words_only(history, new_message):
    # Convert to lowercase and remove punctuation for comparison
    history_words = remove_punctuation(history.lower()).split()[-10:]
    new_message_words = remove_punctuation(new_message.lower()).split()
    
    # Append only new words not found in the last 10 words of history
    updated_words = [word for word in new_message_words if word not in history_words]
    updated_history = ' '.join(history.split() + updated_words)
    return updated_history

def process_messages(messages_file_path, history_file_path):
    # Load history from history.json
    try:
        with open(history_file_path, "r") as file:
            history_data = json.load(file)
            history = history_data.get("history", "")
    except (FileNotFoundError, json.JSONDecodeError):
        history = ""

    messages = load_messages(messages_file_path)
    
    # Process each new message
    for message in messages:
        new_message = message["new_message"]
        history = append_new_words_only(history, new_message)
    
    # Save the updated history
    save_messages(history_file_path, {"history": history})
    
    # Update the file with unprocessed messages (empty in this case)
    save_messages(messages_file_path, [])

messages_file_path = "message_queue_live.json"
history_file_path = "history.json"

while True:
    process_messages(messages_file_path, history_file_path)
    # Adjust the sleep time as needed
    time.sleep(1)  # Check for new messages every second
