import React, { useState } from 'react';
import { Copy, Search, Globe, AlertTriangle, CheckCircle, TrendingUp, Users, Database, Eye } from 'lucide-react';

const ClonePage = () => {
  const [url, setUrl] = useState('');
  const [domain, setDomain] = useState('');
  const [scanResult, setScanResult] = useState(null);
  const [isScanning, setIsScanning] = useState(false);

  const handleUrlCheck = async () => {
    if (!url) return;
    setIsScanning(true);
    
    setTimeout(() => {
      setScanResult({
        type: 'url',
        target: url,
        isClone: Math.random() > 0.6,
        similarity: Math.floor(Math.random() * 40 + 60),
        details: {
          originalSite: 'amazon.com',
          cloneIndicators: Math.floor(Math.random() * 5),
          riskScore: Math.floor(Math.random() * 100),
          registrationDate: '2024-08-20',
          lastChecked: new Date().toLocaleString()
        }
      });
      setIsScanning(false);
    }, 2000);
  };

  const handleDomainCheck = async () => {
    if (!domain) return;
    setIsScanning(true);
    
    setTimeout(() => {
      setScanResult({
        type: 'domain',
        target: domain,
        isClone: Math.random() > 0.5,
        similarity: Math.floor(Math.random() * 30 + 70),
        details: {
          suspiciousDomains: Math.floor(Math.random() * 10 + 1),
          typosquatting: Math.random() > 0.7,
          phishingRisk: Math.floor(Math.random() * 100),
          dnsRecords: 'Analyzed',
          lastChecked: new Date().toLocaleString()
        }
      });
      setIsScanning(false);
    }, 2000);
  };

  const stats = [
    { icon: Eye, label: 'Sites Monitored', value: '2.8M+', color: 'text-blue-400' },
    { icon: Copy, label: 'Clones Detected', value: '156K', color: 'text-red-400' },
    { icon: Database, label: 'Domain Database', value: '890M+', color: 'text-green-400' },
    { icon: TrendingUp, label: 'Detection Accuracy', value: '97.3%', color: 'text-purple-400' }
  ];

  const recentClones = [
    { 
      original: 'paypal.com', 
      clone: 'paypaI-security.com', 
      similarity: 94, 
      status: 'blocked',
      time: '5 minutes ago' 
    },
    { 
      original: 'microsoft.com', 
      clone: 'microsft-update.net', 
      similarity: 87, 
      status: 'investigating',
      time: '12 minutes ago' 
    },
    { 
      original: 'google.com', 
      clone: 'goog1e-login.org', 
      similarity: 91, 
      status: 'blocked',
      time: '28 minutes ago' 
    },
    { 
      original: 'facebook.com', 
      clone: 'faceb00k-verify.com', 
      similarity: 89, 
      status: 'blocked',
      time: '45 minutes ago' 
    }
  ];

  return (
    <div className="clone-page">
      <div className="page-header animate-fade-in">
        <div className="header-content">
          <div className="header-icon">
            <Copy size={48} className="animate-spin-slow" />
          </div>
          <div className="header-text">
            <h1>Clone Detection</h1>
            <p>Identify and prevent website and application cloning</p>
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
        <div className="scan-grid">
          {/* URL Clone Checker */}
          <div className="scan-card animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <div className="scan-header">
              <Globe className="scan-icon" />
              <h3>Website Clone Checker</h3>
            </div>
            <div className="scan-content">
              <input
                type="url"
                placeholder="Enter website URL to check for clones"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="scan-input"
              />
              <button 
                onClick={handleUrlCheck}
                disabled={!url || isScanning}
                className="scan-button"
              >
                {isScanning ? (
                  <Copy className="animate-spin" />
                ) : (
                  <Search />
                )}
                {isScanning ? 'Checking...' : 'Check for Clones'}
              </button>
            </div>
          </div>

          {/* Domain Monitor */}
          <div className="scan-card animate-slide-up" style={{ animationDelay: '0.3s' }}>
            <div className="scan-header">
              <Database className="scan-icon" />
              <h3>Domain Monitor</h3>
            </div>
            <div className="scan-content">
              <input
                type="text"
                placeholder="Enter domain name to monitor (e.g., example.com)"
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                className="scan-input"
              />
              <button 
                onClick={handleDomainCheck}
                disabled={!domain || isScanning}
                className="scan-button"
              >
                {isScanning ? (
                  <Eye className="animate-pulse" />
                ) : (
                  <Search />
                )}
                {isScanning ? 'Monitoring...' : 'Monitor Domain'}
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
              <h3>Clone Analysis Results</h3>
              <div className={`threat-badge ${scanResult.isClone ? 'threat-high' : 'threat-safe'}`}>
                {scanResult.isClone ? <AlertTriangle size={16} /> : <CheckCircle size={16} />}
                {scanResult.isClone ? 'CLONE DETECTED' : 'LEGITIMATE'}
              </div>
            </div>
            <div className="results-content">
              <div className="similarity-score">
                <div className="similarity-label">Similarity Score</div>
                <div className="similarity-bar">
                  <div 
                    className="similarity-fill" 
                    style={{ 
                      width: `${scanResult.similarity}%`,
                      background: scanResult.similarity > 80 ? '#ef4444' : scanResult.similarity > 60 ? '#f59e0b' : '#10b981'
                    }}
                  ></div>
                </div>
                <div className="similarity-percentage">{scanResult.similarity}%</div>
              </div>
              
              <div className="result-details">
                <div className="detail-item">
                  <span className="detail-label">Target:</span>
                  <span className="detail-value">{scanResult.target}</span>
                </div>
                
                {scanResult.type === 'url' && (
                  <>
                    <div className="detail-item">
                      <span className="detail-label">Potential Original:</span>
                      <span className="detail-value">{scanResult.details.originalSite}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Clone Indicators:</span>
                      <span className="detail-value">{scanResult.details.cloneIndicators}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Risk Score:</span>
                      <span className="detail-value">{scanResult.details.riskScore}/100</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Registration Date:</span>
                      <span className="detail-value">{scanResult.details.registrationDate}</span>
                    </div>
                  </>
                )}
                
                {scanResult.type === 'domain' && (
                  <>
                    <div className="detail-item">
                      <span className="detail-label">Suspicious Domains Found:</span>
                      <span className="detail-value">{scanResult.details.suspiciousDomains}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Typosquatting Risk:</span>
                      <span className="detail-value">{scanResult.details.typosquatting ? 'High' : 'Low'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Phishing Risk:</span>
                      <span className="detail-value">{scanResult.details.phishingRisk}/100</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">DNS Analysis:</span>
                      <span className="detail-value">{scanResult.details.dnsRecords}</span>
                    </div>
                  </>
                )}
              </div>
              <div className="scan-timestamp">
                Last checked: {scanResult.details.lastChecked}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Recent Clone Detections */}
      <div className="threats-section animate-fade-in-up">
        <h3>Recent Clone Detections</h3>
        <div className="clone-list">
          {recentClones.map((clone, index) => (
            <div key={index} className="clone-item" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="clone-info">
                <div className="clone-details">
                  <span className="original-site">Original: {clone.original}</span>
                  <span className="clone-site">Clone: {clone.clone}</span>
                  <span className="clone-time">{clone.time}</span>
                </div>
                <div className="similarity-mini">
                  <span>{clone.similarity}% similar</span>
                  <div className="mini-bar">
                    <div 
                      className="mini-fill" 
                      style={{ 
                        width: `${clone.similarity}%`,
                        background: clone.similarity > 90 ? '#ef4444' : '#f59e0b'
                      }}
                    ></div>
                  </div>
                </div>
              </div>
              <div className={`status-badge status-${clone.status}`}>
                {clone.status.toUpperCase()}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ClonePage;
