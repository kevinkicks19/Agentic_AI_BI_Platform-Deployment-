const { askOpenAI } = require('./openai');
const { upsertMessageEmbedding, queryVectorInIndex, generateEmbedding } = require('./pinecone');
const { callN8nWorkflow } = require('./n8n');

/**
 * Detect if a message requires workflow execution
 * @param {string} message - The message to analyze
 * @param {Array} context - Previous context messages
 * @returns {Promise<{shouldTrigger: boolean, workflowId: string, params: object}>}
 */
async function detectWorkflowTrigger(message, context) {
  // Ask OpenAI to analyze if this requires a workflow
  const analysisPrompt = `You are a workflow detection system. Analyze if this user request requires executing a workflow.

Available workflows:
1. Data Analysis Workflow (data_analysis)
   - Analyzes data sets and generates insights
   - Trigger words: analyze data, run analysis, process data
   - Required parameters: dataSource, analysisType

2. Report Generation (report_generation)
   - Creates reports from existing data
   - Trigger words: generate report, create report, compile report
   - Required parameters: reportType, timeRange

3. Data Integration (data_integration)
   - Integrates data between different systems
   - Trigger words: sync data, import data, export data
   - Required parameters: sourceSystem, targetSystem

Message: ${message}
Previous Context: ${context.map(c => c.content).join('\n')}

Determine if this requires executing an automated workflow. If yes, identify:
1. Which workflow matches the user's intent
2. Extract any mentioned parameters
3. Infer reasonable defaults for missing parameters

Respond in JSON format:
{
  "requiresWorkflow": true/false,
  "workflowType": "workflow_id",
  "parameters": {
    "param1": "value1",
    ...
  },
  "confidence": 0-1,
  "missingParams": ["param1", "param2"]
}`;

  const analysis = await askOpenAI(analysisPrompt);
  let result;
  try {
    result = JSON.parse(analysis);
  } catch (e) {
    console.error('Failed to parse workflow analysis:', e);
    return { shouldTrigger: false };
  }

  // Map workflow types to n8n workflow IDs
  const workflowMap = {
    'data_analysis': 'https://bmccartn.app.n8n.cloud/webhook/ca361862-55b2-49a0-a765-ff06b90e416a/chat',
    'report_generation': 'report-gen-workflow',
    'data_integration': 'data-integration-flow'
  };

  // If we're missing critical parameters, ask for them
  if (result.requiresWorkflow && result.missingParams?.length > 0) {
    const paramPrompt = `The workflow "${result.workflowType}" requires additional information. Please provide:
${result.missingParams.join('\n')}`;
    
    // Add this to the response so the chat handler can request more info
    return {
      shouldTrigger: true,
      workflowId: workflowMap[result.workflowType],
      params: result.parameters,
      needsMoreInfo: true,
      missingParams: result.missingParams,
      paramPrompt
    };
  }

  return {
    shouldTrigger: result.requiresWorkflow && result.confidence > 0.7,
    workflowId: workflowMap[result.workflowType],
    params: result.parameters
  };
}

/**
 * Handle a chat message through the coordinator agent
 * @param {string} userMessage - The user's message
 * @param {object} options - Additional options including context
 * @returns {Promise<string>} - The agent's response
 */
async function handleChat(userMessage, options = {}) {
  try {
    const pineconeIndex = process.env.PINECONE_INDEX;
    if (!pineconeIndex) {
      throw new Error("PINECONE_INDEX environment variable not set.");
    }

    // 1. Get relevant context from vector store
    const contextResults = await queryVectorInIndex(userMessage, pineconeIndex, 5);
    const contextMessages = contextResults.map(match => match.message).join('\\n');
    console.log('Retrieved context from Pinecone:', contextMessages);

    // 2. Store the current message for future context
    await upsertMessageEmbedding(userMessage, pineconeIndex);

    // 3. Prepare prompt with context
    let prompt = `Based on the following context, please answer the user's question.
    
Context:
---
${contextMessages}
---

User Message: "${userMessage}"`;

    const workflowAnalysis = await detectWorkflowTrigger(userMessage, options.context || []);
    let workflowResult = null;
    if (workflowAnalysis.shouldTrigger && workflowAnalysis.workflowId) {
       console.log('Triggering n8n workflow:', workflowAnalysis.workflowId);
      try {
        workflowResult = await callN8nWorkflow(
          workflowAnalysis.workflowId,
          workflowAnalysis.params
        );
        prompt += `\\n\\nAn n8n workflow was triggered and returned the following result: ${JSON.stringify(workflowResult)}`;
        console.log('Workflow execution result:', workflowResult);
      } catch (error) {
        console.error('Workflow execution failed:', error);
        prompt += `\\n\\nAn attempt to run a workflow failed with the error: ${error.message}`;
      }
    }

    // 4. Get response from OpenAI
    const response = await askOpenAI(prompt, {
      ...options,
      system: `You are a helpful coordinator agent. You have access to a vector store for context and can trigger n8n workflows.`
    });

    // 5. Store the agent's response for future context
    await upsertMessageEmbedding(response, pineconeIndex);

    return response;
  } catch (error) {
    console.error('Error in handleChat:', error);
    throw error;
  }
}

