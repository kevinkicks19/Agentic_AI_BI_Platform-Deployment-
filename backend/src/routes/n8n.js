const express = require('express');
const router = express.Router();
const { triggerWorkflow } = require('../coordinator/n8n');
const { v4: uuidv4 } = require('uuid');

// POST /api/workflow/test
router.post('/test', async (req, res) => {
  try {
    const sessionId = uuidv4();
    const result = await triggerWorkflow('test', { sessionId, ...req.body });
    res.json({ success: true, sessionId, result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router; 