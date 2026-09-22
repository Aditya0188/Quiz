import React from 'react';
import { Link } from 'react-router-dom';
import { SUBJECTS } from '../utils/constants';
import * as Icons from 'lucide-react';

const SubjectSelect = () => {
  return (
    <div className="pt-24 pb-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-8 sm:mb-12">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-2 sm:mb-4">Choose a Subject</h1>
        <p className="text-xs sm:text-base text-slate-600 max-w-2xl mx-auto">
          Select a specific subject to focus on, or choose custom mix to combine multiple topics.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {/* Custom Mix Card */}
        <Link 
          to="/quiz/config?subject=MIX"
          className="group bg-gradient-to-br from-primary to-primary-light rounded-xl p-6 shadow-md hover:shadow-xl transition-all transform hover:-translate-y-1 overflow-hidden relative"
        >
          <div className="absolute top-0 right-0 p-4 opacity-20 transform translate-x-4 -translate-y-4 group-hover:scale-110 transition-transform">
            <Icons.Shuffle className="w-24 h-24 text-white" />
          </div>
          <div className="relative z-10 h-full flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                <Icons.Shuffle className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Custom Mix</h3>
              <p className="text-primary-100 text-sm">Create a personalized test combining multiple subjects</p>
            </div>
            <div className="mt-6 flex items-center text-white font-medium text-sm">
              Configure Quiz <Icons.ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </Link>

        {/* Subject Cards */}
        {SUBJECTS.map((subject) => {
          const IconComponent = Icons[subject.icon] || Icons.Book;
          return (
            <Link
              key={subject.id}
              to={`/quiz/config?subject=${encodeURIComponent(subject.name)}`}
              className="group bg-white rounded-xl p-6 shadow-sm border border-slate-200 hover:shadow-lg hover:border-primary/30 transition-all transform hover:-translate-y-1"
            >
              <div className="flex flex-col h-full justify-between">
                <div>
                  <div className={`w-12 h-12 ${subject.bg} rounded-lg flex items-center justify-center mb-4`}>
                    <IconComponent className={`w-6 h-6 ${subject.color}`} />
                  </div>
                  <h3 className="text-lg font-bold text-slate-800 mb-1 leading-tight group-hover:text-primary transition-colors">
                    {subject.displayName}
                  </h3>
                  {subject.subtitle && (
                    <p className="text-xs text-slate-500 line-clamp-2 mb-3">
                      {subject.subtitle}
                    </p>
                  )}
                </div>
                <div className="mt-4 flex items-center text-slate-500 font-medium text-sm group-hover:text-primary transition-colors">
                  Start Subject Quiz <Icons.ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default SubjectSelect;
