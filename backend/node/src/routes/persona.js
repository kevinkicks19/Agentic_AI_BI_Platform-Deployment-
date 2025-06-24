const express = require('express');
const router = express.Router();

// GET /api/persona
router.get('/', (req, res) => {
  res.json({ persona: 'Persona endpoint placeholder' });
});

module.exports = router; 