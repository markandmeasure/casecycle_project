import { useEffect, useState } from 'react';

function UserList({ refreshToken }) {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      try {
        setError(null);
        const resp = await fetch(new URL('/users/', API_BASE_URL));
        if (!resp.ok) {
          throw new Error(await resp.text());
        }
        const data = await resp.json();
        setUsers(data);
      } catch (err) {
        console.error('Error fetching users:', err);
        setError(`Failed to load users: ${err.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [refreshToken, API_BASE_URL]);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Users</h2>
      {loading && <p>Loading…</p>}
      {error && <div role="alert" className="text-red-600">{error}</div>}
      <ul className="list-disc pl-5">
        {users.map((u) => (
          <li key={u.id}>{u.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;
