import os
import sys

import nltk

from app.data_processing.preprocessor import DataPreprocessor
from app.detections.profanity.pattern import contains_profanity, detect_profanity


def run():
    # data = DataPreprocessor("All_Conversations_(1)/0b6979e4-8c05-49e1-b7a7-94d85a627df5.json")
    # data.transform()
    # print(data.conversation)
    d = {"agent": 0, "customer": 0}

    for filename in os.listdir('All_Conversations_(1)'):
        file_path = os.path.join('All_Conversations_(1)', filename)
        data = DataPreprocessor(file_path)
        data.transform()

        temp = detect_profanity(data)
        d['agent'] += 1 if temp["is_agent_profane"] else 0
        d['customer'] += 1 if temp["is_customer_profane"] else 0

        if temp["is_agent_profane"]:
            print(data.conversation)
    print(d)

if __name__ == '__main__':
    run()