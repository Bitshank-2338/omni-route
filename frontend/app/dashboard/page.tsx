"use client";

import { useState } from "react";
import Link from "next/link";

interface Flashcard {
  id: number;
  front: string;
  back: string;
}

export default function Dashboard() {
  const [file, setFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setIsProcessing(true);
    setError(null);
    setFlashcards([]);

    const formData = new FormData();
    formData.append("file", file);

    const isAudio = file.type.startsWith("audio/");
    const endpoint = isAudio ? "/process-audio" : "/process-document";

    try {
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process file.");
      }

      const data = await response.json();
      setFlashcards(data.flashcards);
    } catch (err: any) {
      setError(err.message || "An error occurred.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-8 font-sans">
      <header className="mb-12 border-b border-gray-800 pb-4 flex justify-between items-center">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Link href="/" className="text-gray-400 hover:text-white underline">
          Back to Home
        </Link>
      </header>

      <main className="max-w-4xl mx-auto space-y-12">
        <section className="border-2 border-white p-8">
          <h2 className="text-2xl font-semibold mb-6">Upload Material</h2>
          <div className="flex flex-col gap-4">
            <input
              type="file"
              accept=".pdf,audio/*"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-400
                file:mr-4 file:py-2 file:px-4
                file:border-0 file:text-sm file:font-semibold
                file:bg-white file:text-black
                hover:file:bg-gray-200 cursor-pointer"
            />
            {error && <p className="text-white bg-gray-900 border border-white p-2">{error}</p>}
            <button
              onClick={handleUpload}
              disabled={isProcessing || !file}
              className="mt-4 bg-white text-black px-6 py-2 font-bold disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-200 transition-colors self-start"
            >
              {isProcessing ? "Processing..." : "Process File"}
            </button>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-6">Generated Flashcards</h2>

          {isProcessing ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="border border-gray-700 p-6 h-32 bg-gray-900">
                  <div className="h-4 bg-gray-700 rounded w-3/4 mb-4"></div>
                  <div className="h-4 bg-gray-700 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : flashcards.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {flashcards.map((card) => (
                <div key={card.id} className="border border-white p-6 flex flex-col justify-between">
                  <div>
                    <h3 className="font-bold text-gray-400 uppercase text-xs mb-2">Front</h3>
                    <p className="text-lg mb-4">{card.front}</p>
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-400 uppercase text-xs mb-2">Back</h3>
                    <p className="text-md text-gray-300">{card.back}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 italic">No flashcards generated yet. Upload a file to begin.</p>
          )}
        </section>
      </main>
    </div>
  );
}
