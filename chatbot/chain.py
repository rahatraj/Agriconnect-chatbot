from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import add_messages, StateGraph, END
from typing import TypedDict, Annotated
from langgraph.prebuilt import ToolNode
import os 
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "agriChatbot"


# Get absolute path of current file (chain.py)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct full path to agriconnect.txt
file_path = os.path.join(base_dir, "..", "agriconnect.txt")
# Load EventSphere doc (small file)
with open(file_path, "r", encoding="utf-8") as f:
    agriconnect_text = f.read()

# Memory for message state
memory = MemorySaver()

# LangGraph thread config
config = {
    "configurable": {
        "thread_id": 1  # Use same thread to maintain memory
    }
}

# Chat state schema
class BasicChatBot(TypedDict):
    messages: Annotated[list, add_messages]


# Tools

#  Tool 1: Tavily Search
search_tool = TavilySearchResults(max_results=2)

#  Tool 2: Reads local EventSphere documentation
@tool
def AgriconnectDocReader(question: str) -> str:
    """Use this tool to answer questions about the Agriconnect platform using its internal documentation."""
    return f"Question: {question}\n\nEventSphere Documentation:\n{agriconnect_text}"

tools = [search_tool, AgriconnectDocReader]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
llm_with_tools = llm.bind_tools(tools=tools)
output_parser = StrOutputParser()


# Chatbot node (calls LLM with responses from both tools)
def chatbot(state: BasicChatBot):
    # Get the user question
    last_message = state["messages"][-1]
    question = last_message.content

    # Get the responses from both tools
    event_response = AgriconnectDocReader.invoke(question)  # Send question to Agriconnect docs
    search_response = search_tool.run(question)  # Send question to search tool
    
    # Combine the responses with clear labels
    combined_responses = (
        f"Here’s what I found from AgriConnect Documentation:\n{event_response}\n\n"
        f"Additionally, here’s some information I found from the web:\n{search_response}"
    )

    # Create a list of messages
    messages = [
        HumanMessage(content=question),  # User's question
        AIMessage(content=combined_responses)  # Combined tool responses
    ]

    # Send the list of messages to the LLM for analysis
    llm_response = llm.invoke(messages)

    return {"messages": [llm_response]}

# Conditional tool routing node (send to both tools)
def tools_router(state: BasicChatBot):
    # This function now routes to both tools directly, no need for a conditional check here
    return "tool_node"
# Tool handler node (processes both tools)
tool_node = ToolNode(tools=[AgriconnectDocReader, search_tool]) 

# Agriconnect keyword filtering
event_keywords = [
    "bidding", "price", "booking", "bid", "dashboard",
    "crops", "weather", "payment", "wallet", "buyer", "farmer",
    "greeting", "hi", "hello"
]

def is_event_related(question: str) -> bool:
    return any(keyword in question.lower() for keyword in event_keywords)

# App interface to get response
def get_response(question: str) -> str:
    if not is_event_related(question):
        return "Sorry, I can only answer questions related to events or venues."
    
    response = app.invoke({
        "messages": [HumanMessage(content=question)]
    }, config=config)

    # Get latest message
    final_messages = response.get("messages", [])
    if final_messages:
        return final_messages[-1].content
    return "I'm not sure how to respond."

# Graph structure
graph = StateGraph(BasicChatBot)
graph.add_node("chatbot", chatbot)
graph.add_node("tool_node", tool_node)
graph.set_entry_point("chatbot")

# Compile LangGraph app
app = graph.compile(checkpointer=memory)

# CLI loop
if __name__ == "__main__":
    print("EventSphere ChatBot (type 'exit' or 'end' to quit)\n")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "end"]:
            break
        else:
            response = get_response(user_input)
            print("Bot:", response)
