import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';

const ForgotPassword = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(false);

    if (!email) {
      setError('Email is required');
      return;
    }

    setLoading(true);
    try {
      const response = await authAPI.forgotPassword(email);
      setSuccess(true);
      setEmail('');
      setTimeout(() => {
        navigate('/reset-password', { state: { email } });
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send reset code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <h1>Forgot Password</h1>
          <p>Enter your email to receive a reset code</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">Reset code sent! Check your email and terminal. Redirecting...</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              disabled={success}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading || success}>
            {loading ? 'Sending...' : 'Send Reset Code'}
          </button>
        </form>

        <div className="footer">
          Remember password? <Link to="/login" className="link">Login</Link>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
