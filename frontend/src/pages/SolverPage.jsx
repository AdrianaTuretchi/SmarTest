import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import NashMatrix from '../components/NashMatrix';

const SolverPage = () => {
  const [questionText, setQuestionText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSolve = async () => {
    if (!questionText.trim()) {
      setError('Te rugăm să introduci textul întrebării.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8001/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question_text: questionText }),
      });

      if (!response.ok) {
        throw new Error('Eroare la server');
      }

      const data = await response.json();
      setResult(data);

      if (data.error_message) {
        setError(data.error_message);
      }
    } catch (err) {
      setError('Nu am putut comunica cu serverul. Verifică dacă backend-ul rulează.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuestionText('');
    setResult(null);
    setError(null);
  };

  const getTypeLabel = (type) => {
    const labels = {
      nash: 'Nash Equilibrium',
      csp: 'CSP (Constraint Satisfaction)',
      strategy: 'Selecție Strategie',
      minmax: 'MinMax',
      unknown: 'Necunoscut',
    };
    return labels[type] || type;
  };

  const getTypeColor = (type) => {
    const colors = {
      nash: 'bg-blue-100 text-blue-800 border-blue-300',
      csp: 'bg-purple-100 text-purple-800 border-purple-300',
      strategy: 'bg-orange-100 text-orange-800 border-orange-300',
      minmax: 'bg-cyan-100 text-cyan-800 border-cyan-300',
      unknown: 'bg-gray-100 text-gray-800 border-gray-300',
    };
    return colors[type] || colors.unknown;
  };

  const renderSolution = () => {
    if (!result || !result.solution) return null;

    const { detected_type, solution, extracted_data } = result;

    if (detected_type === 'nash') {
      return (
        <div className="space-y-4">
          {/* Matrice vizualizată */}
          {extracted_data.raw_data && (
            <div>
              <h4 className="font-semibold text-brand-dark mb-2">Matricea extrasă:</h4>
              <NashMatrix matrixData={extracted_data.raw_data} />
            </div>
          )}

          {/* Strategii Dominate (dacă sunt în soluție) */}
          {solution.dominated !== undefined && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-800 mb-2">Strategii Dominate:</h4>
              {solution.has_dominated ? (
                <div className="space-y-2">
                  {solution.dominated.player1?.length > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="text-blue-700 font-medium">Jucător 1 (rânduri):</span>
                      <div className="flex flex-wrap gap-1">
                        {solution.dominated.player1.map((idx) => (
                          <span key={`p1-${idx}`} className="bg-red-200 text-red-800 px-2 py-0.5 rounded font-mono text-sm">
                            S{idx + 1} (rând {idx})
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {solution.dominated.player2?.length > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="text-blue-700 font-medium">Jucător 2 (coloane):</span>
                      <div className="flex flex-wrap gap-1">
                        {solution.dominated.player2.map((idx) => (
                          <span key={`p2-${idx}`} className="bg-red-200 text-red-800 px-2 py-0.5 rounded font-mono text-sm">
                            S{idx + 1} (col {idx})
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {!solution.dominated.player1?.length && !solution.dominated.player2?.length && (
                    <p className="text-blue-700">Nu există strategii strict dominate.</p>
                  )}
                </div>
              ) : (
                <p className="text-blue-700">Nu există strategii strict dominate în această matrice.</p>
              )}
            </div>
          )}

          {/* Echilibre */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-semibold text-green-800 mb-2">Echilibre Nash găsite:</h4>
            {solution.equilibria && solution.equilibria.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {solution.equilibria.map((eq, idx) => (
                  <span
                    key={idx}
                    className="bg-green-200 text-green-900 px-3 py-1 rounded-full font-mono"
                  >
                    ({eq[0]}, {eq[1]})
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-green-700">Nu există echilibre Nash pure.</p>
            )}
          </div>
        </div>
      );
    }

    if (detected_type === 'csp') {
      return (
        <div className="space-y-4">
          {/* Variabile și domenii */}
          {extracted_data.variables && (
            <div>
              <h4 className="font-semibold text-brand-dark mb-2">Date extrase:</h4>
              <div className="bg-gray-50 rounded-lg p-3 font-mono text-sm">
                <p><strong>Variabile:</strong> {extracted_data.variables.join(', ')}</p>
                {extracted_data.domain_size && (
                  <p><strong>Domeniu:</strong> {extracted_data.domain_size} valori</p>
                )}
                {extracted_data.constraints && (
                  <p><strong>Constrângeri:</strong> {extracted_data.constraints.map(c => c.join('≠')).join(', ')}</p>
                )}
              </div>
            </div>
          )}

          {/* Soluție */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-semibold text-green-800 mb-2">Soluție găsită:</h4>
            {solution.assignment ? (
              <div className="flex flex-wrap gap-2">
                {Object.entries(solution.assignment).map(([variable, value]) => (
                  <span
                    key={variable}
                    className="bg-green-200 text-green-900 px-3 py-1 rounded-lg font-mono"
                  >
                    {variable} = {value}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-red-600">Problema nu are soluție.</p>
            )}
            {solution.method && (
              <p className="text-sm text-green-700 mt-2">Metodă: {solution.method}</p>
            )}
          </div>
        </div>
      );
    }

    if (detected_type === 'strategy') {
      return (
        <div className="space-y-4">
          {/* Tipul problemei */}
          {extracted_data.problem_type && (
            <div>
              <h4 className="font-semibold text-brand-dark mb-2">Problemă detectată:</h4>
              <div className="bg-gray-50 rounded-lg p-3">
                <p><strong>Tip:</strong> {extracted_data.problem_type}</p>
                {extracted_data.n && <p><strong>N:</strong> {extracted_data.n}</p>}
                {extracted_data.num_nodes && <p><strong>Noduri:</strong> {extracted_data.num_nodes}</p>}
                {extracted_data.is_tree !== undefined && (
                  <p><strong>Este arbore:</strong> {extracted_data.is_tree ? 'Da' : 'Nu'}</p>
                )}
              </div>
            </div>
          )}

          {/* Strategie recomandată */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-semibold text-green-800 mb-2">Strategie recomandată:</h4>
            <p className="text-xl font-bold text-green-900">{solution.recommended_strategy}</p>
          </div>
        </div>
      );
    }

    if (detected_type === 'minmax') {
      return (
        <div className="space-y-4">
          {/* Informații arbore */}
          {extracted_data.tree_depth !== undefined && (
            <div>
              <h4 className="font-semibold text-brand-dark mb-2">Arbore detectat:</h4>
              <div className="bg-gray-50 rounded-lg p-3">
                <p><strong>Adâncime:</strong> {extracted_data.tree_depth} niveluri</p>
              </div>
            </div>
          )}

          {/* Rezultat MinMax */}
          <div className="bg-cyan-50 border border-cyan-200 rounded-lg p-4">
            <h4 className="font-semibold text-cyan-800 mb-3">Rezultat MinMax cu Alpha-Beta:</h4>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-cyan-700 font-medium">Valoarea rădăcinii:</span>
                <span className="bg-cyan-200 text-cyan-900 px-3 py-1 rounded-full font-bold text-lg">
                  {solution.root_value}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-cyan-700 font-medium">Noduri frunză vizitate:</span>
                <span className="bg-cyan-200 text-cyan-900 px-3 py-1 rounded-full font-bold">
                  {solution.visited_count}
                </span>
              </div>
              {solution.visited_nodes && (
                <div className="mt-2">
                  <span className="text-cyan-700 font-medium">Ordinea vizitării:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {solution.visited_nodes.map((val, idx) => (
                      <span
                        key={idx}
                        className="bg-cyan-100 text-cyan-800 px-2 py-0.5 rounded text-sm font-mono"
                      >
                        {val}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="bg-gray-50 rounded-lg p-4">
        <pre className="text-sm overflow-x-auto">{JSON.stringify(solution, null, 2)}</pre>
      </div>
    );
  };

  return (
    <div className="bg-brand-bg min-h-screen py-10 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Link
            to="/"
            className="inline-flex items-center text-brand-primary hover:text-brand-hover transition-colors mb-6"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Înapoi la Home
          </Link>
        </div>

        {/* Title */}
        <div className="text-center mb-10">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            <span className="text-brand-primary">Solver</span>{' '}
            <span className="text-brand-hover">Automat</span>
          </h1>
          <p className="text-brand-neutral text-lg max-w-2xl mx-auto">
            Introdu o întrebare și sistemul va detecta automat tipul, va extrage datele și va calcula răspunsul corect.
          </p>
        </div>

        {/* Input Area */}
        <div className="bg-brand-surface rounded-xl shadow-lg p-6 mb-6 border border-brand-neutral/20">
          <label className="block text-brand-dark font-semibold mb-3">
            Textul întrebării:
          </label>
          <textarea
            value={questionText}
            onChange={(e) => setQuestionText(e.target.value)}
            placeholder={`Exemplu:\n\n"Găsiți echilibrele Nash pentru matricea:\n   (3,2) (1,4)\n   (2,1) (4,3)"\n\nsau\n\n"Pentru problema N-Queens cu N=100, care este cea mai potrivită strategie?"`}
            className="w-full h-48 px-4 py-3 border border-brand-neutral/30 rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-brand-primary resize-none font-mono text-sm"
          />

          <div className="flex gap-4 mt-4">
            <button
              onClick={handleSolve}
              disabled={loading || !questionText.trim()}
              className={`flex-1 py-3 px-6 rounded-lg font-semibold text-white transition-colors ${
                loading || !questionText.trim()
                  ? 'bg-brand-neutral cursor-not-allowed'
                  : 'bg-brand-primary hover:bg-brand-hover'
              }`}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Analizez...
                </span>
              ) : (
                'Analizează și Rezolvă'
              )}
            </button>
            <button
              onClick={handleClear}
              className="py-3 px-6 rounded-lg font-semibold border border-brand-neutral/30 text-brand-neutral hover:bg-brand-neutral/10 transition-colors"
            >
              Șterge
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
            <div className="flex items-start gap-3">
              <svg className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="bg-brand-surface rounded-xl shadow-lg p-6 border border-brand-neutral/20">
            {/* Detection Info */}
            <div className="flex items-center gap-4 mb-6 pb-4 border-b border-brand-neutral/20">
              <div className={`px-4 py-2 rounded-lg border ${getTypeColor(result.detected_type)}`}>
                <span className="font-semibold">{getTypeLabel(result.detected_type)}</span>
              </div>
            </div>

            {/* Solution */}
            {result.solution && (
              <div className="mb-6">
                <h3 className="text-xl font-bold text-brand-dark mb-4">Soluție:</h3>
                {renderSolution()}
              </div>
            )}

            {/* Justification */}
            {result.justification && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-semibold text-blue-800 mb-2">Justificare:</h4>
                <p className="text-blue-700">{result.justification}</p>
              </div>
            )}

            {/* Extracted Data Debug (collapsed) */}
            <details className="mt-6">
              <summary className="cursor-pointer text-sm text-brand-neutral hover:text-brand-dark">
                Date extrase (detalii tehnice)
              </summary>
              <pre className="mt-2 bg-gray-100 rounded-lg p-3 text-xs overflow-x-auto">
                {JSON.stringify(result.extracted_data, null, 2)}
              </pre>
            </details>
          </div>
        )}

        {/* Examples */}
        <div className="mt-10 bg-brand-surface rounded-xl p-6 border border-brand-neutral/20">
          <h3 className="text-lg font-bold text-brand-dark mb-4">Exemple de întrebări:</h3>
          <div className="grid gap-4">
            <button
              onClick={() =>
                setQuestionText(
                  'Găsiți echilibrele Nash pentru următoarea matrice de joc:\n\n   (3,2) (1,4)\n   (2,1) (4,3)'
                )
              }
              className="text-left p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors border border-blue-200"
            >
              <span className="font-semibold text-blue-800">Nash:</span>
              <span className="text-blue-600 ml-2">Găsiți echilibrele Nash pentru matricea de joc...</span>
            </button>

            <button
              onClick={() =>
                setQuestionText(
                  'Colorați graful cu 3 culori.\nNoduri: A, B, C, D\nMuchii: A-B, B-C, C-D, D-A, A-C'
                )
              }
              className="text-left p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors border border-purple-200"
            >
              <span className="font-semibold text-purple-800">CSP:</span>
              <span className="text-purple-600 ml-2">Colorați graful cu 3 culori. Noduri: A, B, C, D...</span>
            </button>

            <button
              onClick={() =>
                setQuestionText(
                  'Pentru problema N-Queens cu N=100, care este cea mai potrivită strategie de rezolvare?'
                )
              }
              className="text-left p-4 bg-orange-50 rounded-lg hover:bg-orange-100 transition-colors border border-orange-200"
            >
              <span className="font-semibold text-orange-800">Strategy:</span>
              <span className="text-orange-600 ml-2">Pentru problema N-Queens cu N=100, care strategie...</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SolverPage;
