import re

from app.data_processing.preprocessor import DataPreprocessor


def get_profanity_pattern():
    """"
    Gets all the profane words from data/profanity_words.txt then convert
    it into a regex pattern. That way it is easy to search for the said
    pattern in the text files.
    """
    with open('./data/profanity_words.txt', 'r', encoding='utf-8') as f:
        PROFANE_WORDS = set(line.strip() for line in f if line.strip())

    profane_pattern = re.compile(r'\b(' + '|'.join(PROFANE_WORDS) + r')\b', re.IGNORECASE)
    return profane_pattern

def contains_profanity(text):
    """
    If there is any match with the profane pattern, return True
    """
    profane_pattern = get_profanity_pattern()
    return bool(profane_pattern.search(text))

def detect_profanity(data: DataPreprocessor):
    """
    Traverse through a list of conversation between the agent and the customer
    to find if the agent was profane and/or the customer was profane.
    """

    is_agent_profane = False
    is_customer_profane = False

    for conv in data.conversation:
        print(conv)
        if contains_profanity(conv['text']):
            if conv['speaker'] == 'Agent':
                is_agent_profane = True
            if conv['speaker'] == 'Customer':
                is_customer_profane = True


    return {"is_agent_profane": is_agent_profane, "is_customer_profane": is_customer_profane}

