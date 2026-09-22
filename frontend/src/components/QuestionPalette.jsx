import React from 'react';

const QuestionPalette = ({
  questions,
  currentIndex,
  answers,
  visited,
  markedForReview,
  onQuestionSelect
}) => {
  const getStatus = (question, index) => {
    const qId = question.id;
    const hasAnswer = answers[qId] !== undefined && answers[qId] !== null &&
      (Array.isArray(answers[qId]) ? answers[qId].length > 0 : answers[qId] !== '');
    const isVisited = visited.has(index);
    const isMarked = markedForReview.has(qId);
    const isCurrent = index === currentIndex;

    if (isMarked && hasAnswer) return 'marked-answered';
    if (isMarked) return 'marked';
    if (hasAnswer) return 'answered';
    if (isVisited) return 'not-answered';
    return 'not-visited';
  };

  const statusStyles = {
    'answered': 'bg-emerald-500 text-white hover:bg-emerald-600',
    'not-answered': 'bg-red-500 text-white hover:bg-red-600',
    'not-visited': 'bg-slate-200 text-slate-600 hover:bg-slate-300',
    'marked': 'bg-purple-500 text-white hover:bg-purple-600',
    'marked-answered': 'bg-purple-500 text-white ring-2 ring-emerald-400 hover:bg-purple-600',
  };

  const stats = {
    answered: 0,
    notAnswered: 0,
    notVisited: 0,
    marked: 0,
  };

  questions.forEach((q, i) => {
    const s = getStatus(q, i);
    if (s === 'answered' || s === 'marked-answered') stats.answered++;
    else if (s === 'not-answered') stats.notAnswered++;
    else if (s === 'not-visited') stats.notVisited++;
    if (s === 'marked' || s === 'marked-answered') stats.marked++;
  });

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 h-full flex flex-col overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-200 bg-slate-50">
        <h3 className="font-bold text-slate-800">Question Palette</h3>
      </div>

      {/* Grid */}
      <div className="flex-grow overflow-y-auto p-4">
        <div className="grid grid-cols-5 gap-2">
          {questions.map((q, index) => {
            const status = getStatus(q, index);
            const isCurrent = index === currentIndex;
            return (
              <button
                key={q.id}
                onClick={() => onQuestionSelect(index)}
                className={`w-full aspect-square rounded-lg font-bold text-sm flex items-center justify-center transition-all ${statusStyles[status]} ${
                  isCurrent ? 'ring-2 ring-primary ring-offset-2 scale-110' : ''
                }`}
              >
                {index + 1}
              </button>
            );
          })}
        </div>
      </div>

      {/* Legend */}
      <div className="px-5 py-4 border-t border-slate-200 bg-slate-50 space-y-2">
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded bg-emerald-500" />
            <span className="text-slate-600">Answered ({stats.answered})</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded bg-red-500" />
            <span className="text-slate-600">Not Answered ({stats.notAnswered})</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded bg-slate-200" />
            <span className="text-slate-600">Not Visited ({stats.notVisited})</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded bg-purple-500" />
            <span className="text-slate-600">Review ({stats.marked})</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestionPalette;
