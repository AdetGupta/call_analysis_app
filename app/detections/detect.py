from app.data_processing.processor import DataProcessor
from app.detections.privacy_violation.llm import detect_privacy_violation_llm
from app.detections.privacy_violation.pattern import detect_privacy_violation_regex
from app.detections.profanity.ml import detect_profanity_ml
from app.detections.profanity.pattern import detect_profanity_regex


def detect_entity(data:DataProcessor, entity, approach):
    if entity == "Profanity Detection":
        if approach == "Pattern Matching":
            return detect_profanity_regex(data)
        if approach == "Machine Learning":
            return detect_profanity_ml(data)

    if entity == "Privacy and Compliance Violation":
        if approach == "Pattern Matching":
            return detect_privacy_violation_regex(data)
        if approach == "Machine Learning":
            return detect_privacy_violation_llm(data)

    return None