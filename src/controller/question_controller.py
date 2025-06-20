from fastapi import APIRouter
from src.llmServer.langchain_ollama_learning import chain
from src.prompt.static_prompt import database_analyst_prompt,response_prompt,display_type_prompt
from src.database.sqlite_connection import SqliteConnector
from src.database.my_sql_connection import MySqlConnection
import json
from src.parser.output_parser import BasicParser
from src.response_obj.data_render import DataRender
from src.parameters.question import Question
router = APIRouter(prefix="/chat",tags=["llmInteraction"])

@router.post("/askQuestion")
async def ask_question(question:Question):
    print("ask_question")
    sqlite_connector = SqliteConnector("src/sqlite/chinook.db")
    table_infos = sqlite_connector.get_table_simple_info()
    # mysql_connector = MySqlConnection("127.0.0.1","tyy","TangYiYe@123","airport")
    # table_infos = mysql_connector.get_table_simple_infos()
    json_response = chain.invoke({"question":question.question,"knowledge":database_analyst_prompt.format(table_info=table_infos,user_input=question,response=response_prompt,dialect=sqlite_connector.db_dialect,top_k=1,display_type=display_type_prompt)})
    print(json_response)
    parser = BasicParser()
    json_answer_of_text_to_sql = json.loads(parser.parse_prompt_response(json_response.content))
    data_coulmns,data_result = sqlite_connector.getJsonData(json_answer_of_text_to_sql["sql"])
    data_render = DataRender(json_answer_of_text_to_sql["sql"],json_answer_of_text_to_sql["display_type"],data_result,data_coulmns)
    data_render.process_data_by_display_type()
    print(data_render.data)
    sqlite_connector.close_connection()
    return data_render
