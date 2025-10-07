import pandas as pd
import ast

# ---------- Data Helpers ----------

def load_data(metrics_path: str, detections_path: str):
    """Load and merge metrics + detection data."""
    metrics_df = pd.read_csv(metrics_path)
    detections_df = pd.read_csv(detections_path)

    def parse_dict_column(col):
        return col.apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    for col in ["profanity_regex", "profanity_ml", "privacy_regex", "privacy_llm"]:
        detections_df[col] = parse_dict_column(detections_df[col])

    detections_df["is_profane"] = detections_df["profanity_ml"].apply(
        lambda x: x.get("is_agent_profane") or x.get("is_customer_profane")
    )
    detections_df["privacy_violation"] = detections_df["privacy_llm"].apply(
        lambda x: x.get("violation")
    )

    merged = metrics_df.merge(detections_df, on="call_id", how="left")
    return merged


