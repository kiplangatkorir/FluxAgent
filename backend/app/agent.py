import uuid
from typing import Dict, List, Optional

from langchain.agents import AgentType, initialize_agent
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.language_models.chat_models import BaseChatModel

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

from langfuse.callback import CallbackHandler as LangfuseCallbackHandler

from .config import get_settings
from .rag import similarity_search
from .tools import build_tools

settings = get_settings()


class TimelineStep(BaseCallbackHandler):
    def __init__(self) -> None:
        self.steps: List[Dict] = []

    def on_tool_start(self, serialized, input_str, **kwargs):
        step = {
            "id": str(uuid.uuid4()),
            "name": serialized.get("name", "tool"),
            "type": "tool",
            "status": "in_progress",
            "input": input_str,
        }
        self.steps.append(step)

    def on_tool_end(self, output, **kwargs):
        if not self.steps:
            return
        step = self.steps[-1]
        if step["status"] == "in_progress":
            step["status"] = "done"
            step["output"] = output

    def on_tool_error(self, error, **kwargs):
        if not self.steps:
            return
        step = self.steps[-1]
        step["status"] = "error"
        step["output"] = str(error)


def _resolve_llm(provider: Optional[str], model: Optional[str]) -> BaseChatModel:
    provider = provider or settings.default_provider
    model = model or settings.default_model

    if provider == "openai":
        return ChatOpenAI(
            model=model,
            temperature=0.2,
            streaming=False,
            api_key=settings.openai_api_key,
        )
    if provider == "anthropic":
        return ChatAnthropic(
            model=model,
            temperature=0.2,
            anthropic_api_key=settings.anthropic_api_key,
        )
    if provider == "groq" and ChatGroq:
        return ChatGroq(
            model=model,
            groq_api_key=settings.groq_api_key,
            temperature=0.2,
        )
    return ChatOpenAI(
        model=settings.default_model,
        temperature=0.2,
        api_key=settings.openai_api_key,
    )


def run_agent(
    query: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict:
    llm = _resolve_llm(provider, model)
    tools = build_tools()
    rag_docs = similarity_search(query, k=3)
    timeline_handler = TimelineStep()
    langfuse_handler = LangfuseCallbackHandler()

    agent_executor = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True,
    )
    result = agent_executor.invoke(
        {
            "input": query,
            "context": "\n\n".join(doc.page_content for doc in rag_docs),
        },
        callbacks=[timeline_handler, langfuse_handler],
    )
    return {
        "final_answer": result.get("output"),
        "steps": timeline_handler.steps,
        "rag_hits": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in rag_docs
        ],
        "provider": provider or settings.default_provider,
        "model": model or settings.default_model,
    }

