"use client";

type RagHit = {
  content: string;
  metadata: Record<string, string>;
};

export function RagHits({ hits }: { hits: RagHit[] }) {
  if (!hits?.length) {
    return (
      <p className="text-slate-400 text-sm">
        No vector-store matches used for this answer.
      </p>
    );
  }

  return (
    <div className="space-y-3">
      {hits.map((hit, index) => (
        <article
          key={`${index}-${hit.metadata?.filename ?? "hit"}`}
          className="rounded-xl border border-slate-800 bg-slate-900/60 p-4"
        >
          <p className="text-xs text-cyan-300 uppercase tracking-widest mb-2">
            RAG MATCH #{index + 1}
          </p>
          <p className="text-sm text-slate-200 whitespace-pre-wrap">
            {hit.content.slice(0, 400)}
          </p>
          <p className="text-xs text-slate-500 mt-2">
            {hit.metadata?.filename ?? "uploaded document"}
          </p>
        </article>
      ))}
    </div>
  );
}


