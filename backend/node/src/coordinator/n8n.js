const axios = require('axios');

/**
 * Configuration for n8n connection
 * @type {Object}
 */
const n8nConfig = {
  baseUrl: process.env.N8N_BASE_URL || 'http://localhost:5678',
  apiKey: process.env.N8N_API_KEY,
  webhookBaseUrl: process.env.N8N_WEBHOOK_BASE_URL
};

// Debug log configuration
console.log('N8N Configuration:', {
  baseUrl: n8nConfig.baseUrl,
  webhookBaseUrl: n8nConfig.webhookBaseUrl,
  hasApiKey: !!n8nConfig.apiKey
});

/**
 * Call an n8n workflow via webhook
 * @param {string} workflowId - The n8n workflow ID or webhook URL
 * @param {object} payload - Data to send to the workflow
 * @param {object} [options] - Additional options
 * @returns {Promise<any>} - The workflow response
 */
async function callN8nWorkflow(workflowId, payload = {}, options = {}) {
  try {
    // Use the workflowId directly as the URL since it's now a full webhook URL
    const url = new URL(workflowId);
    
    // Add payload as query parameters
    Object.entries(payload).forEach(([key, value]) => {
      url.searchParams.append(key, typeof value === 'object' ? JSON.stringify(value) : value);
    });

    // Add chat-specific headers if this is a chat interaction
    const headers = {
      ...(n8nConfig.apiKey ? { 'X-N8N-API-KEY': n8nConfig.apiKey } : {}),
      ...(payload.type === 'chat' ? { 'X-Chat-Session': payload.sessionId } : {})
    };

    console.log('Calling n8n workflow:', url.toString());
    console.log('Query parameters:', Object.fromEntries(url.searchParams));

    const response = await axios.get(url.toString(), { headers });

    // Handle chat-specific response format
    if (response.data.error) {
      throw new Error(response.data.error);
    }

    // If this is a chat response, include chat metadata
    if (response.data.chatMetadata) {
      return {
        ...response.data,
        supportsChat: true,
        sessionId: response.data.chatMetadata.sessionId,
        endHandoff: response.data.chatMetadata.endHandoff
      };
    }

    return response.data;
  } catch (error) {
    console.error('n8n workflow error:', error.response?.data || error.message);
    throw new Error(`Failed to execute workflow: ${error.message}`);
  }
}

/**
 * Get workflow execution status
 * @param {string} executionId - The execution ID
 * @returns {Promise<object>} - Execution status
 */
async function getWorkflowStatus(executionId) {
  if (!n8nConfig.apiKey) {
    throw new Error('N8N_API_KEY not configured');
  }

  try {
    const response = await axios.get(
      `${n8nConfig.baseUrl}/api/v1/executions/${executionId}`,
      {
        headers: {
          'X-N8N-API-KEY': n8nConfig.apiKey
        }
      }
    );
    return response.data;
  } catch (error) {
    console.error('Error getting workflow status:', error.response?.data || error.message);
    throw error;
  }
}

/**
 * List available workflows
 * @returns {Promise<Array>} - List of workflows
 */
async function listWorkflows() {
  if (!n8nConfig.apiKey) {
    throw new Error('N8N_API_KEY not configured');
  }

  try {
    const response = await axios.get(
      `${n8nConfig.baseUrl}/api/v1/workflows`,
      {
        headers: {
          'X-N8N-API-KEY': n8nConfig.apiKey
        }
      }
    );
    return response.data.data;
  } catch (error) {
    console.error('Error listing workflows:', error.response?.data || error.message);
    throw error;
  }
}

module.exports = {
  callN8nWorkflow,
  getWorkflowStatus,
  listWorkflows
};
