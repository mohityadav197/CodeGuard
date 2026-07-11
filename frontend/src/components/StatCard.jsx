export default function StatCard({ label, value }) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-6">
      <p className="text-gray-400 text-sm">{label}</p>
      <p className="text-3xl font-bold text-white mt-2">{value}</p>
    </div>
  );
}
