import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-8">
      <main className="max-w-2xl text-center flex flex-col gap-8 items-center">
        <h1 className="text-5xl font-bold tracking-tight">Omni-Route</h1>
        <p className="text-xl text-gray-400">
          Offline-first educational orchestrator.
        </p>

        <div className="flex gap-4 items-center flex-col sm:flex-row mt-8">
          <Link
            className="rounded-none border-2 border-white bg-white text-black px-8 py-3 text-lg font-semibold hover:bg-black hover:text-white transition-colors"
            href="/dashboard"
          >
            Go to Dashboard
          </Link>
        </div>
      </main>
      <footer className="absolute bottom-8 text-gray-500 text-sm">
        Strictly Monochromatic
      </footer>
    </div>
  );
}
