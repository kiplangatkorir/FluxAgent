const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

export type ModelOption = {
  provider: string;
  model: string;
};

export async function uploadDocument(file: File) {
  const data = new FormData();
  data.append("file", file);

  const response = await fetch(`${API_BASE}/documents/upload`, {
    method: "POST",
    body: data,
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

export async function fetchModels(): Promise<ModelOption[]> {
  const response = await fetch(`${API_BASE}/models`);
  if (!response.ok) {
    throw new Error("Failed to load model list");
  }
  const data = await response.json();
  return data.options;
}

export type StepStatus = "pending" | "in_progress" | "done" | "error";

export type AgentResponse = {
  final_answer: string;
  steps: {
    id: string;
    name: string;
    type: string;
    status: StepStatus;
    input?: string;
    output?: string;
  }[];
  rag_hits: {
    content: string;
    metadata: Record<string, string>;
  }[];
  provider: string;
  model: string;
};

export async function runAgent(body: {
  query: string;
  provider?: string;
  model?: string;
}): Promise<AgentResponse> {
  const response = await fetch(`${API_BASE}/agent/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

