import React from 'react';
import { Bookmark, Eraser } from 'lucide-react';
import { parseLaTeX } from '../utils/helpers';

const DIFF_COLORS = {
  easy: 'bg-emerald-100 text-emerald-700 border-emerald-200',
  medium: 'bg-amber-100 text-amber-700 border-amber-200',
  hard: 'bg-red-100 text-red-700 border-red-200',
};

const TYPE_COLORS = {
  MCQ: 'bg-blue-100 text-blue-700',
  MSQ: 'bg-purple-100 text-purple-700',
  NAT: 'bg-teal-100 text-teal-700',
};

const QuestionCard = ({
  question,
  questionNumber,
  totalQuestions,
  selectedAnswer,
  onAnswerSelect,
  isMarked,
  onMarkToggle,
  onClearResponse
}) => {
  if (!question) return null;

  const { id, subject, topic, question_type, question_text, options, marks, difficulty, year, set_number } = question;
  const optionEntries = options ? Object.entries(options) : [];

  const handleOptionClick = (key) => {
    if (question_type === 'MCQ') {
      onAnswerSelect(key);
    } else if (question_type === 'MSQ') {
      let current = selectedAnswer || [];
      if (typeof current === 'string') current = current.split(',').filter(Boolean);
      if (current.includes(key)) {
        current = current.filter(k => k !== key);
      } else {
        current = [...current, key];
      }
      onAnswerSelect(current.sort());
    }
  };

  const handleNatChange = (e) => {
    onAnswerSelect(e.target.value);
  };

  const isOptionSelected = (key) => {
    if (!selectedAnswer) return false;
    if (question_type === 'MCQ') return selectedAnswer === key;
    if (question_type === 'MSQ') {
      if (Array.isArray(selectedAnswer)) return selectedAnswer.includes(key);
      if (typeof selectedAnswer === 'string') return selectedAnswer.split(',').includes(key);
    }
    return false;
  };

  const hasAnswer = selectedAnswer !== undefined && selectedAnswer !== null &&
    (Array.isArray(selectedAnswer) ? selectedAnswer.length > 0 : selectedAnswer !== '');

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col h-full">
      
      {/* Header */}
      <div className="bg-slate-50 border-b border-slate-200 px-6 py-4 flex flex-wrap justify-between items-center gap-2">
        <div className="flex items-center space-x-3">
          <span className="font-extrabold text-xl text-slate-800">
            Question {questionNumber}
          </span>
          <span className="text-sm text-slate-400 font-bold">
            / {totalQuestions}
          </span>

          {subject && (
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-md bg-primary/10 text-primary border border-primary/20">
              {subject}
            </span>
          )}
          {topic && (
            <span className="px-2.5 py-0.5 text-xs font-medium rounded-md bg-slate-200 text-slate-700">
              {topic}
            </span>
          )}
          {year > 0 && (
            <span className="text-xs text-slate-600 bg-white border border-slate-200 px-2 py-0.5 rounded font-mono font-bold">
              GATE {year} {set_number ? `(${set_number})` : ''}
            </span>
          )}
        </div>

        <div className="flex items-center space-x-2">
          <span className={`px-2.5 py-1 text-xs font-black rounded ${TYPE_COLORS[question_type] || 'bg-slate-200 text-slate-700'}`}>
            {question_type}
          </span>
          <span className="px-2.5 py-1 text-xs font-black rounded bg-blue-100 text-blue-800">
            {marks} Mark{marks > 1 ? 's' : ''}
          </span>
          {difficulty && (
            <span className={`px-2.5 py-1 text-xs font-bold rounded border capitalize ${DIFF_COLORS[difficulty] || ''}`}>
              {difficulty}
            </span>
          )}
        </div>
      </div>

      {/* Question Text */}
      <div className="p-6 md:p-8 flex-grow overflow-y-auto max-w-full">
        <div className="text-base md:text-lg text-slate-900 mb-8 leading-relaxed break-words whitespace-pre-line select-text">
          {parseLaTeX(question_text)}
        </div>

        {/* Options for MCQ / MSQ */}
        {(question_type === 'MCQ' || question_type === 'MSQ') && (
          <div className="space-y-3">
            {question_type === 'MSQ' && (
              <p className="text-xs text-purple-700 font-bold mb-2 bg-purple-50 p-2.5 rounded-lg border border-purple-100">
                ✦ Multiple Select Question (MSQ): Select ALL correct options. No negative marking.
              </p>
            )}
            {optionEntries.map(([key, text]) => {
              const selected = isOptionSelected(key);
              return (
                <button
                  key={key}
                  type="button"
                  onClick={() => handleOptionClick(key)}
                  className={`w-full flex items-start p-4 rounded-xl border-2 text-left transition-all ${
                    selected
                      ? 'border-primary bg-primary/5 shadow-xs ring-1 ring-primary/30'
                      : 'border-slate-200 hover:border-primary/40 hover:bg-slate-50'
                  }`}
                >
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mr-4 font-black text-sm ${
                    selected
                      ? 'bg-primary text-white shadow-xs'
                      : 'bg-slate-100 text-slate-600 border border-slate-200'
                  }`}>
                    {key}
                  </div>
                  <div className="flex-1 pt-1 text-sm md:text-base text-slate-800 break-words leading-relaxed">
                    {parseLaTeX(text)}
                  </div>
                  <div className="ml-3 shrink-0 pt-1.5">
                    {question_type === 'MCQ' ? (
                      <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                        selected ? 'border-primary' : 'border-slate-300'
                      }`}>
                        {selected && <div className="w-2.5 h-2.5 rounded-full bg-primary" />}
                      </div>
                    ) : (
                      <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                        selected ? 'border-primary bg-primary' : 'border-slate-300'
                      }`}>
                        {selected && (
                          <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                          </svg>
                        )}
                      </div>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        )}

        {/* NAT Input */}
        {question_type === 'NAT' && (
          <div className="mt-6 bg-slate-50 p-6 rounded-xl border border-slate-200 max-w-md">
            <p className="text-xs text-teal-700 font-bold mb-3">
              ✦ Numerical Answer Type (NAT): Type a real number or integer value. No negative marking.
            </p>
            <label className="block text-xs font-bold text-slate-600 uppercase mb-2">
              Enter Your Numerical Answer:
            </label>
            <input
              type="text"
              value={selectedAnswer || ''}
              onChange={handleNatChange}
              className="w-full px-4 py-3 border-2 border-slate-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-colors text-xl font-mono font-bold bg-white text-slate-900"
              placeholder="e.g. 42 or 3.14"
            />
          </div>
        )}
      </div>

      {/* Footer Actions */}
      <div className="bg-slate-50 border-t border-slate-200 px-6 py-4 flex flex-wrap justify-between items-center gap-3">
        <button
          type="button"
          onClick={onClearResponse}
          disabled={!hasAnswer}
          className="flex items-center space-x-1.5 text-slate-500 hover:text-red-600 transition-colors disabled:opacity-30 disabled:cursor-not-allowed text-sm font-semibold py-1.5 px-3 rounded-lg"
        >
          <Eraser className="w-4 h-4" />
          <span>Clear Response</span>
        </button>

        <div className="flex items-center space-x-3">
          {question_type === 'MCQ' && (
            <span className="text-xs text-red-500 font-medium">
              Negative Marking: -{marks === 1 ? '0.33' : '0.66'}
            </span>
          )}
          <button
            type="button"
            onClick={onMarkToggle}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl font-bold text-sm transition-all ${
              isMarked
                ? 'bg-purple-100 text-purple-800 ring-1 ring-purple-300'
                : 'bg-white border border-slate-300 text-slate-700 hover:bg-slate-100'
            }`}
          >
            <Bookmark className={`w-4 h-4 ${isMarked ? 'fill-current' : ''}`} />
            <span>{isMarked ? 'Marked' : 'Mark for Review'}</span>
          </button>
        </div>
      </div>

    </div>
  );
};

export default QuestionCard;
