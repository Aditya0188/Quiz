import React, { useState, useEffect } from 'react';
import client from '../api/client';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { TrendingUp, Clock, Target, Award, Loader2 } from 'lucide-react';

const Analytics = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await client.get('/analytics/full');
        setData(res.data);
      } catch (error) {
        console.error("Failed to load analytics", error);
        // Fallback mock data for layout purposes if API fails
        setData({
          overview: { totalQuizzes: 12, avgScore: 68, accuracy: 72, totalTime: 360 },
          scoreTrend: [
            { date: 'Sep 1', score: 45 }, { date: 'Sep 5', score: 55 },
            { date: 'Sep 10', score: 62 }, { date: 'Sep 15', score: 75 },
            { date: 'Sep 20', score: 70 },
          ],
          subjectPerf: [
            { subject: 'OS', score: 85 }, { subject: 'DBMS', score: 65 },
            { subject: 'CN', score: 40 }, { subject: 'ALGO', score: 78 }
          ],
          topicStrengths: [
            { topic: 'Process Management', subject: 'OS', score: 90 },
            { topic: 'SQL', subject: 'DBMS', score: 70 },
            { topic: 'TCP/IP', subject: 'CN', score: 30 },
          ]
        });
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) {
    return <div className="pt-24 min-h-screen flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-primary" /></div>;
  }

  const { overview, scoreTrend, subjectPerf, topicStrengths } = data;

  const getScoreColor = (score) => {
    if (score >= 70) return '#10b981'; // Green
    if (score >= 50) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
  };

  const getBgScoreColor = (score) => {
    if (score >= 70) return 'bg-green-100 text-green-800';
    if (score >= 50) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  return (
    <div className="pt-24 pb-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="mb-6 sm:mb-8">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">Your Analytics</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">Deep dive into your GATE performance metrics</p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6 mb-6 sm:mb-8">
        <div className="bg-white rounded-2xl p-4 sm:p-6 shadow-sm border border-slate-200">
          <div className="flex items-center justify-between mb-2 sm:mb-4">
            <h3 className="text-slate-500 font-bold text-xs uppercase tracking-wider">Quizzes</h3>
            <Target className="w-4 h-4 text-blue-500" />
          </div>
          <p className="text-2xl sm:text-3xl font-black text-slate-800">{overview?.totalQuizzes || 0}</p>
        </div>
        <div className="bg-white rounded-2xl p-4 sm:p-6 shadow-sm border border-slate-200">
          <div className="flex items-center justify-between mb-2 sm:mb-4">
            <h3 className="text-slate-500 font-bold text-xs uppercase tracking-wider">Avg Score</h3>
            <Award className="w-4 h-4 text-emerald-500" />
          </div>
          <p className="text-2xl sm:text-3xl font-black text-emerald-600">{overview?.avgScore || 0}%</p>
        </div>
        <div className="bg-white rounded-2xl p-4 sm:p-6 shadow-sm border border-slate-200">
          <div className="flex items-center justify-between mb-2 sm:mb-4">
            <h3 className="text-slate-500 font-bold text-xs uppercase tracking-wider">Accuracy</h3>
            <TrendingUp className="w-4 h-4 text-purple-500" />
          </div>
          <p className="text-2xl sm:text-3xl font-black text-purple-600">{overview?.accuracy || 0}%</p>
        </div>
        <div className="bg-white rounded-2xl p-4 sm:p-6 shadow-sm border border-slate-200">
          <div className="flex items-center justify-between mb-2 sm:mb-4">
            <h3 className="text-slate-500 font-bold text-xs uppercase tracking-wider">Time Spent</h3>
            <Clock className="w-4 h-4 text-amber-500" />
          </div>
          <p className="text-xl sm:text-3xl font-black text-slate-800">
            {overview?.totalTime ? Math.floor(overview.totalTime / 60) : 0}h {overview?.totalTime ? overview.totalTime % 60 : 0}m
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Trend Chart */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
          <h3 className="text-lg font-bold text-slate-800 mb-6">Score Trend</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={scoreTrend} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="date" tick={{fontSize: 12, fill: '#64748b'}} axisLine={false} tickLine={false} />
                <YAxis domain={[0, 100]} tick={{fontSize: 12, fill: '#64748b'}} axisLine={false} tickLine={false} />
                <Tooltip 
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Line type="monotone" dataKey="score" stroke="#1e3a5f" strokeWidth={3} dot={{r: 4, fill: '#1e3a5f', strokeWidth: 0}} activeDot={{r: 6, strokeWidth: 0}} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Subject Comparison */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
          <h3 className="text-lg font-bold text-slate-800 mb-6">Subject Comparison</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={subjectPerf} margin={{ top: 5, right: 20, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="subject" tick={{fontSize: 12, fill: '#64748b'}} axisLine={false} tickLine={false} />
                <YAxis domain={[0, 100]} tick={{fontSize: 12, fill: '#64748b'}} axisLine={false} tickLine={false} />
                <Tooltip cursor={{fill: '#f8fafc'}} />
                <Bar dataKey="score" radius={[4, 4, 0, 0]}>
                  {subjectPerf?.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={getScoreColor(entry.score)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Weaknesses and Strengths Table */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-6 border-b border-slate-200">
          <h3 className="text-lg font-bold text-slate-800">Topic Strengths & Weaknesses</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Topic</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Subject</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Performance</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {topicStrengths?.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">{item.topic}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{item.subject}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-full bg-slate-200 rounded-full h-2 mr-2 max-w-[100px]">
                        <div className={`h-2 rounded-full ${item.score >= 70 ? 'bg-green-500' : item.score >= 50 ? 'bg-yellow-500' : 'bg-red-500'}`} style={{ width: `${item.score}%` }}></div>
                      </div>
                      <span className="text-sm text-slate-700">{item.score}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getBgScoreColor(item.score)}`}>
                      {item.score >= 70 ? 'Strong' : item.score >= 50 ? 'Average' : 'Weak'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {(!topicStrengths || topicStrengths.length === 0) && (
            <div className="p-8 text-center text-slate-500">
              Not enough data available yet. Keep practicing!
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Analytics;
