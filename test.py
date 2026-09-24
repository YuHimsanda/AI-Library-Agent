import os
import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


CSV_PATH = "data/books_data.csv"
CHROMA_PATH = "chroma_db"

def ingest_data():
    print("Loading data from CSV...")
    
   
    df = pd.read_csv(CSV_PATH)

    documents = []
    
   
    for index, row in df.iterrows():
       
        page_content = f"Title: {row['title']}\nAuthor: {row['author']}\nDescription: {row['description']}"

      
        metadata = {"book_id": row['book_id'], "title": row['title']}

        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)

    print(f"Loaded {len(documents)} books. Creating embeddings (This may take a minute for the first time)...")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

  
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    print(f"Successfully ingested data into Chroma DB at: {CHROMA_PATH}")

if __name__ == "__main__":
    ingest_data()