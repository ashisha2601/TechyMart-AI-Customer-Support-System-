"""
TechyMart Customer Support AI Agent - FastAPI Web Application
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
from chatbot import techymart_bot

app = FastAPI(title="TechyMart Customer Support AI", version="1.0.0")

# Setup templates
templates = Jinja2Templates(directory="templates")

# In-memory conversation storage (in production, use a proper database)
conversations = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main chatbot interface"""
    return templates.TemplateResponse("premium_index.html", {
        "request": request,
        "bot_name": "TechBot Pro",
        "welcome_message": techymart_bot.get_conversation_starter()
    })

@app.post("/chat")
async def chat(request: Request, message: str = Form(...), session_id: str = Form(default="default")):
    """Handle chat messages"""
    
    # Initialize conversation if new session
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message to conversation
    conversations[session_id].append({
        "role": "user",
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Generate bot response
    bot_response = techymart_bot.generate_response(message)
    
    # Add bot response to conversation
    conversations[session_id].append({
        "role": "bot",
        "message": bot_response['response'],
        "type": bot_response.get('type', 'general'),
        "escalate": bot_response.get('escalate', False),
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "response": bot_response['response'],
        "type": bot_response.get('type', 'general'),
        "escalate": bot_response.get('escalate', False),
        "confidence": bot_response.get('confidence', 0)
    }

@app.post("/chat/advanced")
async def advanced_chat(request: Request, message: str = Form(...), session_id: str = Form(default="default")):
    """Advanced chat endpoint for premium UI"""
    
    # Initialize conversation if new session
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message to conversation
    conversations[session_id].append({
        "role": "user",
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Generate bot response
    bot_response = techymart_bot.generate_response(message)
    
    # Add bot response to conversation
    conversations[session_id].append({
        "role": "bot",
        "message": bot_response['response'],
        "type": bot_response.get('type', 'general'),
        "escalate": bot_response.get('escalate', False),
        "timestamp": datetime.now().isoformat()
    })
    
    # Enhanced response for premium UI
    return {
        "response": bot_response['response'],
        "type": bot_response.get('type', 'general'),
        "escalate": bot_response.get('escalate', False),
        "confidence": bot_response.get('confidence', 0.95),
        "suggestions": [
            "Can I help with anything else?",
            "Need more information?",
            "Want to track an order?",
            "Have a return question?"
        ],
        "intent": {
            "intent": bot_response.get('type', 'general'),
            "confidence": bot_response.get('confidence', 0.95)
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "TechyMart Support AI"}

@app.get("/stats")
async def get_stats():
    """Get basic usage statistics"""
    total_conversations = len(conversations)
    total_messages = sum(len(conv) for conv in conversations.values())
    
    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "faq_count": len(techymart_bot.name)  # This would be expanded in a real app
    }

@app.post("/feedback")
async def submit_feedback(request: Request):
    """Handle user feedback for AI responses"""
    try:
        data = await request.json()
        
        # Simple feedback logging (in production, store in database)
        print(f"Feedback received: {data.get('feedback_type')} for message: {data.get('user_message', '')[:50]}...")
        
        return JSONResponse(content={
            "status": "success",
            "message": "Feedback recorded successfully",
            "feedback_id": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Feedback error: {e}")
        return JSONResponse(
            content={
                "status": "error", 
                "message": str(e)
            },
            status_code=500
        )

if __name__ == "__main__":
    print("🤖 Starting TechyMart Customer Support AI...")
    print("🌐 Open your browser to: http://localhost:8000")
    print("📚 API docs available at: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
