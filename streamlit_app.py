import streamlit as st
import requests

# PAGE CONFIG

st.set_page_config(

    page_title="OmniMind AI",

    page_icon="🤖",

    layout="wide"
)

# TITLE

st.title("🤖 OmniMind AI")

st.markdown(

    "Advanced Multi-Agent Hybrid RAG System"
)

# PDF UPLOAD

uploaded_files = st.file_uploader(

    "Upload PDF Files",

    type=["pdf"],

    accept_multiple_files=True
)

# UPLOAD BUTTON

if st.button("Upload PDFs"):

    if uploaded_files:

        with st.spinner(

            "Uploading PDFs..."
        ):

            for file in uploaded_files:

                files = {

                    "file": (
                        file.name,
                        file,
                        "application/pdf"
                    )
                }

                response = requests.post(

                    "http://127.0.0.1:8000/upload",

                    files=files
                )

            st.success(

                "PDFs uploaded successfully!"
            )

# QUESTION INPUT

question = st.text_input(

    "Ask your question:"
)

# ASK BUTTON

if st.button("Ask AI"):

    if question:

        with st.spinner(

            "Thinking..."
        ):

            response = requests.post(

                "http://127.0.0.1:8000/ask",

                json={

                    "question": question
                }
            )

            data = response.json()

            # ANSWER

            st.subheader("Answer")

            st.write(

                data["answer"]
            )

            # SEARCHED FILES

            st.subheader(

                "Searched Files"
            )

            for file in data[
                "searched_files"
            ]:

                st.write(f"• {file}")

            # SOURCES

            if "sources" in data:

                st.subheader(

                    "Relevant Sources"
                )

                for source in data[
                    "sources"
                ]:

                    st.write(
                        f"• {source}"
                    )