require('dotenv').config();
const express = require('express');
const cors = require('cors');

const chatRoutes = require('./routes/chat');
const uploadRoutes = require('./routes/upload');
const personaRoutes = require('./routes/persona');
const authRoutes = require('./routes/auth');
const n8nRoutes = require('./routes/n8n');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Health check
app.get('/', (req, res) => {
  res.json({ status: 'ok', message: 'API is running' });
});

// API routes
app.use('/api/chat', chatRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/persona', personaRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/n8n', n8nRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
