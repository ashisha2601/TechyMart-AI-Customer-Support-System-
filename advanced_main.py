"""
Advanced TechyMart Customer Support AI - Premium FastAPI Application
Enhanced with advanced AI, analytics, and modern features
"""


from feedback_learning_system import FeedbackLearningSystem
from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
import json
import asyncio
from typing import Dict, List
import logging

# Import our advanced components
try:
    from advanced_chatbot import advanced_bot
    from rag_enhanced_chatbot import rag_enhanced_chatbot
    ADVANCED_MODE = True
    RAG_MODE = True
    print("🚀 Advanced AI system with RAG loaded successfully!")
except ImportError as e:
    print(f"⚠️ Advanced AI system unavailable: {e}")
    print("🔄 Falling back to basic system...")
    from chatbot import techymart_bot as advanced_bot
    ADVANCED_MODE = False
    RAG_MODE = False


# Initialize feedback learning system
feedback_learner = FeedbackLearningSystem()

app = FastAPI(
    title="TechyMart Customer Support AI - Premium",
    description="Advanced AI-powered customer support with premium features",
    version="2.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")

# Enhanced conversation storage with analytics
class ConversationManager:
    def __init__(self):
        self.conversations = {}
        self.analytics = {
            "total_sessions": 0,
            "total_messages": 0,
            "escalation_rate": 0,
            "avg_satisfaction": 0,
            "popular_topics": {}
        }
    
    def create_session(self, session_id: str) -> Dict:
        """Create a new conversation session"""
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "user_satisfaction": None,
                "escalated": False,
                "resolved": False,
                "topics": []
            }
            self.analytics["total_sessions"] += 1
        return self.conversations[session_id]
    
    def add_message(self, session_id: str, role: str, message: str, metadata: Dict = None):
        """Add a message to the conversation"""
        session = self.create_session(session_id)
        message_data = {
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        session["messages"].append(message_data)
        self.analytics["total_messages"] += 1
        
        # Track topics
        if metadata and "category" in metadata:
            category = metadata["category"]
            session["topics"].append(category)
            self.analytics["popular_topics"][category] = self.analytics["popular_topics"].get(category, 0) + 1
    
    def get_session_analytics(self, session_id: str) -> Dict:
        """Get analytics for a specific session"""
        if session_id not in self.conversations:
            return {"error": "Session not found"}
        
        session = self.conversations[session_id]
        message_count = len(session["messages"])
        user_messages = [m for m in session["messages"] if m["role"] == "user"]
        bot_messages = [m for m in session["messages"] if m["role"] == "bot"]
        
        escalations = sum(1 for m in bot_messages if m.get("metadata", {}).get("escalate", False))
        
        return {
            "session_id": session_id,
            "message_count": message_count,
            "user_messages": len(user_messages),
            "bot_messages": len(bot_messages),
            "escalation_count": escalations,
            "escalation_rate": escalations / max(len(bot_messages), 1),
            "topics_discussed": list(set(session["topics"])),
            "session_duration": self._calculate_duration(session),
            "created_at": session["created_at"]
        }
    
    def _calculate_duration(self, session: Dict) -> str:
        """Calculate session duration"""
        if not session["messages"]:
            return "0 minutes"
        
        start_time = datetime.fromisoformat(session["created_at"])
        last_message_time = datetime.fromisoformat(session["messages"][-1]["timestamp"])
        duration = last_message_time - start_time
        
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutes"
    
    def get_global_analytics(self) -> Dict:
        """Get global analytics across all sessions"""
        total_escalations = sum(
            sum(1 for m in session["messages"] 
                if m.get("metadata", {}).get("escalate", False))
            for session in self.conversations.values()
        )
        
        return {
            **self.analytics,
            "total_escalations": total_escalations,
            "escalation_rate": total_escalations / max(self.analytics["total_messages"], 1),
            "avg_messages_per_session": self.analytics["total_messages"] / max(self.analytics["total_sessions"], 1),
            "active_sessions": len(self.conversations)
        }

# Global conversation manager
conversation_manager = ConversationManager()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def premium_home(request: Request):
    """Premium chatbot interface"""
    return templates.TemplateResponse("premium_index.html", {
        "request": request,
        "bot_name": "TechBot Pro",
        "version": "2.0",
        "advanced_mode": ADVANCED_MODE
    })

@app.get("/classic", response_class=HTMLResponse)
async def classic_home(request: Request):
    """Classic chatbot interface for comparison"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "bot_name": "TechBot",
        "welcome_message": "Classic TechyMart Support"
    })

@app.get("/rag", response_class=HTMLResponse)
async def rag_home(request: Request):
    """RAG-enhanced chatbot interface"""
    return templates.TemplateResponse("rag_index.html", {
        "request": request,
        "bot_name": "TechBot Pro RAG",
        "welcome_message": "RAG-Enhanced TechyMart Support"
    })

@app.post("/chat/advanced")
async def advanced_chat(request: Request, message: str = Form(...), session_id: str = Form(default="default")):
    """Advanced chat endpoint with enhanced AI"""
    
    # Add user message to conversation
    conversation_manager.add_message(session_id, "user", message)
    
    # Generate advanced bot response
    if ADVANCED_MODE:
        bot_response = advanced_bot.generate_enhanced_response(message, session_id)
    else:
        # Fallback to basic bot with enhanced formatting
        basic_response = advanced_bot.generate_response(message)
        bot_response = {
            **basic_response,
            'suggestions': ["Can I help with anything else?"],
            'intent': {'intent': 'unknown', 'confidence': 0.5}
        }
    
    # Add bot response to conversation
    conversation_manager.add_message(
        session_id, 
        "bot", 
        bot_response['response'],
        {
            "type": bot_response['type'],
            "escalate": bot_response.get('escalate', False),
            "confidence": bot_response.get('confidence', 0),
            "category": bot_response.get('category')
        }
    )
    
    return JSONResponse(content=bot_response)

@app.post("/chat/rag")
async def rag_chat(request: Request, message: str = Form(...), session_id: str = Form(default="default")):
    """RAG-enhanced chat endpoint with advanced retrieval and generation"""
    
    # Add user message to conversation
    conversation_manager.add_message(session_id, "user", message)
    
    # Generate RAG-enhanced response
    if RAG_MODE:
        bot_response = rag_enhanced_chatbot.generate_response(message, session_id, use_rag=True)
    else:
        # Fallback to advanced bot
        bot_response = advanced_bot.generate_enhanced_response(message, session_id)
    
    # Add bot response to conversation
    conversation_manager.add_message(
        session_id, 
        "bot", 
        bot_response['response'],
        {
            "type": bot_response['type'],
            "escalate": bot_response.get('escalate', False),
            "confidence": bot_response.get('confidence', 0),
            "category": bot_response.get('category'),
            "method": bot_response.get('method', 'unknown'),
            "sources": bot_response.get('sources', []),
            "context_used": bot_response.get('context_used', 0)
        }
    )
    
    return JSONResponse(content=bot_response)

@app.post("/chat")
async def classic_chat(request: Request, message: str = Form(...), session_id: str = Form(default="default")):
    """Classic chat endpoint for backward compatibility"""
    
    # Add user message
    conversation_manager.add_message(session_id, "user", message)
    
    # Generate response using basic bot
    bot_response = advanced_bot.generate_response(message)
    
    # Add bot response
    conversation_manager.add_message(
        session_id,
        "bot", 
        bot_response['response'],
        {
            "type": bot_response['type'],
            "escalate": bot_response.get('escalate', False)
        }
    )
    
    return JSONResponse(content=bot_response)

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat_message":
                message = message_data["message"]
                
                # Add user message
                conversation_manager.add_message(session_id, "user", message)
                
                # Generate bot response
                if ADVANCED_MODE:
                    bot_response = advanced_bot.generate_enhanced_response(message, session_id)
                else:
                    bot_response = advanced_bot.generate_response(message)
                
                # Add bot response
                conversation_manager.add_message(
                    session_id,
                    "bot",
                    bot_response['response'],
                    {
                        "type": bot_response['type'],
                        "escalate": bot_response.get('escalate', False),
                        "confidence": bot_response.get('confidence', 0)
                    }
                )
                
                # Send response back
                await websocket.send_text(json.dumps({
                    "type": "bot_response",
                    "data": bot_response
                }))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/analytics/session/{session_id}")
async def get_session_analytics(session_id: str):
    """Get analytics for a specific session"""
    analytics = conversation_manager.get_session_analytics(session_id)
    return JSONResponse(content=analytics)

@app.get("/analytics/global")
async def get_global_analytics():
    """Get global analytics across all sessions"""
    analytics = conversation_manager.get_global_analytics()
    return JSONResponse(content=analytics)

@app.get("/health/advanced")
async def advanced_health_check():
    """Advanced health check with system status"""
    return JSONResponse(content={
        "status": "healthy",
        "service": "TechyMart Support AI Premium",
        "version": "2.0.0",
        "advanced_mode": ADVANCED_MODE,
        "features": {
            "advanced_rag": ADVANCED_MODE,
            "context_awareness": ADVANCED_MODE,
            "personality_adaptation": ADVANCED_MODE,
            "websocket_support": True,
            "analytics": True
        },
        "stats": conversation_manager.get_global_analytics()
    })

@app.get("/demo/features")
async def demo_features():
    """Demonstrate advanced features"""
    return JSONResponse(content={
        "advanced_features": {
            "semantic_search": "Uses sentence transformers for better understanding",
            "context_awareness": "Remembers conversation history and adapts responses",
            "personality_adaptation": "Switches between professional and friendly modes",
            "smart_escalation": "Intelligent routing based on query complexity",
            "real_time_analytics": "Live conversation tracking and insights",
            "websocket_support": "Real-time bidirectional communication",
            "confidence_scoring": "AI confidence levels for each response",
            "smart_suggestions": "Context-aware follow-up suggestions"
        },
        "rag_features": {
            "vector_search": "Advanced semantic search using FAISS/Pinecone",
            "document_retrieval": "Retrieves relevant documents from knowledge base",
            "conversation_memory": "LangGraph-powered conversation state management",
            "context_enhancement": "Enhances responses with retrieved context",
            "multi_source_rag": "Combines multiple knowledge sources",
            "intelligent_escalation": "Smart escalation based on confidence and context"
        },
        "ui_improvements": {
            "premium_design": "Modern glassmorphism design with animations",
            "responsive_layout": "Optimized for all device sizes",
            "accessibility": "WCAG compliant with keyboard navigation",
            "performance": "Optimized loading and smooth interactions",
            "visual_feedback": "Loading states, typing indicators, and status updates"
        }
    })

@app.get("/rag/status")
async def rag_status():
    """Get RAG system status and statistics"""
    try:
        if RAG_MODE:
            analytics = rag_enhanced_chatbot.get_conversation_analytics()
            return JSONResponse(content={
                "status": "active",
                "rag_mode": True,
                "analytics": analytics,
                "features": {
                    "vector_search": True,
                    "conversation_memory": True,
                    "document_retrieval": True,
                    "context_enhancement": True
                }
            })
        else:
            return JSONResponse(content={
                "status": "inactive",
                "rag_mode": False,
                "message": "RAG system not available"
            })
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.get("/rag/analytics")
async def rag_analytics():
    """Get detailed RAG analytics"""
    try:
        if RAG_MODE:
            analytics = rag_enhanced_chatbot.get_conversation_analytics()
            return JSONResponse(content=analytics)
        else:
            return JSONResponse(
                content={"error": "RAG system not available"},
                status_code=404
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.post("/rag/clear-conversation")
async def clear_rag_conversation(request: Request):
    """Clear conversation memory for a session"""
    try:
        data = await request.json()
        session_id = data.get('session_id', 'default')
        
        if RAG_MODE:
            success = rag_enhanced_chatbot.clear_conversation(session_id)
            return JSONResponse(content={
                "status": "success" if success else "failed",
                "session_id": session_id,
                "message": "Conversation cleared" if success else "Failed to clear conversation"
            })
        else:
            return JSONResponse(
                content={"error": "RAG system not available"},
                status_code=404
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.post("/rag/add-documents")
async def add_documents_to_rag(request: Request):
    """Add new documents to the RAG knowledge base"""
    try:
        data = await request.json()
        documents = data.get('documents', [])
        
        if not documents:
            return JSONResponse(
                content={"error": "No documents provided"},
                status_code=400
            )
        
        if RAG_MODE:
            success = rag_enhanced_chatbot.add_documents_to_knowledge_base(documents)
            return JSONResponse(content={
                "status": "success" if success else "failed",
                "documents_added": len(documents),
                "message": "Documents added to knowledge base" if success else "Failed to add documents"
            })
        else:
            return JSONResponse(
                content={"error": "RAG system not available"},
                status_code=404
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/rag/conversation/{session_id}")
async def get_rag_conversation(session_id: str):
    """Get conversation history for a specific session"""
    try:
        if RAG_MODE:
            from rag_conversation_memory import rag_conversation_memory
            history = rag_conversation_memory.get_conversation_history(session_id)
            analytics = rag_conversation_memory.get_conversation_analytics(session_id)
            
            return JSONResponse(content={
                "session_id": session_id,
                "conversation_history": history,
                "analytics": analytics
            })
        else:
            return JSONResponse(
                content={"error": "RAG system not available"},
                status_code=404
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )




@app.post("/feedback")
async def submit_feedback(request: Request):
    """Handle user feedback for AI responses with learning capabilities"""
    try:
        data = await request.json()
        
        # Record feedback with learning system
        feedback_learner.record_feedback(
            user_message=data.get('user_message', ''),
            bot_response=data.get('bot_response', ''),
            confidence=data.get('confidence', 0.0),
            feedback_type=data.get('feedback_type', ''),
            keyword_matched=data.get('keyword_matched', '')
        )
        
        # Get updated statistics
        stats = feedback_learner.get_learning_statistics()
        
        return JSONResponse(content={
            "status": "success",
            "message": "Feedback recorded and learning system updated",
            "feedback_id": datetime.now().isoformat(),
            "learning_stats": stats
        })
        
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.get("/feedback/stats")
async def get_feedback_stats():
    """Get comprehensive feedback and learning statistics"""
    try:
        stats = feedback_learner.get_learning_statistics()
        return JSONResponse(content=stats)
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.get("/feedback/learning-report")
async def get_learning_report():
    """Get detailed learning system report"""
    try:
        report = feedback_learner.export_learning_report()
        return JSONResponse(content={"report": report})
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.post("/feedback/force-learn")
async def force_learning():
    """Force the learning system to analyze and learn from feedback"""
    try:
        feedback_learner.analyze_and_learn()
        stats = feedback_learner.get_learning_statistics()
        return JSONResponse(content={
            "status": "success",
            "message": "Learning analysis completed",
            "stats": stats
        })
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
@app.get("/feedback/stats")
async def get_feedback_stats():
    """Get comprehensive feedback and learning statistics"""
    try:
        stats = feedback_learner.get_learning_statistics()
        return JSONResponse(content=stats)
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.get("/feedback/learning-report")
async def get_learning_report():
    """Get detailed learning system report"""
    try:
        report = feedback_learner.export_learning_report()
        return JSONResponse(content={"report": report})
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.post("/feedback/force-learn")
async def force_learning():
    """Force the learning system to analyze and learn from feedback"""
    try:
        feedback_learner.analyze_and_learn()
        stats = feedback_learner.get_learning_statistics()
        return JSONResponse(content={
            "status": "success",
            "message": "Learning analysis completed",
            "stats": stats
        })
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
@app.get("/feedback/stats")
async def get_feedback_stats():
    """Get feedback statistics"""
    return JSONResponse(content={
        "message": "Feedback system is active",
        "total_feedback": 0,
        "positive_feedback": 0,
        "negative_feedback": 0,
        "satisfaction_rate": 0
    })


if __name__ == "__main__":
    print("🚀 Starting TechyMart Customer Support AI - Premium Edition with RAG...")
    print("🌐 Premium interface: http://localhost:8000")
    print("🔧 Classic interface: http://localhost:8000/classic")
    print("🧠 RAG interface: http://localhost:8000/rag")
    print("📊 Analytics: http://localhost:8000/analytics/global")
    print("📚 API docs: http://localhost:8000/docs")
    print("🎯 Feature demo: http://localhost:8000/demo/features")
    print("🧠 RAG status: http://localhost:8000/rag/status")
    print("📈 RAG analytics: http://localhost:8000/rag/analytics")
    
    if ADVANCED_MODE:
        print("✅ Advanced AI features enabled!")
    else:
        print("⚠️ Running in basic mode - install advanced dependencies for full features")
    
    if RAG_MODE:
        print("🧠 RAG system enabled with vector search and conversation memory!")
    else:
        print("⚠️ RAG system not available - install RAG dependencies for full features")
    
    uvicorn.run(
        "advanced_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