/**
 * Upsert a chat message embedding into Pinecone
 * @param {string} message - The message text
 * @param {string} index - The Pinecone index name
 * @returns {Promise<boolean>}
 */
async function upsertMessage(message, index) {
  return upsertMessageEmbedding(message, index);
}

/**
 * Trigger an n8n workflow via webhook
 * @param {string} webhookUrl - The n8n webhook URL
 * @param {object} [params] - Query parameters for GET or body for POST
 * @param {string} [method] - HTTP method ('GET' or 'POST')
 * @returns {Promise<any>}
 */
async function triggerN8nAgent(webhookUrl, params = {}, method = 'GET') {
  if (method === 'GET') {
    // Append query params to URL
    const url = new URL(webhookUrl);
    Object.entries(params).forEach(([key, value]) => url.searchParams.append(key, value));
    return callN8nWorkflow(url.toString(), {}); // GET, so payload is empty
  } else {
    // POST with payload
    return callN8nWorkflow(webhookUrl, params);
  }
}

class Coordinator {
  constructor() {
    this.context = {};
  }

  createResponse(message, buttons = [], handoff = null) {
    return {
      message,
      buttons,
      handoff
    };
  }

  async processMessage(userId, message) {
    try {
      if (!this.context[userId]) {
        this.context[userId] = { history: [], activeHandoff: null };
      }
      const userContext = this.context[userId];
      
      // Special case: if user types 'test', offer the Test Workflow button
      if (message.trim().toLowerCase() === 'test') {
        return this.createResponse(
          'Would you like to test the n8n workflow? Click the button below to start.',
          [
            {
              label: 'Test Workflow',
              value: 'open_n8n_chat',
              action: 'open_n8n_chat'
            }
          ],
          null
        );
      }

      // 1. If a handoff is active, forward the message to the workflow
      if (userContext.activeHandoff) {
        console.log(`Forwarding message to active handoff: ${userContext.activeHandoff.name}`);
        const workflowResult = await callN8nWorkflow(userContext.activeHandoff.workflowId, { message });
        
        // If the workflow signals the end of the handoff
        if (workflowResult.endHandoff) {
          userContext.activeHandoff = null;
          return this.createResponse("The workflow chat has ended. How can I help you next?");
        }
        
        return this.createResponse(workflowResult.message, workflowResult.buttons, userContext.activeHandoff);
      }

      const pineconeIndex = process.env.PINECONE_INDEX;

      if (!pineconeIndex) {
        throw new Error("PINECONE_INDEX environment variable not set.");
      }
      
      // 2. Check if the message should trigger a workflow
      const workflowAnalysis = await detectWorkflowTrigger(message, userContext.history);
      
      let responseMessage;
      let handoffData = null;

      if (workflowAnalysis.shouldTrigger && workflowAnalysis.workflowId) {
        console.log('Triggering n8n workflow:', workflowAnalysis.workflowId, 'with params:', workflowAnalysis.params);
        const workflowResult = await callN8nWorkflow(
          workflowAnalysis.workflowId,
          { ...workflowAnalysis.params, message } // Send original message as well
        );
        console.log('Workflow execution result:', workflowResult);
        
        // 2a. If workflow supports chat, initiate handoff
        if (workflowResult.supportsChat) {
          userContext.activeHandoff = {
            name: workflowResult.name || 'Workflow Agent',
            workflowId: workflowAnalysis.workflowId,
            sessionId: workflowResult.sessionId
          };
          handoffData = userContext.activeHandoff;
          responseMessage = workflowResult.message || `Starting a chat with ${handoffData.name}.`;
        } else {
          // 2b. Standard one-off workflow response
          responseMessage = `Successfully ran the workflow! Here's the result: ${JSON.stringify(workflowResult)}`;
        }
      } else {
        // 3. If no workflow, proceed with a contextual chat response
        const contextResults = await queryVectorInIndex(message, pineconeIndex, 3);
        const retrievedContext = contextResults.map(match => match.message).join('\\n---\\n');
        
        const prompt = `You are a helpful coordinator agent.
Context from previous conversations:
---
\${retrievedContext}
---
User message: "\${message}"`;
        
        responseMessage = await askOpenAI(prompt, { context: userContext.history });
      }

      await upsertMessageEmbedding(message, pineconeIndex);
      await upsertMessageEmbedding(responseMessage, pineconeIndex);
      
      userContext.history.push({ role: 'user', content: message });
      userContext.history.push({ role: 'assistant', content: responseMessage });
      
      return this.createResponse(responseMessage, [], handoffData);

    } catch (error) {
      console.error(`Error processing message for user ${userId}:`, error);
      return this.createResponse('Sorry, an error occurred while processing your request.');
    }
  }

  async detectWorkflow(message) {
    // This can be simplified or integrated into handleChat's workflow detection
    const analysis = await detectWorkflowTrigger(message, []);
    return {
      trigger: analysis.shouldTrigger,
      workflowId: analysis.workflowId,
      params: analysis.params
    };
  }
}

const coordinatorInstance = new Coordinator();

module.exports = {
  Coordinator: coordinatorInstance,
  handleChat,
  triggerN8nAgent,
  upsertMessage
};

