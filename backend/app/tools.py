import json
from datetime import datetime
from typing import Any, Dict, List

import requests
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from sqlalchemy import text

from .config import get_settings
from .database import SessionLocal, support_table
from .rag import similarity_search

settings = get_settings()


class SearchInput(BaseModel):
    query: str = Field(..., description="Search query string")


class CalculatorInput(BaseModel):
    expression: str = Field(..., description="Mathematical expression")


class RagInput(BaseModel):
    query: str = Field(..., description="Question to look up in documents")
    top_k: int = Field(default=3, le=8)


class SendMailInput(BaseModel):
    to: str
    subject: str
    body: str


class HttpInput(BaseModel):
    path: str = Field(..., description="Path appended to webhook base URL")
    method: str = Field(default="GET")
    payload: Dict[str, Any] | None = None


class SqlFetchInput(BaseModel):
    sql: str = Field(
        ...,
        description="Read-only SQL query targeting support_records table.",
    )


def _mock_search(query: str) -> str:
    corpus = [
        {
            "title": "FluxAgent Release Notes",
            "summary": "Latest updates for the FluxAgent AI assistant platform.",
            "url": "https://docs.example.com/fluxagent/release",
        },
        {
            "title": "Playbook: Handling VIP Outages",
            "summary": "Step-by-step guide for triaging production issues.",
            "url": "https://wiki.example.com/vip-outages",
        },
        {
            "title": "Feature Flag Rollouts",
            "summary": "Best practices for gradual feature enablement.",
            "url": "https://wiki.example.com/feature-flags",
        },
    ]
    query_lower = query.lower()
    filtered = [
        item for item in corpus if query_lower in item["summary"].lower()
    ]
    if not filtered:
        filtered = corpus[:1]
    return json.dumps(filtered, indent=2)


def _evaluate_expression(expression: str) -> str:
    import ast
    import operator as op

    allowed_ops = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.USub: op.neg,
    }

    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp):
            return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            return allowed_ops[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported expression")

    parsed = ast.parse(expression, mode="eval").body
    return str(_eval(parsed))


def _rag_lookup(query: str, top_k: int) -> str:
    docs = similarity_search(query, k=top_k)
    return json.dumps(
        [
            {
                "content": doc.page_content[:500],
                "metadata": doc.metadata,
            }
            for doc in docs
        ],
        indent=2,
    )


def _send_mail(to: str, subject: str, body: str) -> str:
    path = settings.mail_log_path
    timestamp = datetime.utcnow().isoformat()
    record = {"to": to, "subject": subject, "body": body, "ts": timestamp}
    with open(path, "a", encoding="utf-8") as handler:
        handler.write(json.dumps(record) + "\n")
    return f"Queued email to {to}"


def _http_call(path: str, method: str, payload: Dict[str, Any] | None) -> str:
    url = settings.webhook_base_url.rstrip("/") + "/" + path.lstrip("/")
    method_upper = method.upper()
    response = requests.request(method_upper, url, json=payload, timeout=10)
    return json.dumps(
        {"status_code": response.status_code, "text": response.text[:500]},
        indent=2,
    )


def _sql_fetch(sql: str) -> str:
    sql_clean = sql.strip().lower()
    if not sql_clean.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    with SessionLocal() as session:
        results = session.execute(text(sql)).mappings().all()
    return json.dumps([dict(row) for row in results], default=str, indent=2)


def build_tools() -> List[StructuredTool]:
    def search_tool(query: str) -> str:
        return _mock_search(query)

    def calculator_tool(expression: str) -> str:
        return _evaluate_expression(expression)

    def rag_tool(query: str, top_k: int = 3) -> str:
        return _rag_lookup(query, top_k)

    def send_mail_tool(to: str, subject: str, body: str) -> str:
        return _send_mail(to, subject, body)

    def http_tool(path: str, method: str = "GET", payload: Dict[str, Any] | None = None) -> str:
        return _http_call(path, method, payload)

    def sql_tool(sql: str) -> str:
        return _sql_fetch(sql)

    return [
        StructuredTool.from_function(
            func=search_tool,
            name="web_search",
            description="Useful for searching recent knowledge base snippets.",
            args_schema=SearchInput,
        ),
        StructuredTool.from_function(
            func=calculator_tool,
            name="calculator",
            description="Evaluate arithmetic expressions safely.",
            args_schema=CalculatorInput,
        ),
        StructuredTool.from_function(
            func=rag_tool,
            name="document_rag_lookup",
            description="Look up enterprise documents stored in pgvector.",
            args_schema=RagInput,
        ),
        StructuredTool.from_function(
            func=send_mail_tool,
            name="send_mail",
            description="Send a mock email that is logged to disk.",
            args_schema=SendMailInput,
        ),
        StructuredTool.from_function(
            func=http_tool,
            name="http_webhook",
            description="Make HTTP GET/POST requests to webhook.site endpoint.",
            args_schema=HttpInput,
        ),
        StructuredTool.from_function(
            func=sql_tool,
            name="sql_fetch",
            description="Run read-only SQL queries over support_records.",
            args_schema=SqlFetchInput,
        ),
    ]

