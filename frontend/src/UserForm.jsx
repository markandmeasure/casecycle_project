import { useState } from 'react';
import { useAuth } from './AuthContext.jsx';

function UserForm({ onUserCreated }) {
  const [name, setName] = useState('');
  const [feedback, setFeedback] = useState(null);
  const { login } = useAuth();

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
      await login(name);
    } catch (err) {
      console.error('Error creating user:', err);
      setFeedback('Failed to create user');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 items-center">
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="User name"
        required
        className="flex-1 p-2 border rounded"
      />
      <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">Add User</button>
      {feedback && <div role="alert">{feedback}</div>}
    </form>
  );
}

export default UserForm;
