import json
import time
import re

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

# Remove punctuation using regex
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def append_new_words_only(history, new_message):
    history_words = remove_punctuation(history.lower()).split()[-10:]
    new_message_words = remove_punctuation(new_message.lower()).split()
    
    # Append only new words not found in the last 10 words of history
    updated_words = [word for word in new_message_words if word not in history_words]
    updated_history = ' '.join(history.split() + updated_words)
    return updated_history

def process_messages(messages_file_path, history_file_path):
    try:
        with open(history_file_path, "r") as file:
            history_data = json.load(file)
            history = history_data.get("history", "")
    except (FileNotFoundError, json.JSONDecodeError):
        history = ""

    messages = load_messages(messages_file_path)
    
    for message in messages:
        new_message = message["new_message"]
        history = append_new_words_only(history, new_message)
    
    save_messages(history_file_path, {"history": history})
    
    # Update the file with unprocessed messages
    save_messages(messages_file_path, [])


if __name__ == "__main__":
    messages_file_path = "json_files/message_queue_live.json"
    history_file_path = "json_files/history_live.json"

    while True:
        process_messages(messages_file_path, history_file_path)
        time.sleep(1)
