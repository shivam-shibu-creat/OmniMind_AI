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

            files_data = {}

            for i, file in enumerate(uploaded_files):

                files_data[f"file{i+1}"] = (
                    file.name,
                    file,
                    "application/pdf"
                )

            try:

                response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files=files_data
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        f"{data['total_files']} PDF(s) uploaded successfully!"
                    )

                else:

                    st.error(
                        f"Upload failed! Status code: {response.status_code}"
                    )

                    st.write(response.text)

            except Exception as e:

                st.error(f"Error: {str(e)}")

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

                if response.status_code == 200:

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

                else:

                    st.error(
                        f"Request failed! Status code: {response.status_code}"
                    )

                    st.write(response.text)

            except Exception as e:

                st.error(f"Error: {str(e)}")