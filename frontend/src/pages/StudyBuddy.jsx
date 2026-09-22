import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';
import { parseLaTeX, formatDate } from '../utils/helpers';
import { 
  Users, User, Trophy, Target, Clock, TrendingUp, 
  CheckCircle2, XCircle, ArrowRight, Eye, X, BookOpen, 
  Flame, Award, Sparkles, RefreshCw, Loader2, Trash2 
} from 'lucide-react';
import { 
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, 
  Tooltip, Legend, CartesianGrid 
} from 'recharts';
import toast from 'react-hot-toast';

const StudyBuddy = () => {
  const [loading, setLoading] = useState(true);
  const [peersList, setPeersList] = useState([]);
  const [selectedBuddyId, setSelectedBuddyId] = useState(null);
  const [comparisonData, setComparisonData] = useState(null);
  const [activityFeed, setActivityFeed] = useState([]);
  
  // Inspect attempt modal state
  const [inspectModalOpen, setInspectModalOpen] = useState(false);
  const [inspectLoading, setInspectLoading] = useState(false);
  const [inspectedAttempt, setInspectedAttempt] = useState(null);
  const [attemptFilter, setAttemptFilter] = useState('all');

  // Load initial peers & activity
  const fetchData = async (keepSelection = false) => {
    try {
      const [peersRes, feedRes] = await Promise.all([
        client.get('/peers/list').catch(() => ({ data: [] })),
        client.get('/peers/feed').catch(() => ({ data: [] }))
      ]);

      const peers = peersRes.data || [];
      setPeersList(peers);
      setActivityFeed(feedRes.data || []);

      if (!keepSelection) {
        // Pick default buddy (first peer that is not self)
        const otherPeer = peers.find(p => !p.is_self);
        setSelectedBuddyId(otherPeer ? otherPeer.id : null);
      }
    } catch (err) {
      console.error('Failed to load study buddy data', err);
      toast.error('Could not load peer data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDeletePeer = async (peerId) => {
    const peer = peersList.find(p => p.id === peerId);
    if (!window.confirm(`Are you sure you want to permanently delete test account "${peer?.name || 'User'}" and all their test data?`)) {
      return;
    }
    try {
      await client.delete(`/peers/user/${peerId}`);
      toast.success(`Removed test account: ${peer?.name}`);
      setSelectedBuddyId(null);
      await fetchData(false);
    } catch (err) {
      console.error('Failed to delete peer', err);
      toast.error(err.response?.data?.detail || 'Failed to remove user');
    }
  };

  // Fetch comparison whenever selectedBuddyId changes
  useEffect(() => {
    const fetchComparison = async () => {
      try {
        const url = selectedBuddyId ? `/peers/compare?buddy_id=${selectedBuddyId}` : '/peers/compare';
        const res = await client.get(url);
        setComparisonData(res.data);
      } catch (err) {
        console.error('Failed to load peer comparison', err);
      }
    };
    if (selectedBuddyId !== undefined) {
      fetchComparison();
    }
  }, [selectedBuddyId]);

  // Open inspection modal for a quiz attempt
  const handleInspectAttempt = async (sessionId) => {
    setInspectModalOpen(true);
    setInspectLoading(true);
    setAttemptFilter('all');
    try {
      const res = await client.get(`/peers/attempt/${sessionId}`);
      setInspectedAttempt(res.data);
    } catch (err) {
      console.error('Failed to inspect attempt', err);
      toast.error('Could not load quiz details');
      setInspectModalOpen(false);
    } finally {
      setInspectLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="pt-24 min-h-screen flex flex-col items-center justify-center bg-slate-50">
        <Loader2 className="w-10 h-10 animate-spin text-primary mb-3" />
        <p className="text-slate-600 font-bold text-sm">Connecting to Study Buddy Hub...</p>
      </div>
    );
  }

  const userObj = comparisonData?.user;
  const buddyObj = comparisonData?.buddy;
  const uStats = userObj?.stats || {};
  const bStats = buddyObj?.stats || {};

  // Format chart data for Recharts
  const chartData = (comparisonData?.subject_comparison || []).map(item => ({
    name: item.subject.length > 14 ? item.subject.slice(0, 12) + '..' : item.subject,
    fullName: item.subject,
    You: item.user_accuracy,
    [buddyObj?.name || 'Buddy']: item.buddy_accuracy,
  }));

  return (
    <div className="pt-24 pb-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-primary via-primary-light to-indigo-900 rounded-3xl p-6 sm:p-8 text-white shadow-lg mb-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-6 opacity-10 pointer-events-none">
          <Users className="w-64 h-64 text-white transform translate-x-12 -translate-y-12" />
        </div>

        <div className="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div>
            <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-md px-3 py-1 rounded-full text-xs font-bold text-amber-300 border border-white/20 mb-3">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Collaborative GATE Learning</span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-black tracking-tight">
              Study Buddy & Peer Hub
            </h1>
            <p className="text-primary-100 text-xs sm:text-sm mt-1.5 max-w-2xl leading-relaxed">
              Track mutual progress, compare subject strengths side-by-side, and inspect each other's attempted test papers to learn together.
            </p>
          </div>

          {/* Buddy Selector Dropdown */}
          <div className="bg-white/10 backdrop-blur-md p-3 sm:p-4 rounded-2xl border border-white/20 flex flex-col sm:flex-row items-start sm:items-center gap-3">
            <div className="text-xs font-bold text-primary-100 flex items-center gap-1.5">
              <User className="w-4 h-4 text-emerald-400" />
              <span>Comparing with:</span>
            </div>
            <div className="flex items-center gap-2">
              <select
                value={selectedBuddyId || ''}
                onChange={(e) => setSelectedBuddyId(Number(e.target.value) || null)}
                className="bg-white text-slate-900 font-extrabold text-xs sm:text-sm px-3.5 py-2 rounded-xl border-2 border-white/40 focus:ring-2 focus:ring-primary outline-none cursor-pointer shadow-sm"
              >
                {peersList.filter(p => !p.is_self).map(p => (
                  <option key={p.id} value={p.id}>
                    {p.name} ({p.total_quizzes} Quizzes • {p.accuracy_rate}% Acc)
                  </option>
                ))}
                {peersList.filter(p => !p.is_self).length === 0 && (
                  <option value="">No other peer registered yet</option>
                )}
              </select>
              {selectedBuddyId && (
                <button
                  onClick={() => handleDeletePeer(selectedBuddyId)}
                  title="Delete this test account"
                  className="px-2.5 py-2 rounded-xl bg-red-500/20 hover:bg-red-600 text-red-200 hover:text-white transition-all border border-red-400/30 text-xs font-bold flex items-center gap-1 cursor-pointer"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">Remove</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Head-to-Head Comparison Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 sm:gap-6 mb-8">
        
        {/* KPI 1: Quizzes Attempted */}
        <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200">
          <div className="flex items-center justify-between text-xs font-bold uppercase text-slate-400 mb-3">
            <span>Quizzes Attempted</span>
            <Trophy className="w-4 h-4 text-amber-500" />
          </div>
          <div className="flex justify-between items-baseline">
            <div>
              <span className="text-2xl font-black text-primary">{uStats.total_quizzes || 0}</span>
              <span className="text-[11px] block font-bold text-slate-400">You</span>
            </div>
            <div className="text-right">
              <span className="text-2xl font-black text-purple-600">{bStats.total_quizzes || 0}</span>
              <span className="text-[11px] block font-bold text-slate-400 truncate max-w-[100px]">
                {buddyObj?.name?.split(' ')[0] || 'Buddy'}
              </span>
            </div>
          </div>
          <div className="mt-3 w-full bg-slate-100 rounded-full h-2 overflow-hidden flex">
            <div 
              className="bg-primary h-full transition-all" 
              style={{ width: `${(uStats.total_quizzes / ((uStats.total_quizzes + bStats.total_quizzes) || 1)) * 100}%` }} 
            />
            <div 
              className="bg-purple-500 h-full transition-all" 
              style={{ width: `${(bStats.total_quizzes / ((uStats.total_quizzes + bStats.total_quizzes) || 1)) * 100}%` }} 
            />
          </div>
        </div>

        {/* KPI 2: Overall Accuracy */}
        <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200">
          <div className="flex items-center justify-between text-xs font-bold uppercase text-slate-400 mb-3">
            <span>Overall Accuracy</span>
            <Target className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="flex justify-between items-baseline">
            <div>
              <span className="text-2xl font-black text-primary">{uStats.accuracy_rate || 0}%</span>
              <span className="text-[11px] block font-bold text-slate-400">You</span>
            </div>
            <div className="text-right">
              <span className="text-2xl font-black text-purple-600">{bStats.accuracy_rate || 0}%</span>
              <span className="text-[11px] block font-bold text-slate-400 truncate max-w-[100px]">
                {buddyObj?.name?.split(' ')[0] || 'Buddy'}
              </span>
            </div>
          </div>
          <div className="mt-3 w-full bg-slate-100 rounded-full h-2 overflow-hidden flex">
            <div 
              className="bg-primary h-full transition-all" 
              style={{ width: `${(uStats.accuracy_rate / ((uStats.accuracy_rate + bStats.accuracy_rate) || 1)) * 100}%` }} 
            />
            <div 
              className="bg-purple-500 h-full transition-all" 
              style={{ width: `${(bStats.accuracy_rate / ((uStats.accuracy_rate + bStats.accuracy_rate) || 1)) * 100}%` }} 
            />
          </div>
        </div>

        {/* KPI 3: Average Marks */}
        <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200">
          <div className="flex items-center justify-between text-xs font-bold uppercase text-slate-400 mb-3">
            <span>Average Score</span>
            <TrendingUp className="w-4 h-4 text-blue-500" />
          </div>
          <div className="flex justify-between items-baseline">
            <div>
              <span className="text-2xl font-black text-primary">{uStats.avg_score || 0}%</span>
              <span className="text-[11px] block font-bold text-slate-400">You</span>
            </div>
            <div className="text-right">
              <span className="text-2xl font-black text-purple-600">{bStats.avg_score || 0}%</span>
              <span className="text-[11px] block font-bold text-slate-400 truncate max-w-[100px]">
                {buddyObj?.name?.split(' ')[0] || 'Buddy'}
              </span>
            </div>
          </div>
          <div className="mt-3 w-full bg-slate-100 rounded-full h-2 overflow-hidden flex">
            <div 
              className="bg-primary h-full transition-all" 
              style={{ width: `${(uStats.avg_score / ((uStats.avg_score + bStats.avg_score) || 1)) * 100}%` }} 
            />
            <div 
              className="bg-purple-500 h-full transition-all" 
              style={{ width: `${(bStats.avg_score / ((uStats.avg_score + bStats.avg_score) || 1)) * 100}%` }} 
            />
          </div>
        </div>

        {/* KPI 4: Best Test Score */}
        <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200">
          <div className="flex items-center justify-between text-xs font-bold uppercase text-slate-400 mb-3">
            <span>Best Test Score</span>
            <Flame className="w-4 h-4 text-red-500" />
          </div>
          <div className="flex justify-between items-baseline">
            <div>
              <span className="text-2xl font-black text-primary">{uStats.best_score || 0}M</span>
              <span className="text-[11px] block font-bold text-slate-400">You</span>
            </div>
            <div className="text-right">
              <span className="text-2xl font-black text-purple-600">{bStats.best_score || 0}M</span>
              <span className="text-[11px] block font-bold text-slate-400 truncate max-w-[100px]">
                {buddyObj?.name?.split(' ')[0] || 'Buddy'}
              </span>
            </div>
          </div>
          <div className="mt-3 w-full bg-slate-100 rounded-full h-2 overflow-hidden flex">
            <div 
              className="bg-primary h-full transition-all" 
              style={{ width: `${(uStats.best_score / ((uStats.best_score + bStats.best_score) || 1)) * 100}%` }} 
            />
            <div 
              className="bg-purple-500 h-full transition-all" 
              style={{ width: `${(bStats.best_score / ((uStats.best_score + bStats.best_score) || 1)) * 100}%` }} 
            />
          </div>
        </div>

      </div>

      {/* Main Grid: Subject Comparison Chart (Left) + Shared Activity Feed (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left 7 Columns: Head-to-Head Subject Comparison Chart */}
        <div className="lg:col-span-7 bg-white rounded-2xl p-6 shadow-sm border border-slate-200 flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center mb-4">
              <div>
                <h2 className="text-lg font-black text-slate-900">Head-to-Head Subject Accuracy</h2>
                <p className="text-xs text-slate-500">Comparing your subject accuracy vs {buddyObj?.name || 'Buddy'}</p>
              </div>
              <div className="flex items-center space-x-3 text-xs font-bold">
                <span className="flex items-center gap-1.5 text-primary">
                  <span className="w-3 h-3 rounded bg-primary inline-block" /> You
                </span>
                <span className="flex items-center gap-1.5 text-purple-600">
                  <span className="w-3 h-3 rounded bg-purple-500 inline-block" /> {buddyObj?.name?.split(' ')[0] || 'Buddy'}
                </span>
              </div>
            </div>

            <div className="h-80 w-full pt-2">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 10, left: -15, bottom: 45 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis 
                    dataKey="name" 
                    angle={-30} 
                    textAnchor="end" 
                    interval={0} 
                    tick={{ fontSize: 10, fill: '#64748b', fontWeight: 600 }} 
                  />
                  <YAxis unit="%" tick={{ fontSize: 11, fill: '#94a3b8' }} domain={[0, 100]} />
                  <Tooltip 
                    formatter={(val, name) => [`${val}% Accuracy`, name]}
                    labelFormatter={(lbl, items) => items?.[0]?.payload?.fullName || lbl}
                    contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Bar dataKey="You" fill="#1e3a5f" radius={[4, 4, 0, 0]} />
                  <Bar dataKey={buddyObj?.name || 'Buddy'} fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>💡 High accuracy in a subject signifies solid concept mastery.</span>
            <Link to="/subjects" className="text-primary font-bold hover:underline flex items-center">
              Practice weak subjects <ArrowRight className="w-3.5 h-3.5 ml-1" />
            </Link>
          </div>
        </div>

        {/* Right 5 Columns: Shared Practice Activity Feed */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-6 shadow-sm border border-slate-200 flex flex-col h-full">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-black text-slate-900">Shared Activity Stream</h2>
              <p className="text-xs text-slate-500">Live feed of test submissions</p>
            </div>
            <span className="text-xs bg-slate-100 text-slate-600 font-bold px-2.5 py-1 rounded-full">
              {activityFeed.length} Attempts
            </span>
          </div>

          <div className="flex-grow overflow-y-auto space-y-3 max-h-[460px] pr-1 scrollbar-thin">
            {activityFeed.map((item) => (
              <div 
                key={item.session_id}
                className="p-3.5 rounded-xl border border-slate-200/80 hover:border-primary/40 bg-slate-50/50 hover:bg-white transition-all shadow-2xs"
              >
                <div className="flex justify-between items-start mb-1.5">
                  <div className="flex items-center space-x-2">
                    <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-black text-white ${
                      item.is_self ? 'bg-primary' : 'bg-purple-600'
                    }`}>
                      {item.user_name.charAt(0).toUpperCase()}
                    </div>
                    <span className="font-extrabold text-xs text-slate-800">
                      {item.is_self ? 'You' : item.user_name}
                    </span>
                  </div>
                  <span className="text-[11px] font-medium text-slate-400">
                    {formatDate(item.completed_at)}
                  </span>
                </div>

                <div className="flex justify-between items-center my-2">
                  <span className="text-xs font-bold text-slate-700 truncate max-w-[180px]">
                    {item.quiz_title}
                  </span>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-black ${
                      item.percentage >= 60 ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                    }`}>
                      {item.score} / {item.max_score}M ({item.percentage}%)
                    </span>
                  </div>
                </div>

                <div className="flex justify-between items-center pt-2 border-t border-slate-100 text-[11px] text-slate-500">
                  <span>{item.correct_count} Correct • {item.wrong_count} Wrong</span>
                  <button
                    onClick={() => handleInspectAttempt(item.session_id)}
                    className="flex items-center space-x-1 text-primary hover:text-primary-light font-extrabold hover:underline"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    <span>Review Test Paper</span>
                  </button>
                </div>
              </div>
            ))}

            {activityFeed.length === 0 && (
              <div className="text-center py-12 text-slate-400">
                <BookOpen className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-xs font-bold">No test attempts logged yet.</p>
                <p className="text-[11px] mt-0.5">Take a quiz to start building your shared study history!</p>
              </div>
            )}
          </div>
        </div>

      </div>

      {/* ========================================================================= */}
      {/* ATTEMPT INSPECTION MODAL */}
      {/* ========================================================================= */}
      {inspectModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6">
          <div 
            className="absolute inset-0 bg-black/60 backdrop-blur-xs transition-opacity" 
            onClick={() => setInspectModalOpen(false)} 
          />
          <div className="relative bg-white rounded-3xl shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden border border-slate-100 animate-in zoom-in-95 duration-150">
            
            {/* Modal Header */}
            <div className="bg-slate-50 border-b border-slate-200 px-6 py-4 flex justify-between items-center shrink-0">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-black uppercase text-primary bg-primary/10 px-2.5 py-0.5 rounded-md">
                    Peer Attempt Review
                  </span>
                  <span className="text-xs font-bold text-slate-500">
                    Candidate: <strong>{inspectedAttempt?.user_name}</strong>
                  </span>
                </div>
                <h3 className="text-base sm:text-lg font-black text-slate-900 mt-0.5">
                  Detailed Solution & Answer Key
                </h3>
              </div>
              <button 
                onClick={() => setInspectModalOpen(false)}
                className="p-2 rounded-full hover:bg-slate-200 text-slate-500 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto flex-grow space-y-6">
              {inspectLoading ? (
                <div className="py-16 text-center">
                  <Loader2 className="w-8 h-8 animate-spin text-primary mx-auto mb-2" />
                  <p className="text-xs font-bold text-slate-500">Loading attempt details...</p>
                </div>
              ) : (
                <>
                  {/* Summary Bar */}
                  <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 bg-slate-50 p-4 rounded-2xl border border-slate-200 text-center">
                    <div>
                      <span className="block text-xl font-black text-primary">{inspectedAttempt?.score}M</span>
                      <span className="text-[10px] uppercase font-bold text-slate-400">Score</span>
                    </div>
                    <div>
                      <span className="block text-xl font-black text-emerald-600">{inspectedAttempt?.correct_count}</span>
                      <span className="text-[10px] uppercase font-bold text-slate-400">Correct</span>
                    </div>
                    <div>
                      <span className="block text-xl font-black text-red-500">{inspectedAttempt?.wrong_count}</span>
                      <span className="text-[10px] uppercase font-bold text-slate-400">Wrong</span>
                    </div>
                    <div>
                      <span className="block text-xl font-black text-amber-600">{inspectedAttempt?.unanswered_count}</span>
                      <span className="text-[10px] uppercase font-bold text-slate-400">Skipped</span>
                    </div>
                    <div className="col-span-2 sm:col-span-1">
                      <span className="block text-xl font-black text-slate-700">{inspectedAttempt?.percentage}%</span>
                      <span className="text-[10px] uppercase font-bold text-slate-400">Percentage</span>
                    </div>
                  </div>

                  {/* Filter Chips */}
                  {(() => {
                    const qList = inspectedAttempt?.questions || [];
                    const attemptedCount = qList.filter(q => q.is_attempted).length;
                    const correctCount = qList.filter(q => q.status === 'correct').length;
                    const wrongCount = qList.filter(q => q.status === 'wrong').length;
                    const skippedCount = qList.filter(q => !q.is_attempted).length;

                    return (
                      <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-100">
                        <span className="text-xs font-bold text-slate-400 mr-1">Filter questions:</span>
                        <button
                          onClick={() => setAttemptFilter('all')}
                          className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                            attemptFilter === 'all'
                              ? 'bg-slate-900 text-white shadow-xs'
                              : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                          }`}
                        >
                          All ({qList.length})
                        </button>
                        <button
                          onClick={() => setAttemptFilter('attempted')}
                          className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                            attemptFilter === 'attempted'
                              ? 'bg-primary text-white shadow-xs'
                              : 'bg-primary/10 text-primary hover:bg-primary/20'
                          }`}
                        >
                          Buddy Attempted ({attemptedCount})
                        </button>
                        <button
                          onClick={() => setAttemptFilter('correct')}
                          className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                            attemptFilter === 'correct'
                              ? 'bg-emerald-600 text-white shadow-xs'
                              : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
                          }`}
                        >
                          Correct ({correctCount})
                        </button>
                        <button
                          onClick={() => setAttemptFilter('wrong')}
                          className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                            attemptFilter === 'wrong'
                              ? 'bg-red-600 text-white shadow-xs'
                              : 'bg-red-50 text-red-700 hover:bg-red-100'
                          }`}
                        >
                          Wrong ({wrongCount})
                        </button>
                        <button
                          onClick={() => setAttemptFilter('skipped')}
                          className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                            attemptFilter === 'skipped'
                              ? 'bg-amber-600 text-white shadow-xs'
                              : 'bg-amber-50 text-amber-700 hover:bg-amber-100'
                          }`}
                        >
                          Skipped ({skippedCount})
                        </button>
                      </div>
                    );
                  })()}

                  {/* Question-by-Question breakdown */}
                  <div className="space-y-5">
                    {(() => {
                      const qList = inspectedAttempt?.questions || [];
                      const filtered = qList.filter(q => {
                        if (attemptFilter === 'attempted') return q.is_attempted;
                        if (attemptFilter === 'correct') return q.status === 'correct';
                        if (attemptFilter === 'wrong') return q.status === 'wrong';
                        if (attemptFilter === 'skipped') return !q.is_attempted;
                        return true;
                      });

                      if (filtered.length === 0) {
                        return (
                          <div className="text-center py-10 bg-slate-50 rounded-2xl border border-slate-200">
                            <p className="text-xs font-bold text-slate-500">No questions found in this category.</p>
                          </div>
                        );
                      }

                      return filtered.map((q, idx) => {
                        const isCorrect = q.status === 'correct';
                        const isWrong = q.status === 'wrong';
                        const isAttempted = q.is_attempted;

                        return (
                          <div 
                            key={q.id}
                            className={`p-5 rounded-2xl border-2 transition-all ${
                              isCorrect 
                                ? 'border-emerald-300 bg-emerald-50/20' 
                                : isWrong 
                                ? 'border-red-300 bg-red-50/20' 
                                : 'border-slate-200 bg-slate-50/30'
                            }`}
                          >
                            <div className="flex flex-wrap justify-between items-center gap-2 mb-3">
                              <div className="flex items-center space-x-2">
                                <span className="font-black text-sm text-slate-900">Q.{idx + 1}</span>
                                <span className="text-xs px-2.5 py-0.5 rounded-md bg-slate-100 font-bold text-slate-700">
                                  {q.subject}
                                </span>
                                <span className="text-xs px-2 py-0.5 rounded-md bg-slate-200/70 font-black text-slate-600">
                                  {q.marks} Mark{q.marks > 1 ? 's' : ''}
                                </span>
                                <span className="text-[11px] px-2 py-0.5 rounded-md bg-primary/10 font-bold text-primary">
                                  {q.question_type}
                                </span>
                              </div>

                              <div>
                                {isCorrect ? (
                                  <span className="px-2.5 py-1 rounded-full text-xs font-black uppercase bg-emerald-100 text-emerald-800 border border-emerald-300 flex items-center gap-1">
                                    <CheckCircle2 className="w-3.5 h-3.5" />
                                    <span>Correct (+{q.marks_awarded}M)</span>
                                  </span>
                                ) : isWrong ? (
                                  <span className="px-2.5 py-1 rounded-full text-xs font-black uppercase bg-red-100 text-red-800 border border-red-300 flex items-center gap-1">
                                    <XCircle className="w-3.5 h-3.5" />
                                    <span>Wrong ({q.marks_awarded}M)</span>
                                  </span>
                                ) : (
                                  <span className="px-2.5 py-1 rounded-full text-xs font-bold uppercase bg-slate-200 text-slate-700">
                                    Not Attempted (0M)
                                  </span>
                                )}
                              </div>
                            </div>

                            {/* Question Text */}
                            <div className="text-sm font-medium text-slate-800 mb-4 whitespace-pre-line leading-relaxed">
                              {parseLaTeX(q.question_text)}
                            </div>

                            {/* MCQ Options with Buddy Choice Highlighted */}
                            {q.options && typeof q.options === 'object' && (
                              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 mb-4">
                                {Object.entries(q.options).map(([optKey, optVal]) => {
                                  const buddyAnswerNormalized = String(q.student_answer || '').trim().toUpperCase();
                                  const correctAnswerNormalized = String(q.correct_answer || '').trim().toUpperCase();
                                  const isBuddyChoice = buddyAnswerNormalized === optKey.toUpperCase();
                                  const isCorrectChoice = correctAnswerNormalized === optKey.toUpperCase();

                                  let cardStyle = "border-slate-200 bg-white text-slate-700";
                                  let tag = null;

                                  if (isBuddyChoice && isCorrectChoice) {
                                    cardStyle = "border-2 border-emerald-500 bg-emerald-50 text-emerald-950 shadow-xs";
                                    tag = (
                                      <span className="text-[11px] font-black text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-md">
                                        ✓ Buddy's Choice (Correct)
                                      </span>
                                    );
                                  } else if (isBuddyChoice && !isCorrectChoice) {
                                    cardStyle = "border-2 border-red-500 bg-red-50 text-red-950 shadow-xs";
                                    tag = (
                                      <span className="text-[11px] font-black text-red-700 bg-red-100 px-2 py-0.5 rounded-md">
                                        ✗ Buddy's Choice (Incorrect)
                                      </span>
                                    );
                                  } else if (isCorrectChoice) {
                                    cardStyle = "border-2 border-emerald-400 bg-emerald-50/60 text-emerald-900 border-dashed";
                                    tag = (
                                      <span className="text-[11px] font-black text-emerald-700 bg-emerald-100/80 px-2 py-0.5 rounded-md">
                                        ✓ Correct Option
                                      </span>
                                    );
                                  }

                                  return (
                                    <div 
                                      key={optKey} 
                                      className={`p-3 rounded-xl border flex flex-col justify-between text-xs transition-all ${cardStyle}`}
                                    >
                                      <div className="flex items-start space-x-2">
                                        <span className={`font-black px-2 py-0.5 rounded text-xs shrink-0 ${
                                          isBuddyChoice ? (isCorrectChoice ? 'bg-emerald-600 text-white' : 'bg-red-600 text-white') : isCorrectChoice ? 'bg-emerald-500 text-white' : 'bg-slate-100 text-slate-800'
                                        }`}>
                                          {optKey}
                                        </span>
                                        <span className="leading-snug pt-0.5">{parseLaTeX(optVal)}</span>
                                      </div>
                                      {tag && <div className="mt-2 text-right">{tag}</div>}
                                    </div>
                                  );
                                })}
                              </div>
                            )}

                            {/* NAT / Numeric comparison */}
                            {(!q.options || typeof q.options !== 'object') && (
                              <div className="p-3.5 rounded-xl bg-white border border-slate-200 mb-4 text-xs space-y-2">
                                <div className="flex justify-between items-center">
                                  <span className="text-slate-500 font-bold">Buddy's Entered Value:</span>
                                  <span className={`font-black ${
                                    isCorrect ? 'text-emerald-700' : isAttempted ? 'text-red-600' : 'text-slate-400'
                                  }`}>
                                    {isAttempted ? String(q.student_answer) : '(Skipped / Not Attempted)'}
                                  </span>
                                </div>
                                <div className="flex justify-between items-center border-t border-slate-100 pt-2">
                                  <span className="text-slate-500 font-bold">Official Correct Answer:</span>
                                  <span className="text-emerald-700 font-black">{q.correct_answer}</span>
                                </div>
                              </div>
                            )}

                            {/* Answers Comparison Summary Box */}
                            <div className="flex flex-wrap items-center justify-between text-xs p-3 bg-white/80 rounded-xl border border-slate-200 mb-3 gap-2">
                              <div className="flex items-center space-x-2">
                                <span className="text-slate-400 font-bold">Buddy Answer:</span>
                                <span className={`font-black ${isCorrect ? 'text-emerald-700' : isAttempted ? 'text-red-600' : 'text-slate-400'}`}>
                                  {isAttempted ? String(q.student_answer) : 'Not Answered'}
                                </span>
                              </div>
                              <div className="flex items-center space-x-2">
                                <span className="text-slate-400 font-bold">Correct Key:</span>
                                <span className="text-emerald-700 font-black">{q.correct_answer}</span>
                              </div>
                            </div>

                            {/* Step-by-Step Explanation */}
                            {q.explanation && (
                              <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 text-xs text-slate-700">
                                <span className="font-black text-slate-900 block mb-1">Detailed Explanation & Solution:</span>
                                <div className="leading-relaxed whitespace-pre-line">
                                  {parseLaTeX(q.explanation)}
                                </div>
                              </div>
                            )}
                          </div>
                        );
                      });
                    })()}
                  </div>
                </>
              )}
            </div>

            {/* Modal Footer */}
            <div className="bg-slate-50 border-t border-slate-200 px-6 py-3.5 flex justify-end">
              <button
                onClick={() => setInspectModalOpen(false)}
                className="px-5 py-2 rounded-xl bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold text-xs"
              >
                Close Review
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
};

export default StudyBuddy;
