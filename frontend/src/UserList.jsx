import { useEffect, useState } from 'react';

function UserList({ refreshToken }) {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setError(null);
        const resp = await fetch(new URL('/users/', API_BASE_URL));
        if (!resp.ok) {
          throw new Error('Failed to fetch users');
        }
        const data = await resp.json();
        setUsers(data);
      } catch (err) {
        console.error('Error fetching users:', err);
        setError('Failed to load users');
      }
    };

    fetchUsers();
  }, [refreshToken, API_BASE_URL]);

  return (
    <div className="user-list">
      <h2>Users</h2>
      {error && <div role="alert">{error}</div>}
      <ul>
        {users.map((u) => (
          <li key={u.id}>{u.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;
