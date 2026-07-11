import { Link } from "react-router-dom";
import { ShieldCheck } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-[#0B0F1A] border-b border-white/10">
      <Link to="/" className="flex items-center gap-2 text-white font-semibold text-lg">
        <ShieldCheck className="text-[#0ED3CF]" size={22} />
        CodeGuard
      </Link>
      <div className="flex gap-6 text-gray-400 text-sm">
        <Link to="/" className="hover:text-white transition">Home</Link>
        <Link to="/dashboard" className="hover:text-white transition">Dashboard</Link>
      </div>
    </nav>
  );
}
