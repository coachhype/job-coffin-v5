const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.static('public'));

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        version: '5.0.0',
        service: 'Job Coffin V5'
    });
});

// Main route
app.get('/', (req, res) => {
    res.json({
        message: 'Welcome to Job Coffin V5 - Voice-First Job Search for ADHD Professionals',
        version: '5.0.0',
        features: [
            'Voice-first interface',
            'ADHD-optimized design', 
            'Crisis intervention support',
            'Achievement system',
            'Instant application'
        ],
        endpoints: {
            health: '/health',
            api: '/api/v1'
        }
    });
});

// API routes
app.get('/api/v1/status', (req, res) => {
    res.json({
        api_version: '1.0.0',
        status: 'operational',
        features_enabled: true
    });
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).json({ error: 'Route not found' });
});

// CRITICAL: Bind to 0.0.0.0 for Railway compatibility (not localhost!)
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Job Coffin V5 server running on http://0.0.0.0:${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`Health check: http://0.0.0.0:${PORT}/health`);
});
