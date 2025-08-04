import { useState, useEffect, useCallback } from 'react';
import OpportunityInput from './OpportunityInput';
import UserForm from './UserForm';
import UserList from './UserList';
import { useAuth } from './AuthContext.jsx';

function App() {
  const [opportunities, setOpportunities] = useState([]);
  const [errorMessage, setErrorMessage] = useState(null);
  const [page, setPage] = useState(0);
  const [userRefresh, setUserRefresh] = useState(0);
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

  const fetchOpportunities = useCallback(async () => {
    setLoading(true);
    try {
      setErrorMessage(null);

      const response = await fetch(
        new URL(`/opportunities/?skip=${page * 10}&limit=10`, API_BASE_URL),
        { headers: token ? { Authorization: `Bearer ${token}` } : {} }
      );
      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();
      setOpportunities(data);
    } catch (error) {
      console.error('Error fetching opportunities:', error);
      setErrorMessage(`Unable to fetch opportunities: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, [page, API_BASE_URL, token]);

  useEffect(() => {
    fetchOpportunities();
  }, [fetchOpportunities]);

  return (
    <>
      <header className="text-2xl font-semibold p-4 bg-white shadow">CaseCycle</header>
      <main className="max-w-3xl mx-auto p-4 space-y-8">
        <UserForm onUserCreated={() => setUserRefresh((u) => u + 1)} />
        <UserList refreshToken={userRefresh} />
        <OpportunityInput onSaved={fetchOpportunities} />
        {loading && <p>Loading…</p>}
        {errorMessage && <div role="alert" className="text-red-600">{errorMessage}</div>}
        <ul className="space-y-4">
          {opportunities.map((opp, idx) => (
            <li key={opp.id || idx} className="bg-white border rounded p-4">
              <h3 className="font-semibold">{opp.title}</h3>
              <p><strong>Market Description:</strong> {opp.market_description}</p>
              <p><strong>TAM Estimate:</strong> {opp.tam_estimate}</p>
              <p><strong>Growth Rate:</strong> {opp.growth_rate}</p>
              <p><strong>Consumer Insight:</strong> {opp.consumer_insight}</p>
              <p><strong>Hypothesis:</strong> {opp.hypothesis}</p>
            </li>
          ))}
        </ul>
        <div className="flex justify-center items-center gap-4 mt-8">
          <button
            onClick={() => setPage((p) => Math.max(p - 1, 0))}
            disabled={page === 0}
            className="px-3 py-1 bg-blue-500 text-white rounded disabled:opacity-50"
          >
            Prev
          </button>
          <span>Page {page + 1}</span>
          <button
            onClick={() => setPage((p) => p + 1)}
            disabled={opportunities.length < 10}
            className="px-3 py-1 bg-blue-500 text-white rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </main>
      <footer className="text-center text-sm text-gray-500 p-4">Mark&Measure</footer>
    </>
  );
}

export default App;
