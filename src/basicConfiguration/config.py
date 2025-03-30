import os

from src.util.singleton import Singleton


class Config(metaclass=Singleton):
    """configuration class to store the environment variables in this project"""
    def __init__(self)->None:
        """initialize the Config class"""
        #default name is not
        self.LLM_NAME_FOR_SQL = os.getenv("LLM_MODEL","")
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","")
        #the porpotion
        self.TMPERATURE = float(os.getenv("TEMPERATURE",0.7))