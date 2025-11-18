"use client";

import "./globals.css";
import Link from "next/link";
import { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100 min-h-screen">
        <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-20">
          <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
            <Link href="/" className="text-xl font-semibold tracking-wide">
              FluxAgent
            </Link>
            <nav className="flex gap-6 text-sm uppercase tracking-widest">
              <Link href="/upload" className="hover:text-cyan-300 transition">
                Upload Docs
              </Link>
              <Link href="/query" className="hover:text-cyan-300 transition">
                Agent Query
              </Link>
            </nav>
          </div>
        </header>
        <main className="max-w-6xl mx-auto px-6 py-10">{children}</main>
      </body>
    </html>
  );
}

