import os
import uuid
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver


from tools import search_book_semantically, check_book_availability, reserve_book


load_dotenv(".venv/.env")


llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)


tools = [search_book_semantically, check_book_availability, reserve_book]


memory = MemorySaver()


system_prompt = """


Important instructions :
Information Gathering: Request the user's name and Student ID during the conversation (if not already provided). A Student ID is strictly required before reserving a book.

Tool Usage: Before reserving a book (reserve_book), you must check its availability in the system (check_book_availability).

Constraints: Only answer questions related to the library.

Language: Always respond very politely in English.

and when confirming book reseravation ask user from confirmation and then record
"""


agent_executor = create_react_agent(
    llm,
    tools,
    checkpointer=memory,
    prompt=system_prompt
)

if __name__ == "__main__":    
   
    session_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}
    
   
    
    while True:
       
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Thnk You ")
            break
            
        user_message = {"messages": [("user", user_input)]}
        
        print("\nAI Assistant:")
      
        for event in agent_executor.stream(user_message, config=config):
            for value in event.values():
            
                print(value["messages"][-1].content)