import React from "react";
import { Bell, ChevronDown, User } from "lucide-react";

function Navbar() {
  return (
    <header className="sticky top-0 z-30 flex h-20 w-full items-center justify-end border-b border-slate-200/80 bg-white/80 px-6 backdrop-blur-xl lg:px-10">
      
      <div className="flex items-center gap-4 lg:gap-6">
        
        {/* Notification Bell */}
        <button className="relative flex h-10 w-10 items-center justify-center rounded-full text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-800">
          <Bell size={20} />
          <span className="absolute right-2.5 top-2 h-2 w-2 rounded-full border-2 border-white bg-rose-500" />
        </button>

        {/* Divider */}
        <div className="hidden h-8 w-px bg-slate-200 lg:block" />

        {/* User Profile (Name removed as requested) */}
        <button className="group flex items-center gap-3 text-left transition-opacity hover:opacity-80">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-50 text-blue-600 shadow-sm ring-1 ring-blue-600/10">
            <User size={18} strokeWidth={2.5} />
          </div>
          <div className="hidden lg:block">
            <p className="text-sm font-bold text-slate-800">Administrator</p>
            <p className="text-[11px] font-semibold tracking-wide text-slate-400">System Admin</p>
          </div>
          <ChevronDown size={16} className="hidden text-slate-400 transition-transform group-hover:translate-y-0.5 lg:block" />
        </button>

      </div>
    </header>
  );
}

export default Navbar;