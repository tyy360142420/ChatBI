from abc import ABC
from typing import Any, Dict
from src.basicConfiguration import Config
CFG = Config()

class BaseChat(ABC):
    # chat with database or chat with excel and so on
    chat_scene:str = None;
    # used to save the client of llm which is used to chat with
    llm_model_client:Any = None;
    llm_model_name:str = None;
    # used to connect to database 
    db_connector:Any =None;
    chat_session_id:str = None;
    def __init__(self,chat_param:Dict):
        """

        :param chat_param:
            chat_session_id: user related identity
            model_name: used to chat and generate SQL
            db_connector_info: the data source which is used to execute sql
            chat_scene: the scene which is used by user
        """
        self.chat_scene = chat_param["chat_scene"]
        self.chat_session_id = chat_param["chat_session_id"]
        self.llm_model_name = (chat_param["model_name"] if chat_param["model_name"] else CFG.LLM_MODEL)