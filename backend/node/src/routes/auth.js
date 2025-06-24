const express = require('express');
const router = express.Router();

// POST /api/auth/login
router.post('/login', (req, res) => {
  res.json({ message: 'Auth login endpoint placeholder' });
});

module.exports = router; 