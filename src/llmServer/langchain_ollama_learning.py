from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.chat_models import init_chat_model

template = """Question:{question}
Answer:let's think step by step.
"""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.2:1b")
chain = prompt|model

print(chain.invoke({"question":"What is llm"}))