export default function Landing() {
  return (
    <div className="min-h-screen bg-[#0B0F1A] text-white flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-5xl font-bold">CodeGuard</h1>
        <p className="text-gray-400 mt-4 text-lg">AI-powered multi-agent code review</p>
        <a href="/dashboard" className="inline-block mt-8 px-8 py-3 bg-[#0ED3CF] text-black font-semibold rounded-lg hover:opacity-90 transition">
          Open Dashboard
        </a>
      </div>
    </div>
  );
}
