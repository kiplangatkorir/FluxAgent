import uuid
from typing import Dict, List, Optional

from langchain.agents import AgentType, initialize_agent
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.language_models.chat_models import BaseChatModel

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama

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


def _build_langfuse_handler() -> Optional[LangfuseCallbackHandler]:
    """Instantiate Langfuse callback only when real credentials are provided."""
    if not settings.langfuse_public_key or not settings.langfuse_secret_key:
        return None
    if settings.langfuse_public_key == "public-placeholder":
        return None
    if settings.langfuse_secret_key == "secret-placeholder":
        return None
    return LangfuseCallbackHandler(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_host,
    )


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
    if provider == "ollama":
        return ChatOllama(
            model=model,
            base_url=settings.ollama_base_url,
            temperature=0.2,
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
    langfuse_handler = _build_langfuse_handler()
    callbacks: List[BaseCallbackHandler] = [timeline_handler]
    if langfuse_handler:
        callbacks.append(langfuse_handler)

    agent_executor = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True,
    )
    context_blob = "\n\n".join(doc.page_content for doc in rag_docs)
    agent_input = (
        "You are FluxAgent. Use the supplied enterprise context when helpful.\n"
        f"Context:\n{context_blob}\n\nQuestion: {query}"
    )
    result = agent_executor.invoke(
        {"input": agent_input},
        callbacks=callbacks,
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

