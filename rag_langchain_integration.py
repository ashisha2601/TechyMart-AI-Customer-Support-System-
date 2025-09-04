"""
RAG LangChain Integration
Handles query processing, response generation, and conversation memory using LangChain and LangGraph
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from langchain.chains import RetrievalQA
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferWindowMemory
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGLangChainIntegration:
    """LangChain integration for RAG system"""
    
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 model_name: str = "gpt-3.5-turbo",
                 temperature: float = 0.7):
        
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        self.temperature = temperature
        
        # Initialize LLM
        self._initialize_llm()
        
        # Initialize conversation memory
        self.conversation_memories = {}
        
        # Initialize tools
        self.tools = self._create_tools()
        
        # Initialize agent
        self.agent = self._create_agent()
    
    def _initialize_llm(self):
        """Initialize the language model"""
        try:
            if self.openai_api_key:
                self.llm = ChatOpenAI(
                    openai_api_key=self.openai_api_key,
                    model_name=self.model_name,
                    temperature=self.temperature
                )
                logger.info(f"Initialized OpenAI LLM: {self.model_name}")
            else:
                # Fallback to a local model or mock
                logger.warning("OpenAI API key not found, using mock LLM")
                self.llm = self._create_mock_llm()
                
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            self.llm = self._create_mock_llm()
    
    def _create_mock_llm(self):
        """Create a mock LLM for testing without OpenAI API"""
        class MockLLM:
            def invoke(self, messages, **kwargs):
                # Simple mock response based on the last message
                if isinstance(messages, list) and messages:
                    last_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
                else:
                    last_message = str(messages)
                
                # Generate a basic response
                if "hello" in last_message.lower():
                    return "Hello! I'm TechBot Pro, your AI assistant. How can I help you today?"
                elif "order" in last_message.lower():
                    return "I can help you track your order. Please provide your order number."
                elif "return" in last_message.lower():
                    return "Our return policy allows returns within 30 days. Items must be in original condition."
                else:
                    return "I understand you're asking about something. Let me help you with that. Could you provide more details?"
        
        return MockLLM()
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the agent"""
        tools = [
            Tool(
                name="search_knowledge_base",
                description="Search the knowledge base for relevant information about products, policies, and support",
                func=self._search_knowledge_base
            ),
            Tool(
                name="track_order",
                description="Track an order using order number",
                func=self._track_order
            ),
            Tool(
                name="get_product_info",
                description="Get detailed information about a specific product",
                func=self._get_product_info
            ),
            Tool(
                name="escalate_to_human",
                description="Escalate the conversation to a human agent when the AI cannot help",
                func=self._escalate_to_human
            )
        ]
        return tools
    
    def _search_knowledge_base(self, query: str) -> str:
        """Search the knowledge base for relevant information"""
        try:
            # This would integrate with the vector store
            # For now, return a placeholder
            return f"Searching knowledge base for: {query}. Found relevant information about the topic."
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return "I couldn't search the knowledge base at the moment. Please try again."
    
    def _track_order(self, order_number: str) -> str:
        """Track an order"""
        try:
            # This would integrate with the order tracking system
            return f"Order {order_number} is currently being processed. Expected delivery in 2-3 business days."
        except Exception as e:
            logger.error(f"Error tracking order: {e}")
            return "I couldn't track your order at the moment. Please contact customer support."
    
    def _get_product_info(self, product_name: str) -> str:
        """Get product information"""
        try:
            # This would integrate with the product database
            return f"Here's information about {product_name}: It's a high-quality product with excellent reviews."
        except Exception as e:
            logger.error(f"Error getting product info: {e}")
            return "I couldn't retrieve product information at the moment. Please try again."
    
    def _escalate_to_human(self, reason: str) -> str:
        """Escalate to human agent"""
        return f"I'm connecting you with a human agent because: {reason}. Please hold while I transfer you."
    
    def _create_agent(self):
        """Create the LangChain agent"""
        try:
            # Create prompt template
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are TechBot Pro, an advanced AI customer support assistant for TechyMart. 
                You are helpful, friendly, and knowledgeable about all aspects of our products and services.
                
                You have access to the following tools:
                - search_knowledge_base: Search for information in our knowledge base
                - track_order: Track customer orders
                - get_product_info: Get detailed product information
                - escalate_to_human: Escalate to human agents when needed
                
                Always be helpful and provide accurate information. If you're not sure about something, 
                use the search_knowledge_base tool first before escalating to a human.
                
                Current conversation:
                {chat_history}
                
                Human: {input}
                Assistant:"""),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])
            
            # Create agent
            agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )
            
            return agent
            
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            return None
    
    def get_conversation_memory(self, session_id: str) -> ConversationBufferWindowMemory:
        """Get or create conversation memory for a session"""
        if session_id not in self.conversation_memories:
            self.conversation_memories[session_id] = ConversationBufferWindowMemory(
                k=10,  # Keep last 10 exchanges
                memory_key="chat_history",
                return_messages=True
            )
        return self.conversation_memories[session_id]
    
    def process_query_with_rag(self, 
                              query: str, 
                              session_id: str = "default",
                              context_documents: List[Dict] = None) -> Dict[str, Any]:
        """Process a query using RAG with LangChain"""
        try:
            # Get conversation memory
            memory = self.get_conversation_memory(session_id)
            
            # Prepare context from retrieved documents
            context = ""
            if context_documents:
                context = "\n\n".join([
                    f"Source: {doc.get('source', 'Unknown')}\nContent: {doc.get('content', '')}"
                    for doc in context_documents
                ])
            
            # Create enhanced prompt with context
            enhanced_query = f"""
            Context from knowledge base:
            {context}
            
            User query: {query}
            
            Please provide a helpful response based on the context above. If the context doesn't contain 
            enough information, use your tools to search for more information or escalate to a human if needed.
            """
            
            # Get conversation history
            chat_history = memory.chat_memory.messages
            
            # Process with agent
            if self.agent:
                try:
                    response = self.agent.invoke({
                        "input": enhanced_query,
                        "chat_history": chat_history
                    })
                    
                    # Extract response text
                    if isinstance(response, dict) and 'output' in response:
                        response_text = response['output']
                    else:
                        response_text = str(response)
                        
                except Exception as e:
                    logger.error(f"Error with agent: {e}")
                    response_text = self.llm.invoke([HumanMessage(content=enhanced_query)])
                    if hasattr(response_text, 'content'):
                        response_text = response_text.content
                    else:
                        response_text = str(response_text)
            else:
                # Fallback to direct LLM call
                response_text = self.llm.invoke([HumanMessage(content=enhanced_query)])
                if hasattr(response_text, 'content'):
                    response_text = response_text.content
                else:
                    response_text = str(response_text)
            
            # Save to memory
            memory.chat_memory.add_user_message(query)
            memory.chat_memory.add_ai_message(response_text)
            
            return {
                "response": response_text,
                "type": "rag_response",
                "confidence": 0.8,  # Placeholder confidence
                "context_used": len(context_documents) if context_documents else 0,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Error processing query with RAG: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try again.",
                "type": "error",
                "confidence": 0.0,
                "context_used": 0,
                "session_id": session_id
            }
    
    def create_conversation_graph(self) -> StateGraph:
        """Create a conversation graph using LangGraph"""
        try:
            # Define the state
            class ConversationState:
                def __init__(self):
                    self.messages = []
                    self.current_query = ""
                    self.context = []
                    self.response = ""
                    self.escalated = False
            
            # Define nodes
            def process_query(state: ConversationState):
                """Process the user query"""
                state.current_query = state.messages[-1] if state.messages else ""
                return state
            
            def retrieve_context(state: ConversationState):
                """Retrieve relevant context"""
                # This would integrate with the vector store
                state.context = [{"content": "Sample context"}]
                return state
            
            def generate_response(state: ConversationState):
                """Generate response using LLM"""
                if state.context:
                    context_text = "\n".join([ctx["content"] for ctx in state.context])
                    prompt = f"Context: {context_text}\n\nQuery: {state.current_query}\n\nResponse:"
                else:
                    prompt = f"Query: {state.current_query}\n\nResponse:"
                
                response = self.llm.invoke([HumanMessage(content=prompt)])
                if hasattr(response, 'content'):
                    state.response = response.content
                else:
                    state.response = str(response)
                return state
            
            def should_escalate(state: ConversationState):
                """Determine if conversation should be escalated"""
                # Simple escalation logic
                if "escalate" in state.response.lower() or "human" in state.response.lower():
                    state.escalated = True
                return state
            
            # Create the graph
            workflow = StateGraph(ConversationState)
            
            # Add nodes
            workflow.add_node("process_query", process_query)
            workflow.add_node("retrieve_context", retrieve_context)
            workflow.add_node("generate_response", generate_response)
            workflow.add_node("should_escalate", should_escalate)
            
            # Add edges
            workflow.add_edge("process_query", "retrieve_context")
            workflow.add_edge("retrieve_context", "generate_response")
            workflow.add_edge("generate_response", "should_escalate")
            workflow.add_edge("should_escalate", END)
            
            # Set entry point
            workflow.set_entry_point("process_query")
            
            return workflow.compile()
            
        except Exception as e:
            logger.error(f"Error creating conversation graph: {e}")
            return None
    
    def get_conversation_summary(self, session_id: str) -> str:
        """Get a summary of the conversation"""
        try:
            memory = self.get_conversation_memory(session_id)
            messages = memory.chat_memory.messages
            
            if not messages:
                return "No conversation history found."
            
            # Create a simple summary
            user_messages = [msg.content for msg in messages if isinstance(msg, HumanMessage)]
            ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
            
            summary = f"Conversation Summary:\n"
            summary += f"- User asked {len(user_messages)} questions\n"
            summary += f"- AI provided {len(ai_messages)} responses\n"
            summary += f"- Topics discussed: {', '.join(set(user_messages[:3]))}\n"
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            return "Error retrieving conversation summary."
    
    def clear_conversation_memory(self, session_id: str) -> bool:
        """Clear conversation memory for a session"""
        try:
            if session_id in self.conversation_memories:
                del self.conversation_memories[session_id]
                logger.info(f"Cleared conversation memory for session {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing conversation memory: {e}")
            return False

# Global LangChain integration instance
rag_langchain = RAGLangChainIntegration()
