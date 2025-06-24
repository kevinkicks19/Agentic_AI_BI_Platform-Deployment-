const express = require('express');
const router = express.Router();
const { chatWithN8nAgent } = require('../coordinator/n8n');

// POST /api/chat/n8n
router.post('/n8n', async (req, res) => {
  const { sessionId, message } = req.body;
  try {
    const reply = await chatWithN8nAgent(sessionId, message);
    res.json({ success: true, reply });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router; 