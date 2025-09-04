"""
Add thumbs up/down feedback system to improve AI accuracy
"""

import json
from datetime import datetime
from typing import Dict, List

class FeedbackSystem:
    def __init__(self):
        self.feedback_file = "feedback_data.json"
        self.feedback_data = self.load_feedback()
        
    def load_feedback(self) -> Dict:
        """Load existing feedback data"""
        try:
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "total_feedback": 0,
                "positive_feedback": 0,
                "negative_feedback": 0,
                "keyword_feedback": {},
                "confidence_improvements": {},
                "response_improvements": {}
            }
    
    def save_feedback(self):
        """Save feedback data to file"""
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
    
    def record_feedback(self, user_message: str, bot_response: str, confidence: float, 
                       feedback_type: str, keyword_matched: str = None):
        """Record user feedback for a response"""
        
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "bot_response": bot_response,
            "confidence": confidence,
            "feedback_type": feedback_type,  # "positive" or "negative"
            "keyword_matched": keyword_matched
        }
        
        # Update overall stats
        self.feedback_data["total_feedback"] += 1
        if feedback_type == "positive":
            self.feedback_data["positive_feedback"] += 1
        else:
            self.feedback_data["negative_feedback"] += 1
        
        # Update keyword-specific feedback
        if keyword_matched:
            if keyword_matched not in self.feedback_data["keyword_feedback"]:
                self.feedback_data["keyword_feedback"][keyword_matched] = {
                    "total": 0,
                    "positive": 0,
                    "negative": 0
                }
            
            self.feedback_data["keyword_feedback"][keyword_matched]["total"] += 1
            if feedback_type == "positive":
                self.feedback_data["keyword_feedback"][keyword_matched]["positive"] += 1
            else:
                self.feedback_data["keyword_feedback"][keyword_matched]["negative"] += 1
        
        # Track confidence improvements
        confidence_range = f"{int(confidence * 10) * 10}-{int(confidence * 10) * 10 + 9}%"
        if confidence_range not in self.feedback_data["confidence_improvements"]:
            self.feedback_data["confidence_improvements"][confidence_range] = {
                "total": 0,
                "positive": 0,
                "negative": 0
            }
        
        self.feedback_data["confidence_improvements"][confidence_range]["total"] += 1
        if feedback_type == "positive":
            self.feedback_data["confidence_improvements"][confidence_range]["positive"] += 1
        else:
            self.feedback_data["confidence_improvements"][confidence_range]["negative"] += 1
        
        self.save_feedback()
        return feedback_entry
    
    def get_feedback_stats(self) -> Dict:
        """Get comprehensive feedback statistics"""
        total = self.feedback_data["total_feedback"]
        if total == 0:
            return {"message": "No feedback received yet"}
        
        positive = self.feedback_data["positive_feedback"]
        negative = self.feedback_data["negative_feedback"]
        
        return {
            "total_feedback": total,
            "positive_feedback": positive,
            "negative_feedback": negative,
            "satisfaction_rate": (positive / total) * 100,
            "keyword_performance": self.feedback_data["keyword_feedback"],
            "confidence_performance": self.feedback_data["confidence_improvements"]
        }
    
    def get_keyword_improvements(self) -> List[Dict]:
        """Get keywords that need improvement based on feedback"""
        improvements = []
        
        for keyword, data in self.feedback_data["keyword_feedback"].items():
            if data["total"] >= 3:  # Only consider keywords with enough feedback
                satisfaction_rate = (data["positive"] / data["total"]) * 100
                if satisfaction_rate < 70:  # Low satisfaction rate
                    improvements.append({
                        "keyword": keyword,
                        "satisfaction_rate": satisfaction_rate,
                        "total_feedback": data["total"],
                        "positive": data["positive"],
                        "negative": data["negative"],
                        "recommendation": "Consider improving response or adding more context"
                    })
        
        return sorted(improvements, key=lambda x: x["satisfaction_rate"])

# Global feedback system instance
feedback_system = FeedbackSystem()

