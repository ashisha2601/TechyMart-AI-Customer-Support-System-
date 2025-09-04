"""
RAG Conversation Memory with LangGraph
Advanced conversation memory and state management using LangGraph
"""

import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import ConversationSummaryMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ConversationState:
    """State for conversation memory"""
    messages: List[BaseMessage] = field(default_factory=list)
    current_query: str = ""
    context_documents: List[Dict] = field(default_factory=list)
    response: str = ""
    confidence: float = 0.0
    escalated: bool = False
    session_id: str = "default"
    user_intent: str = ""
    conversation_topic: str = ""
    satisfaction_score: Optional[float] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())

class RAGConversationMemory:
    """Advanced conversation memory using LangGraph"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.conversation_states = {}
        self.conversation_graph = self._create_conversation_graph()
        
    def _create_conversation_graph(self) -> StateGraph:
        """Create the conversation memory graph"""
        try:
            # Define the workflow
            workflow = StateGraph(ConversationState)
            
            # Add nodes
            workflow.add_node("analyze_query", self._analyze_query)
            workflow.add_node("retrieve_memory", self._retrieve_memory)
            workflow.add_node("update_context", self._update_context)
            workflow.add_node("generate_response", self._generate_response)
            workflow.add_node("update_memory", self._update_memory)
            workflow.add_node("check_escalation", self._check_escalation)
            
            # Add edges
            workflow.add_edge("analyze_query", "retrieve_memory")
            workflow.add_edge("retrieve_memory", "update_context")
            workflow.add_edge("update_context", "generate_response")
            workflow.add_edge("generate_response", "update_memory")
            workflow.add_edge("update_memory", "check_escalation")
            workflow.add_edge("check_escalation", END)
            
            # Set entry point
            workflow.set_entry_point("analyze_query")
            
            return workflow.compile()
            
        except Exception as e:
            logger.error(f"Error creating conversation graph: {e}")
            return None
    
    def _analyze_query(self, state: ConversationState) -> ConversationState:
        """Analyze the user query for intent and context"""
        try:
            query = state.current_query.lower()
            
            # Simple intent detection
            if any(word in query for word in ['hello', 'hi', 'hey', 'start']):
                state.user_intent = "greeting"
            elif any(word in query for word in ['order', 'track', 'delivery', 'shipped']):
                state.user_intent = "order_inquiry"
            elif any(word in query for word in ['return', 'refund', 'exchange']):
                state.user_intent = "return_inquiry"
            elif any(word in query for word in ['product', 'buy', 'purchase', 'price']):
                state.user_intent = "product_inquiry"
            elif any(word in query for word in ['help', 'support', 'problem', 'issue']):
                state.user_intent = "support_request"
            else:
                state.user_intent = "general_inquiry"
            
            # Extract topic
            if 'shipping' in query or 'delivery' in query:
                state.conversation_topic = "shipping"
            elif 'payment' in query or 'card' in query or 'pay' in query:
                state.conversation_topic = "payment"
            elif 'warranty' in query or 'guarantee' in query:
                state.conversation_topic = "warranty"
            elif 'return' in query or 'refund' in query:
                state.conversation_topic = "returns"
            else:
                state.conversation_topic = "general"
            
            state.last_updated = datetime.now().isoformat()
            logger.info(f"Analyzed query - Intent: {state.user_intent}, Topic: {state.conversation_topic}")
            
        except Exception as e:
            logger.error(f"Error analyzing query: {e}")
        
        return state
    
    def _retrieve_memory(self, state: ConversationState) -> ConversationState:
        """Retrieve relevant conversation memory"""
        try:
            session_id = state.session_id
            
            # Get conversation history
            if session_id in self.conversation_states:
                previous_state = self.conversation_states[session_id]
                state.messages = previous_state.messages[-10:]  # Keep last 10 messages
            
            # Add current query to messages
            state.messages.append(HumanMessage(content=state.current_query))
            
            logger.info(f"Retrieved {len(state.messages)} messages from memory")
            
        except Exception as e:
            logger.error(f"Error retrieving memory: {e}")
        
        return state
    
    def _update_context(self, state: ConversationState) -> ConversationState:
        """Update context with retrieved documents"""
        try:
            # This would integrate with the vector store
            # For now, add some sample context based on intent
            if state.user_intent == "order_inquiry":
                state.context_documents = [{
                    "content": "Order tracking information and delivery status",
                    "source": "order_system",
                    "relevance": 0.9
                }]
            elif state.user_intent == "return_inquiry":
                state.context_documents = [{
                    "content": "Return policy and refund process information",
                    "source": "policy_database",
                    "relevance": 0.9
                }]
            else:
                state.context_documents = [{
                    "content": "General product and service information",
                    "source": "knowledge_base",
                    "relevance": 0.7
                }]
            
            logger.info(f"Updated context with {len(state.context_documents)} documents")
            
        except Exception as e:
            logger.error(f"Error updating context: {e}")
        
        return state
    
    def _generate_response(self, state: ConversationState) -> ConversationState:
        """Generate response using LLM and context"""
        try:
            # Prepare context
            context_text = ""
            if state.context_documents:
                context_text = "\n".join([
                    f"Context: {doc['content']}" for doc in state.context_documents
                ])
            
            # Prepare conversation history
            history_text = ""
            if state.messages:
                history_text = "\n".join([
                    f"{'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content}"
                    for msg in state.messages[-5:]  # Last 5 messages
                ])
            
            # Create prompt
            prompt = f"""
            You are TechBot Pro, an advanced AI customer support assistant for TechyMart.
            
            Context Information:
            {context_text}
            
            Conversation History:
            {history_text}
            
            Current Query: {state.current_query}
            
            Please provide a helpful, accurate, and friendly response. If you need more information,
            ask clarifying questions. If the query is complex, suggest escalating to a human agent.
            """
            
            # Generate response (mock for now)
            if self.llm:
                try:
                    response = self.llm.invoke([HumanMessage(content=prompt)])
                    if hasattr(response, 'content'):
                        state.response = response.content
                    else:
                        state.response = str(response)
                except Exception as e:
                    logger.error(f"Error with LLM: {e}")
                    state.response = self._generate_fallback_response(state)
            else:
                state.response = self._generate_fallback_response(state)
            
            # Calculate confidence
            state.confidence = self._calculate_confidence(state)
            
            logger.info(f"Generated response with confidence {state.confidence}")
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            state.response = "I apologize, but I encountered an error. Please try again."
            state.confidence = 0.0
        
        return state
    
    def _generate_fallback_response(self, state: ConversationState) -> str:
        """Generate a fallback response when LLM is not available"""
        if state.user_intent == "greeting":
            return "Hello! I'm TechBot Pro, your AI assistant. How can I help you today?"
        elif state.user_intent == "order_inquiry":
            return "I can help you track your order. Please provide your order number."
        elif state.user_intent == "return_inquiry":
            return "Our return policy allows returns within 30 days. Items must be in original condition."
        elif state.user_intent == "product_inquiry":
            return "I can help you with product information. What specific product are you interested in?"
        else:
            return "I understand you need help. Let me assist you with that. Could you provide more details?"
    
    def _calculate_confidence(self, state: ConversationState) -> float:
        """Calculate confidence score for the response"""
        try:
            confidence = 0.5  # Base confidence
            
            # Increase confidence based on context
            if state.context_documents:
                avg_relevance = sum(doc.get('relevance', 0.5) for doc in state.context_documents) / len(state.context_documents)
                confidence += avg_relevance * 0.3
            
            # Increase confidence for specific intents
            if state.user_intent in ['greeting', 'order_inquiry', 'return_inquiry']:
                confidence += 0.2
            
            # Decrease confidence for complex queries
            if len(state.current_query.split()) > 20:
                confidence -= 0.1
            
            return min(max(confidence, 0.0), 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.5
    
    def _update_memory(self, state: ConversationState) -> ConversationState:
        """Update conversation memory with new information"""
        try:
            # Add AI response to messages
            state.messages.append(AIMessage(content=state.response))
            
            # Update conversation state
            state.last_updated = datetime.now().isoformat()
            self.conversation_states[state.session_id] = state
            
            logger.info(f"Updated memory for session {state.session_id}")
            
        except Exception as e:
            logger.error(f"Error updating memory: {e}")
        
        return state
    
    def _check_escalation(self, state: ConversationState) -> ConversationState:
        """Check if conversation should be escalated"""
        try:
            # Escalation criteria
            if state.confidence < 0.3:
                state.escalated = True
                state.response += "\n\nI'm connecting you with a human agent for better assistance."
            elif "escalate" in state.response.lower() or "human" in state.response.lower():
                state.escalated = True
            
            logger.info(f"Escalation check: {state.escalated}")
            
        except Exception as e:
            logger.error(f"Error checking escalation: {e}")
        
        return state
    
    def process_conversation(self, 
                           query: str, 
                           session_id: str = "default",
                           context_documents: List[Dict] = None) -> Dict[str, Any]:
        """Process a conversation turn using the memory graph"""
        try:
            # Create initial state
            state = ConversationState(
                current_query=query,
                session_id=session_id,
                context_documents=context_documents or []
            )
            
            # Run the conversation graph
            if self.conversation_graph:
                final_state = self.conversation_graph.invoke(state)
            else:
                # Fallback processing
                final_state = self._process_fallback(state)
            
            return {
                "response": final_state.response,
                "confidence": final_state.confidence,
                "escalated": final_state.escalated,
                "intent": final_state.user_intent,
                "topic": final_state.conversation_topic,
                "session_id": session_id,
                "context_used": len(final_state.context_documents)
            }
            
        except Exception as e:
            logger.error(f"Error processing conversation: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your request.",
                "confidence": 0.0,
                "escalated": True,
                "intent": "error",
                "topic": "general",
                "session_id": session_id,
                "context_used": 0
            }
    
    def _process_fallback(self, state: ConversationState) -> ConversationState:
        """Fallback processing when graph is not available"""
        state = self._analyze_query(state)
        state = self._retrieve_memory(state)
        state = self._update_context(state)
        state = self._generate_response(state)
        state = self._update_memory(state)
        state = self._check_escalation(state)
        return state
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        try:
            if session_id in self.conversation_states:
                state = self.conversation_states[session_id]
                history = []
                
                for msg in state.messages:
                    history.append({
                        "role": "user" if isinstance(msg, HumanMessage) else "assistant",
                        "content": msg.content,
                        "timestamp": state.last_updated
                    })
                
                return history
            return []
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    def get_conversation_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get analytics for a conversation session"""
        try:
            if session_id not in self.conversation_states:
                return {"error": "Session not found"}
            
            state = self.conversation_states[session_id]
            
            return {
                "session_id": session_id,
                "message_count": len(state.messages),
                "intent": state.user_intent,
                "topic": state.conversation_topic,
                "confidence": state.confidence,
                "escalated": state.escalated,
                "created_at": state.created_at,
                "last_updated": state.last_updated,
                "context_documents_used": len(state.context_documents)
            }
            
        except Exception as e:
            logger.error(f"Error getting conversation analytics: {e}")
            return {"error": str(e)}
    
    def clear_conversation(self, session_id: str) -> bool:
        """Clear conversation memory for a session"""
        try:
            if session_id in self.conversation_states:
                del self.conversation_states[session_id]
                logger.info(f"Cleared conversation for session {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            return False

# Global conversation memory instance
rag_conversation_memory = RAGConversationMemory()
