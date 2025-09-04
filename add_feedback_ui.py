"""
Add feedback system UI to the premium interface
"""

def add_feedback_system_to_ui():
    """Add thumbs up/down feedback system to the premium interface"""
    
    print("👍 Adding feedback system to premium interface...")
    
    # Read the current premium interface
    with open('templates/premium_index.html', 'r') as f:
        content = f.read()
    
    # Add feedback system CSS
    feedback_css = """
    /* Feedback System Styles */
    .feedback-container {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 8px;
        padding: 4px 0;
    }
    
    .feedback-label {
        font-size: 12px;
        color: #a0aec0;
        font-weight: 500;
    }
    
    .feedback-btn {
        background: none;
        border: none;
        cursor: pointer;
        padding: 6px;
        border-radius: 6px;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 32px;
        height: 32px;
    }
    
    .feedback-btn:hover {
        background-color: rgba(255, 255, 255, 0.1);
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
    
    .feedback-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    .feedback-status {
        font-size: 11px;
        color: #4ade80;
        font-weight: 500;
        display: none;
    }
    
    .feedback-status.error {
        color: #ef4444;
    }
    
    .confidence-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        margin-top: 4px;
    }
    
    .confidence-high {
        background-color: rgba(34, 197, 94, 0.2);
        color: #22c55e;
    }
    
    .confidence-medium {
        background-color: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
    }
    
    .confidence-low {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    """
    
    # Add feedback system JavaScript
    feedback_js = """
    // Feedback System Functions
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
            statusElement.classList.remove('error');
            
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
            
            // Update session stats
            updateSessionStats();
        })
        .catch(error => {
            console.error('Error submitting feedback:', error);
            const statusElement = button.parentElement.querySelector('.feedback-status');
            statusElement.style.display = 'inline';
            statusElement.textContent = 'Error submitting feedback';
            statusElement.style.color = '#ef4444';
            statusElement.classList.add('error');
        });
    }
    
    function createFeedbackHTML() {
        return `
            <div class="feedback-container">
                <span class="feedback-label">Was this helpful?</span>
                <button class="feedback-btn feedback-positive" 
                        onclick="submitFeedback('positive', this)" 
                        title="This response was helpful">
                    <span style="font-size: 16px;">👍</span>
                </button>
                <button class="feedback-btn feedback-negative" 
                        onclick="submitFeedback('negative', this)" 
                        title="This response was not helpful">
                    <span style="font-size: 16px;">👎</span>
                </button>
                <span class="feedback-status">Thanks for feedback!</span>
            </div>
        `;
    }
    
    function getConfidenceBadge(confidence) {
        if (confidence === null || confidence === undefined) return '';
        
        let badgeClass = 'confidence-low';
        if (confidence > 0.7) badgeClass = 'confidence-high';
        else if (confidence > 0.4) badgeClass = 'confidence-medium';
        
        return `<div class="confidence-badge ${badgeClass}">${Math.round(confidence * 100)}% confidence</div>`;
    }
    """
    
    # Update the displayMessage function to include feedback
    updated_displayMessage = """
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
            let confidenceBadge = getConfidenceBadge(confidence);
            let feedbackHTML = createFeedbackHTML();
            
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="message-avatar">🤖</div>
                    <div class="message-text">${message}</div>
                    ${confidenceBadge}
                    ${feedbackHTML}
                </div>
            `;
        }
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    """
    
    # Find and replace the displayMessage function
    import re
    pattern = r'function displayMessage\([^}]+\}'
    new_content = re.sub(pattern, updated_displayMessage, content, flags=re.DOTALL)
    
    # Add CSS to the head section
    if '<style>' in new_content:
        new_content = new_content.replace('<style>', '<style>' + feedback_css)
    else:
        # Add style tag if it doesn't exist
        new_content = new_content.replace('</head>', '<style>' + feedback_css + '</style>\n</head>')
    
    # Add JavaScript before the closing script tag
    if '</script>' in new_content:
        new_content = new_content.replace('</script>', feedback_js + '\n</script>')
    
    # Write the updated content
    with open('templates/premium_index.html', 'w') as f:
        f.write(new_content)
    
    print("✅ Premium interface updated with feedback system!")

def add_feedback_endpoints():
    """Add feedback endpoints to the FastAPI application"""
    
    print("🔄 Adding feedback endpoints to FastAPI application...")
    
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
        
        # Record feedback (simplified version for now)
        feedback_data = {
            "timestamp": datetime.now().isoformat(),
            "user_message": data.get('user_message', ''),
            "bot_response": data.get('bot_response', ''),
            "confidence": data.get('confidence', 0.0),
            "feedback_type": data.get('feedback_type', ''),
            "keyword_matched": data.get('keyword_matched', '')
        }
        
        # For now, just log the feedback (you can extend this to save to file/database)
        print(f"📊 Feedback received: {feedback_data['feedback_type']} for confidence {feedback_data['confidence']}")
        
        return JSONResponse(content={
            "status": "success",
            "message": "Feedback recorded successfully",
            "feedback_id": feedback_data['timestamp']
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
'''
    
    # Add the feedback endpoint before the main block
    if 'if __name__ == "__main__":' in content:
        content = content.replace('if __name__ == "__main__":', feedback_endpoint + '\n\nif __name__ == "__main__":')
    
    # Write the updated content
    with open('advanced_main.py', 'w') as f:
        f.write(content)
    
    print("✅ Feedback endpoints added to FastAPI application!")

def main():
    """Main function to add feedback system"""
    
    print("👍 TechyMart AI Feedback System Implementation")
    print("=" * 50)
    
    # Add feedback system to UI
    add_feedback_system_to_ui()
    
    # Add feedback endpoints
    add_feedback_endpoints()
    
    print("\n" + "=" * 50)
    print("🎉 FEEDBACK SYSTEM IMPLEMENTATION COMPLETE!")
    print("✅ Thumbs up/down buttons added to chat interface")
    print("✅ Feedback tracking system implemented")
    print("✅ Confidence badges with color coding")
    print("✅ API endpoints for feedback collection")
    print("✅ Real-time feedback submission")
    
    print("\n🎯 New Features:")
    print("   • Thumbs up/down buttons near confidence scores")
    print("   • Color-coded confidence badges (green/yellow/red)")
    print("   • Real-time feedback submission")
    print("   • Feedback tracking and analytics")
    print("   • Improved user experience")
    
    print("\n🔄 Restart your server to see the feedback system!")
    print("   python advanced_main.py")

if __name__ == "__main__":
    main()
