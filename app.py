import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

from compare_images import compare_images_ui

from ask_pdf import ask_pdf_ui
from compare_pdfs import compare_pdfs_ui

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API"))

st.set_page_config(page_title="DocGenius", layout="wide")
st.title("Docs – Intelligent Analysis")

mode = st.selectbox(
    "Choose Mode",
    ["Ask PDF", "Compare PDFs", "Compare Pictures"]
)

if mode == "Ask PDF":
    ask_pdf_ui(client)

elif mode == "Compare PDFs":
    compare_pdfs_ui(client)

elif mode == "Compare Pictures":
    compare_images_ui(client)
