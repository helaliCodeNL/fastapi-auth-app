import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (data) => API.post('/auth/register', data),
  login: (data) => API.post('/auth/login', data),
  setup2fa: (user_id) => API.post(`/auth/setup-2fa?user_id=${user_id}`),
  verify2fa: (user_id, token) => API.post(`/auth/verify-2fa?user_id=${user_id}`, { token }),
  login2fa: (email, token) => API.post(`/auth/login-2fa?email=${email}&token=${token}`),
  forgotPassword: (email) => API.post('/auth/forgot-password', { email }),
  resetPassword: (token, password) => API.post('/auth/reset-password', { token, password }),
  refresh: (refresh_token) => API.post('/auth/refresh', { refresh_token }),
};

export const userAPI = {
  getProfile: () => API.get('/users/me'),
  disable2fa: () => API.post('/users/disable-2fa'),
};

export default API;
