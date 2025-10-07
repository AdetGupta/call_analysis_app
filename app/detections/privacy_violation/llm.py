import json
import os
import re
from dotenv import load_dotenv
from google import genai

from app.data_processing.processor import DataProcessor

def get_client():
    load_dotenv()
    # Access your API key
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    return client

def convert_to_text(conversation):
    """
    Flatten a conversation into a readable string format for the LLM.
    Each message is prefixed by the speaker.
    """
    return "\n".join([f"{message['speaker']}: {message['text']}" for message in conversation])


def build_prompt(conversation_text):
    """
        Construct a structured prompt for the LLM to detect privacy violations.
    """
    prompt = f"""
You are a compliance officer reviewing customer service conversations for privacy violations.

Analyze the conversation below carefully to detect if any **privacy violations** occurred based on the following rules:

1. **Sensitive information** means any mention of:
   - Financial details: balance, account number, loan, payment, bill, credit, or any numeric financial amount.
   - Any data that compromises user privacy or financial security.

2. **Verification** means the agent confirms personal identity through:
   - Personal identifiers: Date of Birth (DOB), full address, Social Security Number (SSN), phone number, or other unique identity data.

3. **Privacy violation occurs if:**
   - Sensitive information is shared **before** verification takes place.
   - Sensitive information is shared **without any** verification at all during the conversation.
   - Personal identifiers are shared improperly without verification.

4. The purpose is to ensure that sensitive information is only disclosed **after identity verification** has been successfully completed.

5. Opening messages of like "outstanding balance with some Bank" can be ingored and they do not imply sensitive information being given.
---

**Conversation:**  
{conversation_text}

---

**Task:**  
Provide a **JSON object only** with the following structure, without any additional text or explanation:

{{
  "violation": true or false,
  "reason": "brief explanation of why this conversation was flagged or not"
}}

**Do NOT include any extra text, steps, or markdown. JSON only.**
    """
    return prompt


def run_llm_violation_check(conversation_text:str):
    """
        Run the LLM on the conversation prompt and extract structured JSON output.
    """
    try:
        client = get_client()
        prompt = build_prompt(conversation_text)

        # Gemini API call
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_output = response.text
        cleaned = re.sub(r"^```json|```$", "", raw_output.strip(), flags=re.MULTILINE).strip()
        json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)

        # Fallback if no JSON found
        return {"violation": False, "reason": "No JSON object found in LLM output."}

        # print("=== Prompt ===")
        # print(prompt)
        # print("=====================")
        # print("=== LLM Raw Output ===")
        # print(response.text)
        # print("=====================")
        # return ""

    except Exception as e:
        print("LLM Error:", e)
        return {"violation": False, "reason": f"Error occurred: {str(e)}"}


def detect_privacy_violation_llm(data: DataProcessor):
    """
        Main function to detect privacy violations using an LLM.

        Args:
            Data (DataProcessor class): List of the whole conversation.

        Returns:
            Dict: Structured detection result with keys:
                - violation: bool
                - reason: str
    """
    conversation_text = convert_to_text(data.conversation)
    return run_llm_violation_check(conversation_text)

if __name__ == "__main__":
    data = DataProcessor("../../../All_Conversations_(1)/c1cf9a45-0a69-4543-9994-117bdd4fdaaf.json")
    output = detect_privacy_violation_llm(data)
    print(output)
