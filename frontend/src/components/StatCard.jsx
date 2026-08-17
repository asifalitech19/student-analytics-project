import React from "react";

function PremiumStatCard({
  title = "Total Revenue",
  value = "$45,231.89",
  trend, // e.g., 20.5 or -5.2
  trendText = "vs last month",
  icon: Icon, // Pass a React component like a Heroicon or Lucide icon
  color = "#2563eb", // Default blue
}) {
  const isPositive = trend >= 0;

  return (
    <div className="group relative overflow-hidden rounded-2xl bg-white p-6 border border-slate-200 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
      
      {/* =========================================================
          BACKGROUND GLOW ACCENT
      ========================================================== */}
      <div 
        className="absolute -right-6 -top-6 h-24 w-24 rounded-full opacity-20 blur-2xl transition-all duration-500 group-hover:scale-150 group-hover:opacity-30"
        style={{ backgroundColor: color }}
      />
      
      {/* TOP BORDER ACCENT */}
      <div 
        className="absolute left-0 top-0 h-1 w-full transition-opacity duration-300 opacity-80 group-hover:opacity-100" 
        style={{ backgroundColor: color }} 
      />

      {/* =========================================================
          CARD CONTENT
      ========================================================== */}
      <div className="relative flex items-start justify-between gap-4">

        {/* TEXT SECTION */}
        <div className="min-w-0">
          <p className="text-sm font-semibold uppercase tracking-wider text-slate-500">
            {title}
          </p>

          <p className="mt-2 text-3xl font-extrabold tracking-tight text-slate-900">
            {value}
          </p>

          {/* TREND INDICATOR (Optional) */}
          {trend !== undefined && (
            <div className="mt-3 flex items-center gap-2">
              <span
                className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold ${
                  isPositive
                    ? "bg-emerald-50 text-emerald-600 border border-emerald-100"
                    : "bg-rose-50 text-rose-600 border border-rose-100"
                }`}
              >
                {isPositive ? (
                  <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                  </svg>
                ) : (
                  <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                  </svg>
                )}
                {Math.abs(trend)}%
              </span>
              <span className="text-xs font-medium text-slate-400">
                {trendText}
              </span>
            </div>
          )}
        </div>

        {/* ICON / ACCENT SECTION */}
        <div
          className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl shadow-inner ring-1 ring-black/5 transition-transform duration-300 group-hover:scale-110 group-hover:-rotate-3"
          style={{
            backgroundColor: `${color}15`,
            color: color,
          }}
        >
          {Icon ? (
            <Icon className="h-7 w-7" />
          ) : (
            <div
              className="h-4 w-4 rounded-full shadow-sm"
              style={{ backgroundColor: color }}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default PremiumStatCard;