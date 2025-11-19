"use client";

import { useState } from "react";
import { uploadDocument } from "@/lib/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) {
      setError("Select a document first.");
      return;
    }
    setStatus(null);
    setError(null);
    setUploading(true);
    try {
      const response = await uploadDocument(file);
      setStatus(
        `Uploaded ${response.filename}, ${response.chunks_indexed} chunks indexed.`
      );
    } catch (err: any) {
      setError(err.message ?? "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <section className="card max-w-3xl mx-auto">
      <h1 className="text-2xl font-semibold mb-4">Upload Documents</h1>
      <p className="text-sm text-slate-400 mb-6">
        Text and PDF files are supported. They are embedded with pgvector and
        become available to the agent&apos;s RAG tool instantly.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <label className="block">
          <input
            type="file"
            className="w-full rounded-xl border border-slate-800 bg-slate-900 p-4 text-slate-200"
            onChange={(event) =>
              setFile(event.target.files ? event.target.files[0] : null)
            }
          />
        </label>
        <button
          type="submit"
          className="rounded-full bg-cyan-400 px-6 py-3 font-semibold text-slate-900 disabled:opacity-60"
          disabled={uploading}
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </form>

      {status && (
        <p className="text-emerald-300 text-sm mt-4 bg-slate-900/60 p-3 rounded-lg">
          {status}
        </p>
      )}
      {error && (
        <p className="text-rose-300 text-sm mt-4 bg-slate-900/60 p-3 rounded-lg">
          {error}
        </p>
      )}
    </section>
  );
}


