import os
import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


CSV_PATH = "data/books.csv"

CHROMA_PATH = "chroma_db"

def ingest_data():
    print("Loading data from CSV...")
    
   
    df = pd.read_csv(CSV_PATH, on_bad_lines="skip")

    documents = []
    
   
    for index, row in df.iterrows():
       
        page_content = (
            f"Title: {row['title']}\n"
            f"Author: {row['authors']}\n"
            f"Rating: {row['average_rating']}\n"
            f"Publisher: {row['publisher']}"
        )

      
        metadata = {"book_id": row['bookID'], "title": row['title']}

        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)

    print(f"Loaded {len(documents)} books. ")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

  
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    # print(f"Successfully ingested data into Chroma DB at: {CHROMA_PATH}")

if __name__ == "__main__":
    ingest_data()