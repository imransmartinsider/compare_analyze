import streamlit as st
from pdf_utils import extract_pdf_pages, pages_to_context

def compare_pdfs_ui(client):
    col1, col2 = st.columns(2)

    with col1:
        pdf_a = st.file_uploader("Upload PDF A", type="pdf", key="pdf_a")

    with col2:
        pdf_b = st.file_uploader("Upload PDF B", type="pdf", key="pdf_b")

    if pdf_a and pdf_b:
        st.success("Both PDFs uploaded. Ready to compare.")

    if st.button("Compare PDFs"):
        with st.spinner("Analyzing and comparing documents..."):
            pages_a = extract_pdf_pages(pdf_a)
            pages_b = extract_pdf_pages(pdf_b)

            context_a = pages_to_context(pages_a)
            context_b = pages_to_context(pages_b)

            prompt = f"""

You are an expert document analyst.

IMPORTANT:
- The two documents may describe the SAME PERSON in different ways.
- Do NOT rely on exact wording.
- Detect semantic similarity even if phrasing, structure, or formatting is different.
- Treat resumes/CVs as a special case.

TASK:
Compare DOCUMENT A and DOCUMENT B deeply.

Analyze and explain:
1. Common background (education, role, career direction)
2. Overlapping skills or experience (even if worded differently)
3. What is newly added, removed, or improved in DOCUMENT B
4. Whether DOCUMENT B is an evolution of DOCUMENT A
5. Overall similarity level (Low / Medium / High) with reasoning

DOCUMENT A:
{context_a}

DOCUMENT B:
{context_b}

FORMAT OUTPUT EXACTLY AS:

Similarity Level:
<Low | Medium | High>

Common Profile Indicators:
- ...

Key Differences:
- ...

What Changed / Improved:
- ...

Relationship Analysis:
Explain whether Document B is an updated version of A and why.

Final Insight:
...
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.subheader("Comparison Result")
            st.write(response.text)
