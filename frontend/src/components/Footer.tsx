export function Footer() {
  return (
    <footer className="border-t border-gray-100 py-12 px-6">
      <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <span className="text-lg font-bold text-gray-900">
            <span className="text-indigo-600">CTO</span> Agent
          </span>
          <p className="text-sm text-gray-400 mt-1">Your AI-powered engineering strategist</p>
        </div>
        <div className="flex gap-6 text-sm text-gray-400">
          <a href="#" className="hover:text-gray-600 transition-colors">Privacy</a>
          <a href="#" className="hover:text-gray-600 transition-colors">Terms</a>
          <a href="#" className="hover:text-gray-600 transition-colors">Contact</a>
        </div>
        <p className="text-xs text-gray-300">© 2026 CTO Agent. All rights reserved.</p>
      </div>
    </footer>
  );
}
