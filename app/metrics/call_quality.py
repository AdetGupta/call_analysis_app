from app.data_processing.processor import DataProcessor

def update_values(speaker, overlap, silence_gap, overall_call, agent, customer):
    """
        Updates the duration for each agent or the customer did overtalk or kept silence.
    """
    overall_call["overtalk"] += overlap
    if speaker.lower() == "agent":
        agent["overtalk"] += overlap
    else:
        customer["overtalk"] += overlap

    overall_call["silence"] += silence_gap
    if speaker.lower() == "agent":
        agent["silence"] += silence_gap
    else:
        customer["silence"] += silence_gap


def calculate_quality(conversation):
    """
    Compute key call quality metrics such as overtalk and silence duration
    of the call as well as by each speaker.

    Args:
        conversation (list[dict]): A list of utterances with 'speaker', 'stime', and 'etime' keys,
                                   representing the speaker label and their start/end times.

    Returns:
        dict: Contains percentage metrics for overtalk and silence in the call.
    """
    # Sort by start time to ensure chronological order
    conversation = sorted(conversation, key=lambda x: x['stime'])

    total_talk_duration = conversation[-1]['etime'] - conversation[0]['stime']
    overall_call = {"overtalk": 0, "silence": 0}
    agent = {"overtalk": 0, "silence": 0}
    customer = {"overtalk": 0, "silence": 0}

    for i in range(len(conversation)-1):
        current = conversation[i]
        next = conversation[i+1]

        overlap = max(0, current["etime"] - next["stime"])
        silence_gap = max(0, next["stime"] - current["etime"])
        update_values(current["speaker"], overlap, silence_gap, overall_call, agent, customer)

    return compute_call_metrics(total_talk_duration, overall_call, agent, customer)

def compute_call_metrics(total_talk_duration, overall_call, agent, customer):
    """
        Calculates overtalk and silence percentages per call.
    """

    def percent(value):
        return round((value / total_talk_duration) * 100, 2) if total_talk_duration > 0 else 0.0
    metrics = {
        "Overall": {"Overtalk (%)": percent(overall_call["overtalk"]), "Silence (%)": percent(overall_call["silence"]),},
        "Agent": {"Overtalk (%)": percent(agent["overtalk"]), "Silence (%)": percent(agent["silence"])},
        "Customer": {"Overtalk (%)": percent(customer["overtalk"]), "Silence (%)": percent(customer["silence"])},
    }
    return {
        "total_duration": total_talk_duration,
        "metrics": metrics,
    }

def analyze_call_quality(data: DataProcessor):
    return calculate_quality(data.conversation)
