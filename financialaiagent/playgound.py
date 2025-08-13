from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
import os
from dotenv import load_dotenv
import phi
from phi.playground import Playground, serve_playground_app



load_dotenv()
os.environ["PHI_API_KEY"] = os.getenv("PHI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

financial_agent = Agent(
    name="Financial AI Agent",
    model=Groq(id="llama-3.1-8b-instant", backend="local"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, company_news=True)
    ],
    instructions=[
        "Use table to display the data and include the source of the information with date."
    ],
    markdown=True,
    show_tools_calls=True,
)

phi.api = os.getenv("PHI_API_KEY")

playground = Playground(agents=[financial_agent])

if __name__ == "__main__":
    # Pass the app to the server
    serve_playground_app(
        app=playground.get_app(),
        host="0.0.0.0",
        port=7777
    )