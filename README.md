# Autonomous ChatBot — LangGraph Agentic AI Platform

A multi-mode agentic AI application built with **LangGraph** and **Streamlit**, demonstrating how to design, compose, and orchestrate stateful AI agent graphs for real-world use cases — from a simple conversational chatbot to a tool-using research agent and an autonomous news-summarization pipeline.

## Overview

Most chatbot demos stop at a single prompt → response loop. This project goes further by treating the LLM as one node in a **directed graph of reasoning steps**, using [LangGraph](https://github.com/langchain-ai/langgraph) to define how state flows between nodes (chatbot, tools, summarizers, savers). The same codebase supports several distinct "use cases" selectable at runtime from the UI, each compiled into its own graph.

## Features

- **Basic Chatbot** — a minimal LangGraph loop (`START → chatbot → END`) for straightforward Q&A.
- **Chatbot with Web Search** — augments the chatbot with a tool node (Tavily search) and conditional routing, so the agent decides *when* it needs to call a tool versus answering directly.
- **AI News Agent** — a three-stage autonomous pipeline (`fetch_news → summarize_news → save_result`) that pulls the latest AI news via the Tavily API for a chosen timeframe (daily/weekly/monthly/yearly), summarizes it with an LLM, and persists the digest to disk.
- **Pluggable LLM backend** — powered by [Groq](https://groq.com/) for low-latency inference, with model selection (Llama 3.3/3.1, GPT-OSS, Qwen) exposed directly in the UI.
- **Streamlit front-end** — a single interactive app for choosing a use case, configuring the model, and viewing results, decoupled from the core agent logic in `src/`.

## Architecture

```
User (Streamlit UI)
        │
        ▼
  LoadStreamlitUI  ──► collects use case + model + API keys
        │
        ▼
   GroqLLM.get_llm_model()
        │
        ▼
  GraphBuilder.setup_graph(usecase)
        │
        ├── Basic Chatbot        : START → chatbot → END
        ├── Chatbot Web Search   : START → chatbot ⇄ tools → END
        └── AI News              : fetch_news → summarize_news → save_result → END
        │
        ▼
  DisplayResultStreamlit ──► renders output back to the UI
```

## Project Structure

```
Autonomous-ChatBot/
├── app.py                                  # Streamlit entry point
├── requirements.txt
├── AINews/
│   └── daily_summary.md                    # Example output of the AI News agent
└── src/langgraphagenticai/
    ├── main.py                             # App orchestration logic
    ├── LLMs/groqllm.py                     # Groq model configuration
    ├── graph/graphbuilder.py               # Graph construction per use case
    ├── nodes/                              # basic_chatbot, chatbot_with_tool, ai_news
    ├── state/state.py                      # Shared LangGraph state schema
    ├── tools/search_tool.py                # Tavily web-search tool binding
    └── ui/
        ├── uiconfigfile.ini                # UI options (use cases, model list)
        └── streamlit/                      # UI rendering + result display
```

## Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph, LangChain |
| LLM inference | Groq (Llama 3.x, GPT-OSS, Qwen) |
| Web search tool | Tavily API |
| UI | Streamlit |
| Config | `.ini` based use-case/model registry |

## Getting Started

### Prerequisites
- Python 3.10+
- A [Groq API key](https://console.groq.com/)
- A [Tavily API key](https://tavily.com/) (required for web search / AI News modes)

### Installation

```bash
git clone https://github.com/MohammedTabarakAhmed/Autonomous-ChatBot.git
cd Autonomous-ChatBot
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root with:

```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Run

```bash
streamlit run app.py
```

Then, in the sidebar, pick an LLM model and one of the four use cases, and start interacting.

## Roadmap

- Add the "Blog Generation" use case referenced in the UI config
- Persist chat history across sessions
- Add automated tests for each graph node

## License

This project is available for educational and personal portfolio use.
