const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const { getEmbedding } = require('../coordinator/openai');
const { upsertVectors } = require('../coordinator/pinecone');

const router = express.Router();

// Configure multer for file uploads (store in memory)
const upload = multer({ storage: multer.memoryStorage() });

// Helper: Chunk text into pieces of maxTokens (approximate by words)
function chunkText(text, maxWords = 200) {
  const words = text.split(/\s+/);
  const chunks = [];
  for (let i = 0; i < words.length; i += maxWords) {
    chunks.push(words.slice(i, i + maxWords).join(' '));
  }
  return chunks;
}

// POST /api/upload
router.post('/', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded.' });
    }
    // Assume text file for simplicity
    const text = req.file.buffer.toString('utf-8');
    const filename = req.file.originalname;
    const chunks = chunkText(text, 200); // 200 words per chunk

    // Generate embeddings for each chunk and upsert to Pinecone
    const vectors = [];
    for (let i = 0; i < chunks.length; i++) {
      const chunk = chunks[i];
      const embedding = await getEmbedding(chunk);
      vectors.push({
        id: `${filename}-chunk-${i}`,
        values: embedding,
        metadata: {
          filename,
          chunk: i,
          text: chunk.slice(0, 100), // Store a preview
        },
      });
    }
    await upsertVectors(vectors);

    res.json({
      message: 'File processed and embedded into Pinecone.',
      filename,
      chunks: chunks.length,
      pineconeIds: vectors.map((v) => v.id),
    });
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ error: 'Failed to process and embed file.' });
  }
});

module.exports = router; 