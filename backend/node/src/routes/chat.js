const express = require('express');
const router = express.Router();
const { Coordinator } = require('../coordinator');

// POST /api/chat
router.post('/', async (req, res) => {
  try {
    const { message } = req.body;
    const userId = req.session?.userId || 'default';

    const response = await Coordinator.processMessage(userId, message);
    
    res.json(response);
  } catch (error) {
    console.error('Error in chat route:', error);
    res.status(500).json({
      message: 'An error occurred while processing your request.',
      error: error.message
    });
  }
});

module.exports = router; 