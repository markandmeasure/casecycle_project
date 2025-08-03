import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [opportunities, setOpportunities] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Use the sanitized base URL (from `main`)
  const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

  useEffect(() => {
    const fetchOpportunities = async () => {
      try {
        setErrorMessage(null);

        // Build the URL safely and check the response status
        const response = await fetch(new URL('/opportunities/', API_BASE_URL));
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setOpportunities(data);
      } catch (error) {
        console.error('Error fetching opportunities:', error);
        setErrorMessage('Unable to fetch opportunities. Please try again later.');
      }
    };

    fetchOpportunities();
  }, [API_BASE_URL]);

  return (
    <div className="App">
      {errorMessage && <div role="alert">{errorMessage}</div>}
      {opportunities && <pre>{JSON.stringify(opportunities, null, 2)}</pre>}
    </div>
  );
}

export default App;
