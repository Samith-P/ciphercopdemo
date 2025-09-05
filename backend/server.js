import express from "express";
import {signup,login,logout} from "./src/controller/auth.js";
import { connectDB } from "./src/lib/db.js";
import cookieParser from "cookie-parser"
import { protectRoute } from "./src/controller/tokengen.js";
import { phishingDetector } from "./src/checks/phishing.js";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();
const app = express();

app.use(
    cors({
        origin: ["http://localhost:5173", "http://localhost:5174"], 
        credentials: true, 
    })
);

app.get("/", (req, res) => {
    res.send("Hello World");
});
const router = express.Router();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.post("/signup", signup);
app.post("/login", login);
app.post("/logout", logout);
app.get('/checkAuth', protectRoute, (req, res) => {
    res.status(200).json({ message: 'User is authenticated', user: req.user });
});

app.get('/calldb', protectRoute, (req, res) => {
    res.status(200).json({ message: 'User is authenticated', user: req.user });
});

// Phishing detection endpoint
app.post('/api/phishing/analyze', protectRoute, async (req, res) => {
    try {
        const { url } = req.body;
        
        if (!url) {
            return res.status(400).json({ 
                error: 'URL is required',
                success: false 
            });
        }

        // Validate URL format - handle both full URLs and domain names
        let isValidInput = false;
        let inputUrl = url.trim();
        
        try {
            // Try parsing as full URL first
            new URL(inputUrl);
            isValidInput = true;
        } catch (urlError) {
            // If that fails, try adding protocol and parsing again
            try {
                new URL('http://' + inputUrl);
                isValidInput = true;
            } catch (protocolError) {
                // Check if it's a valid domain name pattern (more flexible)
                const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-._]*[a-zA-Z0-9]\.[a-zA-Z]{2,}(\/.*)?$/;
                if (domainRegex.test(inputUrl)) {
                    isValidInput = true;
                }
            }
        }
        
        if (!isValidInput) {
            return res.status(400).json({ 
                error: 'Invalid URL or domain format. Please enter a valid URL or domain name.',
                success: false 
            });
        }

        console.log(`Received URL analysis request for: ${inputUrl}`);

        // Perform phishing analysis
        const analysis = await phishingDetector.analyzeUrl(inputUrl);
        
        // Format response for frontend
        const response = {
            success: true,
            data: {
                url: analysis.url,
                domain: analysis.domain,
                isPhishing: analysis.isPhishing,
                threatLevel: analysis.threatLevel || 'low',
                riskScore: analysis.riskScore,
                combinedRiskScore: analysis.combinedRiskScore || analysis.riskScore,
                flags: analysis.flags,
                details: {
                    domainAge: analysis.details.domainAge || 'Unknown',
                    registrar: analysis.details.registrar || 'Unknown',
                    country: analysis.details.country || 'Unknown',
                    reputation: analysis.details.reputation,
                    similarDomains: analysis.details.similarDomains,
                    expiryDate: analysis.details.expiryDate,
                    nameServers: analysis.details.nameServers,
                    status: analysis.details.status,
                    privacyProtection: analysis.details.privacyProtection,
                    lastChecked: analysis.details.lastChecked
                },
                aiAnalysis: {
                    enabled: analysis.aiAnalysis !== null,
                    analysis: analysis.aiAnalysis,
                    riskScore: analysis.aiRiskScore,
                    recommendations: analysis.aiRecommendations || [],
                    insights: analysis.aiInsights || 'No AI insights available'
                },
                whoisData: analysis.whoisData
            }
        };

        res.status(200).json(response);
        
    } catch (error) {
        console.error('Phishing analysis error:', error);
        res.status(500).json({ 
            error: 'Analysis failed: ' + error.message,
            success: false 
        });
    }
});

// Email content analysis endpoint
app.post('/api/phishing/analyze-email', protectRoute, async (req, res) => {
    try {
        const { content } = req.body;
        
        if (!content) {
            return res.status(400).json({ 
                error: 'Email content is required',
                success: false 
            });
        }

        // Simple email analysis (can be enhanced)
        const analysis = analyzeEmailContent(content);
        
        res.status(200).json({
            success: true,
            data: analysis
        });
        
    } catch (error) {
        console.error('Email analysis error:', error);
        res.status(500).json({ 
            error: 'Email analysis failed: ' + error.message,
            success: false 
        });
    }
});

// Simple email content analysis function
function analyzeEmailContent(content) {
    const suspiciousKeywords = [
        'urgent', 'verify', 'suspend', 'confirm', 'click here',
        'act now', 'limited time', 'expire', 'account locked',
        'security alert', 'update payment', 'congratulations'
    ];
    
    const phishingIndicators = [
        'bit.ly', 'tinyurl', 'suspicious-bank', 'paypal-security',
        'amazon-verify', 'microsoft-update', 'apple-id'
    ];
    
    let suspiciousScore = 0;
    const flags = [];
    const contentLower = content.toLowerCase();
    
    // Check for suspicious keywords
    suspiciousKeywords.forEach(keyword => {
        if (contentLower.includes(keyword)) {
            flags.push(`Suspicious keyword: ${keyword}`);
            suspiciousScore += 10;
        }
    });
    
    // Check for phishing indicators
    phishingIndicators.forEach(indicator => {
        if (contentLower.includes(indicator)) {
            flags.push(`Phishing indicator: ${indicator}`);
            suspiciousScore += 20;
        }
    });
    
    // Check for suspicious links count
    const linkCount = (content.match(/https?:\/\/[^\s]+/g) || []).length;
    if (linkCount > 3) {
        flags.push(`Multiple links detected: ${linkCount}`);
        suspiciousScore += 15;
    }
    
    // Determine threat level
    let threatLevel = 'safe';
    if (suspiciousScore >= 50) {
        threatLevel = 'high';
    } else if (suspiciousScore >= 25) {
        threatLevel = 'medium';
    }
    
    return {
        threatLevel,
        riskScore: Math.min(suspiciousScore, 100),
        flags,
        details: {
            suspiciousKeywords: flags.filter(f => f.includes('keyword')).length,
            phishingIndicators: flags.filter(f => f.includes('indicator')).length,
            linkCount,
            contentLength: content.length,
            lastChecked: new Date().toISOString()
        }
    };
}

const PORT = 5001; 

const server = app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    connectDB();
});

server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.log(`Port ${PORT} is busy, trying port ${PORT + 1}...`);
        const newPort = PORT + 1;
        app.listen(newPort, () => {
            console.log(`Server running at http://localhost:${newPort}/`);
            connectDB();
        });
    } else {
        console.error('Server error:', err);
    }
});
