import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await axios.post('http://localhost:5000/detect', { text });
      setPrediction(response.data.prediction);
    } catch (err) {
      setError('An error occurred while making the prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Fake News Detector</h1>
        <form onSubmit={handleSubmit}>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter news text here..."
            rows="10"
            cols="50"
          />
          <br />
          <button type="submit" disabled={loading}>Predict</button>
        </form>
        {loading && <p>Loading...</p>}
        {error && <p className="error">{error}</p>}
        {prediction && (
          <p className="prediction">
            This news is <strong>{prediction}</strong>.
          </p>
        )}
      </header>
    </div>
  );
}

export default App;
