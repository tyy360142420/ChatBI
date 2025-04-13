from typing import Any,List


class DataRender:
    def __init__(self,sql:str,display_type:str,data:Any,columns:List[str]):
        self.sql = sql
        self.display_type = display_type
        self.data = data
        self.columns = columns
