from app.utils.data_utils import load_data
from app.utils.transform_utils import transform_text


class DataPreprocessor:
    def __init__(self, file_name:str):
        self.file_name = file_name
        self.conversation = []
        self.call_id = None
        self.load()

    def load(self):
        """
        Load all YAML/JSON conversation from a file into a list.
        Also adds the call id to the conversation.

        Returns:
            List[dict]: List of conversation objects.
        """
        self.call_id, self.conversation = load_data(self.file_name)

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




