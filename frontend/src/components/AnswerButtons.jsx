import React from 'react';

export const AnswerButtons = ({ onAnswer, disabled }) => {
  return (
    <div className="answer-buttons">
      <button 
        className="btn-yes" 
        onClick={() => onAnswer('yes')}
        disabled={disabled}
      >
        Yes
      </button>
      <button 
        className="btn-no" 
        onClick={() => onAnswer('no')}
        disabled={disabled}
      >
        No
      </button>
      <button 
        className="btn-maybe" 
        onClick={() => onAnswer('maybe')}
        disabled={disabled}
      >
        Maybe
      </button>
      <button 
        className="btn-dont-know" 
        onClick={() => onAnswer('dont_know')}
        disabled={disabled}
      >
        Don't Know
      </button>
    </div>
  );
};
