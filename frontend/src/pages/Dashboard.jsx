import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { userAPI, authAPI } from '../services/api';

const Dashboard = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await userAPI.getProfile();
      setUser(res.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching profile:', err);
      setLoading(false);
    }
  };

  const handleSetup2FA = async () => {
    try {
      const res = await authAPI.setup2fa(user.id);
      setMessage('✓ 2FA setup initiated! Check your server terminal for the code.');
      setTimeout(() => setMessage(''), 5000);
      setTimeout(fetchProfile, 1000);
    } catch (err) {
      setMessage('Error setting up 2FA');
    }
  };

  const handleDisable2FA = async () => {
    try {
      await userAPI.disable2fa();
      setMessage('✓ 2FA disabled');
      setTimeout(() => setMessage(''), 3000);
      setTimeout(fetchProfile, 1000);
    } catch (err) {
      setMessage('Error disabling 2FA');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) return <div className="app"><div className="container">Loading...</div></div>;

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <h1>Welcome, {user?.name}! 👋</h1>
          <p style={{ fontSize: '18px', marginTop: '10px' }}>How can I help you?</p>
        </div>

        {message && <div className="alert alert-success">{message}</div>}

        <div style={{ marginTop: '30px' }}>
          <h3>Your Profile</h3>
          <div className="profile-info" style={{ background: '#f5f5f5', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
            <p><strong>📧 Email:</strong> {user?.email}</p>
            <p><strong>👤 Name:</strong> {user?.name}</p>
            {user?.phone && <p><strong>📱 Phone:</strong> {user.phone}</p>}
            <p><strong>🔐 Account Status:</strong> {user?.is_verified ? '✓ Verified' : 'Pending'}</p>
            <p><strong>🔐 2FA Status:</strong> {user?.two_fa_enabled ? '✓ Enabled' : 'Not Enabled'}</p>
          </div>

          <h3>What Would You Like To Do?</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '20px' }}>
            {!user?.two_fa_enabled && (
              <button onClick={handleSetup2FA} className="btn btn-success">
                🔒 Enable 2FA Security
              </button>
            )}
            
            {user?.two_fa_enabled && (
              <button onClick={handleDisable2FA} className="btn btn-warning">
                🔓 Disable 2FA
              </button>
            )}

            <button onClick={() => navigate('/forgot-password')} className="btn btn-primary">
              🔑 Change Password
            </button>
          </div>

          <button onClick={handleLogout} className="btn btn-danger" style={{ width: '100%' }}>
            🚪 Logout
          </button>
        </div>

        <div style={{ marginTop: '40px', padding: '15px', background: '#e8f4f8', borderRadius: '8px', textAlign: 'center' }}>
          <p style={{ margin: '0', color: '#333' }}>
            <strong>Account created:</strong> {new Date(user?.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
