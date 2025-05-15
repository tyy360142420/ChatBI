from typing import Any,List
from src.enumerations.ResponseTypeEnum import ResponseDisplayType

class DataRender:
    def __init__(self,sql:str,display_type:str,data:Any,columns:List[str]):
        self.sql = sql
        self.display_type = display_type
        self.data = data
        self.columns = columns
        self.value_column = ""
        self.name_column = ""

    def process_data_by_display_type(self):
        print(self.display_type == ResponseDisplayType.RESPONSE_TABLE.value)
        print(self.display_type == ResponseDisplayType.RESPONSE_PIE_CHART.value)
        if self.display_type == ResponseDisplayType.RESPONSE_TABLE.value:
            return
        elif self.display_type == ResponseDisplayType.RESPONSE_PIE_CHART.value:
            self.process_pie_chart()
        elif self.display_type == ResponseDisplayType.RESPONSE_LINE_CHART.value:
            return

    def transform_item_for_pie_chart(self,item):
        return {
            "name":item[self.name_column],
            "value":item[self.value_column]
        }

    def process_pie_chart(self):
        pie_chart_data = []
        pie_chart_labels = []
        if(len(self.data) and len(self.columns) >0):
            self.value_column = ""
            self.name_column = ""
            if isinstance(self.data[0][self.columns[0]],str):
                self.name_column = self.columns[0]
                self.value_column = self.columns[1]
            else:
                self.name_column = self.columns[1]
                self.value_column = self.columns[0]
            pie_chart_data = list(map(self.transform_item_for_pie_chart,self.data))
            pie_chart_labels = [item[self.name_column] for item in self.data]
        print(pie_chart_data)
        self.data = pie_chart_data
        self.columns = pie_chart_labels