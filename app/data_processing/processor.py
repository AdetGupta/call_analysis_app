from typing import List, Dict

from app.utils.data_utils import load_data
from app.utils.transform_utils import transform_text

import os


class DataProcessor:
    def __init__(self, file_path:str):
        self.file_path = file_path
        self.conversation = []
        self.call_id = os.path.splitext(os.path.basename(file_path))[0]
        self.load()

    def load(self):
        """
        Load all YAML/JSON conversation from a file into a list.
        Also adds the call id to the conversation.

        Returns:
            List[dict]: List of conversation objects.
        """
        self.conversation = load_data(self.file_path)

    def transform(self):
        """
            Message in the conversation labeled as text is
                lowercased,
                punctuation removed,
                stop words removed,
                stemmed.
            Returns transformed conversation list[dict]
        """
        transformed_conv = []
        for message in self.conversation:
            transformed_text = transform_text(message["text"])
            transformed_conv.append({**message, "text": transformed_text})
        return transformed_conv

    def messages(self, speaker:str = "agent")->List[Dict]:
        """
        Returns a list of all messages by the speaker.
        returns: List[dict]
        """
        all_messages = []
        for message in self.conversation:
            if message["speaker"].lower() == speaker:
                all_messages.append(message)
        return all_messages





