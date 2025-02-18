from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import time
import os
from langchain_hello_world.TransactionExecutor import TransactionExecutor

load_dotenv()

print("[INFO] Retrieving API's keys from agent's environment variables and setup to their expected names.")
os.environ["TAVILY_API_KEY"] = os.environ.get("CONNECTION_CONFIGS_CONFIG_TAVILY_API_KEY")
os.environ["OPENAI_API_KEY"] = os.environ.get("CONNECTION_CONFIGS_CONFIG_OPENAI_API_KEY")    

print("[INFO] Setting up Langchain agent.")
search = TavilySearchResults(max_results=2)
tools = [search]
model = ChatOpenAI(model="gpt-4o-mini")
memory = MemorySaver()
agent_executor = create_react_agent(model, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}

print("[INFO] Instantiating client to execute transactions")
tx_executor = TransactionExecutor()

print("[INFO] Starting AI interaction")
try:
    for msg in agent_executor.stream(
        {"messages": [HumanMessage(content="Hi, my name is Bob and I live in Denver, Colorado.")]}, config
    ):
        print(msg)
        print("----")
except Exception as err:
        print(f"[ERROR] Error to start AI interaction: {err}")

iteration = 0

while(True):
    print(F"##### ITERATION {iteration} #####")
    try:
        if iteration % 5 == 0:
            print("[INFO] HURRAY! IT IS TIME TO EXECUTE A TRANSACTION")        
            if tx_executor.execute("0xbd02335D8BBE6b5Bcb16Cc1cFD9878B214Cb8B47"):
                print("[INFO] TRANSACTION WAS EXECUTED SUCESSFULLY")
            else:
                print("[INFO] TRANSACTION WAS NOT EXECUTED")

    
        for msg in agent_executor.stream(
            {"messages": [HumanMessage(content="Could you give me a suggestion of what to do today?")]}, config
        ):
            print(msg)
            print("----")

    except Exception as err:
        print(f"[ERROR] ITERATION {iteration} threw an exception: {err}")

    print("##### WAITING FOR 10 SECONDS #####")
    iteration += 1
    time.sleep(10)
