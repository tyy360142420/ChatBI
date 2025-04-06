from typing import Any


class DataRender:
    def __init__(self,sql:str,display_type:str,data:Any):
        self.sql = sql
        self.display_type = display_type
        self.data = data
