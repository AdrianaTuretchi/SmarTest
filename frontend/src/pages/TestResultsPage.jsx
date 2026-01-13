import React, { useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import MinMaxTree from '../components/MinMaxTree';
import NashMatrix from '../components/NashMatrix';

const TestResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const data = location.state;

  const [expandedQuestion, setExpandedQuestion] = useState(null);

  // Redirect if no data
  if (!data) {
    return (
      <div className="bg-brand-bg min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-brand-dark text-lg mb-4">Nu există rezultate de afișat.</p>
          <Link
            to="/tests"
            className="text-brand-primary hover:text-brand-hover font-semibold"
          >
            Începe un test nou
          </Link>
        </div>
      </div>
    );
  }

  const { results, totalTime, totalQuestions } = data;

  // Calculate scores
  const totalScore = results.reduce((sum, r) => sum + (r.result?.score || 0), 0);
  const percentage = Math.round((totalScore / totalQuestions) * 100);

  // Group results by type
  const scoresByType = {};
  results.forEach((r) => {
    const type = r.question.type;
    if (!scoresByType[type]) {
      scoresByType[type] = { correct: 0, total: 0 };
    }
    scoresByType[type].total++;
    if (r.result?.score > 0) {
      scoresByType[type].correct++;
    }
  });

  // Format time
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  };

  // Get grade color
  const getGradeColor = () => {
    if (percentage >= 80) return 'text-brand-primary';
    if (percentage >= 60) return 'text-brand-secondary';
    if (percentage >= 40) return 'text-yellow-500';
    return 'text-red-500';
  };

  // Get grade background
  const getGradeBg = () => {
    if (percentage >= 80) return 'bg-brand-primary';
    if (percentage >= 60) return 'bg-brand-secondary';
    if (percentage >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const typeLabels = {
    nash: 'Nash Equilibrium',
    csp: 'CSP',
    minmax: 'MinMax',
    strategy: 'Strategy',
  };

  const toggleQuestion = (index) => {
    setExpandedQuestion(expandedQuestion === index ? null : index);
  };

  // Format user answer for display
  const formatUserAnswer = (question, answer) => {
    if (!answer) return 'Necompletat';

    if (question.type === 'nash') {
      // Check if it's extended Nash (object with hasDominated, etc.)
      if (typeof answer === 'object' && answer !== null) {
        const parts = [];
        
        if (answer.hasDominated !== null && answer.hasDominated !== undefined) {
          parts.push(`Strategii dominate: ${answer.hasDominated ? 'Da' : 'Nu'}`);
          if (answer.hasDominated) {
            if (answer.dominatedP1?.length > 0) {
              parts.push(`P1: rândurile ${answer.dominatedP1.join(', ')}`);
            }
            if (answer.dominatedP2?.length > 0) {
              parts.push(`P2: coloanele ${answer.dominatedP2.join(', ')}`);
            }
          }
        }
        
        if (answer.hasEquilibrium !== null && answer.hasEquilibrium !== undefined) {
          parts.push(`Echilibru Nash: ${answer.hasEquilibrium ? 'Da' : 'Nu'}`);
          if (answer.hasEquilibrium && answer.equilibria) {
            parts.push(`Coordonate: ${answer.equilibria}`);
          }
        }
        
        return parts.length > 0 ? parts.join('; ') : 'Necompletat';
      }
      // Simple string answer
      return answer || 'Necompletat';
    }

    if (question.type === 'csp') {
      if (Object.keys(answer).length === 0) return 'Necompletat';
      return Object.entries(answer)
        .filter(([_, v]) => v !== '' && v !== undefined)
        .map(([k, v]) => `${k}=${v}`)
        .join(', ') || 'Necompletat';
    }

    if (question.type === 'minmax') {
      if (!answer.root_value && !answer.visited_count) return 'Necompletat';
      return `Rădăcină: ${answer.root_value || '?'}, Vizitate: ${answer.visited_count || '?'}`;
    }

    return answer || 'Necompletat';
  };

  // Format correct answer
  const formatCorrectAnswer = (question, result) => {
    if (question.type === 'nash') {
      const parts = [];
      
      // Afișăm strategii dominate DOAR dacă întrebarea le cere
      if (question.data.requires_dominated) {
        const hasP1 = result.correct_dominated_p1?.length > 0;
        const hasP2 = result.correct_dominated_p2?.length > 0;
        
        if (hasP1 || hasP2) {
          let domText = 'Strategii dominate: ';
          if (hasP1) domText += `P1: rândurile ${result.correct_dominated_p1.join(', ')}`;
          if (hasP1 && hasP2) domText += '; ';
          if (hasP2) domText += `P2: coloanele ${result.correct_dominated_p2.join(', ')}`;
          parts.push(domText);
        } else {
          parts.push('Nu există strategii dominate');
        }
      }
      
      // Afișăm echilibrele Nash
      const coords = result.correct_coords;
      if (!coords || coords.length === 0) {
        parts.push('Nu există echilibre pure');
      } else {
        parts.push(`Echilibre Nash: ${coords.map((c) => `(${c[0]}, ${c[1]})`).join(', ')}`);
      }
      
      return parts.join('; ');
    }

    if (question.type === 'csp') {
      const assignment = result.correct_assignment;
      if (!assignment || Object.keys(assignment).length === 0) return 'Inconsistent';
      return Object.entries(assignment)
        .map(([k, v]) => `${k}=${v}`)
        .join(', ');
    }

    if (question.type === 'minmax') {
      return `Rădăcină: ${result.correct_root_value}, Vizitate: ${result.correct_visited_count}`;
    }

    if (question.type === 'strategy') {
      return result.correct_answer || 'Verifică feedback-ul';
    }

    return 'Verifică feedback-ul';
  };

  return (
    <div className="bg-brand-bg min-h-screen py-10 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            <span className="text-brand-primary">Rezultate</span>{' '}
            <span className="text-brand-hover">Test</span>
          </h1>
        </div>

        {/* Score Card */}
        <div className="bg-brand-surface rounded-xl shadow-lg p-8 mb-8 border border-brand-neutral/20">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            {/* Main Score */}
            <div className="text-center md:text-left">
              <div className={`text-7xl font-bold ${getGradeColor()}`}>
                {percentage}%
              </div>
              <p className="text-brand-neutral text-lg mt-2">
                {totalScore} din {totalQuestions} corecte
              </p>
            </div>

            {/* Score Ring */}
            <div className="relative w-32 h-32">
              <svg className="w-full h-full transform -rotate-90">
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="currentColor"
                  strokeWidth="12"
                  fill="none"
                  className="text-brand-bg"
                />
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="currentColor"
                  strokeWidth="12"
                  fill="none"
                  strokeDasharray={`${percentage * 3.52} 352`}
                  strokeLinecap="round"
                  className={getGradeColor()}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className={`text-2xl font-bold ${getGradeColor()}`}>
                  {totalScore}/{totalQuestions}
                </span>
              </div>
            </div>

            {/* Stats */}
            <div className="text-center md:text-right">
              <div className="text-brand-dark">
                <span className="text-2xl font-bold text-brand-hover">{formatTime(totalTime)}</span>
                <p className="text-brand-neutral">Timp utilizat</p>
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mt-6 h-4 bg-brand-bg rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-1000 ${getGradeBg()}`}
              style={{ width: `${percentage}%` }}
            ></div>
          </div>
        </div>

        {/* Breakdown by Type */}
        <div className="bg-brand-surface rounded-xl shadow-lg p-6 mb-8 border border-brand-neutral/20">
          <h2 className="text-xl font-bold text-brand-dark mb-4">Rezultate pe categorii</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(scoresByType).map(([type, scores]) => {
              const typePercentage = Math.round((scores.correct / scores.total) * 100);
              return (
                <div
                  key={type}
                  className="bg-brand-bg rounded-lg p-4 text-center"
                >
                  <p className="text-sm text-brand-neutral mb-1">{typeLabels[type]}</p>
                  <p className="text-2xl font-bold text-brand-dark">
                    {scores.correct}/{scores.total}
                  </p>
                  <div className="mt-2 h-2 bg-brand-neutral/20 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${typePercentage >= 50 ? 'bg-brand-primary' : 'bg-red-500'}`}
                      style={{ width: `${typePercentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Detailed Results */}
        <div className="bg-brand-surface rounded-xl shadow-lg p-6 mb-8 border border-brand-neutral/20">
          <h2 className="text-xl font-bold text-brand-dark mb-4">Detalii întrebări</h2>
          <div className="space-y-3">
            {results.map((r, index) => {
              const isCorrect = r.result?.score > 0;
              const isExpanded = expandedQuestion === index;

              return (
                <div
                  key={index}
                  className={`rounded-lg border-2 overflow-hidden transition-all ${
                    isCorrect ? 'border-brand-primary/30' : 'border-red-300'
                  }`}
                >
                  {/* Question Header */}
                  <button
                    onClick={() => toggleQuestion(index)}
                    className={`w-full p-4 flex items-center justify-between text-left transition-all ${
                      isCorrect ? 'bg-brand-primary/10' : 'bg-red-50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                          isCorrect ? 'bg-brand-primary' : 'bg-red-500'
                        }`}
                      >
                        {isCorrect ? '✓' : '✗'}
                      </div>
                      <div>
                        <span className="font-semibold text-brand-dark">
                          Întrebarea {index + 1}
                        </span>
                        <span className="ml-2 text-sm text-brand-neutral">
                          ({typeLabels[r.question.type]})
                        </span>
                      </div>
                    </div>
                    <svg
                      className={`w-5 h-5 text-brand-neutral transition-transform ${
                        isExpanded ? 'rotate-180' : ''
                      }`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </button>

                  {/* Expanded Content */}
                  {isExpanded && (
                    <div className="p-4 bg-brand-surface border-t border-brand-neutral/20">
                      {/* Question Preview */}
                      <div className="mb-4">
                        <p className="text-sm font-semibold text-brand-neutral mb-2">Întrebare:</p>
                        {r.question.type === 'minmax' ? (
                          <div className="bg-brand-bg p-3 rounded-lg">
                            <p className="text-sm text-brand-dark mb-2">
                              Aplicați strategia MIN-MAX pentru arborele de mai jos.
                            </p>
                            <MinMaxTree treeData={r.question.data.raw_data} />
                          </div>
                        ) : r.question.type === 'nash' && r.question.data.raw_data ? (
                          <div className="bg-brand-bg p-3 rounded-lg">
                            <p className="text-sm text-brand-dark mb-3">
                              {r.question.data.requires_dominated 
                                ? "Pentru jocul de mai jos, identificați dacă există strategii strict dominate și echilibrele Nash pure."
                                : "Pentru jocul de mai jos, identificați echilibrele Nash pure (dacă există)."
                              }
                            </p>
                            <NashMatrix matrixData={r.question.data.raw_data} />
                          </div>
                        ) : (
                          <p className="text-sm text-brand-dark bg-brand-bg p-3 rounded-lg whitespace-pre-wrap">
                            {r.question.data.question_text}
                          </p>
                        )}
                      </div>

                      {/* Answers Comparison */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div className={`p-3 rounded-lg ${isCorrect ? 'bg-brand-primary/10' : 'bg-red-50'}`}>
                          <p className="text-sm font-semibold text-brand-neutral mb-1">Răspunsul tău:</p>
                          <p className={`font-medium ${isCorrect ? 'text-brand-primary' : 'text-red-600'}`}>
                            {formatUserAnswer(r.question, r.userAnswer)}
                          </p>
                        </div>
                        <div className="p-3 rounded-lg bg-brand-secondary/10">
                          <p className="text-sm font-semibold text-brand-neutral mb-1">Răspunsul corect:</p>
                          <p className="font-medium text-brand-hover">
                            {formatCorrectAnswer(r.question, r.result)}
                          </p>
                        </div>
                      </div>

                      {/* Feedback */}
                      {r.result?.feedback_text && (
                        <div className="bg-brand-bg p-4 rounded-lg">
                          <p className="text-sm font-semibold text-brand-neutral mb-2">Feedback:</p>
                          <p className="text-sm text-brand-dark whitespace-pre-wrap">
                            {r.result.feedback_text}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/tests"
            className="bg-brand-primary text-white px-8 py-4 rounded-lg text-lg font-semibold 
                       hover:bg-brand-hover transition-all shadow-lg text-center"
          >
            Test Nou
          </Link>
          <Link
            to="/"
            className="bg-brand-surface text-brand-dark px-8 py-4 rounded-lg text-lg font-semibold 
                       border-2 border-brand-neutral/30 hover:border-brand-primary transition-all text-center"
          >
            Înapoi la Home
          </Link>
        </div>
      </div>
    </div>
  );
};

export default TestResultsPage;
