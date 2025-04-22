from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    #groq_api_key = os.getenv("GROQ_API_KEY"),
    groq_api_key = "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",
    model_name = "llama-3.3-70b-versatile"
)

if __name__ == "__main__":
    response = llm.invoke("which model is used to answer my question")
    print(response.content)