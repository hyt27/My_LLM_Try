import os
import psycopg2
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
#from langchain.chains.sql_database.query import create_sql_query_chain
from langchain.chains import create_sql_query_chain
from chatglm_llm import ChatGLM_LLM

db=SQLDatabase.from_uri(f"postgresql+psycopg2://postgres:123456@0.0.0.0:5432/postgres")

llm=ChatGLM_LLM(model_path="/mnt/document/Langchain-Chatchat/chatglm3-6b")

chain=create_sql_query_chain(llm,db)

response=chain.invoke({"question":"what is thr id of mary"})

print(response)
