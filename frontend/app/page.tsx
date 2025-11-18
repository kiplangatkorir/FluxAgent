"use client";

import Link from "next/link";

export default function HomePage() {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <section className="card">
        <h1 className="text-2xl font-semibold mb-3">Full-stack AI Agent</h1>
        <p className="text-slate-300 mb-8">
          Upload documents, index them into pgvector, and collaborate with a
          multi-tool agent that explains every reasoning step. Switch LLM models
          on the fly and inspect Langfuse traces.
        </p>
        <div className="flex gap-3">
          <Link
            href="/upload"
            className="px-5 py-3 rounded-full bg-cyan-400 text-slate-900 font-semibold"
          >
            Upload Docs
          </Link>
          <Link
            href="/query"
            className="px-5 py-3 rounded-full border border-cyan-300 text-cyan-200 font-semibold"
          >
            Ask the Agent
          </Link>
        </div>
      </section>
      <section className="card bg-gradient-to-br from-slate-900 to-slate-800 border border-cyan-400/40">
        <h2 className="text-xl font-semibold mb-4">What's inside</h2>
        <ul className="text-sm text-slate-300 space-y-3">
          <li>⚙️ LangChain agent with search, SQL, mail, HTTP, calculator.</li>
          <li>📄 pgvector-backed RAG flow for uploaded knowledge.</li>
          <li>🛰️ Langfuse observability wired into every run.</li>
          <li>🪄 Timeline UI with icons for pending/in-progress/done/error.</li>
          <li>🐳 Docker Compose: backend, frontend, Postgres+pgvector, Langfuse.</li>
        </ul>
      </section>
    </div>
  );
}

