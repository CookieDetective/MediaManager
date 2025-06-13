from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.agents import AgentExecutor, create_openai_functions_agent
from dotenv import load_dotenv
from tools.sql import run_query_tool

load_dotenv()

model = ChatOpenAI()
prompt = ChatPromptTemplate(
  messages=[
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
  ]
)

tools = [run_query_tool]

agent = create_openai_functions_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor({"input": "How many users are in the database?"})