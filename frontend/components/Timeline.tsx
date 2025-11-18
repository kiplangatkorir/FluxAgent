"use client";

import clsx from "clsx";

type Step = {
  id: string;
  name: string;
  type: string;
  status: "pending" | "in_progress" | "done" | "error";
  input?: string;
  output?: string;
};

const statusIcon: Record<Step["status"], string> = {
  pending: "⏳",
  in_progress: "🧠",
  done: "✅",
  error: "⚠️",
};

const statusColor: Record<Step["status"], string> = {
  pending: "text-slate-300",
  in_progress: "text-cyan-300",
  done: "text-emerald-300",
  error: "text-rose-300",
};

export function Timeline({ steps }: { steps: Step[] }) {
  if (!steps?.length) {
    return (
      <p className="text-slate-400 text-sm">
        No intermediate steps were recorded for this run.
      </p>
    );
  }

  return (
    <div className="timeline-grid">
      {steps.map((step) => (
        <article key={step.id} className="timeline-step bg-slate-900/40">
          <header className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span
                className={clsx(
                  "text-xl transition",
                  statusColor[step.status] ?? "text-slate-200"
                )}
              >
                {statusIcon[step.status] ?? "•"}
              </span>
              <div>
                <p className="font-semibold text-sm">{step.name}</p>
                <p className="text-xs uppercase tracking-widest text-slate-400">
                  {step.type}
                </p>
              </div>
            </div>
            <span
              className={clsx(
                "badge px-3 py-1 rounded-full border",
                statusColor[step.status]
              )}
            >
              {step.status.replace("_", " ")}
            </span>
          </header>
          {step.input && (
            <p className="text-xs text-slate-400 mb-2">
              <strong className="text-slate-200">input:</strong> {step.input}
            </p>
          )}
          {step.output && (
            <p className="text-xs text-slate-400 whitespace-pre-wrap">
              <strong className="text-slate-200">output:</strong>{" "}
              {step.output?.slice(0, 500)}
            </p>
          )}
        </article>
      ))}
    </div>
  );
}

