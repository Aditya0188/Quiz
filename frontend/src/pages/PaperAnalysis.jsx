import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import client from '../api/client';
import { SUBJECTS } from '../utils/constants';
import { 
  BarChart2, Calendar, TrendingUp, BookOpen, Clock, 
  CheckCircle, Play, Layers, Award, Target, ArrowRight, Loader2, Sparkles, Filter
} from 'lucide-react';
import { 
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell 
} from 'recharts';
import toast from 'react-hot-toast';

const PaperAnalysis = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState('year'); // 'year' | 'trends'
  const [yearsList, setYearsList] = useState([]);
  const [selectedYear, setSelectedYear] = useState(2026);
  const [yearData, setYearData] = useState(null);
  const [loadingYear, setLoadingYear] = useState(false);

  // Trends Tab state
  const [selectedSubject, setSelectedSubject] = useState('ALL');
  const [trendsData, setTrendsData] = useState([]);
  const [loadingTrends, setLoadingTrends] = useState(false);

  // Overview stats
  const [overview, setOverview] = useState(null);

  // 1. Initial Load: Fetch years list & overall stats
  useEffect(() => {
    const fetchInitial = async () => {
      try {
        const [ovRes, yrRes] = await Promise.all([
          client.get('/paper-analysis/overview').catch(() => ({ data: null })),
          client.get('/paper-analysis/years').catch(() => ({ data: [] }))
        ]);
        setOverview(ovRes.data);
        const yList = yrRes.data || [];
        setYearsList(yList);
        if (yList.length > 0) {
          const defaultYr = yList.find(y => y.year === 2026)?.year || yList[0].year;
          setSelectedYear(defaultYr);
        }
      } catch (err) {
        console.error('Failed to load initial paper analysis', err);
      }
    };
    fetchInitial();
  }, []);

  // 2. Load Selected Year Details
  useEffect(() => {
    if (!selectedYear) return;
    const fetchYearDetail = async () => {
      setLoadingYear(true);
      try {
        const res = await client.get(`/paper-analysis/year/${selectedYear}`);
        setYearData(res.data);
      } catch (err) {
        console.error('Failed to load year analysis', err);
      } finally {
        setLoadingYear(false);
      }
    };
    fetchYearDetail();
  }, [selectedYear]);

  // 3. Load Subject Trends
  useEffect(() => {
    const fetchTrends = async () => {
      setLoadingTrends(true);
      try {
        const querySubj = selectedSubject === 'ALL' ? '' : selectedSubject;
        const res = await client.get(`/paper-analysis/subject-trends?subject=${encodeURIComponent(querySubj)}`);
        setTrendsData(res.data?.topics || []);
      } catch (err) {
        console.error('Failed to load subject trends', err);
      } finally {
        setLoadingTrends(false);
      }
    };
    fetchTrends();
  }, [selectedSubject]);

  // Practice Full Paper Handler
  const handlePracticePaper = () => {
    navigate(`/quiz/config?year=${selectedYear}&subject=ALL`);
  };

  // Practice Specific Topic Handler
  const handlePracticeTopic = (subject, topic) => {
    navigate(`/quiz/config?subject=${encodeURIComponent(subject)}&topic=${encodeURIComponent(topic)}`);
  };

  // Format chart data for year
  const chartData = (yearData?.subjects || []).map(s => ({
    name: s.subject.length > 14 ? s.subject.slice(0, 12) + '..' : s.subject,
    fullName: s.subject,
    marks: s.total_marks,
    questions: s.question_count
  }));

  const COLORS = ['#1e3a5f', '#2563eb', '#0284c7', '#0d9488', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#f97316', '#64748b', '#6366f1'];

  return (
    <div className="pt-24 pb-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-primary to-primary-light rounded-2xl p-5 sm:p-8 text-white shadow-md mb-6 sm:mb-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center space-x-2 text-primary-200 mb-1">
              <BarChart2 className="w-5 h-5 text-amber-300" />
              <span className="text-xs font-bold uppercase tracking-wider text-amber-300">GATE CS Exam Intelligence</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">36-Year Paper Analysis (1991 – 2026)</h1>
            <p className="text-primary-100 text-xs sm:text-sm mt-1 max-w-2xl">
              Understand past paper patterns, high-weightage topics, and question distribution across 36 years of actual GATE CS exams.
            </p>
          </div>

          {/* Quick Metrics */}
          {overview && (
            <div className="flex items-center gap-3 sm:gap-4 bg-white/10 backdrop-blur-md px-4 sm:px-5 py-2.5 sm:py-3 rounded-xl border border-white/20 self-stretch sm:self-auto justify-around">
              <div className="text-center">
                <span className="block text-xl sm:text-2xl font-black text-white">{overview.total_questions}</span>
                <span className="text-[10px] sm:text-xs text-primary-100 font-medium">PYQ Qs</span>
              </div>
              <div className="h-7 w-px bg-white/20"></div>
              <div className="text-center">
                <span className="block text-xl sm:text-2xl font-black text-amber-300">{overview.total_marks}</span>
                <span className="text-[10px] sm:text-xs text-primary-100 font-medium">Marks</span>
              </div>
              <div className="h-7 w-px bg-white/20"></div>
              <div className="text-center">
                <span className="block text-xl sm:text-2xl font-black text-emerald-300">{yearsList.length || 36}</span>
                <span className="text-[10px] sm:text-xs text-primary-100 font-medium">Years</span>
              </div>
            </div>
          )}
        </div>

        {/* Tab Buttons */}
        <div className="flex space-x-2 mt-4 sm:mt-6 border-t border-white/10 pt-4 overflow-x-auto pb-1">
          <button
            onClick={() => setActiveTab('year')}
            className={`flex items-center space-x-2 px-4 sm:px-5 py-2 sm:py-2.5 rounded-xl font-bold text-xs sm:text-sm whitespace-nowrap transition-all ${
              activeTab === 'year'
                ? 'bg-white text-primary shadow-sm'
                : 'bg-white/10 text-white hover:bg-white/20'
            }`}
          >
            <Calendar className="w-4 h-4" />
            <span>Year-by-Year Paper Breakdown</span>
          </button>
          <button
            onClick={() => setActiveTab('trends')}
            className={`flex items-center space-x-2 px-4 sm:px-5 py-2 sm:py-2.5 rounded-xl font-bold text-xs sm:text-sm whitespace-nowrap transition-all ${
              activeTab === 'trends'
                ? 'bg-white text-primary shadow-sm'
                : 'bg-white/10 text-white hover:bg-white/20'
            }`}
          >
            <TrendingUp className="w-4 h-4" />
            <span>36-Year High-Yield Topic Trends</span>
          </button>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* TAB 1: YEAR-BY-YEAR ANALYSIS */}
      {/* ========================================================================= */}
      {activeTab === 'year' && (
        <div className="space-y-6 sm:space-y-8">
          
          {/* Year Selector Toolbar */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 sm:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex flex-col sm:flex-row sm:items-center gap-2 max-w-full">
              <span className="text-xs sm:text-sm font-extrabold text-slate-700 whitespace-nowrap">Exam Year:</span>
              <div className="flex items-center space-x-1.5 overflow-x-auto pb-1 max-w-full">
                {[2026, 2025, 2024, 2023, 2022, 2021, 2020].map(yr => (
                  <button
                    key={yr}
                    onClick={() => setSelectedYear(yr)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap transition-all ${
                      selectedYear === yr
                        ? 'bg-primary text-white shadow-xs'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {yr}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-between sm:justify-end gap-2.5">
              <select
                value={selectedYear}
                onChange={(e) => setSelectedYear(Number(e.target.value))}
                className="flex-1 sm:flex-none px-3 py-2 border-2 border-slate-200 rounded-xl text-xs sm:text-sm font-bold text-slate-800 bg-white focus:ring-2 focus:ring-primary outline-none cursor-pointer"
              >
                {yearsList.map(y => (
                  <option key={y.year} value={y.year}>
                    GATE {y.year} ({y.total_questions} Qs, {y.total_marks}M)
                  </option>
                ))}
              </select>

              <button
                onClick={handlePracticePaper}
                className="flex items-center space-x-1.5 bg-emerald-600 hover:bg-emerald-700 text-white px-3.5 py-2 rounded-xl text-xs sm:text-sm font-black shadow-xs transition-all"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Practice {selectedYear}</span>
              </button>
            </div>
          </div>

          {/* Official Pattern Info Callout */}
          <div className="bg-gradient-to-r from-blue-50 via-indigo-50 to-emerald-50 border border-blue-200/90 rounded-2xl p-4 sm:p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-sm">
            <div className="flex items-start space-x-3.5">
              <div className="p-2.5 bg-primary text-white rounded-xl shadow-sm flex-shrink-0 mt-0.5 sm:mt-0">
                <Award className="w-5 h-5 text-amber-400" />
              </div>
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs font-black uppercase tracking-wider text-primary bg-primary/10 px-2.5 py-0.5 rounded-md">
                    Official GATE CS Pattern
                  </span>
                  <span className="text-xs font-bold text-slate-600">180 Minutes • 100 Total Marks • Exactly 65 Questions</span>
                </div>
                <p className="text-sm font-bold text-slate-800 mt-1">
                  10 General Aptitude (15 Marks) + 55 Core CS & Engg Mathematics (85 Marks) = 65 Questions (100 Marks)
                </p>
                <p className="text-xs text-slate-600 mt-0.5 max-w-3xl">
                  Official GATE Computer Science examinations consist of <strong>65 questions totaling 100 marks</strong> (30 questions of 1-Mark + 35 questions of 2-Marks) with MCQ, MSQ, and NAT question types. GATE 2026, 2025, and 2024 papers in this app feature the complete 65-question / 100-mark format.
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3 flex-shrink-0 self-end md:self-center bg-white/90 backdrop-blur-sm px-4 py-2.5 rounded-xl border border-blue-100 shadow-xs">
              <div className="text-center">
                <span className="block text-lg font-black text-primary leading-tight">65 Qs</span>
                <span className="text-[10px] uppercase font-bold text-slate-400">Total Count</span>
              </div>
              <div className="h-7 w-px bg-slate-200"></div>
              <div className="text-center">
                <span className="block text-lg font-black text-emerald-600 leading-tight">100 M</span>
                <span className="text-[10px] uppercase font-bold text-slate-400">Total Marks</span>
              </div>
            </div>
          </div>

          {loadingYear ? (
            <div className="bg-white rounded-2xl p-16 text-center shadow-sm border border-slate-200">
              <Loader2 className="w-8 h-8 animate-spin text-primary mx-auto mb-3" />
              <p className="text-slate-500 font-medium">Loading GATE {selectedYear} paper analysis...</p>
            </div>
          ) : yearData ? (
            <>
              {/* Year Summary KPI Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                  <span className="text-xs font-bold text-slate-400 uppercase">Questions</span>
                  <div className="text-2xl font-black text-slate-900 mt-1">{yearData.total_questions}</div>
                  <span className="text-xs text-slate-500">In GATE {yearData.year} Paper</span>
                </div>
                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                  <span className="text-xs font-bold text-slate-400 uppercase">Total Marks</span>
                  <div className="text-2xl font-black text-primary mt-1">{yearData.total_marks} Marks</div>
                  <span className="text-xs text-slate-500">{yearData.one_mark_count} (1M) + {yearData.two_mark_count} (2M)</span>
                </div>
                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                  <span className="text-xs font-bold text-slate-400 uppercase">Question Format</span>
                  <div className="flex items-center space-x-2 mt-2">
                    <span className="px-2 py-0.5 rounded bg-blue-100 text-blue-800 text-xs font-bold">{yearData.question_types.MCQ || 0} MCQ</span>
                    <span className="px-2 py-0.5 rounded bg-purple-100 text-purple-800 text-xs font-bold">{yearData.question_types.MSQ || 0} MSQ</span>
                    <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-xs font-bold">{yearData.question_types.NAT || 0} NAT</span>
                  </div>
                  <span className="text-xs text-slate-500 mt-1 block">Authentic CBT breakdown</span>
                </div>
                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                  <span className="text-xs font-bold text-slate-400 uppercase">Difficulty</span>
                  <div className="flex items-center space-x-2 mt-2">
                    <span className="px-2 py-0.5 rounded bg-green-50 text-green-700 text-xs font-semibold">{yearData.difficulty_breakdown.easy || 0} Easy</span>
                    <span className="px-2 py-0.5 rounded bg-amber-50 text-amber-700 text-xs font-semibold">{yearData.difficulty_breakdown.medium || 0} Med</span>
                    <span className="px-2 py-0.5 rounded bg-red-50 text-red-700 text-xs font-semibold">{yearData.difficulty_breakdown.hard || 0} Hard</span>
                  </div>
                  <span className="text-xs text-slate-500 mt-1 block">Balanced cognitive levels</span>
                </div>
              </div>

              {/* Subject Marks Chart */}
              <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div className="flex justify-between items-center mb-4 sm:mb-6">
                  <div>
                    <h3 className="text-base sm:text-lg font-extrabold text-slate-900">Subject Marks Breakdown (GATE {yearData.year})</h3>
                    <p className="text-xs text-slate-500">Total marks contributed by each of the 11 GATE CS subjects in this paper</p>
                  </div>
                </div>

                <div className="h-60 sm:h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} margin={{ top: 10, right: 10, left: -25, bottom: 30 }}>
                      <XAxis 
                        dataKey="name" 
                        tick={{ fontSize: 9, fontWeight: 600 }} 
                        interval={0} 
                        angle={-35} 
                        textAnchor="end"
                        height={40}
                      />
                      <YAxis tick={{ fontSize: 10 }} />
                      <Tooltip 
                        formatter={(val, name, item) => [`${val} Marks (${item.payload.questions} Qs)`, item.payload.fullName]}
                      />
                      <Bar dataKey="marks" radius={[4, 4, 0, 0]}>
                        {chartData.map((entry, idx) => (
                          <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Detailed Topic Breakdown Table */}
              <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                <div className="p-4 sm:p-6 border-b border-slate-100 flex justify-between items-center">
                  <div>
                    <h3 className="text-base sm:text-lg font-extrabold text-slate-900">Topic-Level Syllabus Breakdown</h3>
                    <p className="text-xs text-slate-500">Every topic that appeared in the GATE {yearData.year} paper with marks and practice shortcuts</p>
                  </div>
                </div>

                <div className="divide-y divide-slate-100">
                  {yearData.subjects.map(s => (
                    <div key={s.subject} className="p-6">
                      <div className="flex flex-wrap justify-between items-center mb-3">
                        <div className="flex items-center space-x-2">
                          <span className="font-extrabold text-base text-slate-900">{s.subject}</span>
                          <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                            {s.question_count} Qs • {s.total_marks} Marks
                          </span>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                        {s.topics.map(t => (
                          <div key={t.topic} className="bg-slate-50 border border-slate-200 rounded-xl p-3 flex justify-between items-center hover:bg-white hover:border-primary/40 transition-all">
                            <div>
                              <div className="font-bold text-sm text-slate-800">{t.topic}</div>
                              <div className="text-xs text-slate-500 mt-0.5">
                                {t.question_count} Question{t.question_count > 1 ? 's' : ''} ({t.marks} Marks)
                              </div>
                            </div>
                            <button
                              onClick={() => handlePracticeTopic(s.subject, t.topic)}
                              className="px-2.5 py-1 rounded-lg text-xs font-bold text-primary hover:bg-primary/10 transition-colors flex items-center"
                            >
                              <span>Practice</span>
                              <ArrowRight className="w-3 h-3 ml-1" />
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </>
          ) : null}

        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 2: 35-YEAR TOPIC TRENDS */}
      {/* ========================================================================= */}
      {activeTab === 'trends' && (
        <div className="space-y-6">

          {/* Subject Filter Toolbar */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <Filter className="w-4 h-4 text-primary" />
              <span className="text-sm font-bold text-slate-700">Filter By Subject:</span>
              <select
                value={selectedSubject}
                onChange={(e) => setSelectedSubject(e.target.value)}
                className="px-4 py-2 border-2 border-slate-200 rounded-xl text-sm font-bold text-slate-800 bg-white focus:ring-2 focus:ring-primary focus:border-primary outline-none cursor-pointer"
              >
                <option value="ALL">🌟 All 11 Subjects Combined</option>
                {SUBJECTS.map(s => (
                  <option key={s.name} value={s.name}>
                    {s.displayName} ({s.name})
                  </option>
                ))}
              </select>
            </div>

            <span className="text-xs text-slate-500 font-semibold bg-slate-100 px-3 py-1.5 rounded-full">
              Showing top high-yield topics ranked by 35-year weightage
            </span>
          </div>

          {loadingTrends ? (
            <div className="bg-white rounded-2xl p-16 text-center shadow-sm border border-slate-200">
              <Loader2 className="w-8 h-8 animate-spin text-primary mx-auto mb-3" />
              <p className="text-slate-500 font-medium">Aggregating 35 years of topic appearances...</p>
            </div>
          ) : trendsData.length > 0 ? (
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
              <div className="p-6 border-b border-slate-100">
                <h3 className="text-lg font-bold text-slate-900">
                  Most Frequently Asked Topics (Ranked by 35-Year Weightage)
                </h3>
                <p className="text-xs text-slate-500 mt-1">
                  Topics with high appearance frequency are must-prepare core topics for GATE 2027.
                </p>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-slate-600">
                  <thead className="bg-slate-50 text-xs font-bold uppercase text-slate-400 border-b border-slate-100">
                    <tr>
                      <th className="px-6 py-4">Rank</th>
                      <th className="px-6 py-4">Topic Name</th>
                      <th className="px-6 py-4">Subject</th>
                      <th className="px-6 py-4">Total Marks (35Y)</th>
                      <th className="px-6 py-4">Questions</th>
                      <th className="px-6 py-4">Appearance Freq</th>
                      <th className="px-6 py-4 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {trendsData.map((t, idx) => (
                      <tr key={t.topic} className="hover:bg-slate-50 transition-colors">
                        <td className="px-6 py-4 font-bold text-slate-900">
                          <span className={`inline-flex items-center justify-center w-7 h-7 rounded-full text-xs font-extrabold ${
                            idx === 0 ? 'bg-amber-100 text-amber-800' :
                            idx === 1 ? 'bg-slate-200 text-slate-800' :
                            idx === 2 ? 'bg-orange-100 text-orange-800' :
                            'bg-slate-100 text-slate-600'
                          }`}>
                            #{idx + 1}
                          </span>
                        </td>
                        <td className="px-6 py-4 font-bold text-slate-900">
                          {t.topic}
                        </td>
                        <td className="px-6 py-4">
                          <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-primary/10 text-primary">
                            {t.subject}
                          </span>
                        </td>
                        <td className="px-6 py-4 font-black text-slate-900">
                          {t.total_marks} Marks
                        </td>
                        <td className="px-6 py-4 font-medium text-slate-700">
                          {t.question_count} Qs
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-2">
                            <div className="w-16 bg-slate-200 rounded-full h-2 overflow-hidden">
                              <div
                                className="bg-primary h-2 rounded-full"
                                style={{ width: `${Math.min(100, t.appearance_frequency_pct)}%` }}
                              />
                            </div>
                            <span className="text-xs font-bold text-slate-700">
                              {t.appearance_frequency_pct}%
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <button
                            onClick={() => handlePracticeTopic(t.subject, t.topic)}
                            className="inline-flex items-center space-x-1 bg-primary hover:bg-primary-light text-white px-3 py-1.5 rounded-lg text-xs font-bold shadow-sm transition-all"
                          >
                            <Play className="w-3 h-3 fill-current" />
                            <span>Practice</span>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-2xl p-12 text-center shadow-sm border border-slate-200">
              <p className="text-slate-500">No trend data available for this selection.</p>
            </div>
          )}

        </div>
      )}

    </div>
  );
};

export default PaperAnalysis;
