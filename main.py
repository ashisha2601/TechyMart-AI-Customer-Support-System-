"""
TechyMart Customer Support AI Agent - FastAPI Web Application
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
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
    return templates.TemplateResponse("index.html", {
        "request": request,
        "bot_name": "TechBot",
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
        "type": bot_response['type'],
        "escalate": bot_response.get('escalate', False),
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "response": bot_response['response'],
        "type": bot_response['type'],
        "escalate": bot_response.get('escalate', False),
        "confidence": bot_response.get('confidence', 0)
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
