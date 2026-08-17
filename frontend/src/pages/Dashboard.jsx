
import React, { useEffect, useState } from "react";
import {
  Activity,
  BarChart3,
  BookOpen,
  GraduationCap,
  Users,
  Loader2,
  Sparkles,
  ShieldCheck,
  Languages,
  Home,
  LayoutDashboard
} from "lucide-react";
import {
  PieChart, Pie, Cell, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from "recharts";
import api from "../api/api";
import StatCard from "../components/StatCard";

const COLORS = ["#4f46e5", "#0ea5e9", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"];

// ============================================================
// REUSABLE COMPONENTS (Optimized)
// ============================================================

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-2xl border border-white/20 bg-white/80 p-4 shadow-xl backdrop-blur-md ring-1 ring-slate-900/5">
        <p className="mb-3 text-sm font-bold uppercase tracking-wider text-slate-500">{label}</p>
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center gap-3">
            <div className="h-3 w-3 rounded-full shadow-sm" style={{ backgroundColor: entry.color }} />
            <span className="font-semibold text-slate-700">{entry.name}:</span>
            <span className="font-extrabold text-slate-900">{entry.value}</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

const ChartShell = ({ title, subtitle, children, icon: Icon, colorClass, bgClass }) => (
  <div className="group relative flex h-full flex-col overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-sm transition-all hover:shadow-xl hover:-translate-y-1">
    <div className="border-b border-slate-100 bg-slate-50/50 px-6 py-5">
      <div className="flex items-center gap-4">
        <div className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl ${bgClass}`}>
          <Icon size={22} className={colorClass} strokeWidth={2.5} />
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-800">{title}</h3>
          <p className="text-xs font-medium text-slate-500">{subtitle}</p>
        </div>
      </div>
    </div>
    <div className="flex-1 px-4 py-6">
      <ResponsiveContainer width="100%" height={320}>
        {children}
      </ResponsiveContainer>
    </div>
  </div>
);

// ============================================================
// MAIN DASHBOARD COMPONENT
// ============================================================

function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Tab State: "overview" or "deepdive"
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get("/api/dashboard/analytics");
      setAnalytics(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load data.");
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // LOADING & ERROR STATES
  // ==========================================================
  if (loading) {
    return (
      <div className="flex min-h-[70vh] items-center justify-center">
        <div className="text-center">
          <Loader2 size={40} className="mx-auto animate-spin text-blue-600" />
          <h2 className="mt-5 text-xl font-bold text-slate-800">Initializing Command Center</h2>
          <p className="mt-2 text-sm text-slate-500">Fetching unified analytics and predictions...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-[70vh] items-center justify-center">
        <div className="w-full max-w-lg rounded-3xl border border-rose-200 bg-white p-8 text-center shadow-lg">
          <Activity size={40} className="mx-auto text-rose-500" />
          <h2 className="mt-5 text-2xl font-bold text-slate-900">Connection Lost</h2>
          <p className="mt-2 text-slate-500">{error}</p>
          <button onClick={loadDashboard} className="mt-6 rounded-xl bg-blue-600 px-6 py-3 font-bold text-white hover:bg-blue-700">
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  const kpis = analytics?.kpis || {};
  const charts = analytics?.charts || {};
  const insights = analytics?.insights || {};

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8 animate-in fade-in duration-500">
      
      {/* ======================================================
          PAGE HEADER & TAB SWITCHER
      ====================================================== */}
      <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <h1 className="text-4xl font-black tracking-tight text-slate-900">
            Student <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Analytics</span>
          </h1>
          <p className="mt-2 font-medium text-slate-500">Complete overview and deep-dive analytics of the student dataset.</p>
        </div>

        <div className="flex rounded-2xl bg-slate-100 p-1.5 shadow-inner">
          <button
            onClick={() => setActiveTab("overview")}
            className={`flex items-center gap-2 rounded-xl px-6 py-2.5 text-sm font-bold transition-all ${
              activeTab === "overview" ? "bg-white text-blue-700 shadow-sm" : "text-slate-500 hover:text-slate-800"
            }`}
          >
            <LayoutDashboard size={18} /> Basic Overview
          </button>
          <button
            onClick={() => setActiveTab("deepdive")}
            className={`flex items-center gap-2 rounded-xl px-6 py-2.5 text-sm font-bold transition-all ${
              activeTab === "deepdive" ? "bg-white text-indigo-700 shadow-sm" : "text-slate-500 hover:text-slate-800"
            }`}
          >
            <BarChart3 size={18} /> Deep Dive Analytics
          </button>
        </div>
      </div>

      {/* ======================================================
          TAB 1: BASIC OVERVIEW
      ====================================================== */}
      {activeTab === "overview" && (
        <div className="space-y-8 animate-in slide-in-from-bottom-4 duration-500">
          
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
            <StatCard title="Total Students" value={kpis.total_students ?? 0} color="#2563EB" />
            <StatCard title="Average CGPA" value={Number(kpis.average_cgpa ?? 0).toFixed(2)} color="#10B981" />
            <StatCard title="Study Hours/Day" value={Number(kpis.average_study_hours ?? 0).toFixed(1)} color="#F59E0B" />
            <StatCard title="Scholarship Rate" value={`${Number(kpis.scholarship_rate ?? 0).toFixed(1)}%`} color="#8B5CF6" />
          </div>

          <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
            <ChartShell title="Gender Breakdown" subtitle="Distribution by gender" icon={Users} colorClass="text-blue-600" bgClass="bg-blue-50">
              <PieChart>
                <Pie data={charts.gender_distribution || []} dataKey="count" nameKey="gender" cx="50%" cy="45%" outerRadius={105} innerRadius={60} paddingAngle={4} stroke="none">
                  {(charts.gender_distribution || []).map((_, i) => <Cell key={`cell-${i}`} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend verticalAlign="bottom" height={36} iconType="circle" />
              </PieChart>
            </ChartShell>

            <ChartShell title="Relationship Status" subtitle="Student distribution by relationship" icon={Users} colorClass="text-amber-600" bgClass="bg-amber-50">
              <BarChart data={charts.relationship_distribution || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="status" tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} dy={10} />
                <YAxis tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} />
                <RechartsTooltip content={<CustomTooltip />} cursor={{ fill: "#f59e0b10" }} />
                <Bar dataKey="count" name="Students" fill="#f59e0b" radius={[6, 6, 0, 0]} maxBarSize={60} />
              </BarChart>
            </ChartShell>

            <ChartShell title="Living Arrangements" subtitle="Where the student body resides" icon={Home} colorClass="text-purple-600" bgClass="bg-purple-50">
              <BarChart data={charts.living_distribution || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="arrangement" tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} dy={10} />
                <YAxis tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} />
                <RechartsTooltip content={<CustomTooltip />} cursor={{ fill: "#8b5cf610" }} />
                <Bar dataKey="count" name="Students" fill="#8b5cf6" radius={[6, 6, 0, 0]} maxBarSize={60} />
              </BarChart>
            </ChartShell>
          </div>
        </div>
      )}

      {/* ======================================================
          TAB 2: DEEP DIVE ANALYTICS
      ====================================================== */}
      {activeTab === "deepdive" && (
        <div className="space-y-8 animate-in slide-in-from-bottom-4 duration-500">
          
          <div>
            <div className="mb-4 flex items-center gap-2">
              <Sparkles size={24} className="text-indigo-500" />
              <h2 className="text-2xl font-bold tracking-tight text-slate-900">AI Discoveries</h2>
            </div>
            <div className="grid grid-cols-1 gap-5 md:grid-cols-3">
              <div className="rounded-3xl bg-gradient-to-br from-indigo-900 to-slate-900 p-6 text-white shadow-lg">
                <p className="text-[11px] font-bold uppercase tracking-wider text-indigo-300">Largest Demographic</p>
                <h3 className="mt-2 text-2xl font-black">{insights.top_gender?.gender ? `${insights.top_gender.gender}s` : "N/A"}</h3>
                <p className="text-sm font-medium text-indigo-200">{insights.top_gender?.count ?? 0} students</p>
              </div>
              <div className="rounded-3xl bg-gradient-to-br from-purple-900 to-slate-900 p-6 text-white shadow-lg">
                <p className="text-[11px] font-bold uppercase tracking-wider text-purple-300">Primary Funding</p>
                <h3 className="mt-2 text-2xl font-black">{insights.top_scholarship?.status === 'No' ? 'Self-Funded' : insights.top_scholarship?.status === 'Yes' ? 'On Scholarship' : 'N/A'}</h3>
                <p className="text-sm font-medium text-purple-200">{insights.top_scholarship?.students ?? 0} students</p>
              </div>
              <div className="rounded-3xl bg-gradient-to-br from-emerald-900 to-slate-900 p-6 text-white shadow-lg">
                <p className="text-[11px] font-bold uppercase tracking-wider text-emerald-300">Highest Achievers</p>
                <h3 className="mt-2 text-2xl font-black">{insights.best_scholarship_group?.status === 'Yes' ? 'Scholarship Holders' : insights.best_scholarship_group?.status === 'No' ? 'Self-Funded' : 'N/A'}</h3>
                <p className="text-sm font-medium text-emerald-200">Avg CGPA: {Number(insights.best_scholarship_group?.average_cgpa || 0).toFixed(2)}</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-8 xl:grid-cols-2">
            <ChartShell title="CGPA Distribution" subtitle="Performance spectrum across all students" icon={GraduationCap} colorClass="text-blue-600" bgClass="bg-blue-50">
              <BarChart data={charts.cgpa_distribution || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="range" tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} dy={10} />
                <YAxis tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} />
                <RechartsTooltip content={<CustomTooltip />} cursor={{ fill: "#2563eb10" }} />
                <Bar dataKey="count" name="Students" fill="#2563eb" radius={[6, 6, 0, 0]} maxBarSize={60} />
              </BarChart>
            </ChartShell>

            <ChartShell title="Study Hours Impact" subtitle="Average CGPA by daily study commitment" icon={BookOpen} colorClass="text-emerald-600" bgClass="bg-emerald-50">
              <BarChart data={charts.study_analysis || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="study_band" tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} dy={10} />
                <YAxis domain={[0, 4]} tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} />
                <RechartsTooltip content={<CustomTooltip />} cursor={{ fill: "#10b98110" }} />
                <Bar dataKey="average_cgpa" name="Average CGPA" fill="#10b981" radius={[6, 6, 0, 0]} maxBarSize={60} />
              </BarChart>
            </ChartShell>

            <ChartShell title="Scholarship Performance" subtitle="Academic outcomes based on funding" icon={ShieldCheck} colorClass="text-purple-600" bgClass="bg-purple-50">
              <BarChart data={charts.scholarship_analysis || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="status" tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} dy={10} />
                <YAxis domain={[0, 4]} tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} />
                <RechartsTooltip content={<CustomTooltip />} cursor={{ fill: "#8b5cf610" }} />
                <Bar dataKey="average_cgpa" name="Average CGPA" fill="#8b5cf6" radius={[6, 6, 0, 0]} maxBarSize={60} />
              </BarChart>
            </ChartShell>

            <ChartShell title="Language Proficiency" subtitle="English communication levels" icon={Languages} colorClass="text-cyan-600" bgClass="bg-cyan-50">
              <BarChart data={charts.english_distribution || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="level" tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} dy={10} />
                <YAxis tick={{ fill: "#64748B", fontSize: 12 }} axisLine={false} tickLine={false} />
                <RechartsTooltip content={<CustomTooltip />} cursor={{ fill: "#06b6d410" }} />
                <Bar dataKey="count" name="Students" fill="#06b6d4" radius={[6, 6, 0, 0]} maxBarSize={60} />
              </BarChart>
            </ChartShell>
          </div>
        </div>
      )}

    </div>
  );
}

export default Dashboard;