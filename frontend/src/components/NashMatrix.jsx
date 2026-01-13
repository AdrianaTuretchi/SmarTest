import React from 'react';

/**
 * Component to display a Nash Equilibrium payoff matrix
 * with styled table and colored player payoffs
 */
const NashMatrix = ({ matrixData }) => {
  if (!matrixData || matrixData.length === 0) {
    return <div className="text-gray-500 italic">Nu există date pentru matrice.</div>;
  }

  const numRows = matrixData.length;
  const numCols = matrixData[0]?.length || 0;

  return (
    <div className="overflow-x-auto py-4">
      <div className="flex justify-center">
        <table className="border-collapse">
          {/* Header row with column labels */}
          <thead>
            <tr>
              {/* Empty corner cells for row labels */}
              <th className="p-2"></th>
              <th className="p-2"></th>
              {/* Player 2 label spanning all columns */}
              <th 
                colSpan={numCols} 
                className="text-center text-red-600 font-bold pb-2 text-sm"
              >
                Jucător 2 (coloane)
              </th>
            </tr>
            <tr>
              {/* Empty corner cells */}
              <th className="p-2"></th>
              <th className="p-2"></th>
              {/* Column headers */}
              {Array.from({ length: numCols }, (_, i) => (
                <th 
                  key={i} 
                  className="px-4 py-2 text-center text-sm font-semibold text-gray-700 bg-gray-100 border border-gray-300"
                >
                  S{i + 1}
                </th>
              ))}
            </tr>
          </thead>
          
          <tbody>
            {matrixData.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {/* Row header with Player 1 label on first row */}
                {rowIndex === 0 ? (
                  <th 
                    rowSpan={numRows}
                    className="text-blue-600 font-bold pr-2 text-sm align-middle"
                    style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)' }}
                  >
                    Jucător 1 (rânduri)
                  </th>
                ) : null}
                
                {/* Row label */}
                <th className="px-4 py-2 text-center text-sm font-semibold text-gray-700 bg-gray-100 border border-gray-300">
                  S{rowIndex + 1}
                </th>
                
                {/* Payoff cells */}
                {row.map((cell, colIndex) => {
                  const [p1, p2] = cell;
                  return (
                    <td 
                      key={colIndex}
                      className="px-4 py-3 text-center border border-gray-300 bg-white hover:bg-gray-50 transition-colors"
                    >
                      <span className="font-mono text-base">
                        (
                        <span className="text-blue-600 font-semibold">{p1}</span>
                        ,{' '}
                        <span className="text-red-600 font-semibold">{p2}</span>
                        )
                      </span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Legend */}
      <div className="flex justify-center gap-6 mt-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-blue-600"></div>
          <span className="text-gray-600">Payoff Jucător 1</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-red-600"></div>
          <span className="text-gray-600">Payoff Jucător 2</span>
        </div>
      </div>
    </div>
  );
};

export default NashMatrix;
