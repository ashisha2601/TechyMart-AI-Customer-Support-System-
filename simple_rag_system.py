"""
Simplified RAG System
A basic RAG implementation using only existing dependencies
"""

import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from faq_data import FAQ_DATABASE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleRAGSystem:
    """Simplified RAG system using TF-IDF and cosine similarity"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
        self.faq_vectors = None
        self.faqs = FAQ_DATABASE
        self.conversation_memory = {}
        self._build_index()
    
    def _build_index(self):
        """Build TF-IDF vectors for all FAQ entries"""
        try:
            # Combine question, answer, and keywords for better matching
            texts = []
            for faq in self.faqs:
                combined_text = f"{faq['question']} {faq['answer']} {' '.join(faq['keywords'])}"
                texts.append(combined_text)
            
            self.faq_vectors = self.vectorizer.fit_transform(texts)
            logger.info(f"Built TF-IDF index with {len(texts)} documents")
        except Exception as e:
            logger.error(f"Error building index: {e}")
            self.faq_vectors = None
    
    def find_best_answer(self, query: str, threshold: float = 0.1) -> Tuple[Dict, float]:
        """
        Find the most relevant FAQ answer for a given query
        
        Args:
            query: User's question
            threshold: Minimum similarity score to consider a match
            
        Returns:
            Tuple of (best_faq_dict, similarity_score)
        """
        try:
            if self.faq_vectors is None:
                return None, 0.0
            
            # Vectorize the query
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vector, self.faq_vectors)[0]
            
            # Find best match
            best_idx = np.argmax(similarities)
            best_score = similarities[best_idx]
            
            if best_score >= threshold:
                return self.faqs[best_idx], best_score
            else:
                return None, best_score
                
        except Exception as e:
            logger.error(f"Error finding best answer: {e}")
            return None, 0.0
    
    def get_conversation_context(self, session_id: str) -> List[Dict]:
        """Get conversation history for context"""
        return self.conversation_memory.get(session_id, [])
    
    def add_to_conversation(self, session_id: str, role: str, message: str, metadata: Dict = None):
        """Add message to conversation history"""
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = []
        
        self.conversation_memory[session_id].append({
            'role': role,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        })
        
        # Keep only last 10 messages
        if len(self.conversation_memory[session_id]) > 10:
            self.conversation_memory[session_id] = self.conversation_memory[session_id][-10:]
    
    def generate_response(self, user_message: str, session_id: str = "default") -> Dict[str, Any]:
        """Generate response using RAG system"""
        try:
            # Add user message to conversation
            self.add_to_conversation(session_id, "user", user_message)
            
            # Get conversation context
            context = self.get_conversation_context(session_id)
            
            # Find best answer
            best_faq, confidence = self.find_best_answer(user_message, threshold=0.1)
            
            if best_faq and confidence >= 0.3:
                # Generate response with context
                response = self._enhance_response(best_faq, confidence, context)
                
                # Add bot response to conversation
                self.add_to_conversation(session_id, "bot", response, {
                    'confidence': confidence,
                    'source': 'faq',
                    'category': best_faq['category']
                })
                
                return {
                    'response': response,
                    'type': 'faq_answer',
                    'category': best_faq['category'],
                    'confidence': confidence,
                    'escalate': False,
                    'method': 'rag',
                    'sources': ['FAQ Database'],
                    'context_used': len(context)
                }
            else:
                # Fallback response
                fallback_response = self._generate_fallback_response(user_message, context)
                
                # Add bot response to conversation
                self.add_to_conversation(session_id, "bot", fallback_response, {
                    'confidence': confidence,
                    'source': 'fallback'
                })
                
                return {
                    'response': fallback_response,
                    'type': 'fallback',
                    'confidence': confidence,
                    'escalate': confidence < 0.1,
                    'method': 'fallback',
                    'sources': [],
                    'context_used': len(context)
                }
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'response': "I apologize, but I encountered an error processing your request. Please try again.",
                'type': 'error',
                'confidence': 0.0,
                'escalate': True,
                'method': 'error',
                'sources': [],
                'context_used': 0
            }
    
    def _enhance_response(self, faq: Dict, confidence: float, context: List[Dict]) -> str:
        """Enhance FAQ response with context and personality"""
        base_response = faq['answer']
        
        # Add confidence-based prefix
        if confidence > 0.8:
            prefix = "I found exactly what you're looking for! "
        elif confidence > 0.5:
            prefix = "Here's what I found: "
        else:
            prefix = "Based on your question, "
        
        # Add context awareness
        if context:
            recent_topics = [msg.get('metadata', {}).get('category', '') for msg in context[-3:] if msg['role'] == 'user']
            if recent_topics and any(topic for topic in recent_topics):
                prefix += "I see you've been asking about related topics. "
        
        # Add helpful follow-up
        follow_up = "\n\nIs there anything specific about this you'd like me to explain further?"
        
        return f"{prefix}{base_response}{follow_up}"
    
    def _generate_fallback_response(self, user_message: str, context: List[Dict]) -> str:
        """Generate fallback response when no good match is found"""
        # Check if this is a greeting
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(greeting in user_message.lower() for greeting in greetings):
            return "Hello! I'm TechBot Pro with RAG capabilities. I can help you with questions about our products, policies, and services. What would you like to know?"
        
        # Check if this is a thank you
        thanks = ['thank', 'thanks', 'appreciate']
        if any(thank in user_message.lower() for thank in thanks):
            return "You're welcome! I'm here to help anytime. Is there anything else you'd like to know?"
        
        # Check conversation context
        if context:
            recent_categories = [msg.get('metadata', {}).get('category', '') for msg in context[-3:] if msg['role'] == 'bot']
            if recent_categories:
                return f"I understand you're asking about something. I can help with questions about our products, policies, shipping, returns, and more. Could you provide more details about what you need help with?"
        
        # Default fallback
        return "I understand you need help. I can assist you with questions about our products, policies, shipping, returns, warranties, and more. Could you be more specific about what you'd like to know?"
    
    def get_conversation_analytics(self, session_id: str = None) -> Dict[str, Any]:
        """Get analytics for conversations"""
        try:
            if session_id:
                # Session-specific analytics
                if session_id in self.conversation_memory:
                    messages = self.conversation_memory[session_id]
                    user_messages = [m for m in messages if m['role'] == 'user']
                    bot_messages = [m for m in messages if m['role'] == 'bot']
                    
                    return {
                        'session_id': session_id,
                        'message_count': len(messages),
                        'user_messages': len(user_messages),
                        'bot_messages': len(bot_messages),
                        'created_at': messages[0]['timestamp'] if messages else None,
                        'last_updated': messages[-1]['timestamp'] if messages else None
                    }
                else:
                    return {'error': 'Session not found'}
            else:
                # Global analytics
                total_sessions = len(self.conversation_memory)
                total_messages = sum(len(msgs) for msgs in self.conversation_memory.values())
                
                return {
                    'total_sessions': total_sessions,
                    'total_messages': total_messages,
                    'active_sessions': total_sessions,
                    'rag_system': 'simple_tfidf',
                    'index_size': len(self.faqs) if self.faqs else 0
                }
                
        except Exception as e:
            logger.error(f"Error getting analytics: {e}")
            return {'error': str(e)}
    
    def clear_conversation(self, session_id: str) -> bool:
        """Clear conversation for a session"""
        try:
            if session_id in self.conversation_memory:
                del self.conversation_memory[session_id]
                logger.info(f"Cleared conversation for session {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            return False

# Global simple RAG system instance
simple_rag_system = SimpleRAGSystem()
