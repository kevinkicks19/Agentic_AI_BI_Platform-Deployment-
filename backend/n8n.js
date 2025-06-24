const axios = require('axios');

/**
 * Call an n8n workflow via HTTP POST
 * @param {string} workflowUrl - The n8n webhook URL
 * @param {object} payload - Data to send to the workflow
 * @returns {Promise<any>} - The workflow response
 */
async function callN8nWorkflow(workflowUrl, payload) {
  try {
    const response = await axios.post(workflowUrl, payload);
    return response.data;
  } catch (error) {
    console.error('n8n workflow error:', error.response?.data || error.message);
    throw error;
  }
}

module.exports = { callN8nWorkflow };
