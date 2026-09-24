from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import sqlite3
import datetime

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)


@tool
def search_book_semantically(book: str) -> str:
    """
    When user ask about book this tool will help to find about book details rating etc.
    """
    
   
    results = vectorstore.similarity_search(book, k=2)
    
   
    if not results:
        return "Sorry We dont know about this book"
    
    response = "these are the books we found:\n"
    
    for doc in results:
       
        response += f"{doc.page_content}\n" 
        
        response += f"Book title: {doc.metadata.get('title')}\n"
        response += "-" * 30 + "\n"
       
    return response


DB_PATH = "library.db" 

@tool
def check_book_availability(title: str) -> str:
    """
    This tool is used to check if a book is available in our library.
    It checks the availability of the book based on its title.
    The 'title' is required to use this tool.
    """
    try:
       
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
       
        cursor.execute(
            "SELECT title, quantity FROM inventory WHERE title LIKE ? COLLATE NOCASE",
            (f"%{title}%",),
        )
        result = cursor.fetchone() 
        
     
        conn.close()
        
       
        if result:
            titleboook = result[0]
            copies = result[1]
            
          
            if int(copies) > 0:
                return f"Yes, '{titleboook}' this book is available at this moment. (copies {copies} are left)"
            else:
                return f"Sorry, '{titleboook}' All copies of this are borrowed."
        else:
          
            return f"Sorry, Book named: '{title}' we cant find in our libreary system."
            
    except Exception as e:
       
        return f"There is some issue with database {str(e)}"


@tool
def reserve_book(title: str, student_id: str) -> str:
    """
    This tool is used to reserve a book for a student.
    It checks the availability of the book and reserves it if available.
    The 'title' and 'student_id' are required to use this tool.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        
        cursor.execute("SELECT book_id, quantity FROM inventory WHERE title = ?", (title,))
        result = cursor.fetchone() 
        
        if result:
            book_id, copies = result
            
            if int(copies) > 0:
               
                current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                status = "Reserved"
                
             
                cursor.execute(
                    "INSERT INTO reservations (book_id, student_id, reserved_date, status) VALUES (?, ?, ?, ?)", 
                    (book_id, student_id, current_date, status)
                )
                
        
                cursor.execute("UPDATE inventory SET quantity = quantity - 1 WHERE book_id = ?", (book_id,))
                
                conn.commit()
                return f"Book '{title}' has been reserved for student ID: {student_id}."
            else:
                return f"Sorry, all copies of '{title}' are currently borrowed."
        else:
            return f"Sorry, Book named: '{title}' we can't find in our library system."
        
    except Exception as e:
        return f"There is some issue with database {str(e)}"
    
    finally:
        if conn:
            cursor.close()
            conn.close()


