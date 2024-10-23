import React from 'react';

const PromptInput = ({ onPromptChange }) => {
  return (
    <div className="prompt-input">
      <textarea
        placeholder="Enter your prompt"
        onChange={(e) => onPromptChange(e.target.value)}
      />
    </div>
  );
};

export default PromptInput;
