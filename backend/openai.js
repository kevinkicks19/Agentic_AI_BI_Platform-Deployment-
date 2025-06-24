const OpenAI = require('openai');
require('dotenv').config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

/**
 * Send a prompt to OpenAI and return the response
 * @param {string} prompt - The prompt to send
 * @param {object} [options] - Optional settings (model, temperature, etc.)
 * @returns {Promise<string>} - The response from OpenAI
 */
async function askOpenAI(prompt, options = {}) {
  try {
    const response = await openai.chat.completions.create({
      model: options.model || 'gpt-4',
      messages: [
        { role: 'system', content: options.system || 'You are a helpful assistant.' },
        { role: 'user', content: prompt },
      ],
      temperature: options.temperature || 0.7,
      ...options.extra,
    });
    return response.choices[0].message.content;
  } catch (error) {
    console.error('OpenAI API error:', error?.error?.message || error.message);
    throw error;
  }
}

module.exports = { askOpenAI };
