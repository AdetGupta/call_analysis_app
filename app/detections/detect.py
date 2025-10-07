from app.data_processing.processor import DataProcessor
from app.detections.privacy_violation.llm import detect_privacy_violation_llm
from app.detections.privacy_violation.pattern import detect_privacy_violation_regex
from app.detections.profanity.ml import detect_profanity_ml
from app.detections.profanity.pattern import detect_profanity_regex


def detect_entity(data:DataProcessor, entity, approach):
    """
    Detects a specified entity in the conversation data using the chosen approach.

    Parameters:
        data: DataProcessor instance with conversation data
        entity: "Profanity Detection" or "Privacy and Compliance Violation"
        approach: "Pattern Matching" or "Machine Learning"

    Returns:
        Detection results as a dict, or None if unsupported.
    """
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