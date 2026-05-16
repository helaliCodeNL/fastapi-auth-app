import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [form, setForm] = useState({ email: '', password: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!form.email) newErrors.email = 'Email required';
    if (!form.password) newErrors.password = 'Password required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    const result = await login(form.email, form.password);
    setLoading(false);

    if (result.success) {
      navigate('/dashboard');
    } else if (result.requires_2fa) {
      localStorage.setItem('2fa_email', result.email);
      navigate('/dashboard'); // For now, redirect to dashboard
    } else {
      setErrors({ general: result.error });
    }
  };

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <h1>Welcome Back</h1>
          <p>Login to your account</p>
        </div>

        {errors.general && <div className="alert alert-error">{errors.general}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input type="email" value={form.email} onChange={(e) => setForm({...form, email: e.target.value})} placeholder="your@email.com" />
            {errors.email && <div className="error-message">{errors.email}</div>}
          </div>

          <div className="form-group">
            <label>Password</label>
            <input type="password" value={form.password} onChange={(e) => setForm({...form, password: e.target.value})} placeholder="••••••••" />
            {errors.password && <div className="error-message">{errors.password}</div>}
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="footer">
          <div style={{ marginBottom: '10px' }}>
            <Link to="/forgot-password" className="link">Forgot Password?</Link>
          </div>
          <div>
            Don't have account? <Link to="/register" className="link">Sign Up</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
