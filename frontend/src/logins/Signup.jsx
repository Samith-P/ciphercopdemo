import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Signup.css';

const Signup = () => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  const { signup } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const result = await signup(fullName, email, password);
      
      if (result.success) {
        navigate('/Home');
      } else {
        setError(result.error || 'Signup failed');
      }
    } catch (error) {
      setError('Signup failed. Please try again.');
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
          <h2>Sign Up</h2>
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
          <form className="form" onSubmit={handleSubmit}>
            <div className="inputBox">
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                disabled={isLoading}
                placeholder=" "
              />
              <i>Full Name</i>
            </div>
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
                autoComplete="new-password"
                disabled={isLoading}
                placeholder=" "
              />
              <i>Password</i>
            </div>
            <div className="links">
              <a href="#">Forgot Password</a>
              <Link to="/Login">Login</Link>
            </div>
            <div className="inputBox">
              <input 
                type="submit" 
                value={isLoading ? "Signing up..." : "Sign Up"} 
                disabled={isLoading}
              />
            </div>
          </form>
          
        </div>
      </div>
    </section>
  );
};

export default Signup;
