/**
 * Get a system prompt for a given persona
 * @param {string} persona - Persona name
 * @returns {string} - System prompt for the persona
 */
function getPersonaPrompt(persona) {
  switch (persona) {
    case 'Consultant':
      return 'You are a business consultant. Provide strategic advice and clear explanations.';
    case 'Project Manager':
      return 'You are a project manager. Focus on planning, coordination, and risk management.';
    case 'Business Analyst':
      return 'You are a business analyst. Analyze requirements and communicate insights clearly.';
    case 'Solution Architect':
      return 'You are a solution architect. Design scalable, robust technical solutions.';
    default:
      return 'You are a helpful assistant.';
  }
}

module.exports = { getPersonaPrompt };
