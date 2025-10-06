from app.utils.data_utils import load_data
from app.utils.transform_utils import transform_text

import os

class DataProcessor:
    def __init__(self, file_path:str):
        self.file_path = file_path
        self.conversation = []
        self.call_id = os.path.basename(file_path)
        self.load()

    def load(self):
        """
        Load all YAML/JSON conversation from a file into a list.
        Also adds the call id to the conversation.

        Returns:
            List[dict]: List of conversation objects.
        """
        self.call_id, self.conversation = load_data(self.file_path)

    def transform(self):
        """
            Message in the conversation labeled as text is
                lowercased,
                punctuation removed,
                stop words removed,
                stemmed.
        """
        for dialog in self.conversation:
            dialog["text"] = transform_text(dialog["text"])




