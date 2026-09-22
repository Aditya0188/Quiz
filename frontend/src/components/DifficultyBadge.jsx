import React from 'react';
import { DIFFICULTY_COLORS } from '../utils/constants';

const DifficultyBadge = ({ difficulty }) => {
  if (!difficulty) return null;
  const colorClass = DIFFICULTY_COLORS[difficulty] || 'bg-slate-100 text-slate-800 border-slate-200';
  
  return (
    <span className={`px-2.5 py-1 text-xs font-semibold rounded border ${colorClass}`}>
      {difficulty}
    </span>
  );
};

export default DifficultyBadge;
