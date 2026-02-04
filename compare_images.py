import streamlit as st
from PIL import Image
import io

def compare_images_ui(client):
    st.subheader("Compare Pictures")

    col1, col2 = st.columns(2)

    with col1:
        img_a_file = st.file_uploader(
            "Upload Image A",
            type=["png", "jpg", "jpeg"],
            key="img_a"
        )

    with col2:
        img_b_file = st.file_uploader(
            "Upload Image B",
            type=["png", "jpg", "jpeg"],
            key="img_b"
        )

    # ---------- SHOW IMAGES SIDE-BY-SIDE ----------
    if img_a_file and img_b_file:
        img_a = Image.open(img_a_file)
        img_b = Image.open(img_b_file)

        st.markdown("### Images")
        img_col1, img_col2 = st.columns(2)

        with img_col1:
            st.image(img_a, caption="Image A", use_container_width=True)

        with img_col2:
            st.image(img_b, caption="Image B", use_container_width=True)

        st.success("Both images uploaded. Ready to compare.")

        # ---------- COMPARE BUTTON ----------
        if st.button("Compare Images"):
            with st.spinner("Analyzing images and highlighting differences..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": """
You are an expert visual analyst.

TASK:
Compare IMAGE A and IMAGE B carefully.

Analyze and explain:
1. Common visual elements
2. Key differences
3. WHERE the differences appear (top/bottom/left/right/center)
4. Whether one image is an updated or modified version
5. Overall similarity level (Low / Medium / High)

IMPORTANT:
- Be very specific about visual difference locations.
- If differences are subtle, still mention them.

FORMAT OUTPUT AS:

Similarity Level:
<Low | Medium | High>

Common Elements:
- ...

Visual Differences (with locations):
- ...

Relationship Analysis:
...

Final Insight:
...
"""
                                },
                                {
                                    "inline_data": {
                                        "mime_type": img_a_file.type,
                                        "data": img_a_file.getvalue()
                                    }
                                },
                                {
                                    "inline_data": {
                                        "mime_type": img_b_file.type,
                                        "data": img_b_file.getvalue()
                                    }
                                }
                            ]
                        }
                    ]
                )

            st.subheader("Comparison Result")
            st.write(response.text)

            # ---------- VISUAL DIFFERENCE HINT ----------
            st.info(
                "💡 Tip: Visual differences are described above with their approximate locations "
                "(e.g., top-left, center). This avoids false pixel-level highlights and keeps results reliable."
            )
