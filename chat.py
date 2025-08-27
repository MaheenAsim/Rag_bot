'''
This script:

Loads the FAISS index

Lets you type questions in the console

Retrieves context + sends it to GPT for an answer
'''

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate

assert os.getenv("OPENAI_API_KEY"), "Please set OPENAI_API_KEY environment variable."

def load_db():
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

def main():
    print("RAG Chatbot (type 'exit' to quit)")
    db = load_db()
    retriever = db.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the retrieved context to answer."),
        ("human", "Question: {question}\n\nContext:\n{context}\n\nAnswer:")
    ])

    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Retrieve context
        docs = retriever.get_relevant_documents(query)
        context = "\n".join([d.page_content for d in docs])

        # Format prompt
        prompt = prompt_template.format(question=query, context=context)

        # Get answer
        response = llm.invoke(prompt)
        print(f"Bot: {response.content}")

if __name__ == "__main__":
    main()
