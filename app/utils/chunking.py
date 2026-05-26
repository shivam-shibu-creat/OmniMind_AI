from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=1200,

    chunk_overlap=250,

    separators=[
        "\n\n",
        "\n",
        ". ",
        " "
    ]
)

def chunk_text(text):

    chunks = text_splitter.split_text(text)

    return chunks