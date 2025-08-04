/* eslint react-refresh/only-export-components: "off" */
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

  const login = async (username) => {
    const body = new URLSearchParams({ username, password: 'unused' });
    const res = await fetch(new URL('/token', API_BASE_URL), {
      method: 'POST',
      body,
    });
    if (!res.ok) throw new Error('Login failed');
    const data = await res.json();
    localStorage.setItem('token', data.access_token);
    setToken(data.access_token);
  };

  const value = { token, login };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
