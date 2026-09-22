import React, { useState, useEffect } from 'react';
import { Clock } from 'lucide-react';

const QuizTimer = ({ totalSeconds, onTimeUp }) => {
  const [timeLeft, setTimeLeft] = useState(totalSeconds);

  useEffect(() => {
    if (timeLeft <= 0) {
      if (onTimeUp) onTimeUp();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft(prev => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, onTimeUp]);

  const formatTime = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return h > 0 ? `${h}:${m}:${s}` : `${m}:${s}`;
  };

  const percentage = (timeLeft / totalSeconds) * 100;
  
  let colorClass = 'text-primary border-primary';
  let bgClass = 'bg-primary';
  let pulseClass = '';

  if (timeLeft < 300) { // < 5 mins
    colorClass = 'text-warning border-warning';
    bgClass = 'bg-warning';
  }
  if (timeLeft < 60) { // < 1 min
    colorClass = 'text-error border-error';
    bgClass = 'bg-error';
    pulseClass = 'animate-pulse';
  }

  return (
    <div className={`flex items-center space-x-2 font-mono font-bold text-lg px-4 py-2 rounded-full border-2 ${colorClass} ${pulseClass} bg-white shadow-sm`}>
      <Clock className="w-5 h-5" />
      <span>{formatTime(timeLeft)}</span>
      
      {/* Tiny progress indicator */}
      <div className="w-16 h-2 bg-slate-100 rounded-full ml-2 overflow-hidden">
        <div 
          className={`h-full ${bgClass} transition-all duration-1000`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
};

export default QuizTimer;
