from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import time
import os
import json
from TransactionExecuter import TransactionExecuter


load_dotenv()

if not os.environ.get("TAVILY_API_KEY"):
    print("Looking for CONNECTION_CONFIGS_CONFIG_TAVILY_API_KEY env_var")
    os.environ["TAVILY_API_KEY"] = os.environ.get("CONNECTION_CONFIGS_CONFIG_TAVILY_API_KEY")


if not os.environ.get("OPENAI_API_KEY"):
    print("Looking for CONNECTION_CONFIGS_CONFIG_OPENAI_API_KEY env_var")
    os.environ["OPENAI_API_KEY"] = os.environ.get("CONNECTION_CONFIGS_CONFIG_OPENAI_API_KEY")    

tx_executor = TransactionExecuter()

search = TavilySearchResults(max_results=2)
tools = [search]
model = ChatOpenAI(model="gpt-4o-mini")
memory = MemorySaver()
agent_executor = create_react_agent(model, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}

try:
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="hi im bob and i live in dublin, ireland!")]}, config
    ):
        print(chunk)
        print("----")
except Exception as err:
        print(f"[ERROR] Error to start AI interaction: {err}")

iteration = 0

while(True):
    print(F"##### ITERATION {iteration} ASKING A QUESTION #####")

    if iteration % 5 == 0:
            print("[INFO] TRYING TO EXECUTE TRANSACTION ####")
            if tx_executor.can_transact() == False:
                print("[INFO] TRANSACTION CAN NOT BE EXECUTED")
            else:
                if tx_executor.execute("0xbd02335D8BBE6b5Bcb16Cc1cFD9878B214Cb8B47"):
                    print("[INFO] TRANSACTION WAS EXECUTED SUCESSFULLY")
                else:
                    print("[INFO] TRANSACTION WAS NOT EXECUTED")

    try:
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content="whats my name and what time it is where I live?")]}, config
        ):
            print(chunk)
            print("----")
    except Exception as err:
        print(f"[ERROR] ITERATION {iteration} threw an exception: {err}")

    print("##### STARTING AGAIN IN 10 SECONDS #####")
    iteration += 1
    time.sleep(10)
