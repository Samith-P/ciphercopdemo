import React, { useState } from 'react';
import { Copy, Search, Globe, AlertTriangle, CheckCircle, TrendingUp, Users, Upload, Eye, FileImage, X } from 'lucide-react';

const ClonePage = () => {
  const [url, setUrl] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [scanResult, setScanResult] = useState(null);
  const [isScanning, setIsScanning] = useState(false);

  // Helper function to extract and clean explanation text
  const extractExplanation = (explanation) => {
    if (!explanation) return '';
    
    // Try to extract JSON and get the explanation field
    try {
      // Remove code fences if present
      let cleanText = explanation.replace(/```json\s*/g, '').replace(/```\s*/g, '');
      
      // Try to find JSON object
      const jsonMatch = cleanText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        return parsed.explanation || cleanText;
      }
    } catch (e) {
      // If parsing fails, return the original text cleaned up
    }
    
    // Clean up the text by removing incomplete JSON
    return explanation.replace(/```json\s*/g, '').replace(/```\s*/g, '').replace(/\{[\s\S]*$/, '').trim();
  };

  // Helper function to extract suspected brand from explanation
  const extractSuspectedBrand = (explanation) => {
    if (!explanation) return '';
    
    try {
      // Remove code fences if present
      let cleanText = explanation.replace(/```json\s*/g, '').replace(/```\s*/g, '');
      
      // Try to find JSON object
      const jsonMatch = cleanText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        return parsed.suspected_brand || '';
      }
    } catch (e) {
      // If parsing fails, return empty
    }
    
    return '';
  };

  // Helper function to extract Gemini likelihood
  const extractGeminiLikelihood = (explanation) => {
    if (!explanation) return null;
    
    try {
      // Remove code fences if present
      let cleanText = explanation.replace(/```json\s*/g, '').replace(/```\s*/g, '');
      
      // Try to find JSON object
      const jsonMatch = cleanText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        return parsed.likelihood || null;
      }
    } catch (e) {
      // If parsing fails, return null
    }
    
    return null;
  };

  const handleUrlCheck = async () => {
    if (!url) return;
    setIsScanning(true);
    setScanResult(null);
    
    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url })
      });

      const data = await response.json();
      
      if (response.ok) {
        setScanResult({
          type: 'url',
          target: url,
          decision: data.decision,
          score: data.score,
          advice: data.advice,
          explanation: data.explanation,
          signals: data.signals,
          breakdown: data.breakdown,
          details: {
            lastChecked: new Date().toLocaleString()
          }
        });
      } else {
        throw new Error(data.error || 'Analysis failed');
      }
    } catch (error) {
      console.error('URL analysis error:', error);
      setScanResult({
        type: 'url',
        target: url,
        error: error.message,
        details: {
          lastChecked: new Date().toLocaleString()
        }
      });
    } finally {
      setIsScanning(false);
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && (file.type.startsWith('image/') || file.type === 'application/pdf')) {
      setSelectedFile(file);
    } else {
      alert('Please select an image file (PNG, JPG, JPEG) or PDF');
    }
  };

  const handleScreenshotAnalysis = async () => {
    if (!selectedFile) return;
    setIsScanning(true);
    setScanResult(null);
    
    try {
      const formData = new FormData();
      formData.append('screenshot', selectedFile);
      
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      
      if (response.ok) {
        setScanResult({
          type: 'screenshot',
          target: selectedFile.name,
          decision: data.decision,
          score: data.score,
          advice: data.advice,
          explanation: data.explanation,
          signals: data.signals,
          breakdown: data.breakdown,
          details: {
            fileSize: (selectedFile.size / 1024).toFixed(2) + ' KB',
            lastChecked: new Date().toLocaleString()
          }
        });
      } else {
        throw new Error(data.error || 'Analysis failed');
      }
    } catch (error) {
      console.error('Screenshot analysis error:', error);
      setScanResult({
        type: 'screenshot',
        target: selectedFile.name,
        error: error.message,
        details: {
          lastChecked: new Date().toLocaleString()
        }
      });
    } finally {
      setIsScanning(false);
    }
  };

  const removeSelectedFile = () => {
    setSelectedFile(null);
  };

  const stats = [
    { icon: Eye, label: 'Sites Analyzed', value: '2.8M+', color: 'text-blue-400' },
    { icon: Copy, label: 'Clones Detected', value: '156K', color: 'text-red-400' },
    { icon: FileImage, label: 'Screenshots Processed', value: '890K+', color: 'text-green-400' },
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
                {isScanning ? 'Analyzing...' : 'Analyze URL'}
              </button>
            </div>
          </div>

          {/* Screenshot Upload */}
          <div className="scan-card animate-slide-up" style={{ animationDelay: '0.3s' }}>
            <div className="scan-header">
              <FileImage className="scan-icon" />
              <h3>Screenshot Analysis</h3>
            </div>
            <div className="scan-content">
              {!selectedFile ? (
                <div className="file-upload-area">
                  <input
                    type="file"
                    id="screenshot-input"
                    onChange={handleFileSelect}
                    className="file-input"
                    accept="image/*,.pdf"
                    style={{ display: 'none' }}
                  />
                  <label htmlFor="screenshot-input" className="file-upload-label">
                    <Upload size={32} />
                    <span>Upload Website Screenshot</span>
                    <small>PNG, JPG, JPEG or PDF files supported</small>
                  </label>
                </div>
              ) : (
                <div className="selected-file">
                  <div className="file-info">
                    <FileImage size={24} />
                    <div className="file-details">
                      <span className="file-name">{selectedFile.name}</span>
                      <span className="file-size">{(selectedFile.size / 1024).toFixed(2)} KB</span>
                    </div>
                    <button onClick={removeSelectedFile} className="remove-file">
                      <X size={16} />
                    </button>
                  </div>
                  <button 
                    onClick={handleScreenshotAnalysis}
                    disabled={isScanning}
                    className="scan-button"
                  >
                    {isScanning ? (
                      <Copy className="animate-spin" />
                    ) : (
                      <Search />
                    )}
                    {isScanning ? 'Analyzing...' : 'Analyze Screenshot'}
                  </button>
                </div>
              )}
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
              {scanResult.error ? (
                <div className="threat-badge threat-error">
                  <AlertTriangle size={16} />
                  ERROR
                </div>
              ) : (
                <div className={`threat-badge threat-${scanResult.decision} ${
                  extractGeminiLikelihood(scanResult.explanation) >= 90 ? 'high-confidence' : ''
                }`}>
                  {scanResult.decision === 'clone' ? <AlertTriangle size={16} /> : <CheckCircle size={16} />}
                  {scanResult.decision?.toUpperCase() || 'ANALYZED'}
                  {extractGeminiLikelihood(scanResult.explanation) >= 90 && (
                    <span className="confidence-indicator">
                      {extractGeminiLikelihood(scanResult.explanation)}% CONFIDENCE
                    </span>
                  )}
                </div>
              )}
            </div>
            <div className="results-content">
              {scanResult.error ? (
                <div className="error-message">
                  <p>Analysis failed: {scanResult.error}</p>
                </div>
              ) : (
                <>
                  {/* Risk Score */}
                  <div className="risk-score-section">
                    <div className="risk-score-header">
                      <span className="risk-label">Risk Score</span>
                      <span className="risk-value">{scanResult.score}/100</span>
                    </div>
                    <div className="risk-bar">
                      <div 
                        className="risk-fill" 
                        style={{ 
                          width: `${scanResult.score}%`,
                          background: scanResult.score >= 60 ? '#ef4444' : scanResult.score >= 30 ? '#f59e0b' : '#10b981'
                        }}
                      ></div>
                    </div>
                    <div className="risk-advice">{scanResult.advice}</div>
                  </div>

                  {/* Gemini AI Highlights */}
                  {scanResult.explanation && (
                    <div className="gemini-highlights-section">
                      <div className="gemini-header">
                        <h4>🤖 AI Detection Results</h4>
                      </div>
                      <div className="gemini-stats">
                        {extractGeminiLikelihood(scanResult.explanation) && (
                          <div className="gemini-stat">
                            <span className="gemini-stat-label">AI Confidence</span>
                            <span className="gemini-stat-value">
                              {extractGeminiLikelihood(scanResult.explanation)}%
                            </span>
                            <div className="gemini-stat-bar">
                              <div 
                                className="gemini-stat-fill"
                                style={{ 
                                  width: `${extractGeminiLikelihood(scanResult.explanation)}%`,
                                  background: extractGeminiLikelihood(scanResult.explanation) >= 70 ? '#ef4444' : 
                                           extractGeminiLikelihood(scanResult.explanation) >= 40 ? '#f59e0b' : '#10b981'
                                }}
                              ></div>
                            </div>
                          </div>
                        )}
                        {extractSuspectedBrand(scanResult.explanation) && (
                          <div className="gemini-stat">
                            <span className="gemini-stat-label">Detected Brand</span>
                            <span className="suspected-brand-tag">
                              {extractSuspectedBrand(scanResult.explanation)}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* AI Explanation */}
                  {scanResult.explanation && (
                    <div className="explanation-section">
                      <h4>📝 Detailed Analysis</h4>
                      <p>{extractExplanation(scanResult.explanation)}</p>
                    </div>
                  )}

                  {/* Detection Breakdown */}
                  {scanResult.breakdown && (
                    <div className="breakdown-section">
                      <h4>📊 Detection Breakdown</h4>
                      <div className="breakdown-grid">
                        {Object.entries(scanResult.breakdown).map(([key, value]) => (
                          <div key={key} className="breakdown-item">
                            <span className="breakdown-label">{key.replace('_', ' ').toUpperCase()}</span>
                            <span className="breakdown-value">{value}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Detailed Signals */}
                  {scanResult.signals && (
                    <div className="signals-section">
                      <h4>🔍 Detection Signals</h4>
                      
                      {/* Heuristics */}
                      {scanResult.signals.heuristics && (
                        <div className="signal-group">
                          <h5>Heuristic Analysis</h5>
                          <div className="signal-details">
                            <div className="signal-item">
                              <span>Risk Score:</span>
                              <span>{scanResult.signals.heuristics.risk}/100</span>
                            </div>
                            <div className="signal-item">
                              <span>Domain:</span>
                              <span>{scanResult.signals.heuristics.host}</span>
                            </div>
                            {scanResult.signals.heuristics.signals && Object.keys(scanResult.signals.heuristics.signals).length > 0 && (
                              <div className="signal-flags">
                                <span>Flags:</span>
                                <div className="flags-list">
                                  {Object.entries(scanResult.signals.heuristics.signals).map(([flag, value]) => 
                                    value && <span key={flag} className="flag">{flag.replace('_', ' ')}</span>
                                  )}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Vision Analysis */}
                      {scanResult.signals.vision && (
                        <div className="signal-group">
                          <h5>Visual Analysis</h5>
                          <div className="signal-details">
                            {scanResult.signals.vision.logos && scanResult.signals.vision.logos.length > 0 && (
                              <div className="signal-item">
                                <span>Detected Brands:</span>
                                <div className="detected-brands">
                                  {scanResult.signals.vision.logos.map((logo, index) => (
                                    <span key={index} className="brand-tag">
                                      {logo.description} ({(logo.score * 100).toFixed(1)}%)
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}
                            {scanResult.signals.vision.text && (
                              <div className="signal-item">
                                <span>Extracted Text:</span>
                                <span className="extracted-text">{scanResult.signals.vision.text.substring(0, 200)}...</span>
                              </div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Gemini Analysis */}
                      {scanResult.signals.gemini && (
                        <div className="signal-group">
                          <h5>AI Analysis</h5>
                          <div className="signal-details">
                            <div className="signal-item">
                              <span>Likelihood:</span>
                              <span>{scanResult.signals.gemini.likelihood}%</span>
                            </div>
                            {/* Show suspected brand from either the main field or parsed explanation */}
                            {(scanResult.signals.gemini.suspected_brand || 
                              (scanResult.explanation && extractSuspectedBrand(scanResult.explanation))) && (
                              <div className="signal-item">
                                <span>Suspected Brand:</span>
                                <span className="brand-tag">
                                  {scanResult.signals.gemini.suspected_brand || 
                                   extractSuspectedBrand(scanResult.explanation)}
                                </span>
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </>
              )}
              
              <div className="result-details">
                <div className="detail-item">
                  <span className="detail-label">Target:</span>
                  <span className="detail-value">{scanResult.target}</span>
                </div>
                {scanResult.type === 'screenshot' && scanResult.details.fileSize && (
                  <div className="detail-item">
                    <span className="detail-label">File Size:</span>
                    <span className="detail-value">{scanResult.details.fileSize}</span>
                  </div>
                )}
                <div className="detail-item">
                  <span className="detail-label">Analysis Type:</span>
                  <span className="detail-value">{scanResult.type === 'screenshot' ? 'Screenshot Analysis' : 'URL Analysis'}</span>
                </div>
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
