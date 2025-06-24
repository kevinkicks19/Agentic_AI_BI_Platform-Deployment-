const axios = require('axios');
const N8N_BASE_URL = process.env.N8N_BASE_URL;
const N8N_API_KEY = process.env.N8N_API_KEY;

const WORKFLOW_ENDPOINTS = {
  test: '/webhook/start-test', // adjust to your n8n workflow
  // ...other workflows
};

async function triggerWorkflow(type, data) {
  const endpoint = WORKFLOW_ENDPOINTS[type];
  const response = await axios.post(`${N8N_BASE_URL}${endpoint}`, data, {
    headers: {
      'Content-Type': 'application/json',
      'X-N8N-API-KEY': N8N_API_KEY
    }
  });
  return response.data;
}

async function chatWithN8nAgent(sessionId, message) {
  const response = await axios.post(`${N8N_BASE_URL}/webhook/chat-n8n`, { sessionId, message }, {
    headers: {
      'Content-Type': 'application/json',
      'X-N8N-API-KEY': N8N_API_KEY
    }
  });
  return response.data.reply;
}

module.exports = { triggerWorkflow, chatWithN8nAgent }; 