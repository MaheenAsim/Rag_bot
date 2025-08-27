'''
----This script:

Reads all PDFs/texts from documents/

Splits them into chunks

Embeds them with OpenAI

Saves them into a FAISS inde
'''
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# Make sure API key is set
assert os.getenv("OPENAI_API_KEY"), "Please set OPENAI_API_KEY environment variable."

def load_documents():
    docs = []
    for file in os.listdir("documents"):
        path = os.path.join("documents", file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        elif file.endswith(".txt"):
            loader = TextLoader(path)
            docs.extend(loader.load())
    return docs

def main():
    print("📂 Loading documents...")
    docs = load_documents()

    print("✂️ Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)

    print("🔎 Embedding and creating FAISS index...")
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(split_docs, embeddings)

    db.save_local("faiss_index")
    print("✅ Index saved to faiss_index/")

if __name__ == "__main__":
    main()
