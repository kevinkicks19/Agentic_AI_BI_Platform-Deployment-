const express = require('express');
const { triggerN8nAgent } = require('../coordinator');
const router = express.Router();

// POST /api/n8n
router.post('/', async (req, res) => {
  try {
    const { webhookUrl, params, method } = req.body;
    if (!webhookUrl) return res.status(400).json({ error: 'webhookUrl is required' });
    const result = await triggerN8nAgent(webhookUrl, params || {}, method || 'GET');
    res.json({ result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router; 