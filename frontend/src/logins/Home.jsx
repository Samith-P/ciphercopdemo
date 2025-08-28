import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, Bug, Copy, DollarSign, Menu, X, Lock, Eye, Users, Zap, TrendingUp, Globe, CheckCircle } from 'lucide-react';
import PhishingPage from './PhishingPage';
import MalwarePage from './MalwarePage';
import ClonePage from './ClonePage';
import ScamPage from './ScamPage';
import './Home.css';
const Home = () => {
  const [activeSection, setActiveSection] = useState('home');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [animationKey, setAnimationKey] = useState(0);

  // Loading effect
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  // Trigger animations when section changes
  useEffect(() => {
    setAnimationKey(prev => prev + 1);
  }, [activeSection]);

  const sidebarItems = [
    { id: 'phishing', name: 'Phishing', icon: AlertTriangle },
    { id: 'malware', name: 'Malware Detection', icon: Bug },
    { id: 'clone', name: 'Clone Check', icon: Copy },
    { id: 'scam', name: 'Scam Check', icon: DollarSign }
  ];

  const features = [
    {
      icon: Shield,
      title: 'Advanced Threat Protection',
      description: 'Real-time monitoring and protection against cyber threats',
      gradient: 'from-blue-500 to-purple-600'
    },
    {
      icon: Eye,
      title: '24/7 Security Monitoring',
      description: 'Continuous surveillance of your digital assets',
      gradient: 'from-green-500 to-blue-500'
    },
    {
      icon: Users,
      title: 'Expert Security Team',
      description: 'Dedicated professionals ensuring your safety',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: Zap,
      title: 'Rapid Response',
      description: 'Instant alerts and immediate threat mitigation',
      gradient: 'from-yellow-500 to-red-500'
    }
  ];

  const stats = [
    { number: '99.9%', label: 'Uptime', icon: TrendingUp },
    { number: '24/7', label: 'Support', icon: Users },
    { number: '500K+', label: 'Protected Sites', icon: Globe },
    { number: '0', label: 'Breaches', icon: CheckCircle }
  ];

  const renderContent = () => {
    switch(activeSection) {
      case 'phishing':
        return <PhishingPage key={animationKey} />;
      case 'malware':
        return <MalwarePage key={animationKey} />;
      case 'clone':
        return <ClonePage key={animationKey} />;
      case 'scam':
        return <ScamPage key={animationKey} />;
      default:
        return (
          <div className="home-content">
            <div className="hero-section">
              <div className="hero-text animate-slide-in-left">
                <h1>Advanced Cybersecurity Solutions</h1>
                <p>Protect your digital assets with our comprehensive security platform. From phishing detection to malware analysis, we've got you covered.</p>
                <div className="hero-buttons">
                  <button className="btn-primary hover-scale">Get Started</button>
                  <button className="btn-secondary hover-scale">Learn More</button>
                </div>
              </div>
              <div className="hero-visual animate-slide-in-right">
                <div className="security-shield">
                  <Shield size={120} />
                  <div className="shield-rings">
                    <div className="ring ring-1"></div>
                    <div className="ring ring-2"></div>
                    <div className="ring ring-3"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="stats-section animate-fade-in-up">
              <div className="stats-grid">
                {stats.map((stat, index) => (
                  <div key={index} className="stat-item animate-count-up" style={{ animationDelay: `${index * 0.2}s` }}>
                    <stat.icon className="stat-icon" />
                    <div className="stat-number">{stat.number}</div>
                    <div className="stat-label">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="features-section">
              <h2 className="animate-slide-in-up">Why Choose Our Platform?</h2>
              <div className="features-grid">
                {features.map((feature, index) => (
                  <div 
                    key={index} 
                    className="feature-item animate-fade-in-up hover-lift" 
                    style={{ animationDelay: `${index * 0.15}s` }}
                  >
                    <div className={`feature-icon-wrapper bg-gradient-to-br ${feature.gradient}`}>
                      <feature.icon className="feature-icon" />
                    </div>
                    <h3>{feature.title}</h3>
                    <p>{feature.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <>
      {/* Loading Screen */}
      {isLoading && (
        <div className="loading-screen">
          <div className="loading-spinner">
            <Shield size={48} className="animate-spin" />
          </div>
          <div className="loading-text">Loading CyberShield...</div>
        </div>
      )}

      <div className={`app ${isLoading ? 'loading' : ''}`}>
        {/* Sidebar */}
        <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="logo animate-pulse">
            <Lock className="logo-icon" />
            <span>CyberShield</span>
          </div>
          <button 
            className="sidebar-toggle desktop-hidden"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={24} />
          </button>
        </div>
        
        <nav className="sidebar-nav">
          <ul>
            <li>
              <button
                className={`nav-item ${activeSection === 'home' ? 'active' : ''}`}
                onClick={() => {
                  setActiveSection('home');
                  setSidebarOpen(false);
                }}
              >
                <Shield className="nav-icon" />
                <span>Home</span>
              </button>
            </li>
            {sidebarItems.map((item) => (
              <li key={item.id}>
                <button
                  className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
                  onClick={() => {
                    setActiveSection(item.id);
                    setSidebarOpen(false);
                  }}
                >
                  <item.icon className="nav-icon" />
                  <span>{item.name}</span>
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <header className="header">
          <button 
            className="sidebar-toggle mobile-only"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu size={24} />
          </button>
          <div className="header-title">
            <h1>Cybersecurity Dashboard</h1>
          </div>
        </header>

        <main className="content">
          {renderContent()}
        </main>
      </div>

        {/* Overlay for mobile */}
        {sidebarOpen && <div className="overlay" onClick={() => setSidebarOpen(false)}></div>}
      </div>
    </>
  );
};

export default Home;