def create_feedback_html():
    """Create HTML for feedback buttons"""
    
    feedback_html = """
    <div class="feedback-container" style="display: flex; align-items: center; gap: 8px; margin-top: 8px;">
        <span class="feedback-label" style="font-size: 12px; color: #a0aec0;">Was this helpful?</span>
        <button class="feedback-btn feedback-positive" 
                onclick="submitFeedback('positive', this)" 
                style="background: none; border: none; cursor: pointer; padding: 4px; border-radius: 4px; transition: all 0.2s;">
            <span style="font-size: 16px;">👍</span>
        </button>
        <button class="feedback-btn feedback-negative" 
                onclick="submitFeedback('negative', this)" 
                style="background: none; border: none; cursor: pointer; padding: 4px; border-radius: 4px; transition: all 0.2s;">
            <span style="font-size: 16px;">👎</span>
        </button>
        <span class="feedback-status" style="font-size: 11px; color: #4ade80; display: none;">Thanks for feedback!</span>
    </div>
    
    <style>
    .feedback-btn:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        transform: scale(1.1);
    }
    .feedback-btn:active {
        transform: scale(0.95);
    }
    .feedback-positive:hover {
        background-color: rgba(34, 197, 94, 0.2) !important;
    }
    .feedback-negative:hover {
        background-color: rgba(239, 68, 68, 0.2) !important;
    }
    </style>
    
    <script>
    function submitFeedback(type, button) {
        // Get the current message data
        const messageContainer = button.closest('.message-container');
        const userMessage = messageContainer.dataset.userMessage || '';
        const botResponse = messageContainer.dataset.botResponse || '';
        const confidence = parseFloat(messageContainer.dataset.confidence || 0);
        const keywordMatched = messageContainer.dataset.keywordMatched || '';
        
        // Send feedback to server
        fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_message: userMessage,
                bot_response: botResponse,
                confidence: confidence,
                feedback_type: type,
                keyword_matched: keywordMatched
            })
        })
        .then(response => response.json())
        .then(data => {
            // Show feedback status
            const statusElement = button.parentElement.querySelector('.feedback-status');
            statusElement.style.display = 'inline';
            statusElement.textContent = 'Thanks for feedback!';
            
            // Disable buttons
            const buttons = button.parentElement.querySelectorAll('.feedback-btn');
            buttons.forEach(btn => {
                btn.disabled = true;
                btn.style.opacity = '0.5';
            });
            
            // Highlight selected button
            if (type === 'positive') {
                button.style.backgroundColor = 'rgba(34, 197, 94, 0.3)';
            } else {
                button.style.backgroundColor = 'rgba(239, 68, 68, 0.3)';
            }
        })
        .catch(error => {
            console.error('Error submitting feedback:', error);
            const statusElement = button.parentElement.querySelector('.feedback-status');
            statusElement.style.display = 'inline';
            statusElement.textContent = 'Error submitting feedback';
            statusElement.style.color = '#ef4444';
        });
    }
    </script>
    """
    
    return feedback_html

def update_premium_interface():
    """Update the premium interface to include feedback system"""
    
    print("🔄 Updating premium interface with feedback system...")
    
    # Read the current premium interface
    with open('templates/premium_index.html', 'r') as f:
        content = f.read()
    
    # Add feedback system to message display
    feedback_integration = """
    // Add feedback system to message display
    function displayMessage(message, isUser = false, confidence = null, keywordMatched = null) {
        const messagesContainer = document.getElementById('messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.setAttribute('data-user-message', isUser ? message : '');
        messageDiv.setAttribute('data-bot-response', isUser ? '' : message);
        messageDiv.setAttribute('data-confidence', confidence || 0);
        messageDiv.setAttribute('data-keyword-matched', keywordMatched || '');
        messageDiv.classList.add('message-container');
        
        if (isUser) {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="message-avatar">👤</div>
                    <div class="message-text">${message}</div>
                </div>
            `;
        } else {
            let confidenceBadge = '';
            if (confidence !== null) {
                const confidenceClass = confidence > 0.7 ? 'confidence-high' : confidence > 0.4 ? 'confidence-medium' : 'confidence-low';
                confidenceBadge = `<div class="confidence-badge ${confidenceClass}">${Math.round(confidence * 100)}% confidence</div>`;
            }
            
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="message-avatar">🤖</div>
                    <div class="message-text">${message}</div>
                    ${confidenceBadge}
                    ${create_feedback_html()}
                </div>
            `;
        }
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    """
    
    # Find the displayMessage function and replace it
    import re
    pattern = r'function displayMessage\([^}]+\}'
    new_content = re.sub(pattern, feedback_integration, content, flags=re.DOTALL)
    
    # Add feedback endpoint handling
    feedback_endpoint = """
    // Handle feedback submission
    async function handleFeedback(data) {
        try {
            const response = await fetch('/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                console.log('Feedback submitted successfully');
                return true;
            } else {
                console.error('Failed to submit feedback');
                return false;
            }
        } catch (error) {
            console.error('Error submitting feedback:', error);
            return false;
        }
    }
    """
    
    # Add the feedback endpoint handling before the closing script tag
    if '</script>' in new_content:
        new_content = new_content.replace('</script>', feedback_endpoint + '\n</script>')
    
    # Write the updated content
    with open('templates/premium_index.html', 'w') as f:
        f.write(new_content)
    
    print("✅ Premium interface updated with feedback system!")

