import os

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tools import mongo_find, mongo_insert, mongo_list

llm = ChatOllama(
    model=os.environ["MODEL"],
    temperature=0,
    base_url=os.environ["LLM_URL"],
)

agent = create_agent(llm, tools=[mongo_list, mongo_find, mongo_insert])

response = agent.invoke(
    {"messages": [{"role": "user", "content": os.environ["QUERY"]}]}
)

print(response["messages"][-1].content)
