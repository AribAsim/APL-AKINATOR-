import React from 'react';

export const ProgressBar = ({ confidence }) => {
  // confidence is between 0 and 1
  const percentage = Math.min(100, Math.max(0, confidence * 100));

  return (
    <div className="progress-container">
      <div className="progress-labels">
        <span>Confidence</span>
        <span>{Math.round(percentage)}%</span>
      </div>
      <div className="progress-bar-bg">
        <div 
          className="progress-bar-fill" 
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
