import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  BrainCircuit,
  GraduationCap,
  Sparkles,
  ChevronRight
} from "lucide-react";

function Sidebar() {
  const menuItems = [
    {
      name: "Overview & Insights", // Name updated here
      path: "/",
      icon: LayoutDashboard,
    },
    {
      name: "AI Prediction",
      path: "/prediction",
      icon: BrainCircuit,
    },
  ];

  return (
    <aside className="sticky top-0 flex h-screen min-h-screen w-[270px] flex-col border-r border-slate-200/80 bg-white shadow-sm">
      
      {/* BRAND AREA */}
      <div className="border-b border-slate-100 px-6 py-6">
        <div className="flex items-center gap-3.5">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-md shadow-blue-500/20">
            <GraduationCap size={22} strokeWidth={2.5} />
          </div>
          <div>
            <h1 className="text-sm font-black tracking-tight text-slate-900">
              AI Student
            </h1>
            <p className="text-[10px] font-bold uppercase tracking-wider text-blue-600">
              Analytics Platform
            </p>
          </div>
        </div>
      </div>

      {/* NAVIGATION MENU */}
      <div className="px-4 pt-6">
        <p className="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400">
          Main Menu
        </p>

        <nav className="space-y-1.5">
          {menuItems.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === "/"}
                className={({ isActive }) =>
                  `group relative flex items-center justify-between rounded-xl px-3.5 py-3 transition-all duration-200 ${
                    isActive
                      ? "bg-blue-50/80 text-blue-700 font-bold shadow-sm"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-900 font-medium"
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    {isActive && (
                      <span className="absolute left-0 top-2.5 bottom-2.5 w-1 rounded-r-full bg-blue-600" />
                    )}

                    <div className="flex items-center gap-3">
                      <div
                        className={`flex h-9 w-9 items-center justify-center rounded-lg transition-colors ${
                          isActive
                            ? "bg-blue-100 text-blue-700"
                            : "bg-slate-100/80 text-slate-500 group-hover:bg-slate-200 group-hover:text-slate-800"
                        }`}
                      >
                        <Icon size={18} strokeWidth={2} />
                      </div>
                      <span className="text-sm">{item.name}</span>
                    </div>

                    <ChevronRight
                      size={15}
                      className={`transition-all ${
                        isActive
                          ? "translate-x-0 text-blue-600 opacity-100"
                        : "-translate-x-2 text-slate-300 opacity-0 group-hover:translate-x-0 group-hover:opacity-100"
                      }`}
                    />
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* BOTTOM STATUS WIDGET */}
      <div className="mt-auto p-4">
        <div className="flex items-center gap-3 rounded-2xl border border-slate-100 bg-slate-50/60 p-3.5">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm">
            <Sparkles size={16} />
          </div>
          <div className="min-w-0">
            <p className="text-xs font-bold text-slate-800">AI Engine Online</p>
            <p className="text-[10px] font-medium text-emerald-600 flex items-center gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Secure & Connected
            </p>
          </div>
        </div>
      </div>

    </aside>
  );
}

export default Sidebar;