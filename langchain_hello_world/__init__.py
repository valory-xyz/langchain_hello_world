from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import time


load_dotenv()

search = TavilySearchResults(max_results=2)


# If we want, we can create other tools.
# Once we have all the tools we want, we can put them in a list that we will reference later.
tools = [search]


model = ChatOpenAI(model="gpt-4o-mini")


memory = MemorySaver()


agent_executor = create_react_agent(model, tools, checkpointer=memory)


config = {"configurable": {"thread_id": "abc123"}}


for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob and i live in dublin, ireland!")]}, config
):
    print(chunk)
    print("----")

while(True):
    print("##### ASKING A QUESTION #####")
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="whats my name and what is the time where I live?")]}, config
    ):
        print(chunk)
        print("----")

    print("##### STARTING AGAIN IN 2 SECONDS #####")
    time.sleep(2)
