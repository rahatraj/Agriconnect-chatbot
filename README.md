#  AgriConnect Chatbot

An intelligent, documentation-aware chatbot for the **AgriConnect Platform**, powered by **FastAPI**, **LangChain**, **LangGraph**, **LangSmith**, **Tavily Search**, and **Google Gemini**. Deployed live on **Render**, this chatbot can answer platform-specific queries using internal documentation and real-time web search.

---

##  Features

-  **FastAPI** backend for real-time chatbot access
-  Reads internal Agriconnect documentation (`.txt`)
-  Performs live web search via **Tavily Search API**
-  Stateful memory handling using **LangGraph**
-  Graph-based routing of tools and logic
-  Full **LangSmith** observability and debugging enabled
-  Powered by **Google Gemini (gemini-2.0-flash)** via LangChain
-  **Deployed on Render** with live API access

---

##  Project Structure

.
├── chain.py # Main logic for chatbot + LangGraph
├── agriconnect.txt # Internal documentation for Agriconnect platform
├── .env # Environment variables (LangSmith, LangChain API keys)
└── README.md # Project documentation


---

## 🔧 Technologies Used


| Tech              | Role                                                    |
|-------------------|--------------------------------------------------------- |
| **Python**        | Core language                                           |
| **FastAPI**       | Backend API framework                                   |
| **LangChain**     | Tool binding, message orchestration                     |
| **LangGraph**     | Graph-based workflow engine                             |
| **LangSmith**     | Observability, tracing, debugging                       |
| **Tavily**        | Real-time external web search                           |
| **Google Gemini** | LLM engine via `ChatGoogleGenerativeAI`                 |
| **Render**        | Cloud deployment platform                               |
| **dotenv**        | Environment variable management                         |

---

##  How It Works

1. **User asks a question** via CLI (or future API).
2. The chatbot:
   - Routes the question to both:
     -  `AgriconnectDocReader`: reads internal docs.
     -  `TavilySearchResults`: performs a real-time web search.
   - Combines both responses and asks the LLM to generate a concise reply.
3. Filters out irrelevant questions using keyword-based rules.
4. Returns the final answer to the user.

##  Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/agriconnect-chatbot.git
   cd agriconnect-chatbot
  ```

## 2. Install dependencies:

pip install -r requirements.txt

## 3. Add your .env file:

Create a .env file in the root directory with the following:

GOOGLE_API_KEY=your_gemini_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=agriChatbot

## 4.  Run Locally

uvicorn main:app --reload
Access the API at: http://127.0.0.1:8000
## 5. Live Deployment

The chatbot is deployed and live at:

👉 https://agriconnect-chatbot.onrender.com

## Supported Questions
This chatbot can answer queries related to:

 Crop Listings, Bidding & Prices

 Wallet & Payment System

 Dashboard, Booking, and Notifications

 Farmer and  Buyer interactions

 Greetings, FAQs, and general help

All unrelated topics are gracefully rejected to maintain relevance.


## LangGraph Flow
chatbot: Accepts user input, queries both tools

tool_node: Executes both:

AgriconnectDocReader (reads from txt)

TavilySearchResults (real-time search)

Final message is passed to ChatGoogleGenerativeAI for summarization

Graph is memory-aware using thread-based state via MemorySaver.

## LangSmith Integration
Every request and tool invocation is logged and visualized using LangSmith.
Useful for:

Tracing and debugging flow

Analyzing LLM performance

Viewing tool outputs side-by-side

## Requirements

fastapi
uvicorn
python-dotenv
langchain
langchain-google-genai
langchain-community
langgraph
langsmith
tavily-python

## Author
MD RAHAT REZA
Full Stack Developer
Email: rahatreza3199@gmail.com

## Future Add-ons
 Redis/Vector store memory support

 Multilingual input/output (Indian languages)

 Admin dashboard for analytics

 Frontend UI with Tailwind & React

 Voice-based query input

