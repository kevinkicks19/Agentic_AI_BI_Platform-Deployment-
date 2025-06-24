const { Pinecone } = require('@pinecone-database/pinecone');
const OpenAI = require('openai');
require('dotenv').config();

// Validate required environment variables
const requiredEnvVars = ['PINECONE_API_KEY', 'PINECONE_INDEX', 'OPENAI_API_KEY', 'PINECONE_ENVIRONMENT'];
const missingEnvVars = requiredEnvVars.filter(envVar => !process.env[envVar]);
if (missingEnvVars.length > 0) {
  throw new Error(`Missing required environment variables: ${missingEnvVars.join(', ')}`);
}

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Initialize Pinecone
const pinecone = new Pinecone();

// Get the index instance
const indexName = process.env.PINECONE_INDEX;

async function getIndex() {
  const allIndexes = await pinecone.listIndexes();
  if (!allIndexes.indexes.some(i => i.name === indexName)) {
    throw new Error(`Pinecone index "${indexName}" does not exist.`);
  }
  return pinecone.index(indexName);
}

async function generateEmbedding(text) {
  const response = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: text,
  });
  return response.data[0].embedding;
}

async function upsertMessageEmbedding(message) {
  try {
    const pineconeIndex = await getIndex();
    const embedding = await generateEmbedding(message);
    await pineconeIndex.upsert([
      {
        id: Date.now().toString(),
        values: embedding,
        metadata: { message },
      },
    ]);
    return true;
  } catch (error) {
    console.error('Error upserting message embedding:', error);
    return false;
  }
}

async function queryVectorInIndex(query, topK = 5) {
  try {
    const pineconeIndex = await getIndex();
    const queryEmbedding = await generateEmbedding(query);
    
    const queryResponse = await pineconeIndex.query({
      vector: queryEmbedding,
      topK,
      includeMetadata: true,
    });

    return queryResponse.matches.map(match => ({
      score: match.score,
      message: match.metadata.message,
    }));
  } catch (error) {
    console.error('Error querying similar messages:', error);
    return [];
  }
}

module.exports = {
  upsertMessageEmbedding,
  queryVectorInIndex,
  generateEmbedding
}; 