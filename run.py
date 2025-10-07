import os
from pprint import pprint

from app.data_processing.processor import DataProcessor

from app.detections.privacy_violation.llm import detect_privacy_violation_llm
from app.detections.privacy_violation.pattern import detect_privacy_violation_pattern
from app.detections.profanity.ml import detect_profanity_ml
from app.detections.profanity.pattern import detect_profanity_regex
from app.metrics.call_quality import analyze_call_quality


def profanity_run():
    d_pattern = {"agent": 0, "customer": 0}
    d_ml = {"agent": 0, "customer": 0}

    for filename in os.listdir('All_Conversations_(1)'):
        file_path = os.path.join('All_Conversations_(1)', filename)
        data = DataProcessor(file_path)
        temp_regex = detect_profanity_regex(data)
        temp_ml = detect_profanity_ml(data)

        d_pattern['agent'] += 1 if temp_regex["is_agent_profane"] else 0
        d_pattern['customer'] += 1 if temp_regex["is_customer_profane"] else 0
        d_ml['agent'] += 1 if temp_ml["is_agent_profane"] else 0
        d_ml['customer'] += 1 if temp_ml["is_customer_profane"] else 0

    print(f"regex patter result: {d_pattern}")
    print(f"ML result: {d_ml}")

def privacy_run():
    violations = []
    i=0
    for filename in os.listdir('All_Conversations_(1)'):
        i += 1
        if i == 5:
            break
        file_path = os.path.join('All_Conversations_(1)', filename)
        data = DataProcessor(file_path)
        result = detect_privacy_violation_llm(data)
        result_pattern = detect_privacy_violation_pattern(data)
        if result.get("violation", True):
            violations.append({
                "call_id": data.call_id,
                "result": result
            })
        print(data.call_id)
        print(i, result)
        print(i, result_pattern)

    return violations

if __name__ == '__main__':
    # profanity_run()
    # d = privacy_run()
    # print(df["violation"].value_counts())
    # print(d)
    # print(len(d))

    data = DataProcessor("All_Conversations_(1)/d7bbea61-d739-43fb-a198-ced1b59f9491.json")
    pprint(analyze_call_quality(data))
    profanity_run()
    privacy_run()