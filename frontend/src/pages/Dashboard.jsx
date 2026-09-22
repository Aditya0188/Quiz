import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import client from '../api/client';
import { Play, TrendingUp, Trophy, Target, Clock, AlertCircle, BookOpen, Loader2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { formatDate } from '../utils/helpers';

const Dashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [subjectPerformance, setSubjectPerformance] = useState([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [overviewRes, historyRes, subjectRes] = await Promise.all([
          client.get('/analytics/overview').catch(() => ({ data: { total_quizzes: 0, avg_score: 0, best_score: 0, total_questions_attempted: 0, accuracy_rate: 0 } })),
          client.get('/quiz/history').catch(() => ({ data: { history: [] } })),
          client.get('/analytics/subject-wise').catch(() => ({ data: [] }))
        ]);

        setStats(overviewRes.data);
        setHistory(historyRes.data.history || historyRes.data || []);

        // Transform subject-wise data for chart
        const chartData = (Array.isArray(subjectRes.data) ? subjectRes.data : []).map(s => ({
          subject: s.subject,
          accuracy: Math.round(s.accuracy || 0)
        }));
        setSubjectPerformance(chartData);
      } catch (error) {
        console.error("Failed to fetch dashboard data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="pt-24 min-h-screen flex flex-col items-center justify-center">
        <Loader2 className="w-10 h-10 animate-spin text-primary mb-4" />
        <p className="text-slate-500">Loading dashboard...</p>
      </div>
    );
  }

  const StatCard = ({ title, value, icon: Icon, color }) => (
    <div className="bg-white rounded-2xl p-3.5 sm:p-5 shadow-sm border border-slate-200/80 flex items-center hover:shadow-md transition-shadow">
      <div className={`p-2.5 sm:p-3.5 rounded-xl ${color} mr-3 sm:mr-4 shrink-0 shadow-xs`}>
        <Icon className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
      </div>
      <div className="min-w-0">
        <p className="text-[11px] sm:text-xs font-bold text-slate-500 uppercase tracking-wider truncate">{title}</p>
        <h3 className="text-xl sm:text-2xl font-black text-slate-900 truncate">{value}</h3>
      </div>
    </div>
  );

  const totalQuizzes = stats?.total_quizzes || 0;

  return (
    <div className="pt-24 pb-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 sm:mb-8 gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            Welcome{user?.name ? `, ${user.name.split(' ')[0]}` : ''}! 👋
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">Track your GATE CS preparation progress.</p>
        </div>
        <div className="flex gap-2.5 w-full sm:w-auto">
          <Link to="/subjects" className="flex-1 sm:flex-none justify-center bg-primary hover:bg-primary-light text-white px-4 sm:px-6 py-2.5 rounded-xl font-bold text-xs sm:text-sm shadow-xs transition-all flex items-center">
            <Play className="w-4 h-4 mr-1.5 fill-current" />
            Start Quiz
          </Link>
          <Link to="/analytics" className="flex-1 sm:flex-none justify-center bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 px-4 sm:px-6 py-2.5 rounded-xl font-bold text-xs sm:text-sm shadow-xs transition-colors flex items-center">
            <TrendingUp className="w-4 h-4 mr-1.5" />
            Analytics
          </Link>
        </div>
      </div>

      {totalQuizzes === 0 ? (
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 sm:p-12 text-center">
          <div className="w-16 h-16 sm:w-20 sm:h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4 sm:mb-6">
            <Target className="w-8 h-8 sm:w-10 sm:h-10 text-primary" />
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-slate-900 mb-2 sm:mb-3">Ready to start your GATE prep?</h2>
          <p className="text-xs sm:text-sm text-slate-500 mb-6 max-w-md mx-auto">
            Take your first quiz to begin tracking your progress. Choose a subject or mix multiple topics.
          </p>
          <Link to="/subjects" className="inline-flex items-center bg-primary hover:bg-primary-light text-white px-6 sm:px-8 py-2.5 sm:py-3 rounded-xl font-bold text-sm shadow-md transition-all">
            <Play className="w-4 h-4 sm:w-5 sm:h-5 mr-2 fill-current" />
            Take Your First Quiz
          </Link>
        </div>
      ) : (
        <>
          {/* Stats Grid */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6 mb-6 sm:mb-8">
            <StatCard title="Total Quizzes" value={totalQuizzes} icon={Target} color="bg-blue-500" />
            <StatCard
              title="Avg Score"
              value={`${Math.round(stats?.avg_score || 0)}%`}
              icon={TrendingUp}
              color="bg-emerald-500"
            />
            <StatCard
              title="Best Score"
              value={typeof stats?.best_score === 'number' ? stats.best_score.toFixed(1) : '0'}
              icon={Trophy}
              color="bg-amber-500"
            />
            <StatCard
              title="Accuracy"
              value={`${Math.round(stats?.accuracy_rate || 0)}%`}
              icon={BookOpen}
              color="bg-purple-500"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8">
            {/* Chart */}
            <div className="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-200 p-4 sm:p-6">
              <h3 className="text-base sm:text-lg font-bold text-slate-800 mb-4 sm:mb-6">Subject Performance</h3>
              {subjectPerformance.length > 0 ? (
                <div className="h-64 sm:h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={subjectPerformance} layout="vertical" margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
                      <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
                      <YAxis dataKey="subject" type="category" width={80} tick={{ fontSize: 11 }} />
                      <Tooltip formatter={(value) => [`${value}%`, 'Accuracy']} />
                      <Bar dataKey="accuracy" radius={[0, 6, 6, 0]} barSize={20}>
                        {subjectPerformance.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.accuracy >= 70 ? '#10b981' : entry.accuracy >= 40 ? '#f59e0b' : '#ef4444'} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="h-72 flex flex-col items-center justify-center text-slate-400">
                  <AlertCircle className="w-12 h-12 mb-3 opacity-30" />
                  <p className="text-sm">Complete some quizzes to see your performance chart</p>
                </div>
              )}
            </div>

            {/* History List */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 overflow-hidden flex flex-col h-[420px]">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-bold text-slate-800">Recent Quizzes</h3>
              </div>

              <div className="flex-grow overflow-y-auto pr-2 space-y-3">
                {history.length > 0 ? history.slice(0, 10).map((quiz) => {
                  const pct = quiz.max_score > 0 ? Math.round((quiz.score / quiz.max_score) * 100) : 0;
                  return (
                    <Link key={quiz.id} to={`/quiz/${quiz.id}/result`} className="block p-4 rounded-lg border border-slate-100 hover:border-primary/30 hover:bg-slate-50 transition-all">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-semibold text-slate-800 text-sm truncate pr-4">
                          {quiz.subjects?.join(', ') || 'Mixed'}
                        </h4>
                        <span className={`text-sm font-bold whitespace-nowrap ${pct >= 70 ? 'text-emerald-600' : pct >= 40 ? 'text-amber-600' : 'text-red-600'}`}>
                          {quiz.score?.toFixed(1)} / {quiz.max_score}
                        </span>
                      </div>
                      <div className="flex justify-between text-xs text-slate-500">
                        <span className="flex items-center">
                          <Clock className="w-3 h-3 mr-1" />
                          {quiz.started_at ? formatDate(quiz.started_at) : 'N/A'}
                        </span>
                        <span>{quiz.correct_count || 0}/{quiz.total_questions} correct</span>
                      </div>
                    </Link>
                  );
                }) : (
                  <p className="text-center text-slate-400 py-8 text-sm">No recent quizzes</p>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
