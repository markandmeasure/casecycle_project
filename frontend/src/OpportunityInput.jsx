import { useState } from 'react';

function OpportunityInput({ onSaved }) {
  const [jsonValue, setJsonValue] = useState('');
  const [feedback, setFeedback] = useState(null);

  // Use the sanitized base URL (from `App`)
  const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

  const numericFields = ['tam_estimate', 'growth_rate', 'user_id'];
  const requiredFields = [
    'title',
    'market_description',
    ...numericFields,
    'consumer_insight',
    'hypothesis',
  ];
  const placeholderObj = requiredFields.reduce((acc, field) => {
    acc[field] = numericFields.includes(field) ? 0 : '';
    return acc;
  }, {});

  const handleSave = async () => {
    setFeedback(null);

    let parsed;
    try {
      parsed = JSON.parse(jsonValue);
    } catch {
      setFeedback('Invalid JSON format');
      return;
    }

    const missing = requiredFields.filter((field) => !(field in parsed));
    if (missing.length > 0) {
      setFeedback(`Missing fields: ${missing.join(', ')}`);
      return;
    }

    for (const field of numericFields) {
      const value = Number(parsed[field]);
      if (Number.isNaN(value)) {
        setFeedback(`${field} must be a number`);
        return;
      }
      parsed[field] = value;
    }

    try {
      const response = await fetch(new URL('/opportunities/', API_BASE_URL), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(parsed),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      setFeedback('Opportunity saved');
      setJsonValue('');
      if (onSaved) {
        onSaved();
      }
    } catch (error) {
      console.error('Error saving opportunity:', error);
      setFeedback('Failed to save opportunity');
    }
  };

  return (
    <div className="opportunity-input">
      <textarea
        value={jsonValue}
        onChange={(e) => setJsonValue(e.target.value)}
        placeholder={JSON.stringify(placeholderObj)}
        rows={12}
      />
      <div>
        <button onClick={handleSave}>Save</button>
      </div>
      {feedback && <div role="alert">{feedback}</div>}
    </div>
  );
}

export default OpportunityInput;
