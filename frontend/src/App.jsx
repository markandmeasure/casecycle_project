import { useState } from 'react';
import './App.css';
import OpportunityInput from './OpportunityInput';

function App() {
  const [opportunities, setOpportunities] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  const fetchOpportunities = async () => {
    try {
      setErrorMessage(null);

      // Use a relative URL; Vite's development proxy forwards this to the backend.
      const response = await fetch('/opportunities/');
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

  return (
    <div className="App">
      <OpportunityInput />
      <button onClick={fetchOpportunities}>Fetch Opportunities</button>
      {errorMessage && <div role="alert">{errorMessage}</div>}
      {opportunities && <pre>{JSON.stringify(opportunities, null, 2)}</pre>}
    </div>
  );
}

export default App;
