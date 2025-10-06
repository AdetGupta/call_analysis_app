import os
from pprint import pprint

from app.data_processing.processor import DataProcessor

from app.detections.profanity.ml import detect_profanity_ml
from app.detections.profanity.pattern import detect_profanity_regex


def run():
    d_pattern = {"agent": 0, "customer": 0}
    d_ml = {"agent": 0, "customer": 0}

    for filename in os.listdir('All_Conversations_(1)'):
        file_path = os.path.join('All_Conversations_(1)', filename)
        data = DataProcessor(file_path)
        data.transform()

        temp_regex = detect_profanity_regex(data)
        temp_ml = detect_profanity_ml(data)

        d_pattern['agent'] += 1 if temp_regex["is_agent_profane"] else 0
        d_pattern['customer'] += 1 if temp_regex["is_customer_profane"] else 0
        d_ml['agent'] += 1 if temp_ml["is_agent_profane"] else 0
        d_ml['customer'] += 1 if temp_ml["is_customer_profane"] else 0

        if temp_regex != temp_ml:
            pprint([dialog['text'] for dialog in data.conversation])

    print(f"regex patter result: {d_pattern}")
    print(f"ML result: {d_ml}")


if __name__ == '__main__':
    run()