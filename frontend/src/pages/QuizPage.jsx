import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import client from '../api/client';
import QuizTimer from '../components/QuizTimer';
import QuestionCard from '../components/QuestionCard';
import QuestionPalette from '../components/QuestionPalette';
import { 
  ChevronLeft, ChevronRight, Send, Loader2 
} from 'lucide-react';
import toast from 'react-hot-toast';

const QuizPage = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [timeLimitMinutes, setTimeLimitMinutes] = useState(30);
  const [subjectName, setSubjectName] = useState('');

  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState({}); // {questionId: "A" | "A,C" | "42.5"}
  const [visited, setVisited] = useState(new Set());
  const [markedForReview, setMarkedForReview] = useState(new Set());
  const [showSubmitModal, setShowSubmitModal] = useState(false);

  useEffect(() => {
    const loadQuiz = async () => {
      try {
        const cached = sessionStorage.getItem(`quiz_${sessionId}`);
        if (cached) {
          const data = JSON.parse(cached);
          setQuestions(data.questions || []);
          setTimeLimitMinutes(data.time_limit_minutes || 30);
          setSubjectName(data.subject || 'GATE Quiz');
          sessionStorage.removeItem(`quiz_${sessionId}`);
        } else {
          const res = await client.get(`/quiz/${sessionId}`);
          if (res.data.session && res.data.session.completed_at) {
            navigate(`/quiz/${sessionId}/result`);
            return;
          }
          setQuestions(res.data.questions || []);
          setTimeLimitMinutes(res.data.session?.time_limit_minutes || 30);
          const cfg = res.data.session?.config || {};
          setSubjectName(cfg.subjects?.length ? cfg.subjects[0] : 'GATE Quiz');
        }
        setVisited(new Set([0]));
      } catch (error) {
        console.error("Failed to load quiz", error);
        toast.error("Failed to load quiz");
        navigate('/dashboard');
      } finally {
        setLoading(false);
      }
    };
    loadQuiz();
  }, [sessionId, navigate]);

  useEffect(() => {
    setVisited(prev => new Set([...prev, currentIdx]));
  }, [currentIdx]);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'ArrowRight') {
        setCurrentIdx(prev => Math.min(prev + 1, questions.length - 1));
      } else if (e.key === 'ArrowLeft') {
        setCurrentIdx(prev => Math.max(prev - 1, 0));
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [questions.length]);

  const handleAnswerSelect = (answer) => {
    if (!questions[currentIdx]) return;
    const qId = questions[currentIdx].id;
    setAnswers(prev => ({ ...prev, [qId]: answer }));
  };

  const handleClearResponse = () => {
    if (!questions[currentIdx]) return;
    const qId = questions[currentIdx].id;
    setAnswers(prev => {
      const newAnswers = { ...prev };
      delete newAnswers[qId];
      return newAnswers;
    });
  };

  const handleMarkToggle = () => {
    if (!questions[currentIdx]) return;
    const qId = questions[currentIdx].id;
    setMarkedForReview(prev => {
      const newSet = new Set(prev);
      if (newSet.has(qId)) newSet.delete(qId);
      else newSet.add(qId);
      return newSet;
    });
  };

  const handleSubmitClick = () => {
    setShowSubmitModal(true);
  };

  const handleTimeUp = useCallback(() => {
    toast.error("⏰ Time's up! Auto-submitting your quiz...", { duration: 3000 });
    submitQuiz();
  }, []);

  const submitQuiz = async () => {
    setSubmitting(true);
    setShowSubmitModal(false);
    try {
      const formattedResponses = {};
      for (const [qId, ans] of Object.entries(answers)) {
        let ansStr = ans;
        if (Array.isArray(ans)) {
          ansStr = ans.join(',');
        }
        formattedResponses[qId] = { 
          answer: ansStr, 
          time_spent: 0, 
          marked_for_review: markedForReview.has(parseInt(qId, 10)) 
        };
      }

      await client.post(`/quiz/${sessionId}/submit`, { responses: formattedResponses });
      toast.success('Quiz submitted successfully!');
      navigate(`/quiz/${sessionId}/result`);
    } catch (error) {
      console.error(error);
      toast.error('Failed to submit quiz. Please try again.');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-100 p-4">
        <Loader2 className="w-10 h-10 animate-spin text-primary mb-3" />
        <p className="text-slate-600 font-bold text-sm">Preparing your GATE examination paper...</p>
      </div>
    );
  }

  if (!questions.length) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-100 p-4">
        <p className="text-slate-600 font-bold mb-4">No questions found for this configuration.</p>
        <button 
          onClick={() => navigate('/dashboard')}
          className="px-4 py-2 bg-primary text-white rounded-xl font-bold text-sm"
        >
          Return to Dashboard
        </button>
      </div>
    );
  }

  const currentQ = questions[currentIdx];
  const answeredCount = Object.keys(answers).length;
  const unansweredCount = questions.length - answeredCount;
  const isCurrentMarked = currentQ ? markedForReview.has(currentQ.id) : false;

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col justify-between">
      
      {/* Quiz Top Header */}
      <header className="bg-white border-b border-slate-200 shadow-xs sticky top-0 z-30">
        <div className="max-w-[1600px] mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          
          {/* Left: Progress info */}
          <div className="flex items-center space-x-3">
            <div className="bg-primary/10 text-primary px-3 py-1 rounded-lg font-black text-sm">
              Question {currentIdx + 1} / {questions.length}
            </div>
            <span className="font-bold text-sm text-slate-700 truncate max-w-[250px]">
              {subjectName}
            </span>
          </div>

          {/* Center: Timer */}
          <div className="flex items-center">
            <QuizTimer
              totalSeconds={timeLimitMinutes * 60}
              onTimeUp={handleTimeUp}
            />
          </div>

          {/* Right: Submit Button */}
          <div className="flex items-center space-x-3">
            <button
              onClick={handleSubmitClick}
              disabled={submitting}
              className="flex items-center space-x-2 bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2 rounded-xl font-bold text-sm transition-all shadow-xs"
            >
              {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              <span>Submit Examination</span>
            </button>
          </div>

        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-grow flex max-w-[1600px] w-full mx-auto p-4 md:p-6 gap-6 overflow-hidden">
        
        {/* Left Side: Question Display */}
        <div className="flex-grow flex flex-col min-w-0 h-full">
          <div className="flex-grow overflow-y-auto">
            <QuestionCard
              question={currentQ}
              questionNumber={currentIdx + 1}
              totalQuestions={questions.length}
              selectedAnswer={currentQ ? answers[currentQ.id] : null}
              onAnswerSelect={handleAnswerSelect}
              isMarked={isCurrentMarked}
              onMarkToggle={handleMarkToggle}
              onClearResponse={handleClearResponse}
            />
          </div>

          {/* Bottom Navigation Buttons */}
          <div className="mt-4 bg-white border border-slate-200 rounded-xl p-4 flex justify-between items-center shadow-xs">
            <button
              onClick={() => setCurrentIdx(prev => Math.max(prev - 1, 0))}
              disabled={currentIdx === 0}
              className="flex items-center space-x-2 px-5 py-2.5 rounded-xl font-bold text-sm text-slate-700 bg-slate-100 hover:bg-slate-200 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>Previous Question</span>
            </button>

            <button
              onClick={() => setCurrentIdx(prev => Math.min(prev + 1, questions.length - 1))}
              disabled={currentIdx === questions.length - 1}
              className="flex items-center space-x-2 px-6 py-2.5 rounded-xl font-black text-sm text-white bg-primary hover:bg-primary-light disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-xs"
            >
              <span>Save & Next</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Right Side: Palette Sidebar */}
        <div className="hidden lg:block w-80 shrink-0 h-full">
          <QuestionPalette
            questions={questions}
            currentIndex={currentIdx}
            answers={answers}
            visited={visited}
            markedForReview={markedForReview}
            onQuestionSelect={(idx) => setCurrentIdx(idx)}
          />
        </div>
      </main>

      {/* Submit Confirmation Modal */}
      {showSubmitModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-xs" onClick={() => setShowSubmitModal(false)} />
          <div className="relative bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full border border-slate-100 animate-in zoom-in-95 duration-150">
            <h3 className="text-xl font-black text-slate-900 mb-2">Submit Examination?</h3>
            <p className="text-sm text-slate-500 mb-6">Check your completion status before final submission:</p>

            <div className="grid grid-cols-3 gap-3 p-4 bg-slate-50 rounded-xl border border-slate-200 text-center mb-6">
              <div>
                <span className="block text-2xl font-black text-emerald-600">{answeredCount}</span>
                <span className="text-xs uppercase font-bold text-slate-400">Answered</span>
              </div>
              <div className="border-x border-slate-200">
                <span className="block text-2xl font-black text-red-500">{unansweredCount}</span>
                <span className="text-xs uppercase font-bold text-slate-400">Unanswered</span>
              </div>
              <div>
                <span className="block text-2xl font-black text-purple-600">{markedForReview.size}</span>
                <span className="text-xs uppercase font-bold text-slate-400">Review</span>
              </div>
            </div>

            {unansweredCount > 0 && (
              <p className="text-amber-700 text-xs bg-amber-50 p-3 rounded-xl border border-amber-200 mb-6">
                ⚠️ You have <strong>{unansweredCount}</strong> unanswered question{unansweredCount > 1 ? 's' : ''}.
              </p>
            )}

            <div className="flex space-x-3">
              <button
                type="button"
                onClick={() => setShowSubmitModal(false)}
                className="flex-1 py-3 px-4 rounded-xl font-bold text-sm text-slate-700 bg-slate-100 hover:bg-slate-200 transition-colors"
              >
                Go Back
              </button>
              <button
                type="button"
                onClick={submitQuiz}
                disabled={submitting}
                className="flex-1 py-3 px-4 rounded-xl font-black text-sm text-white bg-emerald-600 hover:bg-emerald-700 transition-colors flex items-center justify-center shadow-xs"
              >
                {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Confirm Submit'}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default QuizPage;
