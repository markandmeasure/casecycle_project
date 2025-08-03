import { useState } from 'react';

function UserForm({ onUserCreated }) {
  const [name, setName] = useState('');
  const [feedback, setFeedback] = useState(null);

  const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFeedback(null);
    try {
      const resp = await fetch(new URL('/users/', API_BASE_URL), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }),
      });
      if (!resp.ok) {
        throw new Error('Failed to create user');
      }
      setName('');
      setFeedback('User created');
      if (onUserCreated) {
        onUserCreated();
      }
    } catch (err) {
      console.error('Error creating user:', err);
      setFeedback('Failed to create user');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="user-form">
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="User name"
        required
      />
      <button type="submit">Add User</button>
      {feedback && <div role="alert">{feedback}</div>}
    </form>
  );
}

export default UserForm;
