import json
import yaml

def load_data(file_name: str):
        conversation = {}
        if file_name.endswith(".json"):
            with open(file_name, "r", encoding="utf-8") as f:
                conversation = json.load(f)

        elif file_name.endswith(".yaml") or file_name.endswith(".yml"):
            with open(file_name, "r", encoding="utf-8") as f:
                conversation = yaml.safe_load(f)

        return conversation

def get_message_from_speaker(speaker, conversation):
    all_messages = []
    for message in conversation:
        if message["speaker"].lower() == speaker:
            all_messages.append(message)
    return all_messages