import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import SubjectSelect from './pages/SubjectSelect';
import QuizConfig from './pages/QuizConfig';
import QuizPage from './pages/QuizPage';
import ResultPage from './pages/ResultPage';
import Analytics from './pages/Analytics';
import PaperAnalysis from './pages/PaperAnalysis';
import StudyBuddy from './pages/StudyBuddy';

const App = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          
          <Route path="/subjects" element={
            <ProtectedRoute>
              <SubjectSelect />
            </ProtectedRoute>
          } />

          <Route path="/paper-analysis" element={
            <ProtectedRoute>
              <PaperAnalysis />
            </ProtectedRoute>
          } />
          
          <Route path="/quiz/config" element={
            <ProtectedRoute>
              <QuizConfig />
            </ProtectedRoute>
          } />
          
          <Route path="/quiz/:sessionId" element={
            <ProtectedRoute>
              <QuizPage />
            </ProtectedRoute>
          } />
          
          <Route path="/quiz/:sessionId/result" element={
            <ProtectedRoute>
              <ResultPage />
            </ProtectedRoute>
          } />
          
          <Route path="/analytics" element={
            <ProtectedRoute>
              <Analytics />
            </ProtectedRoute>
          } />

          <Route path="/study-buddy" element={
            <ProtectedRoute>
              <StudyBuddy />
            </ProtectedRoute>
          } />
          
          {/* 404 Route */}
          <Route path="*" element={
            <div className="min-h-screen flex items-center justify-center flex-col text-center px-4">
              <h1 className="text-6xl font-bold text-primary mb-4">404</h1>
              <h2 className="text-2xl font-semibold text-slate-800 mb-6">Page Not Found</h2>
              <p className="text-slate-500 mb-8">The page you are looking for doesn't exist or has been moved.</p>
              <a href="/" className="bg-primary hover:bg-primary-light text-white px-6 py-3 rounded-lg font-medium transition-colors">
                Back to Home
              </a>
            </div>
          } />
        </Routes>
      </main>
    </div>
  );
};

export default App;
