import streamlit as st 
from pathlib import Path 
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="Langchain:Chat with SQL Database",page_icon="🦜")
st.title("🦜 Langchain:Chat with SQL Database")

# INJECTION_WARNING="""
# SQL agent can be vulnerable to prompt injection.Use a Database rolewith limited permissions.
# Read more [here](https://python.langchain.com/docs/security).
# """

LOCAl_DB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["Use SQLLite3 Database -  Student.db","Connect to your SQL Database"]

selected_opt=st.sidebar.radio(label="Choose the Database which you want to chat",options=radio_opt)

if radio_opt.index(selected_opt)==1:
      db_uri=MYSQL
      mysql_host=st.sidebar.text_input("MySQL Host")
      mysql_user=st.sidebar.text_input("MySQL User")
      mysql_password=st.sidebar.text_input("MySQL Password",type="password")
      mysql_db=st.sidebar.text_input("MySQL Database Name")
else:
      db_uri=LOCAl_DB
      
api_key=st.sidebar.text_input(label="GROQ API Key",type="password")

if not db_uri:
      st.info("Please enter the database information and URI")
      st.stop()
      
if not api_key:
      st.info("PLease add the GROQ api key")
      st.stop()
      
llm=ChatGroq(groq_api_key=api_key,model_name="llama-3.3-70b-versatile",streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
      if db_uri==LOCAl_DB:
            dbfilepath=(Path(__file__).parent/"student.db").absolute()
            print(dbfilepath)
            creator=lambda:sqlite3.connect(f"file:{dbfilepath}?mode=ro",uri=True)
            return SQLDatabase(create_engine("sqlite://",creator=creator))
      elif db_uri==MYSQL:
            if not (mysql_host and mysql_user and mysql_password and mysql_db):
                  st.error("Please provide all MySQL connection Details")
                  st.stop()
            print("🧪 Connecting to MySQL with URI:", db_uri)
            return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

if db_uri==MYSQL:
      db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
else:
      db=configure_db(db_uri)


toolkit=SQLDatabaseToolkit(db=db,llm=llm)

agent=create_sql_agent(
      llm=llm,
      toolkit=toolkit,
      verbose=True,
      agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
      st.session_state["messages"]=[{"role":"assistant","content":"How can I help you?"}]

for msg in st.session_state.messages:
      st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="Ask anything from the database")

if user_query:
      st.session_state.messages.append({"role":"user","content":user_query})
      st.chat_message("user").write(user_query)
      
      with st.chat_message("assistant"):
            streamlit_callback=StreamlitCallbackHandler(st.container())
            response=agent.run(user_query,callbacks=[streamlit_callback])
            st.session_state.messages.append({"role":"assistant","content":response})
            st.write(response)