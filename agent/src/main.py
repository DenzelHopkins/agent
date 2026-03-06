from database import migrate
from tools import web_fetch, web_search, save_promises
from langchain.agents import create_agent
import os

from utils import get_logger, LoggingCallback

logger = get_logger(__name__)


# Run database migrations
migrate.run()

# Select LLM provider
provider = os.environ.get("LLM_PROVIDER", "ollama")

if provider == "anthropic":
    from langchain_anthropic import ChatAnthropic
    llm = ChatAnthropic(
        model=os.environ["MODEL"],
        temperature=0,
        api_key=os.environ["ANTHROPIC_API_KEY"],
    )
else:
    from langchain_ollama import ChatOllama
    llm = ChatOllama(
        model=os.environ["MODEL"],
        temperature=0,
        base_url=os.environ["LLM_URL"],
    )

# Build agent with tools
agent = create_agent(llm, tools=[web_search, web_fetch, save_promises])

# Run agent with query
agent.invoke(
    {"messages": [{"role": "user", "content": (
        f"{os.environ['QUERY']} "
        "Suche zuerst mit web_search nach Ergebnissen. "
        "Extrahiere dann die Versprechen aus den Suchergebnissen. "
        "Speichere sie erst danach mit save_promises. "
        "Jedes Versprechen muss enthalten: promise (String), source (URL-String), date (YYYY-MM-DD-String)."
    )}]},
    config={"callbacks": [LoggingCallback()]},
)
