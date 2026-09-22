import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import client from '../api/client';
import { parseLaTeX } from '../utils/helpers';
import { CheckCircle, XCircle, MinusCircle, ArrowLeft, RefreshCw, Loader2 } from 'lucide-react';

const ResultPage = () => {
  const { sessionId } = useParams();
  const [session, setSession] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const res = await client.get(`/quiz/${sessionId}`);
        setSession(res.data.session);
        setQuestions(res.data.questions);
      } catch (err) {
        console.error("Failed to load results", err);
        setError("Failed to load quiz results.");
      } finally {
        setLoading(false);
      }
    };
    fetchResults();
  }, [sessionId]);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center">
        <Loader2 className="w-10 h-10 animate-spin text-primary mb-4" />
        <p className="text-slate-500">Loading results...</p>
      </div>
    );
  }

  if (error || !session) {
    return (
      <div className="pt-24 text-center">
        <p className="text-red-500 mb-4">{error || 'Failed to load result.'}</p>
        <Link to="/dashboard" className="text-primary font-medium hover:underline">Back to Dashboard</Link>
      </div>
    );
  }

  const { score, max_score, correct_count, wrong_count, unanswered_count } = session;
  const percentage = max_score > 0 ? Math.round((score / max_score) * 100) : 0;
  const accuracy = (correct_count + wrong_count) > 0
    ? Math.round((correct_count / (correct_count + wrong_count)) * 100)
    : 0;

  const getScoreColor = (pct) => {
    if (pct >= 70) return '#10b981'; // green
    if (pct >= 40) return '#f59e0b'; // amber
    return '#ef4444'; // red
  };

  const scoreColor = getScoreColor(percentage);

  return (
    <div className="pt-24 pb-16 max-w-5xl mx-auto px-4 sm:px-6">

      {/* Top Actions */}
      <div className="flex justify-between items-center mb-6 sm:mb-8 text-xs sm:text-sm font-bold">
        <Link to="/dashboard" className="flex items-center text-slate-500 hover:text-primary transition-colors">
          <ArrowLeft className="w-4 h-4 mr-1" /> Dashboard
        </Link>
        <Link to="/subjects" className="flex items-center text-primary hover:text-primary-light transition-colors">
          <RefreshCw className="w-4 h-4 mr-1" /> New Quiz
        </Link>
      </div>

      {/* Summary Card */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 sm:p-8 mb-6 sm:mb-8 text-center">
        <h1 className="text-2xl font-bold text-slate-800 mb-8">Quiz Results</h1>

        <div className="flex flex-col md:flex-row items-center justify-center gap-12">
          {/* Circular Score */}
          <div className="relative w-48 h-48">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="42" fill="none" stroke="#f1f5f9" strokeWidth="8" />
              <circle
                cx="50" cy="50" r="42" fill="none"
                stroke={scoreColor}
                strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray={`${(Math.max(0, percentage) * 264) / 100} 264`}
                className="transition-all duration-1000 ease-out"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-4xl font-extrabold" style={{ color: scoreColor }}>
                {typeof score === 'number' ? score.toFixed(1) : score}
              </span>
              <span className="text-sm text-slate-400 font-medium mt-1">
                / {max_score}
              </span>
              <span className="text-xs text-slate-400 mt-0.5">{percentage}%</span>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-4 text-left">
            <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-100">
              <div className="text-emerald-600 font-medium text-sm flex items-center">
                <CheckCircle className="w-4 h-4 mr-1.5" /> Correct
              </div>
              <div className="text-3xl font-bold text-emerald-700 mt-1">{correct_count}</div>
            </div>
            <div className="bg-red-50 rounded-xl p-4 border border-red-100">
              <div className="text-red-600 font-medium text-sm flex items-center">
                <XCircle className="w-4 h-4 mr-1.5" /> Wrong
              </div>
              <div className="text-3xl font-bold text-red-700 mt-1">{wrong_count}</div>
            </div>
            <div className="bg-slate-50 rounded-xl p-4 border border-slate-200">
              <div className="text-slate-600 font-medium text-sm flex items-center">
                <MinusCircle className="w-4 h-4 mr-1.5" /> Unanswered
              </div>
              <div className="text-3xl font-bold text-slate-700 mt-1">{unanswered_count}</div>
            </div>
            <div className="bg-blue-50 rounded-xl p-4 border border-blue-100">
              <div className="text-blue-600 font-medium text-sm">Accuracy</div>
              <div className="text-3xl font-bold text-blue-700 mt-1">{accuracy}%</div>
            </div>
          </div>
        </div>
      </div>

      {/* Question Review */}
      <h2 className="text-xl font-bold text-slate-800 mb-4">Detailed Review</h2>
      <div className="space-y-5">
        {questions.map((q, idx) => {
          const resp = q.user_response || {};
          const status = resp.status; // 'correct', 'wrong', 'unanswered'
          const userAns = resp.user_answer;
          const marksAwarded = resp.marks_awarded || 0;
          const optionEntries = q.options ? Object.entries(q.options) : [];

          const headerBg = status === 'correct' ? 'bg-emerald-50 border-emerald-200'
            : status === 'wrong' ? 'bg-red-50 border-red-200'
            : 'bg-slate-50 border-slate-200';

          return (
            <div key={q.id} className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
              {/* Q Header */}
              <div className={`px-6 py-3 border-b flex justify-between items-center ${headerBg}`}>
                <div className="flex items-center space-x-2.5 flex-wrap gap-y-1">
                  <span className="font-bold text-slate-700">Q{idx + 1}.</span>
                  {q.subject && (
                    <span className="px-2 py-0.5 text-xs font-bold rounded bg-primary/10 text-primary border border-primary/20">
                      {q.subject}
                    </span>
                  )}
                  {q.topic && (
                    <span className="px-2 py-0.5 text-xs font-medium rounded bg-white border border-slate-200 text-slate-700">
                      {q.topic}
                    </span>
                  )}
                  <span className="px-2 py-0.5 text-xs font-bold rounded bg-white border border-slate-200 text-slate-600">
                    {q.question_type}
                  </span>
                  <span className="px-2 py-0.5 text-xs font-bold rounded bg-white border border-slate-200 text-slate-600">
                    {q.marks}M
                  </span>
                  {q.year > 0 && (
                    <span className="text-xs text-slate-500 font-mono">GATE {q.year} {q.set_number ? `(${q.set_number})` : ''}</span>
                  )}
                </div>
                <div className="font-bold text-sm">
                  {status === 'correct' ? (
                    <span className="text-emerald-600 flex items-center"><CheckCircle className="w-4 h-4 mr-1" /> +{q.marks}</span>
                  ) : status === 'wrong' ? (
                    <span className="text-red-600 flex items-center"><XCircle className="w-4 h-4 mr-1" /> {marksAwarded.toFixed(2)}</span>
                  ) : (
                    <span className="text-slate-400">Not Attempted</span>
                  )}
                </div>
              </div>

              <div className="p-6">
                {/* Question Text */}
                <div className="text-slate-800 mb-6 leading-relaxed whitespace-pre-line">
                  {parseLaTeX(q.question_text)}
                </div>

                {/* Options Review for MCQ/MSQ */}
                {(q.question_type === 'MCQ' || q.question_type === 'MSQ') && optionEntries.length > 0 && (
                  <div className="space-y-2 mb-6">
                    {optionEntries.map(([key, text]) => {
                      const isUserAnswer = userAns ? (
                        q.question_type === 'MSQ'
                          ? userAns.split(',').includes(key)
                          : userAns === key
                      ) : false;
                      const isCorrect = q.correct_answer ? (
                        q.question_type === 'MSQ'
                          ? q.correct_answer.split(',').includes(key)
                          : q.correct_answer === key
                      ) : false;

                      let borderColor = 'border-slate-200 bg-white';
                      let icon = null;

                      if (isUserAnswer && isCorrect) {
                        borderColor = 'border-emerald-500 bg-emerald-50 ring-1 ring-emerald-300';
                        icon = <CheckCircle className="w-5 h-5 text-emerald-500 shrink-0" />;
                      } else if (isUserAnswer && !isCorrect) {
                        borderColor = 'border-red-500 bg-red-50 ring-1 ring-red-300';
                        icon = <XCircle className="w-5 h-5 text-red-500 shrink-0" />;
                      } else if (!isUserAnswer && isCorrect) {
                        borderColor = 'border-emerald-400 bg-emerald-50/50 border-dashed';
                        icon = <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0" />;
                      }

                      return (
                        <div key={key} className={`p-3 rounded-lg border-2 flex items-center gap-3 ${borderColor}`}>
                          <div className="w-7 h-7 rounded-full bg-slate-100 flex items-center justify-center text-sm font-bold text-slate-500 shrink-0">
                            {key}
                          </div>
                          <div className="flex-1 text-sm text-slate-700">{parseLaTeX(text)}</div>
                          {icon}
                        </div>
                      );
                    })}
                  </div>
                )}

                {/* NAT Review */}
                {q.question_type === 'NAT' && (
                  <div className="flex flex-wrap items-center gap-4 mb-6 bg-slate-50 p-4 rounded-lg">
                    <div>
                      <span className="text-xs font-medium text-slate-500 block mb-1">Your Answer</span>
                      <span className={`text-lg font-mono font-bold ${status === 'correct' ? 'text-emerald-600' : status === 'wrong' ? 'text-red-600' : 'text-slate-400'}`}>
                        {userAns || '—'}
                      </span>
                    </div>
                    {status !== 'correct' && q.correct_answer && (
                      <div>
                        <span className="text-xs font-medium text-slate-500 block mb-1">Correct Answer</span>
                        <span className="text-lg font-mono font-bold text-emerald-600">{q.correct_answer}</span>
                      </div>
                    )}
                  </div>
                )}

                {/* Explanation */}
                {q.explanation && (
                  <div className="bg-blue-50 border border-blue-100 rounded-lg p-5">
                    <h4 className="text-sm font-bold text-blue-800 mb-2">💡 Explanation</h4>
                    <div className="text-slate-700 text-sm leading-relaxed whitespace-pre-line">
                      {parseLaTeX(q.explanation)}
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Bottom Actions */}
      <div className="flex justify-center gap-4 mt-8">
        <Link
          to="/dashboard"
          className="px-6 py-3 rounded-lg font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 transition-colors"
        >
          Back to Dashboard
        </Link>
        <Link
          to="/subjects"
          className="px-6 py-3 rounded-lg font-bold text-white bg-primary hover:bg-primary-light transition-colors"
        >
          Take Another Quiz
        </Link>
      </div>
    </div>
  );
};

export default ResultPage;
