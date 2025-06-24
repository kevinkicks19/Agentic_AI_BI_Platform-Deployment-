/**
 * Sanitize user input for safe processing
 * @param {string} input
 * @returns {string}
 */
function sanitizeInput(input) {
  return String(input).replace(/[<>]/g, '').trim();
}

module.exports = { sanitizeInput };
