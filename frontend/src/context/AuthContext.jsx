import React, { createContext, useState, useContext } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token'));

  const login = async (email, password) => {
    try {
      const res = await authAPI.login({ email, password });
      if (res.data.requires_2fa) {
        return { requires_2fa: true, email };
      }
      localStorage.setItem('access_token', res.data.access_token);
      localStorage.setItem('refresh_token', res.data.refresh_token);
      setToken(res.data.access_token);
      setUser(res.data);
      return { success: true };
    } catch (err) {
      return { success: false, error: err.response?.data?.detail || 'Login failed' };
    }
  };

  const register = async (formData) => {
    try {
      const res = await authAPI.register(formData);
      return { success: true, data: res.data };
    } catch (err) {
      return { success: false, error: err.response?.data?.detail || 'Registration failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
