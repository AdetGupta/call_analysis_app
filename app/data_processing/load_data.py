import os
import json
import yaml

def load_all_conversations(folder_path: str):
    """
        Load all YAML/JSON conversation files from a folder into a list.
        Also adds the call id to each conversation.

        Args:
            folder_path (str): Path to the folder containing conversation files.

        Returns:
            List[dict]: List of conversation objects.
    """

    all_conversations = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if file_name.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                conversation = json.load(f)

                #Adding call id to the conversation.
                call_id = {"call_id": file_name[:-5]}
                conversation.append(call_id)

        elif file_name.endswith(".yaml") or file_name.endswith(".yml"):
            with open(file_path, "r", encoding="utf-8") as f:
                conversation = yaml.safe_load(f)

                # Adding call id to the conversation.
                call_id = {"call_id": file_name[:-5]}
                conversation.append(call_id)
        else:
            continue

        all_conversations.append(conversation)

    return all_conversations



if __name__ == "__main__":
    all_conversations = load_all_conversations("All_Conversations_(1)")
    print(len(all_conversations))
    print(all_conversations[0])