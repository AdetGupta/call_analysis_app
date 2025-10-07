import streamlit as st
import nltk
from nltk.data import find

# For fixing missing downloads during deployment
def download_if_missing(resource_name):
    try:
        find(resource_name)
    except LookupError:
        nltk.download(resource_name.split('/')[-1], quiet=True)

# Check and download only if missing
download_if_missing('tokenizers/punkt')      # for punkt
download_if_missing('corpora/stopwords')

st.set_page_config(
    page_title="App"
)

st.title("📉Conversation analysis app")

st.write("""
### Welcome!
- To test with your own .json or .yaml file go to the 📁Analyze File page.
- To see visualizations of the input All_Conversations_(1) go to 📊Visualizations page
""")

