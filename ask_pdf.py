import streamlit as st
from pdf_utils import extract_pdf_pages, pages_to_context

def ask_pdf_ui(client):
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

    if uploaded_file:
        pages = extract_pdf_pages(uploaded_file)
        st.success(f"PDF loaded ({len(pages)} pages)")

        question = st.text_input("Ask a question about your PDF")

        if question:
            context = pages_to_context(pages)

            prompt = f"""
Answer strictly from the document.
Cite page number and exact paragraph.
If not found, say: Not found in document.

DOCUMENT:
{context}

QUESTION:
{question}

FORMAT:

Source:
Page <number>

Answer:
<answer>

Evidence:
"<exact paragraph>"
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.subheader("Answer")
            st.write(response.text)
