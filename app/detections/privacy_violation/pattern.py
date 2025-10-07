from typing import List
import re
from app.data_processing.processor import DataProcessor
from app.utils.data_utils import get_message_from_speaker

SENSITIVE_PATTERNS = [
    r"\b(balanc|amount|payment|due|owe|bill|account|loan|emi|instal|credit|outstand|settl|clear|receiv)\b.*?(\d+|rs|usd|\$)",
]

VERIFICATION_PATTERNS = [
    r"\b(verifi|confirm|check|authent)\b.*\b(address|dob|birth|date|ident|ssn|social|secur|detail|info|person)\b",
    r"\b(address|dob|birth|date|ident|ssn|social|secur|detail|info|person)\b.*\b(verifi|confirm|check|authent)\b"
]

def find_all_sensitive(messages: List[dict]) -> List[int]:
    """
        Returns list of indices where sensitive information was shared.
    """
    sensitive_indices = []
    for i, message in enumerate(messages):
        text = message.get("text", "")
        if any(re.search(p, text) for p in SENSITIVE_PATTERNS):
            sensitive_indices.append(i)
    return sensitive_indices


def find_all_verification(messages: List[dict]) -> List:
    """
        Returns list of indices where agent asked for identity verification.
    """
    verification_indices = []
    for i, message in enumerate(messages):
        text = message.get("text", "")
        if any(re.search(p, text) for p in VERIFICATION_PATTERNS):
            verification_indices.append(i)
    return verification_indices


def verify_violation(sensitive_indices, verification_indices):
    """
        Determine if a privacy violation occurred based on the order of sensitive information
        and verification attempts in a conversation.

        Returns a dictionary containing:
            - 'violation': True if sensitive information was shared without proper verification, False otherwise.
            - 'reason': A short explanation of the compliance outcome.
    """
    result = {
        "violation": False,
        "reason": "None",
    }

    # Case 1: No sensitive info shared -> no violation
    if not sensitive_indices:
        result["reason"] = "Sensitive information not shared."
        return result

    # Case 2: Sensitive info shared but no verification -> violation
    if not verification_indices:
        result["violation"] = True
        result["reason"] = "Sensitive information shared but no verification done."
        return result

    # Case 3: Sensitive info shared before first verification → violation
    if min(sensitive_indices) < min(verification_indices):
        result["violation"] = True
        result["reason"] = "Sensitive info shared before verification."
        return result

    # Otherwise compliant
    result["reason"] = "Verification done before sharing sensitive info."
    return result


def detect_privacy_violation_regex(data: DataProcessor):
    """
        Detect if Privacy and Compliance Violation.
        Returns a dict with structured results for reporting.
    """
    transformed_conversation = data.transform()
    all_agent_messages = get_message_from_speaker(speaker='agent', conversation=transformed_conversation)

    sensitive_indices = find_all_sensitive(all_agent_messages)
    verification_indices = find_all_verification(all_agent_messages)

    return verify_violation(sensitive_indices, verification_indices)


if __name__ == '__main__':
    data = DataProcessor("../../../All_Conversations_(1)/2db2965e-54fa-41fa-823b-ed79b943f0b1.json")
    print(detect_privacy_violation_regex(data))

