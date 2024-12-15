# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# os.environ["MODELSCOPE_CACHE"] = "D:/dataset/cache/modelscope/"
# from llama_index.llms.modelscope import ModelScopeLLM
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding


from langchain_community.llms import QianfanLLMEndpoint
from llama_index.llms.langchain import LangChainLLM
from llama_index.core.callbacks import (
    CallbackManager,
    LlamaDebugHandler,
    CBEventType,
)

import os

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
)

from llama_index.core import SQLDatabase
# from llama_index.core.query_engine import NLSQLTableQueryEngine
from my_engine import NLSQLTableQueryEngine
from llama_index.core.prompts.base import PromptTemplate
from llama_index.core.prompts.prompt_type import PromptType

llama_debug = LlamaDebugHandler(print_trace_on_end=True)
# callback_manager = CallbackManager([llama_debug, aim_callback])
callback_manager = CallbackManager([llama_debug])

os.environ["QIANFAN_AK"] = "BbTpj7vuUUk7GOt6t6X8XjtO"
os.environ["QIANFAN_SK"] = "LzTSlYubQ3bapZkfLmqzYvWmw644WpUR"

llm = QianfanLLMEndpoint(model="ERNIE-4.0-8K", streaming=False)
# llm = QianfanLLMEndpoint(model="ERNIE-3.5-8K", streaming=False)
llm = LangChainLLM(llm=llm)

os.environ["OPENAI_API_KEY"] = "sk-lxsdYSlP1l5fSMjF3c27C8Cc9cC74955AcB673C826BdAd88"

db_password = "4402115bac2c1c68"
DATABASE_URL = f"mysql+pymysql://root:{db_password}@59.68.29.90:3306/liukun"

url = 'mysql+pymysql://root:12345@localhost:3306/test2'
engine = create_engine(DATABASE_URL)

sql_database = SQLDatabase(engine,
                           include_tables=["administrative_division_city", "administrative_division_community_village",
                                           "administrative_division_district",
                                           "administrative_division_town", "city_roads", "data_governance_achievements",
                                           "data_source_table", "real_estate", "real_buildings", "resident_info",
                                           "standard_address", "units", "water_bodies_rivers", "data_collection_table"])

DEFAULT_TEXT_TO_SQL_TMPL = (
    "Given an input question, first create a syntactically correct {dialect} "
    "query to run, then look at the results of the query and return the answer. "
    "You can order the results by a relevant column to return the most "
    "interesting examples in the database.\n\n"
    "Never query for all the columns from a specific table, only ask for a "
    "few relevant columns given the question.\n\n"
    "Pay attention to use only the column names that you can see in the schema "
    "description. "
    "Be careful to not query for columns that do not exist. "
    "Pay attention to which column is in which table. "
    "Also, qualify column names with the table name when needed. "
    "Here is SQLQuery example SQLQuery:'```SELECT DISTINCT Source_Table_Name FROM Data_Source_Table WHERE Collected_Data_Resource_Name ='aa';```'"
    "Don't like this, SQLQuery:'```sql\nSELECT DISTINCT Source_Table_Name FROM Data_Source_Table WHERE Collected_Data_Resource_Name ='aa';```'"
    "You are required to use the following format, each taking one line:\n\n"
    "Question: Question here\n"
    "SQLQuery: SQL Query to run\n"
    "SQLResult: Result of the SQLQuery\n"
    "Answer: Final answer here\n\n"
    "Only use tables listed below.\n"
    "{schema}\n\n"
    "Question: {query_str}\n"
    "SQLQuery: "

)

MY_TEXT_TO_SQL_PROMPT = PromptTemplate(
    DEFAULT_TEXT_TO_SQL_TMPL,
    prompt_type=PromptType.TEXT_TO_SQL,
)

context_query_kwargs = {
    "units": "units指实际存在的各种单位组织，通常指的是工商管理部门登记注册的各类企业、政府机关以及事业单位,其中政府机关和事业单位合起来称为党政机关，该表的数据全是湖北省鄂州关于党政机关和企业数量分布的数据",
    "data_source_table": "里面包含数公基数据各种数据表，如果要查询数所有数公基的数据量，则要查询所有Source_Table_Name字段值对应的表的数据的条数"
}
context_str_prefix = '''
数据库名称：liukun
语及指标定义:
数据总量：也称之为数据量，指的是结构化数据表的数据条数。
数据容量：指的是结构化数据表或非结构化数据的存储容量。
上图：指的是一标三实数据和城市数字模型在CIM平台上进行展示。
上图率：可上图数据数量占治理后数据数量的比例。举个例子“鄂州市数公基标准地址的上图率是多少”，首先这个问题涉及到的表名是“标准地址表”和数据治理成果表，标准地址上图率=数据治理成果表（Data_Governance_Achievements）中Collected_Data_Resource_Name字段值为“标准地址”对应的治理后数据量（Data_Volume_After_Governance字段对应的值）/标准地址表的中数据的总条数，其他的一些数据的上图率也以此类推
数据治理：指归集后的原始数据资源经过数据清洗转换、加工处理之后形成的标准化、高质量的数据。
治理率：治理后的数据量占治理前数据量的比例。数源单位：提供原始数据资源的政府单位。
鄂州市的行政区划：鄂城区（行政区）、华容区（行政区）、梁子湖区（行政区）、葛店经济技术开发区（功能区）、临空经济开发区（功能区）。鄂州市：湖北省内的一个地级市。
数源单位：提供原始数据资源的政府单位。
'''
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=["administrative_division_city", "administrative_division_community_village",
                                       "administrative_division_district",
                                       "administrative_division_town", "city_roads", "data_governance_achievements",
                                       "data_source_table", "real_estate", "real_buildings", "resident_info",
                                       "standard_address", "units", "water_bodies_rivers", "data_collection_table"],
    llm=llm, context_query_kwargs=context_query_kwargs, context_str_prefix=context_str_prefix
)

while (True):
    query_str = input("USER INPUT: ")
    response = query_engine.query(query_str)

    print(response)
