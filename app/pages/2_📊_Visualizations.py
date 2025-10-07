import os
import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from app.visualizations.plots import (
    plot_overtalk,
    plot_silence,
    plot_duration_distribution,
    plot_overtalk_silence_box,
    plot_profanity_pie,
    plot_privacy_pie,
    plot_duration_vs_overtalk,
    plot_correlation_heatmap
)
from app.visualizations.visualizations import load_data

st.set_page_config(page_title="📊 Visualizations", layout="wide")
st.title("📊 Conversation Insights Dashboard")

metrics_path = "./app/visualizations/data/call_metrics.csv"
detections_path = "./app/visualizations/data/detections.csv"

if not (os.path.exists(metrics_path) and os.path.exists(detections_path)):
    st.error("### CSV files not found in the data/ folder.")
    st.stop()

merged = load_data(metrics_path, detections_path)

st.subheader("📌 Overview")

st.divider()

st.write(f"Input: All_Conversations_(1)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Calls", len(merged))
col2.metric("Avg Duration (s)", f"{merged['total_duration'].mean():.2f}")
col3.metric("Avg Overtalk (%)", f"{merged['Overall_overtalk'].mean():.2f}")

st.divider()

# --- Plots ---
st.plotly_chart(plot_overtalk(merged), use_container_width=True, key="ot")
st.plotly_chart(plot_silence(merged), use_container_width=True, key="sl")

st.divider()

st.plotly_chart(plot_duration_distribution(merged), use_container_width=True, key="dur")
st.plotly_chart(plot_overtalk_silence_box(merged), use_container_width=True, key="box")

st.divider()

st.plotly_chart(plot_profanity_pie(merged), use_container_width=True, key="prof")
st.plotly_chart(plot_privacy_pie(merged), use_container_width=True, key="priv")

st.divider()

st.plotly_chart(plot_duration_vs_overtalk(merged), use_container_width=True)

heatmap = plot_correlation_heatmap(merged)
if heatmap:
    st.plotly_chart(heatmap, use_container_width=True)
else:
    st.info("No numeric data for correlation heatmap.")

st.subheader("⚠️ Flagged Calls Summary")
flagged = merged[(merged["is_profane"]) | (merged["privacy_violation"])]
if not flagged.empty:
    st.dataframe(flagged[["call_id", "is_profane", "privacy_violation", "total_duration", "Overall_overtalk", "Overall_silence"]])
else:
    st.success("No flagged calls found — all calls are clean and compliant.")







