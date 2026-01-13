import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const TestConfigPage = () => {
  const navigate = useNavigate();
  
  const [questionCount, setQuestionCount] = useState(10);
  const [selectedTypes, setSelectedTypes] = useState({
    nash: true,
    csp: true,
    minmax: true,
    strategy: true,
  });
  
  const questionTypeLabels = {
    nash: 'Nash Equilibrium',
    csp: 'CSP (Constraint Satisfaction)',
    minmax: 'MinMax / Alpha-Beta',
    strategy: 'Strategy Selection',
  };
  
  // Calculate time based on question count (2 minutes per question)
  const getTimeForQuestions = (count) => {
    const minutes = count * 2;
    return minutes;
  };
  
  const handleTypeToggle = (type) => {
    setSelectedTypes((prev) => ({
      ...prev,
      [type]: !prev[type],
    }));
  };
  
  const handleSelectAll = () => {
    setSelectedTypes({
      nash: true,
      csp: true,
      minmax: true,
      strategy: true,
    });
  };
  
  const handleRandomMode = () => {
    // Random number of questions between 5-15
    const randomCount = [5, 10, 15][Math.floor(Math.random() * 3)];
    setQuestionCount(randomCount);
    
    // Randomly select 2-4 types
    const types = ['nash', 'csp', 'minmax', 'strategy'];
    const shuffled = types.sort(() => 0.5 - Math.random());
    const selectedCount = Math.floor(Math.random() * 3) + 2; // 2-4 types
    const randomTypes = {};
    types.forEach((type) => {
      randomTypes[type] = shuffled.slice(0, selectedCount).includes(type);
    });
    setSelectedTypes(randomTypes);
  };
  
  const getSelectedTypesArray = () => {
    return Object.entries(selectedTypes)
      .filter(([_, isSelected]) => isSelected)
      .map(([type]) => type);
  };
  
  const canStartTest = () => {
    return getSelectedTypesArray().length > 0;
  };
  
  const handleStartTest = () => {
    const config = {
      questionCount,
      types: getSelectedTypesArray(),
      timeLimit: getTimeForQuestions(questionCount) * 60, // in seconds
    };
    
    // Navigate to test page with config
    navigate('/tests/active', { state: config });
  };
  
  return (
    <div className="bg-brand-bg min-h-screen py-10 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Back to Home */}
        <Link
          to="/"
          className="inline-flex items-center text-brand-primary hover:text-brand-hover transition-colors mb-6"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Înapoi la Home
        </Link>
        
        {/* Title */}
        <h1 className="text-5xl md:text-6xl font-bold text-center mb-4">
          <span className="text-brand-primary">Mod</span>{' '}
          <span className="text-brand-hover">Examen</span>
        </h1>
        
        <p className="text-center text-brand-neutral mb-10">
          Configurează testul și verifică-ți cunoștințele
        </p>
        
        {/* Configuration Card */}
        <div className="bg-brand-surface rounded-xl shadow-lg p-8 border border-brand-neutral/20">
          
          {/* Question Count */}
          <div className="mb-8">
            <label className="block text-lg font-semibold text-brand-dark mb-4">
              Numărul de întrebări
            </label>
            <div className="flex gap-3">
              {[5, 10, 15, 20].map((count) => (
                <button
                  key={count}
                  onClick={() => setQuestionCount(count)}
                  className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all ${
                    questionCount === count
                      ? 'bg-brand-primary text-white shadow-md'
                      : 'bg-brand-bg text-brand-dark border border-brand-neutral/30 hover:border-brand-primary'
                  }`}
                >
                  {count}
                </button>
              ))}
            </div>
            <p className="text-sm text-brand-neutral mt-2">
              Timp alocat: <span className="font-semibold text-brand-primary">{getTimeForQuestions(questionCount)} minute</span>
            </p>
          </div>
          
          {/* Question Types */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <label className="text-lg font-semibold text-brand-dark">
                Tipuri de întrebări
              </label>
              <button
                onClick={handleSelectAll}
                className="text-sm text-brand-primary hover:text-brand-hover transition-colors"
              >
                Selectează toate
              </button>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {Object.entries(questionTypeLabels).map(([type, label]) => (
                <button
                  key={type}
                  onClick={() => handleTypeToggle(type)}
                  className={`p-4 rounded-lg border-2 text-left transition-all ${
                    selectedTypes[type]
                      ? 'border-brand-primary bg-brand-primary/10 text-brand-dark'
                      : 'border-brand-neutral/30 bg-brand-bg text-brand-neutral hover:border-brand-neutral'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-all ${
                        selectedTypes[type]
                          ? 'bg-brand-primary border-brand-primary'
                          : 'border-brand-neutral/50'
                      }`}
                    >
                      {selectedTypes[type] && (
                        <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path
                            fillRule="evenodd"
                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                            clipRule="evenodd"
                          />
                        </svg>
                      )}
                    </div>
                    <span className="font-medium">{label}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
          
          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            <button
              onClick={handleRandomMode}
              className="flex-1 py-4 px-6 rounded-lg font-semibold border-2 border-brand-secondary 
                         text-brand-hover hover:bg-brand-secondary hover:text-white transition-all"
            >
              Mod Random
            </button>
            
            <button
              onClick={handleStartTest}
              disabled={!canStartTest()}
              className={`flex-1 py-4 px-6 rounded-lg font-semibold transition-all ${
                canStartTest()
                  ? 'bg-brand-primary text-white hover:bg-brand-hover shadow-lg hover:shadow-xl'
                  : 'bg-brand-neutral/30 text-brand-neutral cursor-not-allowed'
              }`}
            >
              Începe Testul
            </button>
          </div>
          
          {!canStartTest() && (
            <p className="text-center text-red-500 text-sm mt-4">
              Selectează cel puțin un tip de întrebare
            </p>
          )}
        </div>
        
        {/* Info Box */}
        <div className="mt-8 bg-brand-primary/10 rounded-lg p-6 border border-brand-primary/30">
          <h3 className="font-semibold text-brand-hover mb-2">Cum funcționează?</h3>
          <ul className="text-sm text-brand-dark space-y-2">
            <li>• Răspunde la întrebări în ritmul tău - poți naviga înainte și înapoi</li>
            <li>• Poți sări peste întrebări și reveni mai târziu</li>
            <li>• Feedback-ul și scorul final apar doar după finalizarea testului</li>
            <li>• Cronometrul te ajută să îți gestionezi timpul</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TestConfigPage;
