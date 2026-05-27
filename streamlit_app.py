import streamlit as st
import requests

BACKEND_URL = "https://omnimindai-production.up.railway.app"

st.set_page_config(
    page_title="OmniMind AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 OmniMind AI")

st.markdown(
    "Advanced Multi-Agent Hybrid RAG System"
)

uploaded_files = st.file_uploader(
    "Upload PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Upload PDFs"):

    if uploaded_files:

        with st.spinner("Uploading PDFs..."):

            success_count = 0

            for file in uploaded_files:

                files = {
                    "file": (
                        file.name,
                        file,
                        "application/pdf"
                    )
                }

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/upload",
                        files=files
                    )

                    if response.status_code == 200:
                        success_count += 1

                    else:
                        st.error(
                            f"Failed to upload {file.name}"
                        )

                except Exception as e:

                    st.error(
                        f"Error uploading {file.name}: {str(e)}"
                    )

            if success_count > 0:

                st.success(
                    f"{success_count} PDF(s) uploaded successfully!"
                )

question = st.text_input(
    "Ask your question:"
)

if st.button("Ask AI"):

    if question:

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "question": question
                    }
                )

                data = response.json()

                st.subheader("Answer")

                st.write(
                    data["answer"]
                )

                st.subheader(
                    "Searched Files"
                )

                for file in data["searched_files"]:

                    st.write(f"• {file}")

                if "sources" in data:

                    st.subheader(
                        "Relevant Sources"
                    )

                    for source in data["sources"]:

                        st.write(f"• {source}")

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )