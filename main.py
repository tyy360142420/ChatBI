from enum import Enum

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from src.embedding.embedding_service import VectorService


class ModalNameEnum(str,Enum):
    APPLE = "apple",
    Banana = "Banana"

template = """Question:{question};Background Knowledge:{knowledge}"""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.2:1b")
chain = prompt|model

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"hello world"}

@app.get("/question/{question}")
async def root(question:str):
    vec:VectorService = VectorService()
    knowledges = vec.get_knowledge_from_vector_store(question)
    final_knowledge:str = ""
    for template in knowledges:
        final_knowledge = final_knowledge + template.page_content
    print(final_knowledge)
    return {"answer":chain.invoke({"question":question,"knowledge":final_knowledge})}

