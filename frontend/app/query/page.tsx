"use client";

import { useEffect, useState } from "react";
import { fetchModels, runAgent, AgentResponse, ModelOption } from "@/lib/api";
import { Timeline } from "@/components/Timeline";
import { RagHits } from "@/components/RagHits";

export default function QueryPage() {
  const [question, setQuestion] = useState("");
  const [models, setModels] = useState<ModelOption[]>([]);
  const [selectedModel, setSelectedModel] = useState<ModelOption | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AgentResponse | null>(null);

  useEffect(() => {
    fetchModels()
      .then((options) => {
        setModels(options);
        setSelectedModel(options[0] ?? null);
      })
      .catch((err) => setError(err.message));
  }, []);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await runAgent({
        query: question,
        provider: selectedModel?.provider,
        model: selectedModel?.model,
      });
      setResult(response);
    } catch (err: any) {
      setError(err.message ?? "Agent failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <section className="card">
        <h1 className="text-xl font-semibold mb-4">Ask the Agent</h1>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <label className="block text-sm text-slate-300">
            Question
            <textarea
              className="mt-1 w-full rounded-xl border border-slate-800 bg-slate-900 p-3 text-slate-100"
              rows={5}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Summarize the recent outage and draft a customer email..."
            />
          </label>

          <label className="block text-sm text-slate-300">
            LLM Provider & Model
            <select
              className="mt-1 w-full rounded-xl border border-slate-800 bg-slate-900 p-3 text-slate-100"
              value={
                selectedModel
                  ? `${selectedModel.provider}:${selectedModel.model}`
                  : ""
              }
              onChange={(e) => {
                const [provider, model] = e.target.value.split(":");
                setSelectedModel({ provider, model });
              }}
            >
              {models.map((opt) => (
                <option
                  key={`${opt.provider}-${opt.model}`}
                  value={`${opt.provider}:${opt.model}`}
                >
                  {opt.provider} · {opt.model}
                </option>
              ))}
            </select>
          </label>

          <button
            type="submit"
            className="w-full rounded-full bg-cyan-400 py-3 font-semibold text-slate-900 disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "Thinking..." : "Run Agent"}
          </button>
          {error && <p className="text-rose-300 text-sm">{error}</p>}
        </form>
        {result && (
          <article className="mt-6 p-4 border border-slate-800 rounded-2xl bg-slate-900/40">
            <p className="text-xs uppercase tracking-widest text-slate-400">
              Final Answer
            </p>
            <p className="mt-2 text-slate-100 whitespace-pre-wrap">
              {result.final_answer}
            </p>
            <p className="text-xs text-slate-500 mt-3">
              {result.provider} / {result.model}
            </p>
          </article>
        )}
      </section>
      <section className="card space-y-6">
        <div>
          <h2 className="text-lg font-semibold mb-3">Execution Timeline</h2>
          <Timeline steps={result?.steps ?? []} />
        </div>
        <div>
          <h2 className="text-lg font-semibold mb-3">RAG Evidence</h2>
          <RagHits hits={result?.rag_hits ?? []} />
        </div>
      </section>
    </div>
  );
}