def add_feedback_endpoint():
    """Add feedback endpoint to the FastAPI application"""
    
    print("🔄 Adding feedback endpoint to FastAPI application...")
    
    # Read the current advanced_main.py
    with open('advanced_main.py', 'r') as f:
        content = f.read()
    
    # Add feedback endpoint
    feedback_endpoint = '''
@app.post("/feedback")
async def submit_feedback(request: Request):
    """Handle user feedback for AI responses"""
    try:
        data = await request.json()
        
        # Record feedback
        feedback_entry = feedback_system.record_feedback(
            user_message=data.get('user_message', ''),
            bot_response=data.get('bot_response', ''),
            confidence=data.get('confidence', 0.0),
            feedback_type=data.get('feedback_type', ''),
            keyword_matched=data.get('keyword_matched', '')
        )
        
        return JSONResponse(content={
            "status": "success",
            "message": "Feedback recorded successfully",
            "feedback_id": feedback_entry.get('timestamp', '')
        })
        
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.get("/feedback/stats")
async def get_feedback_stats():
    """Get feedback statistics"""
    stats = feedback_system.get_feedback_stats()
    return JSONResponse(content=stats)

@app.get("/feedback/improvements")
async def get_feedback_improvements():
    """Get keywords that need improvement"""
    improvements = feedback_system.get_keyword_improvements()
    return JSONResponse(content=improvements)
'''
    
    # Add the feedback endpoint before the main block
    if 'if __name__ == "__main__":' in content:
        content = content.replace('if __name__ == "__main__":', feedback_endpoint + '\n\nif __name__ == "__main__":')
    
    # Add import for feedback system
    if 'from keyword_manager import keyword_manager' in content:
        content = content.replace(
            'from keyword_manager import keyword_manager',
            'from keyword_manager import keyword_manager\nfrom add_feedback_system import feedback_system'
        )
    
    # Write the updated content
    with open('advanced_main.py', 'w') as f:
        f.write(content)
    
    print("✅ Feedback endpoint added to FastAPI application!")

def main():
    """Main function to add feedback system"""
    
    print("👍 TechyMart AI Feedback System Enhancement")
    print("=" * 50)
    
    # Add shortform recognition first
    print("🔤 Adding shortform recognition...")
    from add_shortforms import main as add_shortforms_main
    add_shortforms_main()
    
    # Update premium interface
    update_premium_interface()
    
    # Add feedback endpoint
    add_feedback_endpoint()
    
    print("\n" + "=" * 50)
    print("🎉 FEEDBACK SYSTEM ENHANCEMENT COMPLETE!")
    print("✅ Shortform recognition added")
    print("✅ Thumbs up/down feedback system added")
    print("✅ Feedback tracking and analytics added")
    print("✅ Interface updated with feedback buttons")
    print("✅ API endpoints for feedback added")
    
    print("\n🎯 New Features:")
    print("   • Understands shortforms: 'ok', 'gpay', 'no', 'yes', etc.")
    print("   • Thumbs up/down buttons near confidence scores")
    print("   • Feedback tracking and analytics")
    print("   • Keyword performance monitoring")
    print("   • Confidence-based improvements")
    
    print("\n🔄 Restart your server to see the enhanced system!")
    print("   python advanced_main.py")

if __name__ == "__main__":
    main()
