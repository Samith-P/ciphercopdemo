import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Signup.css';

const Login = () => {
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  // Get the feature they wanted to access or default to Home
  const requestedFeature = location.state?.requestedFeature || sessionStorage.getItem('requestedFeature');
  const from = location.state?.from || '/Home';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const result = await login(email, password);

      if (result.success) {
        // Clear the stored feature request
        sessionStorage.removeItem('requestedFeature');

        // Navigate back to Home with the requested feature
        if (requestedFeature) {
          navigate('/Home', { state: { activateFeature: requestedFeature } });
        } else {
          navigate(from);
        }
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (error) {
      setError('Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section>
      {[...Array(256)].map((_, index) => (
        <span key={index}></span>
      ))}
      <div className="signin">
        <div className="content">
          <h2>Login</h2>
          {error && (
            <div className="error-message" style={{
              color: '#ff4757',
              textAlign: 'center',
              marginBottom: '1rem',
              padding: '0.5rem',
              backgroundColor: 'rgba(255, 71, 87, 0.1)',
              borderRadius: '4px',
              border: '1px solid rgba(255, 71, 87, 0.3)'
            }}>
              {error}
            </div>
          )}
          {requestedFeature && (
            <div style={{
              color: '#64b5f6',
              textAlign: 'center',
              marginBottom: '1rem',
              padding: '0.5rem',
              backgroundColor: 'rgba(100, 181, 246, 0.1)',
              borderRadius: '4px',
              border: '1px solid rgba(100, 181, 246, 0.3)'
            }}>
              Please log in to access {requestedFeature} features
            </div>
          )}
          <form className="form" onSubmit={handleSubmit}>
            <div className="inputBox">
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={isLoading}
                placeholder=" "
              />
              <i>Email</i>
            </div>
            <div className="inputBox">
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                disabled={isLoading}
                placeholder=" "
              />
              <i>Password</i>
            </div>
            <div className="links">
              <a href="#">Forgot Password</a>
              <Link to="/Signup">Signup</Link>
            </div>
            <div className="inputBox">
              <input
                type="submit"
                value={isLoading ? "Logging in..." : "Login"}
                disabled={isLoading}
              />
            </div>
          </form>

        </div>
      </div>
    </section>
  );
};

export default Login;
