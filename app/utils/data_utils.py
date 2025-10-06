import json
import yaml

def load_data(file_name: str):
        conversation = {}
        call_id = None
        if file_name.endswith(".json"):
            with open(file_name, "r", encoding="utf-8") as f:
                conversation = json.load(f)
                #Adding call id to the conversation.
                call_id = {"call_id": file_name[:-5]}

        elif file_name.endswith(".yaml") or file_name.endswith(".yml"):
            with open(file_name, "r", encoding="utf-8") as f:
                conversation = yaml.safe_load(f)

                # Adding call id to the conversation.
                call_id = {"call_id": file_name[:-5]}

        return call_id, conversation