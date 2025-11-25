import { createContext, useState, useEffect } from 'react';
import api from '../utils/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const login = async (email, password) => {
    const { data } = await api.post('/token/', { email, password });
    localStorage.setItem('s2s_token', data.access);
    const res = await api.get('/auth/me/');
    setUser(res.data);
  };

  const logout = () => {
    localStorage.removeItem('s2s_token');
    setUser(null);
    window.location = '/login';
  };

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get('/auth/me/');
        setUser(res.data);
      } catch {
        localStorage.removeItem('s2s_token');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};