import React, { createContext, useState, useContext, useEffect } from 'react';
import client from '../api/client';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      try {
        if (token) {
          const res = await client.get('/auth/me');
          setUser(res.data);
        }
      } catch (error) {
        console.error("Auth check failed", error);
        logout();
      } finally {
        setLoading(false);
      }
    };
    initAuth();
  }, [token]);

  const login = async (email, password) => {
    try {
      const res = await client.post('/auth/login', { 
        email: email.trim(), 
        password 
      });
      const newToken = res.data.access_token;
      setToken(newToken);
      localStorage.setItem('token', newToken);
      setUser(res.data.user);
      toast.success('Logged in successfully!');
      return true;
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed');
      return false;
    }
  };

  const register = async (email, name, password) => {
    try {
      const res = await client.post('/auth/register', { 
        email: email.trim(), 
        name: name.trim(), 
        password 
      });
      const newToken = res.data.access_token;
      if (newToken) {
        setToken(newToken);
        localStorage.setItem('token', newToken);
        setUser(res.data.user);
      }
      toast.success('Registration successful! Welcome aboard.');
      return true;
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Registration failed');
      return false;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    toast.success('Logged out successfully');
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
