from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["PHI_API_KEY"] = os.getenv("PHI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# web_search_agent = Agent(
#     name="Web Search Agent",
#     model=Groq(id="llama-3.1-8b-instant", backend="local"),  # ensure correct backend
#     tools=[DuckDuckGo()],
#     instructions=["Always include the source of the information"],
#     markdown=True,
#     show_tools_calls=True,
# )

financial_agent = Agent(
    name="Financial AI Agent",
    model=Groq(id="llama-3.1-8b-instant", backend="local"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_news=True)],
    instructions=["Use table to display the data and include the source of the information with date."],
    markdown=True,
    show_tools_calls=True,
)

# multi_ai_agent = Agent(
#     team=[web_search_agent, financial_agent],
#     model=Groq(id="llama-3.1-8b-instant", backend="local"),
#     instructions=["Always include the source of the information", "Use tables to display the data"],
#     markdown=True,
#     show_tools_calls=True,
# )

financial_agent.print_response("Summarize latest news on Facebook Stocks.", stream=True)
