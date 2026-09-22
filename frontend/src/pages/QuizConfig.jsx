import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import client from '../api/client';
import { SUBJECTS } from '../utils/constants';
import { Settings, Play, Info, Loader2, Sparkles, Clock, CheckCircle2, BookOpen } from 'lucide-react';
import toast from 'react-hot-toast';

const QuizConfig = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const subjectParam = searchParams.get('subject') || '';
  const topicParam = searchParams.get('topic') || '';
  const yearParam = searchParams.get('year') || '';

  // Determine initial selected subject
  const initialSubject = (() => {
    if (!subjectParam || subjectParam.toUpperCase() === 'MIX') return 'ALL';
    const match = SUBJECTS.find(s => s.name === subjectParam || s.id === subjectParam || s.displayName === subjectParam);
    return match ? match.name : 'ALL';
  })();

  const [selectedSubject, setSelectedSubject] = useState(initialSubject);
  const [availableTopics, setAvailableTopics] = useState([]);
  const [selectedTopics, setSelectedTopics] = useState(topicParam ? [topicParam] : []);
  const [loadingTopics, setLoadingTopics] = useState(false);

  const [config, setConfig] = useState({
    numQuestions: 15,
    difficulty: 'mixed',
    timeLimit: 30, // in minutes
    questionTypes: ['MCQ', 'MSQ', 'NAT'],
  });

  const [customTimeInput, setCustomTimeInput] = useState('30');
  const [customQuestionsInput, setCustomQuestionsInput] = useState('15');
  const [starting, setStarting] = useState(false);

  // Fetch topics whenever selectedSubject changes
  useEffect(() => {
    if (selectedSubject === 'ALL') {
      setAvailableTopics([]);
      setSelectedTopics([]);
      return;
    }

    const fetchTopics = async () => {
      setLoadingTopics(true);
      try {
        const res = await client.get(`/subjects/${encodeURIComponent(selectedSubject)}/topics`);
        const topicList = res.data.map(t => t.topic);
        setAvailableTopics(topicList);
        if (topicParam && topicList.includes(topicParam)) {
          setSelectedTopics([topicParam]);
        } else {
          setSelectedTopics([]); // default to all topics in that subject
        }
      } catch (err) {
        console.error('Failed to load topics', err);
      } finally {
        setLoadingTopics(false);
      }
    };

    fetchTopics();
  }, [selectedSubject, topicParam]);

  const presetTimes = [15, 30, 45, 60, 90, 120, 180];
  const presetQCounts = [5, 10, 15, 20, 25, 30, 50, 65];

  const handleTimePresetClick = (minutes) => {
    setConfig(prev => ({ ...prev, timeLimit: minutes }));
    setCustomTimeInput(String(minutes));
  };

  const handleCustomTimeChange = (e) => {
    const val = e.target.value;
    setCustomTimeInput(val);
    const parsed = parseInt(val, 10);
    if (!isNaN(parsed) && parsed > 0) {
      setConfig(prev => ({ ...prev, timeLimit: parsed }));
    }
  };

  const handleQCountPresetClick = (count) => {
    setConfig(prev => ({ ...prev, numQuestions: count }));
    setCustomQuestionsInput(String(count));
  };

  const handleCustomQCountChange = (e) => {
    const val = e.target.value;
    setCustomQuestionsInput(val);
    const parsed = parseInt(val, 10);
    if (!isNaN(parsed) && parsed > 0) {
      setConfig(prev => ({ ...prev, numQuestions: parsed }));
    }
  };

  const toggleTopic = (topic) => {
    setSelectedTopics(prev => {
      if (prev.includes(topic)) {
        return prev.filter(t => t !== topic);
      } else {
        return [...prev, topic];
      }
    });
  };

  const handleStartQuiz = async () => {
    if (config.questionTypes.length === 0) {
      return toast.error('Please select at least one question type');
    }

    const finalTime = parseInt(customTimeInput, 10) || config.timeLimit;
    const finalQCount = parseInt(customQuestionsInput, 10) || config.numQuestions;

    if (finalTime <= 0) {
      return toast.error('Please enter a valid time limit in minutes');
    }
    if (finalQCount <= 0) {
      return toast.error('Please enter a valid number of questions');
    }

    setStarting(true);
    try {
      const subjectList = selectedSubject === 'ALL' ? [] : [selectedSubject];
      const parsedYear = yearParam ? parseInt(yearParam, 10) : null;
      const yearRange = parsedYear ? [parsedYear, parsedYear] : [1991, 2026];
      const payload = {
        subjects: subjectList,
        topics: selectedTopics,
        difficulty: config.difficulty.toLowerCase(),
        num_questions: finalQCount,
        time_limit: finalTime,
        question_types: config.questionTypes,
        year_range: yearRange,
        include_ai: false
      };

      const res = await client.post('/quiz/start', payload);
      const sessionId = res.data.session_id;

      // Identify display title for the quiz
      const displayTitle = yearParam
        ? `GATE ${yearParam} Full Paper`
        : selectedSubject === 'ALL'
        ? 'All Subjects (GATE Mock Mix)'
        : (SUBJECTS.find(s => s.name === selectedSubject)?.displayName || selectedSubject);

      // Store in sessionStorage for fast load
      sessionStorage.setItem(`quiz_${sessionId}`, JSON.stringify({
        questions: res.data.questions,
        time_limit_minutes: res.data.time_limit_minutes,
        subject: displayTitle
      }));

      navigate(`/quiz/${sessionId}`);
    } catch (error) {
      console.error(error);
      const msg = error.response?.data?.detail || 'Failed to start quiz. Try adjusting filters.';
      toast.error(msg);
      setStarting(false);
    }
  };

  const activeSubjectObj = SUBJECTS.find(s => s.name === selectedSubject);

  return (
    <div className="pt-24 pb-16 max-w-4xl mx-auto px-4 sm:px-6">
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-primary to-primary-light px-5 sm:px-8 py-5 sm:py-6 text-white">
          <div className="flex items-center space-x-3">
            <Settings className="w-5 h-5 sm:w-6 sm:h-6 text-white/80" />
            <h1 className="text-xl sm:text-2xl font-extrabold">Customize Your Quiz</h1>
          </div>
          {yearParam ? (
            <div className="mt-2 inline-flex items-center space-x-1.5 bg-emerald-500/30 text-emerald-200 px-3 py-1 rounded-lg text-xs font-bold border border-emerald-400/40">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Full Paper Practice Mode: GATE {yearParam} Exam</span>
            </div>
          ) : (
            <p className="text-white/80 mt-1 text-xs sm:text-sm flex items-center">
              <Sparkles className="w-4 h-4 mr-1.5 text-amber-300 shrink-0" />
              <span>Anti-Repetition Active: Fresh questions on every attempt!</span>
            </p>
          )}
        </div>

        <div className="p-4 sm:p-8 space-y-6 sm:space-y-8">

          {/* 1. Subject Selector */}
          <div>
            <div className="flex justify-between items-center mb-3">
              <label className="block text-sm font-bold text-slate-800">
                1. Select Subject
              </label>
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-primary/10 text-primary">
                {selectedSubject === 'ALL' ? 'Mixed All Subjects' : (activeSubjectObj?.displayName || selectedSubject)}
              </span>
            </div>

            <select
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="w-full px-4 py-3 border-2 border-slate-200 rounded-xl font-medium text-slate-700 bg-white focus:ring-2 focus:ring-primary focus:border-primary transition-all text-base cursor-pointer hover:border-slate-300"
            >
              <option value="ALL">🌟 All Subjects (Complete Mixed GATE Test)</option>
              {SUBJECTS.map(s => (
                <option key={s.id} value={s.name}>
                  {s.displayName} ({s.name})
                </option>
              ))}
            </select>
          </div>

          {/* 1b. Topic Filter (if single subject selected) */}
          {selectedSubject !== 'ALL' && availableTopics.length > 0 && (
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-5">
              <div className="flex justify-between items-center mb-3">
                <span className="text-sm font-bold text-slate-700">
                  Focus on Specific Topics (Optional)
                </span>
                <span className="text-xs text-slate-500">
                  {selectedTopics.length === 0 ? 'All Topics included' : `${selectedTopics.length} selected`}
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setSelectedTopics([])}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    selectedTopics.length === 0
                      ? 'bg-primary text-white shadow-sm'
                      : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  All Topics
                </button>
                {availableTopics.map(t => {
                  const isSelected = selectedTopics.includes(t);
                  return (
                    <button
                      key={t}
                      onClick={() => toggleTopic(t)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                        isSelected
                          ? 'bg-primary text-white shadow-sm ring-1 ring-primary'
                          : 'bg-white border border-slate-200 text-slate-600 hover:border-primary/40 hover:bg-slate-100'
                      }`}
                    >
                      {t}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* 2. Timer Control (Presets + Custom Input) */}
          <div className="border-t border-slate-100 pt-6">
            <div className="flex flex-wrap justify-between items-center mb-3 gap-2">
              <label className="text-sm font-bold text-slate-800 flex items-center">
                <Clock className="w-4 h-4 mr-1.5 text-primary" />
                2. Time Limit
              </label>
              <div className="text-xs font-semibold text-primary bg-primary/10 px-3 py-1 rounded-full">
                Active Timer: {customTimeInput || config.timeLimit} Minutes
              </div>
            </div>

            {/* Presets */}
            <div className="flex flex-wrap gap-2.5 mb-3">
              {presetTimes.map(mins => {
                const isActive = parseInt(customTimeInput, 10) === mins;
                return (
                  <button
                    key={mins}
                    type="button"
                    onClick={() => handleTimePresetClick(mins)}
                    className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                      isActive
                        ? 'bg-primary text-white shadow-md scale-105'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {mins} min
                  </button>
                );
              })}
            </div>

            {/* Custom Time Input */}
            <div className="flex items-center gap-3 bg-slate-50 p-3.5 rounded-xl border border-slate-200">
              <span className="text-sm font-medium text-slate-700">Or Set Custom Time:</span>
              <div className="relative w-36">
                <input
                  type="number"
                  min="1"
                  max="300"
                  value={customTimeInput}
                  onChange={handleCustomTimeChange}
                  className="w-full px-3 py-2 border-2 border-slate-300 rounded-lg font-bold text-slate-800 text-center focus:ring-2 focus:ring-primary focus:border-primary outline-none"
                  placeholder="e.g. 25"
                />
              </div>
              <span className="text-sm text-slate-500 font-medium">Minutes (any duration)</span>
            </div>
          </div>

          {/* 3. Number of Questions Control (Presets + Custom Input) */}
          <div className="border-t border-slate-100 pt-6">
            <div className="flex flex-wrap justify-between items-center mb-3 gap-2">
              <label className="text-sm font-bold text-slate-800 flex items-center">
                <BookOpen className="w-4 h-4 mr-1.5 text-primary" />
                3. Number of Questions
              </label>
              <div className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-3 py-1 rounded-full">
                Selected: {customQuestionsInput || config.numQuestions} Questions
              </div>
            </div>

            {/* Presets */}
            <div className="flex flex-wrap gap-2.5 mb-3">
              {presetQCounts.map(count => {
                const isActive = parseInt(customQuestionsInput, 10) === count;
                return (
                  <button
                    key={count}
                    type="button"
                    onClick={() => handleQCountPresetClick(count)}
                    className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                      isActive
                        ? 'bg-emerald-600 text-white shadow-md scale-105'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {count} Qs {count === 65 ? '(Full GATE)' : ''}
                  </button>
                );
              })}
            </div>

            {/* Custom Question Count Input */}
            <div className="flex items-center gap-3 bg-slate-50 p-3.5 rounded-xl border border-slate-200">
              <span className="text-sm font-medium text-slate-700">Or Set Custom Count:</span>
              <div className="relative w-36">
                <input
                  type="number"
                  min="1"
                  max="100"
                  value={customQuestionsInput}
                  onChange={handleCustomQCountChange}
                  className="w-full px-3 py-2 border-2 border-slate-300 rounded-lg font-bold text-slate-800 text-center focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 outline-none"
                  placeholder="e.g. 18"
                />
              </div>
              <span className="text-sm text-slate-500 font-medium">Questions</span>
            </div>
          </div>

          {/* 4. Difficulty Selection */}
          <div className="border-t border-slate-100 pt-6">
            <label className="block text-sm font-bold text-slate-800 mb-3">
              4. Difficulty Level
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { label: '🎯 Mixed (Exam Like)', value: 'mixed' },
                { label: '🟢 Easy (Foundation)', value: 'easy' },
                { label: '🟡 Medium (Standard)', value: 'medium' },
                { label: '🔴 Hard (Advanced)', value: 'hard' },
              ].map(diff => (
                <button
                  key={diff.value}
                  type="button"
                  onClick={() => setConfig({ ...config, difficulty: diff.value })}
                  className={`py-3 px-3 rounded-xl font-bold text-xs sm:text-sm text-center transition-all ${
                    config.difficulty === diff.value
                      ? 'bg-primary text-white shadow-md ring-2 ring-primary ring-offset-1'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {diff.label}
                </button>
              ))}
            </div>
          </div>

          {/* 5. Question Types Selection */}
          <div className="border-t border-slate-100 pt-6">
            <label className="block text-sm font-bold text-slate-800 mb-3">
              5. Question Types (GATE Format)
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                { id: 'MCQ', label: 'Multiple Choice (MCQ)', desc: 'Official negative marking (-1/3 or -2/3)' },
                { id: 'MSQ', label: 'Multiple Select (MSQ)', desc: 'All-or-nothing, 0 negative marking' },
                { id: 'NAT', label: 'Numerical Answer (NAT)', desc: 'Exact value, 0 negative marking' }
              ].map(type => {
                const checked = config.questionTypes.includes(type.id);
                return (
                  <label
                    key={type.id}
                    className={`flex items-start space-x-3 p-4 rounded-xl border-2 cursor-pointer transition-all ${
                      checked
                        ? 'border-primary bg-primary/5 shadow-sm'
                        : 'border-slate-200 hover:border-primary/40'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={checked}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setConfig({ ...config, questionTypes: [...config.questionTypes, type.id] });
                        } else {
                          setConfig({ ...config, questionTypes: config.questionTypes.filter(t => t !== type.id) });
                        }
                      }}
                      className="w-5 h-5 mt-0.5 text-primary border-slate-300 rounded focus:ring-primary"
                    />
                    <div>
                      <span className="text-slate-800 font-bold text-sm block">{type.label}</span>
                      <p className="text-xs text-slate-500 mt-1">{type.desc}</p>
                    </div>
                  </label>
                );
              })}
            </div>
          </div>

          {/* Anti-Repetition Assurance Banner */}
          <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 flex items-start space-x-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 mt-0.5 shrink-0" />
            <div className="text-xs sm:text-sm text-emerald-900 leading-relaxed">
              <span className="font-bold">Guaranteed New Questions: </span>
              Our smart tracking system remembers all questions you have previously been given. Each new quiz prioritizes unattempted questions from the 35-year archive so you won't see questions repeating!
            </div>
          </div>

          {/* Start Button */}
          <div className="pt-4 border-t border-slate-200">
            <button
              onClick={handleStartQuiz}
              disabled={starting}
              className="w-full flex justify-center items-center py-4 px-6 rounded-xl shadow-xl text-lg font-extrabold text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-4 focus:ring-emerald-300 transition-all transform hover:-translate-y-0.5 disabled:opacity-70 disabled:transform-none cursor-pointer"
            >
              {starting ? (
                <>
                  <Loader2 className="w-6 h-6 animate-spin mr-2" />
                  Generating Your Fresh Question Set...
                </>
              ) : (
                <>
                  <Play className="w-6 h-6 mr-2 fill-current" />
                  Start Quiz — {customQuestionsInput || config.numQuestions} Questions, {customTimeInput || config.timeLimit} Minutes
                </>
              )}
            </button>
          </div>

        </div>
      </div>
    </div>
  );
};

export default QuizConfig;
