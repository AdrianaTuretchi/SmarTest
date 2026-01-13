import React from 'react';

/**
 * Recursive component to render a MinMax tree node
 */
const TreeNode = ({ node, depth = 0, isMax = true }) => {
  const isLeaf = !node.children || node.children.length === 0;
  
  // Alternate colors for MAX and MIN levels
  const nodeColor = isMax ? 'bg-blue-500' : 'bg-red-500';
  const nodeLabel = isMax ? 'MAX' : 'MIN';
  
  return (
    <div className="flex flex-col items-center">
      {/* Node circle */}
      <div
        className={`
          ${isLeaf ? 'bg-green-500' : nodeColor}
          text-white font-bold rounded-full
          w-10 h-10 flex items-center justify-center
          text-sm shadow-md
        `}
        title={isLeaf ? `Frunză: ${node.value}` : `${nodeLabel}`}
      >
        {isLeaf ? node.value : '?'}
      </div>
      
      {/* Small label under node */}
      {!isLeaf && (
        <span className="text-xs text-gray-500 mt-0.5">{nodeLabel}</span>
      )}
      
      {/* Children container */}
      {!isLeaf && node.children && node.children.length > 0 && (
        <div className="flex flex-col items-center">
          {/* Vertical line from parent to horizontal connector */}
          <div className="w-0.5 h-4 bg-gray-400"></div>
          
          {/* Horizontal connector line */}
          <div className="flex items-start">
            {node.children.map((child, index) => (
              <div key={index} className="flex flex-col items-center">
                {/* Horizontal and vertical lines */}
                <div className="flex items-start">
                  {/* Left horizontal line (for all except first child) */}
                  {index > 0 && (
                    <div className="h-0.5 bg-gray-400" style={{ width: '20px' }}></div>
                  )}
                  
                  {/* Center point with vertical line */}
                  <div className="flex flex-col items-center">
                    {index === 0 && node.children.length > 1 && (
                      <div className="h-0.5 bg-gray-400" style={{ width: '20px', marginLeft: '20px' }}></div>
                    )}
                  </div>
                  
                  {/* Right horizontal line (for all except last child) */}
                  {index < node.children.length - 1 && (
                    <div className="h-0.5 bg-gray-400" style={{ width: '20px' }}></div>
                  )}
                </div>
              </div>
            ))}
          </div>
          
          {/* Children nodes */}
          <div className="flex gap-4 mt-0">
            {node.children.map((child, index) => (
              <div key={index} className="flex flex-col items-center">
                <div className="w-0.5 h-4 bg-gray-400"></div>
                <TreeNode node={child} depth={depth + 1} isMax={!isMax} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

/**
 * Main MinMax Tree visualization component
 */
const MinMaxTree = ({ treeData }) => {
  if (!treeData) {
    return <div className="text-gray-500 italic">Nu există date pentru arbore.</div>;
  }

  return (
    <div className="overflow-x-auto py-4">
      <div className="flex justify-center min-w-max px-4">
        <TreeNode node={treeData} depth={0} isMax={true} />
      </div>
      
      {/* Legend */}
      <div className="flex justify-center gap-6 mt-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-blue-500"></div>
          <span className="text-gray-600">MAX</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-red-500"></div>
          <span className="text-gray-600">MIN</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-green-500"></div>
          <span className="text-gray-600">Frunză (valoare)</span>
        </div>
      </div>
    </div>
  );
};

export default MinMaxTree;
