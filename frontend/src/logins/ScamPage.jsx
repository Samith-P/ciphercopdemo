import React, { useState } from 'react';
import { DollarSign, AlertTriangle, Search, Phone, Mail, TrendingUp, Users, Shield, CheckCircle, CreditCard } from 'lucide-react';

const ScamPage = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [email, setEmail] = useState('');
  const [website, setWebsite] = useState('');
  const [scanResult, setScanResult] = useState(null);
  const [isScanning, setIsScanning] = useState(false);

  const handlePhoneCheck = async () => {
    if (!phoneNumber) return;
    setIsScanning(true);
    
    setTimeout(() => {
      setScanResult({
        type: 'phone',
        target: phoneNumber,
        isScam: Math.random() > 0.6,
        riskLevel: Math.random() > 0.7 ? 'high' : Math.random() > 0.4 ? 'medium' : 'low',
        details: {
          reports: Math.floor(Math.random() * 50),
          scamType: ['Fake Investment', 'Tech Support', 'IRS Fraud', 'Romance Scam'][Math.floor(Math.random() * 4)],
          location: 'Unknown',
          carrier: 'Mobile Network',
          lastReported: new Date().toLocaleString()
        }
      });
      setIsScanning(false);
    }, 2000);
  };

  const handleEmailCheck = async () => {
    if (!email) return;
    setIsScanning(true);
    
    setTimeout(() => {
      setScanResult({
        type: 'email',
        target: email,
        isScam: Math.random() > 0.5,
        riskLevel: Math.random() > 0.6 ? 'high' : Math.random() > 0.3 ? 'medium' : 'low',
        details: {
          domain: email.split('@')[1] || 'unknown',
          reputation: Math.floor(Math.random() * 100),
          blacklisted: Math.random() > 0.8,
          phishingAttempts: Math.floor(Math.random() * 20),
          lastActivity: new Date().toLocaleString()
        }
      });
      setIsScanning(false);
    }, 2000);
  };

  const handleWebsiteCheck = async () => {
    if (!website) return;
    setIsScanning(true);
    
    setTimeout(() => {
      setScanResult({
        type: 'website',
        target: website,
        isScam: Math.random() > 0.7,
        riskLevel: Math.random() > 0.6 ? 'high' : Math.random() > 0.3 ? 'medium' : 'low',
        details: {
          scamType: ['Investment Fraud', 'Fake Shop', 'Cryptocurrency Scam', 'Romance Scam'][Math.floor(Math.random() * 4)],
          trustScore: Math.floor(Math.random() * 100),
          ageOfDomain: Math.floor(Math.random() * 365) + ' days',
          reports: Math.floor(Math.random() * 100),
          lastChecked: new Date().toLocaleString()
        }
      });
      setIsScanning(false);
    }, 2000);
  };

  const stats = [
    { icon: Shield, label: 'Scams Blocked', value: '890K+', color: 'text-green-400' },
    { icon: DollarSign, label: 'Money Saved', value: '$45M+', color: 'text-blue-400' },
    { icon: Users, label: 'Protected Users', value: '2.1M+', color: 'text-purple-400' },
    { icon: TrendingUp, label: 'Detection Rate', value: '96.8%', color: 'text-yellow-400' }
  ];

  const recentScams = [
    { 
      type: 'Investment Fraud', 
      contact: '+1-555-SCAM', 
      amount: '$50,000', 
      status: 'blocked',
      time: '2 minutes ago' 
    },
    { 
      type: 'Fake Tech Support', 
      contact: 'support@fake-microsoft.com', 
      amount: '$300', 
      status: 'investigating',
      time: '8 minutes ago' 
    },
    { 
      type: 'Romance Scam', 
      contact: 'love-scammer@email.com', 
      amount: '$25,000', 
      status: 'blocked',
      time: '15 minutes ago' 
    },
    { 
      type: 'Cryptocurrency Fraud', 
      contact: 'crypto-invest.scam', 
      amount: '$100,000', 
      status: 'blocked',
      time: '32 minutes ago' 
    }
  ];

  return (
    <div className="scam-page">
      <div className="page-header animate-fade-in">
        <div className="header-content">
          <div className="header-icon">
            <DollarSign size={48} className="animate-pulse" />
          </div>
          <div className="header-text">
            <h1>Scam Detection</h1>
            <p>Protect yourself from financial fraud and social engineering</p>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid animate-fade-in-up">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card" style={{ animationDelay: `${index * 0.1}s` }}>
            <stat.icon className={`stat-icon ${stat.color}`} />
            <div className="stat-value">{stat.value}</div>
            <div className="stat-label">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Scanning Tools */}
      <div className="scanning-section">
        <div className="scan-grid-3">
          {/* Phone Number Checker */}
          <div className="scan-card animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <div className="scan-header">
              <Phone className="scan-icon" />
              <h3>Phone Number Checker</h3>
            </div>
            <div className="scan-content">
              <input
                type="tel"
                placeholder="Enter phone number (e.g., +1-555-123-4567)"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                className="scan-input"
              />
              <button 
                onClick={handlePhoneCheck}
                disabled={!phoneNumber || isScanning}
                className="scan-button"
              >
                {isScanning ? (
                  <Phone className="animate-pulse" />
                ) : (
                  <Search />
                )}
                {isScanning ? 'Checking...' : 'Check Number'}
              </button>
            </div>
          </div>

          {/* Email Checker */}
          <div className="scan-card animate-slide-up" style={{ animationDelay: '0.3s' }}>
            <div className="scan-header">
              <Mail className="scan-icon" />
              <h3>Email Checker</h3>
            </div>
            <div className="scan-content">
              <input
                type="email"
                placeholder="Enter email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="scan-input"
              />
              <button 
                onClick={handleEmailCheck}
                disabled={!email || isScanning}
                className="scan-button"
              >
                {isScanning ? (
                  <Mail className="animate-pulse" />
                ) : (
                  <Search />
                )}
                {isScanning ? 'Checking...' : 'Check Email'}
              </button>
            </div>
          </div>

          {/* Website Checker */}
          <div className="scan-card animate-slide-up" style={{ animationDelay: '0.4s' }}>
            <div className="scan-header">
              <CreditCard className="scan-icon" />
              <h3>Investment Site Checker</h3>
            </div>
            <div className="scan-content">
              <input
                type="url"
                placeholder="Enter website URL"
                value={website}
                onChange={(e) => setWebsite(e.target.value)}
                className="scan-input"
              />
              <button 
                onClick={handleWebsiteCheck}
                disabled={!website || isScanning}
                className="scan-button"
              >
                {isScanning ? (
                  <CreditCard className="animate-pulse" />
                ) : (
                  <Search />
                )}
                {isScanning ? 'Checking...' : 'Check Site'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Scan Results */}
      {scanResult && (
        <div className="results-section animate-fade-in">
          <div className="results-card">
            <div className="results-header">
              <h3>Scam Analysis Results</h3>
              <div className={`threat-badge threat-${scanResult.riskLevel}`}>
                {scanResult.isScam ? <AlertTriangle size={16} /> : <CheckCircle size={16} />}
                {scanResult.riskLevel.toUpperCase()} RISK
              </div>
            </div>
            <div className="results-content">
              <div className="result-details">
                <div className="detail-item">
                  <span className="detail-label">Target:</span>
                  <span className="detail-value">{scanResult.target}</span>
                </div>
                
                {scanResult.type === 'phone' && (
                  <>
                    <div className="detail-item">
                      <span className="detail-label">Reports:</span>
                      <span className="detail-value">{scanResult.details.reports} user reports</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Scam Type:</span>
                      <span className="detail-value">{scanResult.details.scamType}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Location:</span>
                      <span className="detail-value">{scanResult.details.location}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Carrier:</span>
                      <span className="detail-value">{scanResult.details.carrier}</span>
                    </div>
                  </>
                )}
                
                {scanResult.type === 'email' && (
                  <>
                    <div className="detail-item">
                      <span className="detail-label">Domain:</span>
                      <span className="detail-value">{scanResult.details.domain}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Reputation:</span>
                      <span className="detail-value">{scanResult.details.reputation}/100</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Blacklisted:</span>
                      <span className="detail-value">{scanResult.details.blacklisted ? 'Yes' : 'No'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Phishing Attempts:</span>
                      <span className="detail-value">{scanResult.details.phishingAttempts}</span>
                    </div>
                  </>
                )}
                
                {scanResult.type === 'website' && (
                  <>
                    <div className="detail-item">
                      <span className="detail-label">Scam Type:</span>
                      <span className="detail-value">{scanResult.details.scamType}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Trust Score:</span>
                      <span className="detail-value">{scanResult.details.trustScore}/100</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Domain Age:</span>
                      <span className="detail-value">{scanResult.details.ageOfDomain}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">User Reports:</span>
                      <span className="detail-value">{scanResult.details.reports}</span>
                    </div>
                  </>
                )}
              </div>
              <div className="scan-timestamp">
                Last checked: {scanResult.details.lastChecked || scanResult.details.lastReported || scanResult.details.lastActivity}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Recent Scam Detections */}
      <div className="threats-section animate-fade-in-up">
        <h3>Recent Scam Detections</h3>
        <div className="scam-list">
          {recentScams.map((scam, index) => (
            <div key={index} className="scam-item" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="scam-info">
                <div className="scam-type">{scam.type}</div>
                <div className="scam-contact">{scam.contact}</div>
                <div className="scam-amount">Attempted: {scam.amount}</div>
                <div className="scam-time">{scam.time}</div>
              </div>
              <div className={`status-badge status-${scam.status}`}>
                {scam.status.toUpperCase()}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ScamPage;
