import streamlit as st
import sys
from pathlib import Path
import tempfile

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from app.data_processing.processor import DataProcessor
from app.detections.detect import detect_entity

st.set_page_config(page_title="Upload & Analyze")
st.title("📁 Upload & Analyze")
st.write("Upload a JSON or YAML file to see the call metrics and entities.")

uploaded_file = st.file_uploader(
    "Upload your JSON or YAML file",
    type=['json', 'yaml', 'yml']
)

if uploaded_file is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        data = DataProcessor(tmp_path)

        # Dropdown 1
        entity_options = ["Profanity Detection", "Privacy and Compliance Violation"]
        selected_entity = st.selectbox("Select Entity", entity_options)

        # Dropdown 2
        approach_options = ["Pattern Matching", "Machine Learning"]
        selected_approach = st.selectbox("Select Approach", approach_options)

        analyze_clicked = st.button("Analyze")
        if analyze_clicked:
            st.write("Result")
            st.write(detect_entity(data, selected_entity, selected_approach))

        show_file = st.checkbox("Show File")
        if show_file:
            st.write("File")
            st.write(data.conversation)


    except Exception as e:
        st.error(f"Error processing file: {e}")


