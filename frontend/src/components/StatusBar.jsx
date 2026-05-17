import React from 'react';

export const StatusBar = ({ remaining }) => {
  return (
    <div className="status-bar">
      AI narrowed it down to <strong>{remaining}</strong> players
    </div>
  );
};
