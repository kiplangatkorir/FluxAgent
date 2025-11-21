"use client";

import { useState } from "react";
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
  const [expandedSteps, setExpandedSteps] = useState<Set<string>>(new Set());

  const toggleStep = (stepId: string) => {
    setExpandedSteps((prev) => {
      const next = new Set(prev);
      if (next.has(stepId)) {
        next.delete(stepId);
      } else {
        next.add(stepId);
      }
      return next;
    });
  };

  if (!steps?.length) {
    return (
      <p className="text-slate-400 text-sm">
        No intermediate steps were recorded for this run.
      </p>
    );
  }

  return (
    <div className="timeline-grid">
      {steps.map((step) => {
        const isExpanded = expandedSteps.has(step.id);
        const hasDetails = step.input || step.output;

        return (
          <article key={step.id} className="timeline-step bg-slate-900/40">
            <header
              className={clsx(
                "flex items-center justify-between",
                hasDetails && "cursor-pointer hover:opacity-80 transition-opacity"
              )}
              onClick={() => hasDetails && toggleStep(step.id)}
            >
              <div className="flex items-center gap-2 flex-1">
                <span
                  className={clsx(
                    "text-xl transition",
                    statusColor[step.status] ?? "text-slate-200"
                  )}
                >
                  {statusIcon[step.status] ?? "•"}
                </span>
                <div className="flex-1">
                  <p className="font-semibold text-sm">{step.name}</p>
                  <p className="text-xs uppercase tracking-widest text-slate-400">
                    {step.type}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span
                  className={clsx(
                    "badge px-3 py-1 rounded-full border",
                    statusColor[step.status]
                  )}
                >
                  {step.status.replace("_", " ")}
                </span>
                {hasDetails && (
                  <span
                    className={clsx(
                      "text-slate-400 text-sm transition-transform duration-200",
                      isExpanded && "rotate-90"
                    )}
                  >
                    ▶
                  </span>
                )}
              </div>
            </header>
            {hasDetails && (
              <div
                className={clsx(
                  "overflow-hidden transition-all duration-300 ease-in-out",
                  isExpanded ? "max-h-[2000px] mt-3" : "max-h-0"
                )}
              >
                {step.input && (
                  <div className="mb-3 p-3 rounded-lg bg-slate-800/50 border border-slate-700">
                    <p className="text-xs font-semibold text-slate-300 mb-1">
                      Input
                    </p>
                    <p className="text-xs text-slate-400 whitespace-pre-wrap break-words">
                      {step.input}
                    </p>
                  </div>
                )}
                {step.output && (
                  <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700">
                    <p className="text-xs font-semibold text-slate-300 mb-1">
                      Output
                    </p>
                    <p className="text-xs text-slate-400 whitespace-pre-wrap break-words">
                      {step.output}
                    </p>
                  </div>
                )}
              </div>
            )}
          </article>
        );
      })}
    </div>
  );
}

