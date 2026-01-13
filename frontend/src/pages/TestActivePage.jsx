import React, { useState, useEffect, useCallback } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../services/api';
import MinMaxTree from '../components/MinMaxTree';
import NashMatrix from '../components/NashMatrix';

const TestActivePage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const config = location.state;

  // Redirect if no config
  useEffect(() => {
    if (!config) {
      navigate('/tests');
    }
  }, [config, navigate]);

  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [timeLeft, setTimeLeft] = useState(config?.timeLimit || 600);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Generate questions on mount
  useEffect(() => {
    if (!config) return;

    const generateQuestions = async () => {
      setIsLoading(true);
      const generatedQuestions = [];
      const { questionCount, types } = config;

      // Distribute questions evenly across selected types
      const questionsPerType = Math.floor(questionCount / types.length);
      const remainder = questionCount % types.length;

      for (let i = 0; i < types.length; i++) {
        const type = types[i];
        const count = questionsPerType + (i < remainder ? 1 : 0);

        for (let j = 0; j < count; j++) {
          try {
            const response = await api.get(`/generate/${type}`);
            generatedQuestions.push({
              id: generatedQuestions.length,
              type,
              data: response.data,
            });
          } catch (error) {
            console.error(`Error generating ${type} question:`, error);
          }
        }
      }

      // Shuffle questions
      const shuffled = generatedQuestions.sort(() => Math.random() - 0.5);
      setQuestions(shuffled);

      // Initialize empty answers
      const initialAnswers = {};
      shuffled.forEach((q) => {
        if (q.type === 'csp') {
          initialAnswers[q.id] = {};
        } else if (q.type === 'minmax') {
          initialAnswers[q.id] = { root_value: '', visited_count: '' };
        } else if (q.type === 'nash' && q.data.requires_dominated) {
          // Nash extended with dominated strategies
          initialAnswers[q.id] = {
            hasDominated: null,
            dominatedP1: [],
            dominatedP2: [],
            hasEquilibrium: null,
            equilibria: ''
          };
        } else {
          initialAnswers[q.id] = '';
        }
      });
      setUserAnswers(initialAnswers);
      setIsLoading(false);
    };

    generateQuestions();
  }, [config]);

  // Timer countdown
  useEffect(() => {
    if (isLoading || timeLeft <= 0) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          handleSubmitTest();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isLoading, timeLeft]);

  // Format time as MM:SS
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Get timer color based on remaining time
  const getTimerColor = () => {
    const percentage = (timeLeft / (config?.timeLimit || 600)) * 100;
    if (percentage > 50) return 'text-brand-primary';
    if (percentage > 25) return 'text-yellow-500';
    return 'text-red-500';
  };

  // Get timer background color
  const getTimerBgColor = () => {
    const percentage = (timeLeft / (config?.timeLimit || 600)) * 100;
    if (percentage > 50) return 'bg-brand-primary';
    if (percentage > 25) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  // Handle answer changes
  const handleAnswerChange = (value) => {
    const questionId = questions[currentIndex].id;
    setUserAnswers((prev) => ({
      ...prev,
      [questionId]: value,
    }));
  };

  const handleCspAnswerChange = (variable, value) => {
    const questionId = questions[currentIndex].id;
    setUserAnswers((prev) => ({
      ...prev,
      [questionId]: {
        ...prev[questionId],
        [variable]: value === '' ? '' : parseInt(value, 10),
      },
    }));
  };

  const handleMinMaxAnswerChange = (field, value) => {
    const questionId = questions[currentIndex].id;
    setUserAnswers((prev) => ({
      ...prev,
      [questionId]: {
        ...prev[questionId],
        [field]: value,
      },
    }));
  };

  // Handle Nash extended answer changes
  const handleNashExtendedChange = (field, value) => {
    const questionId = questions[currentIndex].id;
    setUserAnswers((prev) => ({
      ...prev,
      [questionId]: {
        ...prev[questionId],
        [field]: value,
      },
    }));
  };

  // Toggle dominated strategy selection
  const toggleDominatedStrategy = (player, index) => {
    const questionId = questions[currentIndex].id;
    const key = player === 1 ? 'dominatedP1' : 'dominatedP2';
    setUserAnswers((prev) => {
      const current = prev[questionId]?.[key] || [];
      const newArray = current.includes(index)
        ? current.filter((i) => i !== index)
        : [...current, index];
      return {
        ...prev,
        [questionId]: {
          ...prev[questionId],
          [key]: newArray,
        },
      };
    });
  };

  // Navigation
  const goToNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const goToPrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const goToQuestion = (index) => {
    setCurrentIndex(index);
  };

  // Check if question is answered
  const isQuestionAnswered = (questionId) => {
    const answer = userAnswers[questionId];
    if (!answer) return false;

    const question = questions.find((q) => q.id === questionId);
    if (!question) return false;

    if (question.type === 'csp') {
      return Object.values(answer).some((v) => v !== '' && v !== undefined);
    }
    if (question.type === 'minmax') {
      return answer.root_value !== '' || answer.visited_count !== '';
    }
    if (question.type === 'nash' && question.data.requires_dominated) {
      // Extended Nash - check if has any answer
      return answer.hasDominated !== null || answer.hasEquilibrium !== null;
    }
    return answer !== '';
  };

  // Submit test
  const handleSubmitTest = async () => {
    setIsSubmitting(true);

    const results = [];

    for (const question of questions) {
      const answer = userAnswers[question.id];
      let payload;
      let endpoint = `/evaluate/${question.type}`;

      try {
        switch (question.type) {
          case 'nash':
            // Check if it's extended Nash with dominated strategies
            if (question.data.requires_dominated) {
              payload = {
                user_answer: {
                  has_dominated: answer?.hasDominated,
                  dominated_p1: answer?.dominatedP1 || [],
                  dominated_p2: answer?.dominatedP2 || [],
                  has_equilibrium: answer?.hasEquilibrium,
                  equilibria: answer?.equilibria || ''
                },
                raw_data: question.data.raw_data,
                requires_dominated: true
              };
            } else {
              payload = {
                user_answer: answer || '',
                raw_data: question.data.raw_data,
              };
            }
            break;

          case 'csp':
            const cleanedCspAnswer = {};
            Object.entries(answer || {}).forEach(([key, val]) => {
              if (val !== '' && val !== undefined) {
                cleanedCspAnswer[key] = parseInt(val, 10);
              }
            });
            payload = {
              user_answer: cleanedCspAnswer,
              raw_data: question.data.raw_data,
              template_id: question.data.template_id,
            };
            break;

          case 'minmax':
            payload = {
              root_value: answer?.root_value ? parseInt(answer.root_value, 10) : null,
              visited_count: answer?.visited_count ? parseInt(answer.visited_count, 10) : null,
              raw_data: question.data.raw_data,
            };
            break;

          case 'strategy':
            payload = {
              user_answer: answer || '',
              raw_data: question.data.raw_data,
              template_id: question.data.template_id,
            };
            break;

          default:
            continue;
        }

        const response = await api.post(endpoint, payload);
        results.push({
          question,
          userAnswer: answer,
          result: response.data,
        });
      } catch (error) {
        console.error(`Error evaluating question ${question.id}:`, error);
        results.push({
          question,
          userAnswer: answer,
          result: { score: 0, feedback_text: 'Eroare la evaluare' },
        });
      }
    }

    // Navigate to results page
    navigate('/tests/results', {
      state: {
        results,
        totalTime: (config?.timeLimit || 600) - timeLeft,
        totalQuestions: questions.length,
      },
    });
  };

  // Render question content
  const renderQuestionContent = () => {
    if (!questions[currentIndex]) return null;

    const { type, data } = questions[currentIndex];
    const questionId = questions[currentIndex].id;

    return (
      <div>
        {/* Question Text */}
        {type === 'minmax' ? (
          <>
            <p className="text-brand-dark mb-4">
              Pentru arborele de joc generat mai jos, aplicați strategia MIN-MAX.
              Determinați valoarea rădăcinii și numărul de noduri vizitate.
            </p>
            <MinMaxTree treeData={data.raw_data} />
          </>
        ) : type === 'nash' && data.raw_data ? (
          <>
            <p className="text-brand-dark mb-4">
              {data.requires_dominated 
                ? "Pentru jocul reprezentat prin matricea de plăți de mai jos, identificați dacă există strategii strict dominate și echilibrul/echilibrele Nash pure."
                : "Pentru jocul reprezentat prin matricea de plăți de mai jos, identificați echilibrul/echilibrele Nash pure (dacă există)."
              }
            </p>
            <NashMatrix matrixData={data.raw_data} />
          </>
        ) : (
          <p className="text-brand-dark whitespace-pre-wrap">{data.question_text}</p>
        )}

        {/* Answer Input */}
        <div className="mt-6">
          {type === 'nash' && !data.requires_dominated && (
            <div>
              <label className="block text-sm font-medium text-brand-dark mb-2">
                Răspunsul tău (ex: "(0,1)" sau "(0,0), (1,1)"):
              </label>
              <input
                type="text"
                value={userAnswers[questionId] || ''}
                onChange={(e) => handleAnswerChange(e.target.value)}
                placeholder="(rând, coloană)"
                className="w-full border border-brand-neutral/30 rounded-lg px-4 py-3 text-brand-dark 
                           focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-transparent"
              />
            </div>
          )}

          {type === 'nash' && data.requires_dominated && (
            <div className="space-y-6">
              {/* Secțiunea 1: Strategii Dominate */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-semibold text-blue-800 mb-3">1. Strategii Dominate</h4>
                
                <div className="mb-4">
                  <label className="block text-sm font-medium text-brand-dark mb-2">
                    Există strategii strict dominate?
                  </label>
                  <div className="flex gap-4">
                    <button
                      type="button"
                      onClick={() => handleNashExtendedChange('hasDominated', true)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        userAnswers[questionId]?.hasDominated === true
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      Da
                    </button>
                    <button
                      type="button"
                      onClick={() => handleNashExtendedChange('hasDominated', false)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        userAnswers[questionId]?.hasDominated === false
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      Nu
                    </button>
                  </div>
                </div>

                {userAnswers[questionId]?.hasDominated === true && (
                  <div className="space-y-3 border-t border-blue-200 pt-3">
                    <p className="text-sm text-blue-700">Selectează strategiile dominate:</p>
                    
                    <div>
                      <label className="block text-sm font-medium text-brand-dark mb-1">
                        Jucător 1 (rânduri dominate):
                      </label>
                      <div className="flex gap-2 flex-wrap">
                        {Array.from({ length: data.raw_data?.length || 0 }, (_, i) => (
                          <button
                            key={`p1-${i}`}
                            type="button"
                            onClick={() => toggleDominatedStrategy(1, i)}
                            className={`px-3 py-1 rounded-full text-sm font-mono transition-colors ${
                              userAnswers[questionId]?.dominatedP1?.includes(i)
                                ? 'bg-red-500 text-white'
                                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                            }`}
                          >
                            S{i + 1} (rând {i})
                          </button>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-brand-dark mb-1">
                        Jucător 2 (coloane dominate):
                      </label>
                      <div className="flex gap-2 flex-wrap">
                        {Array.from({ length: data.raw_data?.[0]?.length || 0 }, (_, i) => (
                          <button
                            key={`p2-${i}`}
                            type="button"
                            onClick={() => toggleDominatedStrategy(2, i)}
                            className={`px-3 py-1 rounded-full text-sm font-mono transition-colors ${
                              userAnswers[questionId]?.dominatedP2?.includes(i)
                                ? 'bg-red-500 text-white'
                                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                            }`}
                          >
                            S{i + 1} (col {i})
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Secțiunea 2: Echilibru Nash */}
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h4 className="font-semibold text-green-800 mb-3">2. Echilibru Nash Pur</h4>
                
                <div className="mb-4">
                  <label className="block text-sm font-medium text-brand-dark mb-2">
                    Există echilibru Nash pur?
                  </label>
                  <div className="flex gap-4">
                    <button
                      type="button"
                      onClick={() => handleNashExtendedChange('hasEquilibrium', true)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        userAnswers[questionId]?.hasEquilibrium === true
                          ? 'bg-green-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      Da
                    </button>
                    <button
                      type="button"
                      onClick={() => handleNashExtendedChange('hasEquilibrium', false)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        userAnswers[questionId]?.hasEquilibrium === false
                          ? 'bg-green-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      Nu
                    </button>
                  </div>
                </div>

                {userAnswers[questionId]?.hasEquilibrium === true && (
                  <div className="border-t border-green-200 pt-3">
                    <label className="block text-sm font-medium text-brand-dark mb-2">
                      Specifică echilibrele Nash (ex: "(0,1)" sau "(0,0), (1,1)"):
                    </label>
                    <input
                      type="text"
                      value={userAnswers[questionId]?.equilibria || ''}
                      onChange={(e) => handleNashExtendedChange('equilibria', e.target.value)}
                      placeholder="(rând, coloană)"
                      className="w-full border border-brand-neutral/30 rounded-lg px-4 py-3 text-brand-dark 
                                 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    />
                  </div>
                )}
              </div>
            </div>
          )}

          {type === 'csp' && (
            <div>
              <label className="block text-sm font-medium text-brand-dark mb-2">
                Asignează valori pentru fiecare variabilă:
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {(data.raw_data?.variables || []).map((variable) => {
                  const partialAssignment = data.raw_data?.partial_assignment || {};
                  const isPartial = partialAssignment[variable] !== undefined;
                  return (
                    <div key={variable} className="flex items-center gap-2">
                      <span className="font-mono text-brand-dark font-semibold">{variable}:</span>
                      <input
                        type="number"
                        value={
                          isPartial
                            ? partialAssignment[variable]
                            : userAnswers[questionId]?.[variable] ?? ''
                        }
                        onChange={(e) => handleCspAnswerChange(variable, e.target.value)}
                        disabled={isPartial}
                        placeholder="?"
                        className={`flex-1 border border-brand-neutral/30 rounded px-3 py-2 text-brand-dark 
                                   focus:outline-none focus:ring-2 focus:ring-brand-primary
                                   ${isPartial ? 'bg-brand-bg cursor-not-allowed' : ''}`}
                      />
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {type === 'minmax' && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-brand-dark mb-2">
                  Valoarea rădăcinii:
                </label>
                <input
                  type="number"
                  value={userAnswers[questionId]?.root_value || ''}
                  onChange={(e) => handleMinMaxAnswerChange('root_value', e.target.value)}
                  placeholder="ex: 5"
                  className="w-full border border-brand-neutral/30 rounded-lg px-4 py-3 text-brand-dark 
                             focus:outline-none focus:ring-2 focus:ring-brand-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-dark mb-2">
                  Numărul de noduri vizitate:
                </label>
                <input
                  type="number"
                  value={userAnswers[questionId]?.visited_count || ''}
                  onChange={(e) => handleMinMaxAnswerChange('visited_count', e.target.value)}
                  placeholder="ex: 7"
                  className="w-full border border-brand-neutral/30 rounded-lg px-4 py-3 text-brand-dark 
                             focus:outline-none focus:ring-2 focus:ring-brand-primary"
                />
              </div>
            </div>
          )}

          {type === 'strategy' && (
            <div>
              <label className="block text-sm font-medium text-brand-dark mb-2">
                Strategia optimă:
              </label>
              <input
                type="text"
                value={userAnswers[questionId] || ''}
                onChange={(e) => handleAnswerChange(e.target.value)}
                placeholder="ex: Backtracking, BFS, Min-Conflicts..."
                className="w-full border border-brand-neutral/30 rounded-lg px-4 py-3 text-brand-dark 
                           focus:outline-none focus:ring-2 focus:ring-brand-primary"
              />
            </div>
          )}
        </div>
      </div>
    );
  };

  if (!config) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="bg-brand-bg min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-brand-primary border-t-transparent mx-auto mb-4"></div>
          <p className="text-brand-dark text-lg">Se generează întrebările...</p>
        </div>
      </div>
    );
  }

  const progressPercentage = ((currentIndex + 1) / questions.length) * 100;
  const timerPercentage = (timeLeft / (config?.timeLimit || 600)) * 100;

  return (
    <div className="bg-brand-bg min-h-screen py-6 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header with Timer and Progress */}
        <div className="bg-brand-surface rounded-xl shadow-lg p-4 mb-6 border border-brand-neutral/20">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            {/* Timer */}
            <div className="flex items-center gap-3">
              <div className={`text-3xl font-bold font-mono ${getTimerColor()}`}>
                {formatTime(timeLeft)}
              </div>
              <div className="w-24 h-3 bg-brand-bg rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all duration-1000 ${getTimerBgColor()}`}
                  style={{ width: `${timerPercentage}%` }}
                ></div>
              </div>
            </div>

            {/* Question Counter */}
            <div className="text-brand-dark font-semibold">
              Întrebarea{' '}
              <span className="text-brand-primary text-xl">{currentIndex + 1}</span>
              {' '}din{' '}
              <span className="text-brand-hover text-xl">{questions.length}</span>
            </div>

            {/* Submit Button */}
            <button
              onClick={handleSubmitTest}
              disabled={isSubmitting}
              className="bg-brand-hover text-white px-6 py-2 rounded-lg font-semibold 
                         hover:bg-brand-primary transition-all"
            >
              {isSubmitting ? 'Se trimite...' : 'Finalizează'}
            </button>
          </div>

          {/* Progress Bar */}
          <div className="mt-4 h-2 bg-brand-bg rounded-full overflow-hidden">
            <div
              className="h-full bg-brand-secondary transition-all duration-300"
              style={{ width: `${progressPercentage}%` }}
            ></div>
          </div>
        </div>

        {/* Question Navigation Pills */}
        <div className="flex flex-wrap gap-2 mb-6 justify-center">
          {questions.map((q, index) => (
            <button
              key={q.id}
              onClick={() => goToQuestion(index)}
              className={`w-10 h-10 rounded-full font-semibold text-sm transition-all ${
                index === currentIndex
                  ? 'bg-brand-primary text-white scale-110 shadow-lg'
                  : isQuestionAnswered(q.id)
                  ? 'bg-brand-secondary/30 text-brand-hover border-2 border-brand-secondary'
                  : 'bg-brand-surface text-brand-neutral border border-brand-neutral/30 hover:border-brand-primary'
              }`}
            >
              {index + 1}
            </button>
          ))}
        </div>

        {/* Question Card */}
        <div className="bg-brand-surface rounded-xl shadow-lg p-6 border border-brand-neutral/20">
          {/* Question Type Badge */}
          <div className="flex items-center gap-2 mb-4">
            <span className="bg-brand-primary/10 text-brand-hover px-3 py-1 rounded-full text-sm font-semibold">
              {questions[currentIndex]?.type?.toUpperCase()}
            </span>
          </div>

          {/* Question Content */}
          {renderQuestionContent()}

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8 pt-6 border-t border-brand-neutral/20">
            <button
              onClick={goToPrevious}
              disabled={currentIndex === 0}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
                currentIndex === 0
                  ? 'bg-brand-bg text-brand-neutral cursor-not-allowed'
                  : 'bg-brand-bg text-brand-dark hover:bg-brand-neutral/20'
              }`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Precedenta
            </button>

            <button
              onClick={goToNext}
              disabled={currentIndex === questions.length - 1}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
                currentIndex === questions.length - 1
                  ? 'bg-brand-bg text-brand-neutral cursor-not-allowed'
                  : 'bg-brand-primary text-white hover:bg-brand-hover'
              }`}
            >
              Următoarea
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TestActivePage;
