import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

const App = () => {
  const [imageFile, setImageFile] = useState(null); // Store the actual image file
  const [imagePreview, setImagePreview] = useState(null); // Store image URL for preview
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageFile(file); // Store the file for submission
      setImagePreview(URL.createObjectURL(file)); // Set preview URL
    }
  };

  const handlePromptChange = (e) => {
    setPrompt(e.target.value);
  };

  const handleSubmit = async () => {
    if (!imageFile || !prompt) {
      alert("Please upload an image and enter a prompt.");
      return;
    }

    const formData = new FormData();
    formData.append('image', imageFile); // Append the file
    formData.append('prompt', prompt);

    try {
      const result = await axios.post('http://localhost:8000/process/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResponse(result.data.generated_text); // Assuming the backend sends this field
    } catch (error) {
      console.error('Error submitting data:', error);
      setResponse('An error occurred while processing the request.');
    }
  };

  return (
    <div className="page-container">
      <div className="app-container">
        <div className="toolbar">
          <h1>ReadMe</h1>
        </div>
        <div className="content-box">
          <div className="image-preview-box">
            <div className="preview-label">Image Preview</div>
            {imagePreview ? (
              <img src={imagePreview} alt="Uploaded preview" className="image-preview" />
            ) : (
              <div className="placeholder">No image uploaded</div>
            )}
          </div>
          <div className="custom-file-input">
            <input
              type="file"
              id="file-upload"
              accept="image/*"
              onChange={handleImageUpload}
            />
            <label htmlFor="file-upload">Choose File</label>
          </div>
          <input
            type="text"
            placeholder="Enter your prompt"
            value={prompt}
            onChange={handlePromptChange}
            className="prompt-input"
          />
          <button onClick={handleSubmit} className="submit-button">Submit</button>

          {/* Always visible response box with label */}
          <div className="response-box">
            <div className="response-label">Response</div>
            <div className="response-text">
              {response || "Waiting for response..."}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
