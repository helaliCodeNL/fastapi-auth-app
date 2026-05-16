import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { userAPI, authAPI } from '../services/api';

const Dashboard = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [qrCode, setQrCode] = useState('');
  const [showSetup2fa, setShowSetup2fa] = useState(false);

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
      setQrCode(res.data.qr_code);
      setShowSetup2fa(true);
    } catch (err) {
      console.error('Error setting up 2FA:', err);
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
          <h1>Dashboard</h1>
          <p>Welcome, {user?.name}!</p>
        </div>

        <div className="profile-info">
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>Name:</strong> {user?.name}</p>
          {user?.phone && <p><strong>Phone:</strong> {user.phone}</p>}
          <p><strong>2FA:</strong> {user?.two_fa_enabled ? '✓ Enabled' : 'Disabled'}</p>
        </div>

        {!user?.two_fa_enabled && (
          <button onClick={handleSetup2FA} className="btn btn-success">
            Enable 2FA
          </button>
        )}

        {showSetup2fa && (
          <div style={{ textAlign: 'center', margin: '20px 0' }}>
            {qrCode && <img src={qrCode} alt="2FA QR" style={{ maxWidth: '200px' }} />}
          </div>
        )}

        <button onClick={handleLogout} className="btn btn-primary" style={{ marginTop: '20px' }}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
