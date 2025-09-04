"""
Enhanced RAG-based Customer Support Chatbot
Integrates with existing system and provides advanced RAG capabilities
"""

import logging
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from rag_data_ingestion import rag_data_ingestion
from rag_vector_store import rag_vector_store
from rag_langchain_integration import rag_langchain
from rag_conversation_memory import rag_conversation_memory
from faq_data import FAQ_DATABASE
from order_tracker import order_tracker
from keyword_matcher import keyword_matcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGEnhancedChatbot:
    """Enhanced RAG-based chatbot that integrates with existing system"""
    
    def __init__(self):
        self.name = "TechBot Pro RAG"
        self.version = "3.0"
        self.escalation_threshold = 0.3
        self.rag_confidence_threshold = 0.7
        
        # Initialize RAG components
        self._initialize_rag_system()
        
        # Conversation analytics
        self.conversation_analytics = {
            "total_conversations": 0,
            "rag_responses": 0,
            "keyword_responses": 0,
            "escalations": 0,
            "avg_confidence": 0.0
        }
    
    def _initialize_rag_system(self):
        """Initialize the RAG system with knowledge base"""
        try:
            logger.info("Initializing RAG system...")
            
            # Ingest FAQ database
            faq_documents = rag_data_ingestion.ingest_faq_database(FAQ_DATABASE)
            
            # Create sample knowledge base
            sample_documents = rag_data_ingestion.create_sample_knowledge_base()
            
            # Combine all documents
            all_documents = faq_documents + sample_documents
            
            # Add to vector store
            success = rag_vector_store.add_documents(all_documents)
            
            if success:
                logger.info(f"Successfully initialized RAG system with {len(all_documents)} documents")
            else:
                logger.error("Failed to initialize RAG system")
                
        except Exception as e:
            logger.error(f"Error initializing RAG system: {e}")
    
    def generate_response(self, 
                         user_message: str, 
                         session_id: str = "default",
                         use_rag: bool = True) -> Dict[str, Any]:
        """Generate response using the enhanced RAG system"""
        try:
            # Update analytics
            self.conversation_analytics["total_conversations"] += 1
            
            # Step 1: Try keyword matching first (fastest)
            keyword_response = keyword_matcher.generate_keyword_response(user_message)
            if keyword_response and keyword_response.get('confidence', 0) > 0.8:
                self.conversation_analytics["keyword_responses"] += 1
                return self._enhance_keyword_response(keyword_response, session_id)
            
            # Step 2: Check for order inquiries
            if self._is_order_inquiry(user_message):
                order_response = order_tracker.handle_order_inquiry(user_message)
                if order_response:
                    return {
                        'response': order_response,
                        'type': 'order_tracking',
                        'escalate': False,
                        'confidence': 0.95,
                        'method': 'order_tracker',
                        'suggestions': ["Can I help with anything else about your order?"],
                        'session_id': session_id
                    }
            
            # Step 3: Use RAG system if enabled
            if use_rag:
                rag_response = self._process_with_rag(user_message, session_id)
                if rag_response and rag_response.get('confidence', 0) >= self.rag_confidence_threshold:
                    self.conversation_analytics["rag_responses"] += 1
                    return rag_response
            
            # Step 4: Fallback to basic response or escalation
            return self._generate_fallback_response(user_message, session_id)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'response': "I apologize, but I encountered an error processing your request. Please try again.",
                'type': 'error',
                'escalate': True,
                'confidence': 0.0,
                'method': 'error',
                'session_id': session_id
            }
    
    def _process_with_rag(self, user_message: str, session_id: str) -> Optional[Dict[str, Any]]:
        """Process user message using RAG system"""
        try:
            # Retrieve relevant documents from vector store
            relevant_docs = rag_vector_store.similarity_search(
                query=user_message,
                k=4,
                score_threshold=0.1
            )
            
            # Convert to context format
            context_documents = []
            for doc, score in relevant_docs:
                context_documents.append({
                    'content': doc.page_content,
                    'source': doc.metadata.get('source', 'unknown'),
                    'type': doc.metadata.get('type', 'unknown'),
                    'relevance': float(score)
                })
            
            # Process with conversation memory
            memory_response = rag_conversation_memory.process_conversation(
                query=user_message,
                session_id=session_id,
                context_documents=context_documents
            )
            
            # Process with LangChain integration
            langchain_response = rag_langchain.process_query_with_rag(
                query=user_message,
                session_id=session_id,
                context_documents=context_documents
            )
            
            # Combine responses
            if memory_response.get('confidence', 0) > langchain_response.get('confidence', 0):
                primary_response = memory_response
                secondary_response = langchain_response
            else:
                primary_response = langchain_response
                secondary_response = memory_response
            
            # Enhance response with context
            enhanced_response = self._enhance_rag_response(
                primary_response, 
                context_documents, 
                session_id
            )
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Error processing with RAG: {e}")
            return None
    
    def _enhance_rag_response(self, 
                             response: Dict[str, Any], 
                             context_documents: List[Dict],
                             session_id: str) -> Dict[str, Any]:
        """Enhance RAG response with additional context and suggestions"""
        try:
            # Add context information
            if context_documents:
                sources = list(set([doc.get('source', 'Unknown') for doc in context_documents]))
                response['sources'] = sources[:3]  # Top 3 sources
                response['context_used'] = len(context_documents)
            
            # Add smart suggestions based on context
            suggestions = self._generate_smart_suggestions(response, context_documents)
            response['suggestions'] = suggestions
            
            # Add conversation memory info
            response['conversation_memory'] = True
            response['session_id'] = session_id
            
            # Update confidence based on context quality
            if context_documents:
                avg_relevance = sum(doc.get('relevance', 0) for doc in context_documents) / len(context_documents)
                response['confidence'] = min(response.get('confidence', 0.5) + avg_relevance * 0.2, 1.0)
            
            return response
            
        except Exception as e:
            logger.error(f"Error enhancing RAG response: {e}")
            return response
    
    def _enhance_keyword_response(self, keyword_response: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Enhance keyword response with RAG capabilities"""
        try:
            # Add RAG enhancements
            keyword_response['method'] = 'keyword_matching'
            keyword_response['session_id'] = session_id
            keyword_response['conversation_memory'] = True
            
            # Add suggestions
            suggestions = self._generate_suggestions_for_category(keyword_response.get('category', 'general'))
            keyword_response['suggestions'] = suggestions
            
            return keyword_response
            
        except Exception as e:
            logger.error(f"Error enhancing keyword response: {e}")
            return keyword_response
    
    def _generate_smart_suggestions(self, response: Dict[str, Any], context_documents: List[Dict]) -> List[str]:
        """Generate smart suggestions based on response and context"""
        try:
            suggestions = []
            
            # Base suggestions
            if response.get('type') == 'faq_answer':
                suggestions.extend([
                    "Can you tell me more about this?",
                    "Is there anything else I can help with?",
                    "Would you like to know about related topics?"
                ])
            elif response.get('type') == 'order_tracking':
                suggestions.extend([
                    "Can I help with anything else about your order?",
                    "Would you like to track another order?",
                    "Do you have questions about delivery?"
                ])
            else:
                suggestions.extend([
                    "How else can I help you?",
                    "Is there anything specific you'd like to know?",
                    "Would you like to speak with a human agent?"
                ])
            
            # Add context-specific suggestions
            if context_documents:
                categories = list(set([doc.get('type', 'general') for doc in context_documents]))
                if 'product_manual' in categories:
                    suggestions.append("Would you like product specifications?")
                if 'return_policy' in categories:
                    suggestions.append("Do you need help with returns?")
                if 'technical' in categories:
                    suggestions.append("Would you like technical support?")
            
            return suggestions[:3]  # Return top 3 suggestions
            
        except Exception as e:
            logger.error(f"Error generating smart suggestions: {e}")
            return ["How else can I help you?"]
    
    def _generate_suggestions_for_category(self, category: str) -> List[str]:
        """Generate suggestions for a specific category"""
        category_suggestions = {
            'payment': [
                "What payment methods do you accept?",
                "Is my payment secure?",
                "Can I use PayPal?"
            ],
            'shipping': [
                "What are your delivery options?",
                "How long does shipping take?",
                "Do you ship internationally?"
            ],
            'returns': [
                "What's your return policy?",
                "How do I start a return?",
                "When will I get my refund?"
            ],
            'warranty': [
                "What warranty do you offer?",
                "How do I claim warranty?",
                "What's covered under warranty?"
            ],
            'support': [
                "How can I contact support?",
                "What are your support hours?",
                "Can I get technical help?"
            ]
        }
        
        return category_suggestions.get(category, [
            "How else can I help you?",
            "Is there anything specific you'd like to know?",
            "Would you like to speak with a human agent?"
        ])
    
    def _is_order_inquiry(self, message: str) -> bool:
        """Check if message is an order inquiry"""
        order_keywords = ['order', 'track', 'delivery', 'shipped', 'package', 'where is']
        return any(keyword in message.lower() for keyword in order_keywords)
    
    def _generate_fallback_response(self, user_message: str, session_id: str) -> Dict[str, Any]:
        """Generate fallback response when RAG and keyword matching fail"""
        try:
            # Try to get some context from conversation memory
            conversation_history = rag_conversation_memory.get_conversation_history(session_id)
            
            # Generate a contextual response
            if conversation_history:
                # Use conversation context
                response = "I understand you're asking about something. Let me help you with that. Could you provide more specific details about what you need assistance with?"
            else:
                # First-time user response
                response = "Hello! I'm TechBot Pro, your AI assistant. I can help you with orders, returns, products, and more. What would you like to know?"
            
            # Check if we should escalate
            should_escalate = self._should_escalate(user_message, conversation_history)
            
            if should_escalate:
                self.conversation_analytics["escalations"] += 1
                response += "\n\nI'm connecting you with a human agent who can provide more specialized assistance."
            
            return {
                'response': response,
                'type': 'fallback',
                'escalate': should_escalate,
                'confidence': 0.3,
                'method': 'fallback',
                'suggestions': ["Can you be more specific?", "Would you like to speak with a human agent?"],
                'session_id': session_id
            }
            
        except Exception as e:
            logger.error(f"Error generating fallback response: {e}")
            return {
                'response': "I apologize, but I'm having trouble understanding your request. Please try rephrasing your question or contact our support team.",
                'type': 'error',
                'escalate': True,
                'confidence': 0.0,
                'method': 'error',
                'session_id': session_id
            }
    
    def _should_escalate(self, user_message: str, conversation_history: List[Dict]) -> bool:
        """Determine if conversation should be escalated to human agent"""
        try:
            # Escalation keywords
            escalation_keywords = [
                'complaint', 'angry', 'frustrated', 'disappointed', 'terrible',
                'refund', 'cancel', 'stop', 'never', 'worst', 'awful'
            ]
            
            # Check message for escalation keywords
            if any(keyword in user_message.lower() for keyword in escalation_keywords):
                return True
            
            # Check conversation history for repeated issues
            if len(conversation_history) > 5:
                # If user has been asking multiple questions without resolution
                return True
            
            # Check for complex technical terms that might need human expertise
            technical_terms = [
                'firmware', 'bios', 'driver', 'registry', 'debug', 'troubleshoot',
                'warranty claim', 'insurance', 'legal', 'contract'
            ]
            
            if any(term in user_message.lower() for term in technical_terms):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking escalation: {e}")
            return True  # Escalate on error
    
    def get_conversation_analytics(self, session_id: str = None) -> Dict[str, Any]:
        """Get conversation analytics"""
        try:
            if session_id:
                # Get specific session analytics
                session_analytics = rag_conversation_memory.get_conversation_analytics(session_id)
                return {
                    **session_analytics,
                    'global_analytics': self.conversation_analytics
                }
            else:
                # Get global analytics
                return {
                    **self.conversation_analytics,
                    'rag_system_stats': rag_vector_store.get_stats(),
                    'active_sessions': len(rag_conversation_memory.conversation_states)
                }
                
        except Exception as e:
            logger.error(f"Error getting conversation analytics: {e}")
            return {"error": str(e)}
    
    def clear_conversation(self, session_id: str) -> bool:
        """Clear conversation for a session"""
        try:
            success = rag_conversation_memory.clear_conversation(session_id)
            if success:
                logger.info(f"Cleared conversation for session {session_id}")
            return success
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            return False
    
    def add_documents_to_knowledge_base(self, documents: List[Dict]) -> bool:
        """Add new documents to the knowledge base"""
        try:
            # Convert to LangChain documents
            langchain_docs = []
            for doc in documents:
                from langchain.schema import Document
                langchain_doc = Document(
                    page_content=doc.get('content', ''),
                    metadata=doc.get('metadata', {})
                )
                langchain_docs.append(langchain_doc)
            
            # Add to vector store
            success = rag_vector_store.add_documents(langchain_docs)
            
            if success:
                logger.info(f"Added {len(documents)} documents to knowledge base")
            
            return success
            
        except Exception as e:
            logger.error(f"Error adding documents to knowledge base: {e}")
            return False

# Global RAG enhanced chatbot instance
rag_enhanced_chatbot = RAGEnhancedChatbot()
