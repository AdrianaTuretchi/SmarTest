import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import MinMaxTree from '../components/MinMaxTree';
import NashMatrix from '../components/NashMatrix';

const PracticePage = () => {
  const [generatedQuestions, setGeneratedQuestions] = useState({
    strategy: null,
    nash: null,
    csp: null,
    minmax: null,
  });
  const [userAnswers, setUserAnswers] = useState({
    strategy: '',
    nash: '',
    nashExtended: {
      hasDominated: null,  // true/false/null
      dominatedP1: [],      // array of row indices
      dominatedP2: [],      // array of col indices
      hasEquilibrium: null, // true/false/null
      equilibriumCoords: '' // string like "(0,1)"
    },
    csp: {},
    minmax: { root_value: '', visited_count: '' },
  });
  const [evaluationResults, setEvaluationResults] = useState({
    strategy: null,
    nash: null,
    csp: null,
    minmax: null,
  });
  const [isLoading, setIsLoading] = useState({});
  const [isSubmitting, setIsSubmitting] = useState({});
  const [validationErrors, setValidationErrors] = useState({
    strategy: null,
    nash: null,
    csp: {},
    minmax: { root_value: null, visited_count: null },
  });

  const handleGenerateClick = async (type) => {
    setIsLoading((prev) => ({ ...prev, [type]: true }));
    // Reset previous evaluation and validation errors when generating new question
    setEvaluationResults((prev) => ({ ...prev, [type]: null }));
    setValidationErrors((prev) => ({
      ...prev,
      [type]: type === 'csp' ? {} : type === 'minmax' ? { root_value: null, visited_count: null } : null,
    }));
    setUserAnswers((prev) => ({
      ...prev,
      [type]: type === 'csp' ? {} : type === 'minmax' ? { root_value: '', visited_count: '' } : '',
      ...(type === 'nash' ? {
        nashExtended: {
          hasDominated: null,
          dominatedP1: [],
          dominatedP2: [],
          hasEquilibrium: null,
          equilibriumCoords: ''
        }
      } : {})
    }));
    try {
      const response = await api.get(`/generate/${type}`);
      setGeneratedQuestions((prev) => ({ ...prev, [type]: response.data }));
    } catch (error) {
      console.error('Error fetching question:', error);
      alert('Failed to generate question. Please try again.');
    } finally {
      setIsLoading((prev) => ({ ...prev, [type]: false }));
    }
  };

  const handleAnswerChange = (type, value) => {
    setUserAnswers((prev) => ({ ...prev, [type]: value }));
    // Clear validation error when user types
    setValidationErrors((prev) => ({ ...prev, [type]: null }));
  };

  const handleCspAnswerChange = (variable, value) => {
    setUserAnswers((prev) => ({
      ...prev,
      csp: { ...prev.csp, [variable]: value === '' ? '' : parseInt(value, 10) },
    }));
    // Clear validation error for this variable when user types
    setValidationErrors((prev) => ({
      ...prev,
      csp: { ...prev.csp, [variable]: null },
    }));
  };

  const handleMinMaxAnswerChange = (field, value) => {
    setUserAnswers((prev) => ({
      ...prev,
      minmax: { ...prev.minmax, [field]: value },
    }));
    // Clear validation error for this field when user types
    setValidationErrors((prev) => ({
      ...prev,
      minmax: { ...prev.minmax, [field]: null },
    }));
  };

  const handleNashExtendedChange = (field, value) => {
    setUserAnswers((prev) => ({
      ...prev,
      nashExtended: { ...prev.nashExtended, [field]: value },
    }));
  };

  const toggleDominatedStrategy = (player, index) => {
    setUserAnswers((prev) => {
      const key = player === 1 ? 'dominatedP1' : 'dominatedP2';
      const current = prev.nashExtended[key];
      const newList = current.includes(index)
        ? current.filter(i => i !== index)
        : [...current, index];
      return {
        ...prev,
        nashExtended: { ...prev.nashExtended, [key]: newList }
      };
    });
  };

  // Validate answers before submission and set inline errors
  const validateAndSetErrors = (type) => {
    const question = generatedQuestions[type];
    if (!question) return false;

    let hasErrors = false;

    switch (type) {
      case 'nash':
        const isNashExtended = question.requires_dominated;
        if (isNashExtended) {
          // Pentru întrebări extinse, verificăm că au răspuns la ambele secțiuni
          if (userAnswers.nashExtended.hasDominated === null) {
            setValidationErrors((prev) => ({ ...prev, nash: 'Răspunde dacă există strategii dominate' }));
            hasErrors = true;
          }
          if (userAnswers.nashExtended.hasEquilibrium === null) {
            setValidationErrors((prev) => ({ ...prev, nash: 'Răspunde dacă există echilibru Nash' }));
            hasErrors = true;
          }
          if (userAnswers.nashExtended.hasEquilibrium === true && 
              (!userAnswers.nashExtended.equilibriumCoords || userAnswers.nashExtended.equilibriumCoords.trim() === '')) {
            setValidationErrors((prev) => ({ ...prev, nash: 'Specifică coordonatele echilibrului' }));
            hasErrors = true;
          }
        } else {
          if (!userAnswers.nash || userAnswers.nash.trim() === '') {
            setValidationErrors((prev) => ({ ...prev, nash: 'Completează acest câmp' }));
            hasErrors = true;
          }
        }
        break;

      case 'csp':
        const variables = question.raw_data?.variables || [];
        const partialAssignment = question.raw_data?.partial_assignment || {};
        const cspErrors = {};
        variables.forEach((v) => {
          if (partialAssignment[v] !== undefined) return;
          const val = userAnswers.csp[v];
          if (val === undefined || val === '' || isNaN(val)) {
            cspErrors[v] = 'Completează';
            hasErrors = true;
          }
        });
        if (hasErrors) {
          setValidationErrors((prev) => ({ ...prev, csp: cspErrors }));
        }
        break;

      case 'minmax':
        const minmaxErrors = { root_value: null, visited_count: null };
        if (userAnswers.minmax.root_value === '' || userAnswers.minmax.root_value === null || isNaN(parseInt(userAnswers.minmax.root_value, 10))) {
          minmaxErrors.root_value = 'Completează acest câmp';
          hasErrors = true;
        }
        if (userAnswers.minmax.visited_count === '' || userAnswers.minmax.visited_count === null || isNaN(parseInt(userAnswers.minmax.visited_count, 10))) {
          minmaxErrors.visited_count = 'Completează acest câmp';
          hasErrors = true;
        }
        if (hasErrors) {
          setValidationErrors((prev) => ({ ...prev, minmax: minmaxErrors }));
        }
        break;

      case 'strategy':
        if (!userAnswers.strategy || userAnswers.strategy.trim() === '') {
          setValidationErrors((prev) => ({ ...prev, strategy: 'Completează acest câmp' }));
          hasErrors = true;
        }
        break;

      default:
        break;
    }

    return !hasErrors;
  };

  const handleSubmit = async (type) => {
    const question = generatedQuestions[type];
    if (!question) return;

    // Validate before submission
    const isValid = validateAndSetErrors(type);
    if (!isValid) {
      return;
    }

    setIsSubmitting((prev) => ({ ...prev, [type]: true }));

    try {
      let payload;

      switch (type) {
        case 'nash':
          const isExtendedNash = question.requires_dominated;
          if (isExtendedNash) {
            // Extended Nash with dominated strategies
            payload = {
              user_answer: userAnswers.nashExtended.equilibriumCoords || '',
              raw_data: question.raw_data,
              has_dominated: userAnswers.nashExtended.hasDominated,
              dominated_p1: userAnswers.nashExtended.dominatedP1,
              dominated_p2: userAnswers.nashExtended.dominatedP2,
              has_equilibrium: userAnswers.nashExtended.hasEquilibrium,
            };
          } else {
            // Standard Nash
            payload = {
              user_answer: userAnswers.nash,
              raw_data: question.raw_data,
            };
          }
          break;

        case 'csp':
          // Filter out empty values and ensure integers
          const cleanedCspAnswer = {};
          Object.entries(userAnswers.csp).forEach(([key, val]) => {
            if (val !== '' && val !== undefined) {
              cleanedCspAnswer[key] = parseInt(val, 10);
            }
          });
          payload = {
            user_answer: cleanedCspAnswer,
            raw_data: question.raw_data,
            template_id: question.template_id,
          };
          break;

        case 'minmax':
          payload = {
            root_value: parseInt(userAnswers.minmax.root_value, 10),
            visited_count: parseInt(userAnswers.minmax.visited_count, 10),
            raw_data: question.raw_data,
          };
          break;

        case 'strategy':
          payload = {
            user_answer: userAnswers.strategy,
            raw_data: question.raw_data,
            template_id: question.template_id,
          };
          break;

        default:
          throw new Error(`Unknown question type: ${type}`);
      }

      const response = await api.post(`/evaluate/${type}`, payload);
      setEvaluationResults((prev) => ({ ...prev, [type]: response.data }));
    } catch (error) {
      console.error('Error submitting answer:', error);
      alert(`Failed to submit answer: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsSubmitting((prev) => ({ ...prev, [type]: false }));
    }
  };

  // Render answer input based on question type
  const renderAnswerInput = (type) => {
    const question = generatedQuestions[type];
    if (!question) return null;

    switch (type) {
      case 'nash':
        const isExtended = question.requires_dominated;
        const numRows = question.raw_data?.length || 0;
        const numCols = question.raw_data?.[0]?.length || 0;
        
        if (isExtended) {
          // Extended Nash question with dominated strategies
          return (
            <div className="mt-4 space-y-6">
              {/* Secțiunea 1: Strategii Dominate */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-semibold text-blue-800 mb-3">1. Strategii Dominate</h4>
                
                {/* Există strategii dominate? */}
                <div className="mb-4">
                  <label className="block text-sm font-medium text-brand-dark mb-2">
                    Există strategii strict dominate?
                  </label>
                  <div className="flex gap-4">
                    <button
                      type="button"
                      onClick={() => handleNashExtendedChange('hasDominated', true)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        userAnswers.nashExtended.hasDominated === true
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
                        userAnswers.nashExtended.hasDominated === false
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      Nu
                    </button>
                  </div>
                </div>

                {/* Selectare strategii dominate (doar dacă a zis Da) */}
                {userAnswers.nashExtended.hasDominated === true && (
                  <div className="space-y-3 border-t border-blue-200 pt-3">
                    <p className="text-sm text-blue-700">Selectează strategiile dominate:</p>
                    
                    {/* Jucător 1 (rânduri) */}
                    <div>
                      <label className="block text-sm font-medium text-brand-dark mb-1">
                        Jucător 1 (rânduri dominate):
                      </label>
                      <div className="flex gap-2 flex-wrap">
                        {Array.from({ length: numRows }, (_, i) => (
                          <button
                            key={`p1-${i}`}
                            type="button"
                            onClick={() => toggleDominatedStrategy(1, i)}
                            className={`px-3 py-1 rounded-full text-sm font-mono transition-colors ${
                              userAnswers.nashExtended.dominatedP1.includes(i)
                                ? 'bg-red-500 text-white'
                                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                            }`}
                          >
                            S{i + 1} (rând {i})
                          </button>
                        ))}
                      </div>
                    </div>
                    
                    {/* Jucător 2 (coloane) */}
                    <div>
                      <label className="block text-sm font-medium text-brand-dark mb-1">
                        Jucător 2 (coloane dominate):
                      </label>
                      <div className="flex gap-2 flex-wrap">
                        {Array.from({ length: numCols }, (_, i) => (
                          <button
                            key={`p2-${i}`}
                            type="button"
                            onClick={() => toggleDominatedStrategy(2, i)}
                            className={`px-3 py-1 rounded-full text-sm font-mono transition-colors ${
                              userAnswers.nashExtended.dominatedP2.includes(i)
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
                
                {/* Există echilibru? */}
                <div className="mb-4">
                  <label className="block text-sm font-medium text-brand-dark mb-2">
                    Există echilibru Nash pur?
                  </label>
                  <div className="flex gap-4">
                    <button
                      type="button"
                      onClick={() => handleNashExtendedChange('hasEquilibrium', true)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        userAnswers.nashExtended.hasEquilibrium === true
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
                        userAnswers.nashExtended.hasEquilibrium === false
                          ? 'bg-green-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      Nu
                    </button>
                  </div>
                </div>

                {/* Input pentru coordonate (doar dacă a zis Da) */}
                {userAnswers.nashExtended.hasEquilibrium === true && (
                  <div className="border-t border-green-200 pt-3">
                    <label className="block text-sm font-medium text-brand-dark mb-2">
                      Coordonatele echilibrului (ex: "(0,1)" sau "(0,0), (1,1)"):
                    </label>
                    <input
                      type="text"
                      value={userAnswers.nashExtended.equilibriumCoords}
                      onChange={(e) => handleNashExtendedChange('equilibriumCoords', e.target.value)}
                      placeholder="(rând, coloană)"
                      className="w-full border border-brand-neutral/30 rounded px-3 py-2 text-brand-dark focus:outline-none focus:ring-2 focus:ring-brand-primary"
                    />
                  </div>
                )}
              </div>
            </div>
          );
        } else {
          // Standard Nash question (just equilibrium)
          return (
            <div className="mt-4">
              <label className="block text-sm font-medium text-brand-dark mb-2">
                Răspunsul tău (ex: "(0,1)" sau "(0,0), (1,1)" pentru echilibre multiple):
              </label>
              <input
                type="text"
                value={userAnswers.nash}
                onChange={(e) => handleAnswerChange('nash', e.target.value)}
                placeholder="(rând, coloană)"
                className={`w-full border rounded px-3 py-2 text-brand-dark focus:outline-none focus:ring-2 focus:ring-brand-primary ${
                  validationErrors.nash ? 'border-red-500' : 'border-brand-neutral/30'
                }`}
              />
              {validationErrors.nash && (
                <p className="text-red-500 text-sm mt-1">{validationErrors.nash}</p>
              )}
            </div>
          );
        }

      case 'csp':
        const variables = question.raw_data?.variables || [];
        const partialAssignment = question.raw_data?.partial_assignment || {};
        return (
          <div className="mt-4">
            <label className="block text-sm font-medium text-brand-dark mb-2">
              Asignează valori pentru fiecare variabilă:
            </label>
            <div className="grid grid-cols-2 gap-2">
              {variables.map((variable) => {
                const isPartial = partialAssignment[variable] !== undefined;
                const hasError = validationErrors.csp?.[variable];
                return (
                  <div key={variable} className="flex flex-col">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-brand-dark">{variable}:</span>
                      <input
                        type="number"
                        value={isPartial ? partialAssignment[variable] : (userAnswers.csp[variable] ?? '')}
                        onChange={(e) => handleCspAnswerChange(variable, e.target.value)}
                        placeholder="valoare"
                        disabled={isPartial}
                        className={`flex-1 border rounded px-2 py-1 text-brand-dark focus:outline-none focus:ring-2 focus:ring-brand-primary ${
                          hasError ? 'border-red-500' : 'border-brand-neutral/30'
                        } ${isPartial ? 'bg-gray-100 cursor-not-allowed' : ''}`}
                      />
                    </div>
                    {hasError && (
                      <p className="text-red-500 text-xs mt-0.5 ml-8">{hasError}</p>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        );

      case 'minmax':
        return (
          <div className="mt-4 space-y-3">
            <div>
              <label className="block text-sm font-medium text-brand-dark mb-1">
                Valoarea rădăcinii (root value):
              </label>
              <input
                type="number"
                value={userAnswers.minmax.root_value}
                onChange={(e) => handleMinMaxAnswerChange('root_value', e.target.value)}
                placeholder="ex: 5"
                className={`w-full border rounded px-3 py-2 text-brand-dark focus:outline-none focus:ring-2 focus:ring-brand-primary ${
                  validationErrors.minmax?.root_value ? 'border-red-500' : 'border-brand-neutral/30'
                }`}
              />
              {validationErrors.minmax?.root_value && (
                <p className="text-red-500 text-sm mt-1">{validationErrors.minmax.root_value}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-brand-dark mb-1">
                Numărul de noduri vizitate:
              </label>
              <input
                type="number"
                value={userAnswers.minmax.visited_count}
                onChange={(e) => handleMinMaxAnswerChange('visited_count', e.target.value)}
                placeholder="ex: 7"
                className={`w-full border rounded px-3 py-2 text-brand-dark focus:outline-none focus:ring-2 focus:ring-brand-primary ${
                  validationErrors.minmax?.visited_count ? 'border-red-500' : 'border-brand-neutral/30'
                }`}
              />
              {validationErrors.minmax?.visited_count && (
                <p className="text-red-500 text-sm mt-1">{validationErrors.minmax.visited_count}</p>
              )}
            </div>
          </div>
        );

      case 'strategy':
        return (
          <div className="mt-4">
            <label className="block text-sm font-medium text-brand-dark mb-2">
              Alege strategia optimă (ex: "Backtracking", "Hill Climbing", "BFS", "DFS", "Min-Conflicts"):
            </label>
            <input
              type="text"
              value={userAnswers.strategy}
              onChange={(e) => handleAnswerChange('strategy', e.target.value)}
              placeholder="Numele strategiei"
              className={`w-full border rounded px-3 py-2 text-brand-dark focus:outline-none focus:ring-2 focus:ring-brand-primary ${
                validationErrors.strategy ? 'border-red-500' : 'border-brand-neutral/30'
              }`}
            />
            {validationErrors.strategy && (
              <p className="text-red-500 text-sm mt-1">{validationErrors.strategy}</p>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  // Render evaluation result
  const renderEvaluationResult = (type) => {
    const result = evaluationResults[type];
    if (!result) return null;

    const isCorrect = result.score >= 1.0;
    const isPartial = result.score > 0 && result.score < 1.0;

    return (
      <div
        className={`mt-4 p-4 rounded border-l-4 ${
          isCorrect
            ? 'bg-green-50 border-green-500'
            : isPartial
            ? 'bg-yellow-50 border-yellow-500'
            : 'bg-red-50 border-red-500'
        }`}
      >
        <div className="flex items-center gap-2 mb-2">
          <span
            className={`text-lg font-bold ${
              isCorrect ? 'text-green-700' : isPartial ? 'text-yellow-700' : 'text-red-700'
            }`}
          >
            {isCorrect ? '✓ Corect!' : isPartial ? '~ Parțial corect' : '✗ Incorect'}
          </span>
          <span className="text-sm text-brand-neutral">
            (Scor: {(result.score * 100).toFixed(0)}%)
          </span>
        </div>

        {/* Type-specific correct answers */}
        {type === 'nash' && (
          <div className="space-y-2">
            {/* Strategii dominate (dacă sunt returnate) */}
            {(result.correct_dominated_p1 !== undefined || result.correct_dominated_p2 !== undefined) && (
              <p className="text-sm text-brand-dark">
                <strong>Strategii dominate:</strong>{' '}
                {(result.correct_dominated_p1?.length > 0 || result.correct_dominated_p2?.length > 0) ? (
                  <>
                    {result.correct_dominated_p1?.length > 0 && (
                      <span className="text-blue-600">
                        J1: {result.correct_dominated_p1.map(i => `S${i+1}`).join(', ')}
                      </span>
                    )}
                    {result.correct_dominated_p1?.length > 0 && result.correct_dominated_p2?.length > 0 && ' | '}
                    {result.correct_dominated_p2?.length > 0 && (
                      <span className="text-red-600">
                        J2: {result.correct_dominated_p2.map(i => `S${i+1}`).join(', ')}
                      </span>
                    )}
                  </>
                ) : (
                  'Nu există strategii dominate'
                )}
              </p>
            )}
            
            {/* Echilibre Nash */}
            {result.correct_coords && (
              <p className="text-sm text-brand-dark">
                <strong>Echilibre Nash:</strong>{' '}
                {result.correct_coords.length > 0
                  ? result.correct_coords.map((c) => `(${c[0]}, ${c[1]})`).join(', ')
                  : 'Nu există echilibre pure'}
              </p>
            )}
          </div>
        )}

        {type === 'csp' && result.correct_assignment && (
          <p className="text-sm text-brand-dark mb-2">
            <strong>Soluția corectă:</strong>{' '}
            {Object.entries(result.correct_assignment)
              .map(([k, v]) => `${k}=${v}`)
              .join(', ')}
          </p>
        )}

        {type === 'minmax' && (
          <p className="text-sm text-brand-dark mb-2">
            <strong>Valori corecte:</strong> Rădăcină = {result.correct_root_value}, Noduri vizitate ={' '}
            {result.correct_visited_count}
          </p>
        )}

        {result.feedback_text && (
          <div className="mt-2 text-sm text-brand-dark">
            <strong>Feedback:</strong>
            <p className="mt-1 whitespace-pre-wrap">{result.feedback_text}</p>
          </div>
        )}
      </div>
    );
  };

  const questionTypeLabels = {
    strategy: 'Strategy Selection',
    nash: 'Nash Equilibrium',
    csp: 'CSP (Constraint Satisfaction)',
    minmax: 'MinMax / Alpha-Beta',
  };

  return (
    <div className="bg-brand-bg min-h-screen py-10 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Back to Home Button */}
        <Link
          to="/"
          className="inline-flex items-center text-brand-primary hover:text-brand-hover transition-colors mb-6"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Înapoi la Home
        </Link>
        
        <h1 className="text-5xl md:text-6xl font-bold text-center mb-10">
          <span className="text-brand-primary">Practice</span>{' '}
          <span className="text-brand-hover">Area</span>
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {['strategy', 'nash', 'csp', 'minmax'].map((type) => (
            <div
              key={type}
              className="bg-brand-surface rounded-lg border border-brand-neutral/20 shadow-md p-6 hover:shadow-lg hover:shadow-brand-secondary/20 transition-shadow"
            >
              <h2 className="text-xl font-semibold mb-4 text-brand-hover">
                {questionTypeLabels[type]}
              </h2>
              <p className="text-sm text-brand-neutral mb-6">
                Exersează rezolvarea problemelor de tip {type}.
              </p>
              <button
                onClick={() => handleGenerateClick(type)}
                className="bg-brand-primary text-white rounded px-4 py-2 font-semibold hover:bg-brand-hover transition-all"
                disabled={isLoading[type]}
              >
                {isLoading[type] ? 'Se încarcă...' : 'Generează Întrebare'}
              </button>

              {generatedQuestions[type] && (
                <div className="mt-4 bg-brand-secondary/10 p-4 rounded border-l-4 border-brand-primary">
                  <h3 className="text-lg font-bold mb-2 text-brand-dark">Întrebare:</h3>
                  
                  {/* For MinMax, show tree visualization separately */}
                  {type === 'minmax' ? (
                    <>
                      <p className="text-sm text-brand-dark mb-4">
                        Pentru arborele de joc generat mai jos, aplicați strategia MIN-MAX.
                        Determinați valoarea rădăcinii și numărul de noduri vizitate.
                      </p>
                      <MinMaxTree treeData={generatedQuestions[type].raw_data} />
                    </>
                  ) : type === 'nash' && generatedQuestions[type].raw_data ? (
                    <>
                      <p className="text-sm text-brand-dark mb-4 whitespace-pre-wrap">
                        {generatedQuestions[type].question_text}
                      </p>
                      <NashMatrix matrixData={generatedQuestions[type].raw_data} />
                    </>
                  ) : (
                    <p className="text-sm text-brand-dark whitespace-pre-wrap mb-4">
                      {generatedQuestions[type].question_text}
                    </p>
                  )}

                  {/* Answer input section */}
                  {renderAnswerInput(type)}

                  {/* Submit button */}
                  {!evaluationResults[type] && (
                    <button
                      onClick={() => handleSubmit(type)}
                      className="mt-4 bg-brand-hover text-white rounded px-4 py-2 font-semibold hover:bg-brand-primary transition-all"
                      disabled={isSubmitting[type]}
                    >
                      {isSubmitting[type] ? 'Se evaluează...' : 'Trimite Răspunsul'}
                    </button>
                  )}

                  {/* Evaluation result */}
                  {renderEvaluationResult(type)}

                  {/* Try again button after evaluation */}
                  {evaluationResults[type] && (
                    <button
                      onClick={() => handleGenerateClick(type)}
                      className="mt-4 bg-brand-neutral text-white rounded px-4 py-2 font-semibold hover:bg-brand-dark transition-all"
                    >
                      Încearcă altă întrebare
                    </button>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PracticePage;