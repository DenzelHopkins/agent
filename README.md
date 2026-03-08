# Agent

A LangGraph-based web research agent that searches the internet for political promises and stores them in MongoDB.

```mermaid
graph TD
    Agent --> LLM
    Agent --> WebSearch[Web Search]
    Agent --> Database[Database]
```
