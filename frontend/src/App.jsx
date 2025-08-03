import { useState, useEffect, useCallback } from 'react';
import './App.css';
import OpportunityInput from './OpportunityInput';

function App() {
  const [opportunities, setOpportunities] = useState([]);
  const [errorMessage, setErrorMessage] = useState(null);
  const [page, setPage] = useState(0);

  const fetchOpportunities = useCallback(async () => {
    try {
      setErrorMessage(null);

      // Use a relative URL; Vite's development proxy forwards this to the backend.
      const response = await fetch(
        `/opportunities/?skip=${page * 10}&limit=10`
      );
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setOpportunities(data);
    } catch (error) {
      console.error('Error fetching opportunities:', error);
      setErrorMessage('Unable to fetch opportunities. Please try again later.');
    }
  }, [page]);

  useEffect(() => {
    fetchOpportunities();
  }, [fetchOpportunities]);

  return (
    <div className="App">
      <OpportunityInput onSaved={fetchOpportunities} />
      {errorMessage && <div role="alert">{errorMessage}</div>}
      <ul>
        {opportunities.map((opp, idx) => (
          <li key={opp.id || idx}>
            <h3>{opp.title}</h3>
            <p><strong>Market Description:</strong> {opp.market_description}</p>
            <p><strong>TAM Estimate:</strong> {opp.tam_estimate}</p>
            <p><strong>Growth Rate:</strong> {opp.growth_rate}</p>
            <p><strong>Consumer Insight:</strong> {opp.consumer_insight}</p>
            <p><strong>Hypothesis:</strong> {opp.hypothesis}</p>
          </li>
        ))}
      </ul>
      <div>
        <button
          onClick={() => setPage((p) => Math.max(p - 1, 0))}
          disabled={page === 0}
        >
          Prev
        </button>
        <span>Page {page + 1}</span>
        <button
          onClick={() => setPage((p) => p + 1)}
          disabled={opportunities.length < 10}
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default App;
