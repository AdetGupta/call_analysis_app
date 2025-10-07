import os.path

import joblib

from app.data_processing.processor import DataProcessor


def load_model():
    """
    Returns trained SVC Linear model, vectorizer saved in model/checkpoints
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = os.path.dirname(base_dir)

    vectorizer = joblib.load(os.path.join(base_dir, "model/checkpoints/profanity_vectorizer.joblib"))
    model = joblib.load(os.path.join(base_dir, "model/checkpoints/profanity_model.joblib"))
    return vectorizer, model

def detect_profanity_ml(data: DataProcessor):
    """
        Traverse through a list of conversation between the agent and the customer
        to find if the agent was profane and/or the customer was profane.
    """
    data.transform()
    vectorizer, model = load_model()

    is_agent_profane = False
    is_customer_profane = False

    for message in data.conversation:
        tx = vectorizer.transform([message['text']])
        tx = model.predict(tx)
        if tx[0] == 1:
            if message['speaker'] == 'Agent':
                is_agent_profane = True
            if message['speaker'] == 'Customer':
                is_customer_profane = True
            break

    return {"is_agent_profane": is_agent_profane, "is_customer_profane": is_customer_profane}

if __name__ == "__main__":
    load_model()