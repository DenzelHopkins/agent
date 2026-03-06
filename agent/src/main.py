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

# Step 1: search and fetch content
search_agent = create_agent(llm, tools=[web_search, web_fetch])
search_result = search_agent.invoke(
    {"messages": [{"role": "user", "content": (
        f"{os.environ['QUERY']} "
        "Suche mit web_search und rufe die relevantesten Seiten mit web_fetch ab. "
        "Gib den gesamten gesammelten Inhalt zurück."
    )}]},
    config={"callbacks": [LoggingCallback()]},
)

# Extract final text from search result
search_content = search_result["messages"][-1].content

# Step 2: extract promises and save
save_agent = create_agent(llm, tools=[save_promises])
save_agent.invoke(
    {"messages": [{"role": "user", "content": (
        f"Hier sind Webinhalte über Versprechen von Friedrich Merz:\n\n{search_content}\n\n"
        "Extrahiere alle Versprechen und speichere sie mit save_promises. "
        "Jedes Versprechen muss enthalten: promise (String), source (URL-String), date (YYYY-MM-DD-String)."
    )}]},
    config={"callbacks": [LoggingCallback()]},
)
