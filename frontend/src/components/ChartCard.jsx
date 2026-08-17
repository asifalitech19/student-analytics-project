
import React from "react";

function PremiumChartCard({ 
  title = "Analytics Overview", 
  subtitle = "Student dataset analytics",
  isLive = true,
  action, // Pass buttons or dropdowns here (e.g., <button>Last 7 Days</button>)
  children 
}) {
  return (
    <div className="group relative flex flex-col overflow-hidden rounded-2xl bg-white border border-slate-200 shadow-sm transition-all duration-300 hover:shadow-xl">
      
      {/* =========================================================
          TOP HOVER ACCENT
      ========================================================== */}
      <div className="absolute top-0 left-0 h-1 w-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />

      {/* =========================================================
          HEADER SECTION
      ========================================================== */}
      <div className="px-6 py-5 border-b border-slate-100 bg-slate-50/50 flex flex-wrap items-center justify-between gap-4">
        
        {/* TEXT & BADGES */}
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-lg font-extrabold tracking-tight text-slate-900">
              {title}
            </h2>
            
            {/* UPGRADED LIVE INDICATOR */}
            {isLive && (
              <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] uppercase tracking-wide font-bold text-emerald-600 border border-emerald-100 shadow-sm transition-colors hover:bg-emerald-100">
                <span className="relative flex h-1.5 w-1.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-emerald-500"></span>
                </span>
                Live
              </span>
            )}
          </div>
          
          {subtitle && (
            <p className="mt-1 text-sm font-medium text-slate-500">
              {subtitle}
            </p>
          )}
        </div>

        {/* OPTIONAL ACTION AREA (Filters, Export, etc.) */}
        {action && (
          <div className="shrink-0">
            {action}
          </div>
        )}
      </div>

      {/* =========================================================
          CHART AREA
      ========================================================== */}
      <div className="relative flex-1 bg-white p-6">
        
        {/* SUBTLE BACKGROUND GRID */}
        <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_right,#f1f5f9_1px,transparent_1px),linear-gradient(to_bottom,#f1f5f9_1px,transparent_1px)] bg-[size:24px_24px] opacity-40" />
        
        {/* CONTENT */}
        <div className="relative z-10 h-full w-full">
          {children}
        </div>
        
      </div>
      
    </div>
  );
}

export default PremiumChartCard;