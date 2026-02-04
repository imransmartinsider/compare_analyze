from pypdf import PdfReader

def extract_pdf_pages(uploaded_file):
    reader = PdfReader(uploaded_file)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append({
                "page": i + 1,
                "text": text.strip()
            })
    return pages


def pages_to_context(pages):
    context = ""
    for p in pages:
        context += f"\n--- Page {p['page']} ---\n{p['text']}\n"
    return context
