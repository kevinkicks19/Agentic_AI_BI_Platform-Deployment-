from typing import Dict, Any, List
import logging
import re
from collections import Counter
from app.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class DocumentAnalysisTool(BaseTool):
    """Tool for analyzing business documents and extracting key information."""
    
    def __init__(self):
        super().__init__(
            name="document_analysis",
            description="Analyze business documents and extract key information"
        )
        self.parameters = {
            "text": {
                "type": "string",
                "description": "Document text to analyze",
                "required": True
            },
            "analysis_type": {
                "type": "string",
                "description": "Type of analysis to perform (summary, keywords, sentiment, entities)",
                "required": True,
                "enum": ["summary", "keywords", "sentiment", "entities"]
            }
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the document analysis."""
        if not self.validate_parameters(**kwargs):
            return {
                "status": "error",
                "error": "Invalid parameters"
            }
        
        try:
            text = kwargs["text"]
            analysis_type = kwargs["analysis_type"]
            
            if analysis_type == "summary":
                return self._generate_summary(text)
            elif analysis_type == "keywords":
                return self._extract_keywords(text)
            elif analysis_type == "sentiment":
                return self._analyze_sentiment(text)
            elif analysis_type == "entities":
                return self._extract_entities(text)
            else:
                return {
                    "status": "error",
                    "error": f"Unknown analysis type: {analysis_type}"
                }
        
        except Exception as e:
            logger.error(f"Error performing document analysis: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _generate_summary(self, text: str) -> Dict[str, Any]:
        """Generate a summary of the document."""
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Simple summary: first sentence and last sentence
        summary = f"{sentences[0]} {sentences[-1]}"
        
        return {
            "status": "success",
            "results": {
                "summary": summary,
                "sentence_count": len(sentences),
                "word_count": len(text.split())
            }
        }
    
    def _extract_keywords(self, text: str) -> Dict[str, Any]:
        """Extract key keywords from the document."""
        # Remove punctuation and convert to lowercase
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Remove common words
        common_words = {'the', 'and', 'a', 'to', 'of', 'in', 'is', 'that', 'it', 'with'}
        words = [word for word in words if word not in common_words and len(word) > 3]
        
        # Count word frequencies
        word_counts = Counter(words)
        
        return {
            "status": "success",
            "results": {
                "top_keywords": dict(word_counts.most_common(10)),
                "total_keywords": len(word_counts)
            }
        }
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze the sentiment of the document."""
        # Simple sentiment analysis based on positive/negative word lists
        positive_words = {'good', 'great', 'excellent', 'positive', 'success', 'improve', 'benefit'}
        negative_words = {'bad', 'poor', 'negative', 'problem', 'issue', 'concern', 'risk'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        sentiment_score = (positive_count - negative_count) / len(words) if words else 0
        
        return {
            "status": "success",
            "results": {
                "sentiment_score": sentiment_score,
                "positive_words": positive_count,
                "negative_words": negative_count,
                "sentiment": "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
            }
        }
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract named entities from the document."""
        # Simple entity extraction using regex patterns
        entities = {
            "dates": re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text),
            "emails": re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
            "urls": re.findall(r'https?://\S+', text),
            "numbers": re.findall(r'\b\d+\b', text)
        }
        
        return {
            "status": "success",
            "results": {
                "entities": entities,
                "entity_counts": {k: len(v) for k, v in entities.items()}
            }
        } 