import os
from dotenv import load_dotenv
#from langchain_ollama import ChatOllama
#from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import init_chat_model



load_dotenv() 

llm = init_chat_model(
    model=os.getenv("MODEL_NAME"),
    temperature=0.1
)

history = [{"role": "system", "content": "You are a helpful Corvit AI Assistant!"}]

print("Welcome to the Corvit AI Assistant!")

while True:
    question = input("You: ").strip()

    if not question:
       continue
    if question in ("exit", "quit", "bye"):
       print("Goodbye!")
       break

    history.append({
         "role": "user",
         "content": question
      })
    print("bot: {chunk.text}", end="", flush=True)
    
    full = None  
    for chunk in llm.stream("history"):
      print(chunk.text, end="", flush=True)
      full = chunk if full is None else full + chunk
    print()


history.append(full)

