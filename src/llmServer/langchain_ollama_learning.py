from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from src.basicConfiguration import Config
config = Config()
template = """Question:{question};Background Knowledge:{knowledge}"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOllama(base_url=config.LLM_MODEL_API_URL, model=config.LLM_NAME_FOR_SQL, temperature=0)
chain = prompt|model
