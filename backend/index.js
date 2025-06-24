const { askOpenAI } = require('./openai');
const express = require('express');
const app = express();
const n8nRoutes = require('./src/routes/n8n');
const chatRoutes = require('./src/routes/chat');

/**
 * Handle a chat message through the coordinator agent
 * @param {string} userMessage - The user's message
 * @param {object} [options] - Persona, context, etc.
 * @returns {Promise<string>} - The agent's response
 */
async function handleChat(userMessage, options = {}) {
  // You can expand this to include persona/context logic
  const systemPrompt = options.persona
    ? `You are acting as a ${options.persona}. ${options.system || ''}`
    : options.system || 'You are a helpful coordinator agent.';
  return askOpenAI(userMessage, { system: systemPrompt, ...options });
}

app.use('/api/workflow', n8nRoutes);
app.use('/api/chat', chatRoutes);

module.exports = { handleChat };
