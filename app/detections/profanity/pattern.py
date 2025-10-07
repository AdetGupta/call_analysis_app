import os
import re

from app.data_processing.processor import DataProcessor


def get_profanity_pattern():
    """"
    Gets all the profane words from profanity/profanity_words.txt then convert
    it into a regex pattern.
    """
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, 'profanity_words.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        profane_words = set(line.strip() for line in f if line.strip())

    profane_pattern = re.compile(r'\b(' + '|'.join(profane_words) + r')\b', re.IGNORECASE)
    return profane_pattern

def contains_profanity_regex(text):
    """
    Input: text(str)
    If there is any match with the profane pattern, return True
    """
    profane_pattern = get_profanity_pattern()
    return bool(profane_pattern.search(text))

def detect_profanity_regex(data: DataProcessor):
    """
    Traverse through a list of conversation between the agent and the customer
    to find if the agent was profane and/or the customer was profane.
    """
    transformed_conversation = data.transform()

    is_agent_profane = False
    is_customer_profane = False

    for message in transformed_conversation:
        if contains_profanity_regex(message['text']):
            if message['speaker'] == 'Agent':
                is_agent_profane = True
            if message['speaker'] == 'Customer':
                is_customer_profane = True


    return {"is_agent_profane": is_agent_profane, "is_customer_profane": is_customer_profane}

