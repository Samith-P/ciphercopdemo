import React, { useState } from 'react';
import { AlertTriangle, Mail, Link, Shield, Search, FileText, Activity, TrendingUp, Users, CheckCircle } from 'lucide-react';

const PhishingPage = () => {
  const [url, setUrl] = useState('');
  const [emailContent, setEmailContent] = useState('');
  const [scanResult, setScanResult] = useState(null);
  const [isScanning, setIsScanning] = useState(false);

  const handleUrlScan = async () => {
    if (!url) return;
    setIsScanning(true);
    setScanResult(null);
    
    try {
      const response = await fetch('http://localhost:5001/api/phishing/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ url })
      });

      const data = await response.json();
      
      if (data.success) {
        setScanResult({
          type: 'url',
          threat: data.data.threatLevel,
          isPhishing: data.data.isPhishing,
          riskScore: data.data.riskScore,
          combinedRiskScore: data.data.combinedRiskScore,
          flags: data.data.flags,
          details: {
            domain: data.data.domain,
            reputation: data.data.details.reputation,
            similarSites: data.data.details.similarDomains,
            domainAge: data.data.details.domainAge,
            registrar: data.data.details.registrar,
            country: data.data.details.country,
            expiryDate: data.data.details.expiryDate,
            nameServers: data.data.details.nameServers,
            status: data.data.details.status,
            privacyProtection: data.data.details.privacyProtection,
            lastChecked: data.data.details.lastChecked
          },
          aiAnalysis: {
            enabled: data.data.aiAnalysis.enabled,
            analysis: data.data.aiAnalysis.analysis,
            riskScore: data.data.aiAnalysis.riskScore,
            recommendations: data.data.aiAnalysis.recommendations,
            insights: data.data.aiAnalysis.insights
          }
        });
      } else {
        throw new Error(data.error || 'Analysis failed');
      }
    } catch (error) {
      console.error('URL scan error:', error);
      setScanResult({
        type: 'url',
        threat: 'error',
        error: error.message,
        details: {
          domain: url,
          lastChecked: new Date().toLocaleString()
        }
      });
    } finally {
      setIsScanning(false);
    }
  };

  const handleEmailScan = async () => {
    if (!emailContent) return;
    setIsScanning(true);
    setScanResult(null);
    
    try {
      const response = await fetch('http://localhost:5002/api/phishing/analyze-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ content: emailContent })
      });

      const data = await response.json();
      
      if (data.success) {
        setScanResult({
          type: 'email',
          threat: data.data.threatLevel,
          riskScore: data.data.riskScore,
          flags: data.data.flags,
          details: {
            suspiciousLinks: data.data.details.linkCount,
            suspiciousKeywords: data.data.details.suspiciousKeywords,
            phishingIndicators: data.data.details.phishingIndicators,
            contentLength: data.data.details.contentLength,
            senderReputation: Math.floor(Math.random() * 100), // Mock data
            contentAnalysis: 'Analyzed for suspicious patterns',
            lastChecked: data.data.details.lastChecked
          }
        });
      } else {
        throw new Error(data.error || 'Email analysis failed');
      }
    } catch (error) {
      console.error('Email scan error:', error);
      setScanResult({
        type: 'email',
        threat: 'error',
        error: error.message,
        details: {
          lastChecked: new Date().toLocaleString()
        }
      });
    } finally {
      setIsScanning(false);
    }
  };

  const stats = [
    { icon: Shield, label: 'Threats Blocked', value: '2.3M+', color: 'text-green-400' },
    { icon: AlertTriangle, label: 'Phishing Attempts', value: '847K', color: 'text-red-400' },
    { icon: Users, label: 'Protected Users', value: '150K+', color: 'text-blue-400' },
    { icon: TrendingUp, label: 'Success Rate', value: '99.7%', color: 'text-purple-400' }
  ];

  const recentThreats = [
    { domain: 'fake-bank-login.com', threat: 'high', time: '2 minutes ago' },
    { domain: 'phishing-paypal.net', threat: 'high', time: '5 minutes ago' },
    { domain: 'suspicious-amazon.org', threat: 'medium', time: '12 minutes ago' },
    { domain: 'fake-microsoft.co', threat: 'high', time: '18 minutes ago' }
  ];

  return (
    <div className="phishing-page">
      <div className="page-header animate-fade-in">
        <div className="header-content">
          <div className="header-icon">
            <AlertTriangle size={48} className="animate-pulse" />
          </div>
          <div className="header-text">
            <h1>Phishing Protection</h1>
            <p>Advanced detection and prevention against phishing attacks</p>
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
          {/* URL Scanner */}
          <div className="scan-card animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <div className="scan-header">
              <Link className="scan-icon" />
              <h3>URL Scanner</h3>
            </div>
            <div className="scan-content">
              <input
                type="url"
                placeholder="Enter URL to scan (e.g., https://example.com)"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="scan-input"
              />
              <button 
                onClick={handleUrlScan}
                disabled={!url || isScanning}
                className="scan-button"
              >
                {isScanning ? (
                  <Activity className="animate-spin" />
                ) : (
                  <Search />
                )}
                {isScanning ? 'Scanning...' : 'Scan URL'}
              </button>
            </div>
          </div>

          {/* Email Scanner */}
          <div className="scan-card animate-slide-up" style={{ animationDelay: '0.3s' }}>
            <div className="scan-header">
              <Mail className="scan-icon" />
              <h3>Email Content Scanner</h3>
            </div>
            <div className="scan-content">
              <textarea
                placeholder="Paste email content here to analyze for phishing attempts..."
                value={emailContent}
                onChange={(e) => setEmailContent(e.target.value)}
                className="scan-textarea"
                rows={4}
              />
              <button 
                onClick={handleEmailScan}
                disabled={!emailContent || isScanning}
                className="scan-button"
              >
                {isScanning ? (
                  <Activity className="animate-spin" />
                ) : (
                  <FileText />
                )}
                {isScanning ? 'Analyzing...' : 'Analyze Email'}
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
              <h3>Scan Results</h3>
              <div className={`threat-badge threat-${
                scanResult.threat === 'error' ? 'high' : 
                scanResult.aiAnalysis?.enabled && scanResult.aiAnalysis.riskScore ? 
                  (scanResult.aiAnalysis.riskScore >= 70 ? 'high' : 
                   scanResult.aiAnalysis.riskScore >= 40 ? 'medium' : 'low') :
                scanResult.threat
              }`}>
                {scanResult.threat === 'error' ? (
                  <AlertTriangle size={16} />
                ) : (scanResult.aiAnalysis?.enabled && scanResult.aiAnalysis.riskScore ? 
                    (scanResult.aiAnalysis.riskScore >= 70 ? <AlertTriangle size={16} /> :
                     scanResult.aiAnalysis.riskScore >= 40 ? <AlertTriangle size={16} /> : <CheckCircle size={16} />) :
                    (scanResult.threat === 'safe' || scanResult.threat === 'low' ? <CheckCircle size={16} /> : <AlertTriangle size={16} />)
                )}
                {scanResult.threat === 'error' ? 'ERROR' : 
                 scanResult.aiAnalysis?.enabled && scanResult.aiAnalysis.riskScore ? 
                   (scanResult.aiAnalysis.riskScore >= 70 ? 'HIGH' : 
                    scanResult.aiAnalysis.riskScore >= 40 ? 'MEDIUM' : 'LOW') :
                 scanResult.threat.toUpperCase()}
              </div>
            </div>
            <div className="results-content">
              {scanResult.error ? (
                <div className="error-message">
                  <AlertTriangle size={24} className="error-icon" />
                  <div>
                    <h4>Analysis Failed</h4>
                    <p>{scanResult.error}</p>
                  </div>
                </div>
              ) : (
                <>
                  {scanResult.flags && scanResult.flags.length > 0 && (
                    <div className="flags-section">
                      <h4>Security Flags</h4>
                      <div className="flags-list">
                        {scanResult.flags.map((flag, index) => (
                          <div key={index} className="flag-item">
                            <AlertTriangle size={14} />
                            {flag}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {scanResult.type === 'url' && (
                    <div className="result-details">
                      <div className="detail-item">
                        <span className="detail-label">Domain:</span>
                        <span className="detail-value">{scanResult.details.domain}</span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Reputation Score:</span>
                        <span className="detail-value">{scanResult.details.reputation}/100</span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Similar Suspicious Sites:</span>
                        <span className="detail-value">{scanResult.details.similarSites}</span>
                      </div>
                      {scanResult.details.domainAge && (
                        <div className="detail-item">
                          <span className="detail-label">Domain Age:</span>
                          <span className="detail-value">{scanResult.details.domainAge}</span>
                        </div>
                      )}
                      {scanResult.details.registrar && (
                        <div className="detail-item">
                          <span className="detail-label">Registrar:</span>
                          <span className="detail-value">{scanResult.details.registrar}</span>
                        </div>
                      )}
                      {scanResult.details.country && (
                        <div className="detail-item">
                          <span className="detail-label">Country:</span>
                          <span className="detail-value">{scanResult.details.country}</span>
                        </div>
                      )}
                      {scanResult.details.expiryDate && (
                        <div className="detail-item">
                          <span className="detail-label">Expiry Date:</span>
                          <span className="detail-value">{new Date(scanResult.details.expiryDate).toLocaleDateString()}</span>
                        </div>
                      )}
                      {scanResult.details.nameServers && (
                        <div className="detail-item">
                          <span className="detail-label">Name Servers:</span>
                          <span className="detail-value">{scanResult.details.nameServers}</span>
                        </div>
                      )}
                      {scanResult.details.status && (
                        <div className="detail-item">
                          <span className="detail-label">Domain Status:</span>
                          <span className="detail-value">{scanResult.details.status}</span>
                        </div>
                      )}
                      {scanResult.details.privacyProtection && (
                        <div className="detail-item">
                          <span className="detail-label">Privacy Protection:</span>
                          <span className="detail-value">Enabled</span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* AI Analysis Section */}
                  {scanResult.aiAnalysis && (
                    <div className="ai-analysis-section">
                      <div className="ai-header">
                        <h4>🤖 AI Security Analysis</h4>
                        {scanResult.aiAnalysis.enabled && scanResult.aiAnalysis.analysis?.confidence && (
                          <div className="ai-confidence-badge">
                            Confidence: {scanResult.aiAnalysis.analysis.confidence}%
                          </div>
                        )}
                      </div>
                      
                      {scanResult.aiAnalysis.enabled ? (
                        <div className="ai-content">
                          {/* AI Risk Score */}
                          {scanResult.aiAnalysis.riskScore && (
                            <div className="ai-risk-score-container">
                              <h5>📊 AI Risk Assessment</h5>
                              <div className="ai-risk-score">
                                <div className="score-item ai">
                                  <div className="score-label">AI Risk Score</div>
                                  <div className="score-value">{scanResult.aiAnalysis.riskScore}/100</div>
                                  <div className="score-bar">
                                    <div 
                                      className="score-fill ai-fill" 
                                      style={{ 
                                        width: `${scanResult.aiAnalysis.riskScore}%`,
                                        background: scanResult.aiAnalysis.riskScore > 70 ? '#ef4444' : 
                                                   scanResult.aiAnalysis.riskScore > 40 ? '#f59e0b' : '#10b981'
                                      }}
                                    ></div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          )}
                          
                          {/* AI Risk Factors */}
                          {scanResult.aiAnalysis.analysis?.riskFactors && scanResult.aiAnalysis.analysis.riskFactors.length > 0 && (
                            <div className="ai-risk-factors-container">
                              <h5>⚠️ Risk Factors Identified</h5>
                              <div className="ai-risk-factors">
                                {scanResult.aiAnalysis.analysis.riskFactors.map((factor, index) => (
                                  <div key={index} className="risk-factor-item">
                                    <div className="risk-factor-icon">⚠️</div>
                                    <div className="risk-factor-text">{factor}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                          
                          {/* Legitimacy Indicators */}
                          {scanResult.aiAnalysis.analysis?.legitimacyIndicators && scanResult.aiAnalysis.analysis.legitimacyIndicators.length > 0 && (
                            <div className="ai-legitimacy-container">
                              <h5>✅ Legitimacy Indicators</h5>
                              <div className="ai-legitimacy-indicators">
                                {scanResult.aiAnalysis.analysis.legitimacyIndicators.map((indicator, index) => (
                                  <div key={index} className="legitimacy-indicator-item">
                                    <div className="legitimacy-indicator-icon">✅</div>
                                    <div className="legitimacy-indicator-text">{indicator}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                          
                          {/* AI Insights */}
                          {scanResult.aiAnalysis.insights && (
                            <div className="ai-insights-container">
                              <h5>🧠 AI Insights</h5>
                              <div className="ai-insights-content">
                                <p>{scanResult.aiAnalysis.insights}</p>
                              </div>
                            </div>
                          )}
                          
                          {/* AI Recommendations */}
                          {scanResult.aiAnalysis.recommendations && scanResult.aiAnalysis.recommendations.length > 0 && (
                            <div className="ai-recommendations-container">
                              <h5>💡 AI Recommendations</h5>
                              <div className="ai-recommendations">
                                {scanResult.aiAnalysis.recommendations.map((rec, index) => (
                                  <div key={index} className="recommendation-item">
                                    <div className="recommendation-icon">💡</div>
                                    <div className="recommendation-text">{rec}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                          
                          {/* Technical Summary */}
                          {scanResult.aiAnalysis.analysis?.technicalInsights && (
                            <div className="ai-technical-container">
                              <h5>🔧 Technical Analysis</h5>
                              <div className="ai-technical-content">
                                <p>{scanResult.aiAnalysis.analysis.technicalInsights}</p>
                              </div>
                            </div>
                          )}
                        </div>
                      ) : (
                        <div className="ai-disabled">
                          <div className="ai-disabled-content">
                            <div className="ai-disabled-icon">🔒</div>
                            <div className="ai-disabled-text">
                              <h5>AI Analysis Unavailable</h5>
                              <p>Add Gemini API key to enable enhanced AI-powered threat analysis.</p>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                  
                  {scanResult.type === 'email' && (
                    <div className="result-details">
                      <div className="detail-item">
                        <span className="detail-label">Suspicious Links:</span>
                        <span className="detail-value">{scanResult.details.suspiciousLinks || 0}</span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Suspicious Keywords:</span>
                        <span className="detail-value">{scanResult.details.suspiciousKeywords || 0}</span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Phishing Indicators:</span>
                        <span className="detail-value">{scanResult.details.phishingIndicators || 0}</span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Content Length:</span>
                        <span className="detail-value">{scanResult.details.contentLength} characters</span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Sender Reputation:</span>
                        <span className="detail-value">{scanResult.details.senderReputation}/100</span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Content Analysis:</span>
                        <span className="detail-value">{scanResult.details.contentAnalysis}</span>
                      </div>
                    </div>
                  )}
                </>
              )}
              <div className="scan-timestamp">
                Last checked: {scanResult.details.lastChecked}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Recent Threats */}
      <div className="threats-section animate-fade-in-up">
        <h3>Recent Threats Detected</h3>
        <div className="threats-list">
          {recentThreats.map((threat, index) => (
            <div key={index} className="threat-item" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="threat-info">
                <span className="threat-domain">{threat.domain}</span>
                <span className="threat-time">{threat.time}</span>
              </div>
              <div className={`threat-level threat-${threat.threat}`}>
                <AlertTriangle size={16} />
                {threat.threat.toUpperCase()}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PhishingPage;
