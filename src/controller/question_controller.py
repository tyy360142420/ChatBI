from fastapi import APIRouter
from src.llmServer.langchain_ollama_learning import chain
from src.prompt.static_prompt import database_analyst_prompt,response_prompt,display_type_prompt
from src.database.sqlite_connection import SqliteConnector
from src.database.my_sql_connection import MySqlConnection
import json
from src.parser.output_parser import BasicParser
from src.response_obj.data_render import DataRender
router = APIRouter(prefix="/askQuestion",tags=["llmInteraction"])

@router.get("/{question}")
async def ask_question(question:str):
    sqliteConnector = SqliteConnector("src/sqlite/chinook.db")
    table_infos = sqliteConnector.get_table_simple_info()
    # mysql_connector = MySqlConnection("127.0.0.1","tyy","TangYiYe@123","airport")
    # table_infos = mysql_connector.get_table_simple_infos()
    json_response = chain.invoke({"question":question,"knowledge":database_analyst_prompt.format(table_info=table_infos,user_input=question,response=response_prompt,dialect=sqliteConnector.db_dialect,top_k=1,display_type=display_type_prompt)})
    parser = BasicParser()
    json_answer_of_text_to_sql = json.loads(parser.parse_prompt_response(json_response))
    data_coulmns,data_result = sqliteConnector.getJsonData(json_answer_of_text_to_sql["sql"])
    dataRender = DataRender(json_answer_of_text_to_sql["sql"],json_answer_of_text_to_sql["display_type"],data_result,data_coulmns)
    return dataRender
