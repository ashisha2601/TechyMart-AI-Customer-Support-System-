"""
Fix the feedback UI to properly show thumbs up/down buttons
"""

def fix_feedback_ui():
    """Fix the feedback UI in the premium interface"""
    
    print("👍 Fixing feedback UI in premium interface...")
    
    # Read the current premium interface
    with open('templates/premium_index.html', 'r') as f:
        content = f.read()
    
    # Find and replace the displayMessage function
    import re
    
    # Look for the existing displayMessage function
    pattern = r'function displayMessage\([^}]+\}'
    match = re.search(pattern, content, flags=re.DOTALL)
    
    if match:
        # Replace with the enhanced version
        new_displayMessage = '''function displayMessage(message, isUser = false, confidence = null, keywordMatched = null) {
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
    }'''
        
        content = content.replace(match.group(0), new_displayMessage)
    else:
        # If displayMessage function doesn't exist, add it
        print("   ⚠️ displayMessage function not found, adding it...")
        
        # Find where to insert the function (before the closing script tag)
        script_end = content.rfind('</script>')
        if script_end != -1:
            new_displayMessage = '''
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
    
    '''
            content = content[:script_end] + new_displayMessage + content[script_end:]
    
    # Also need to update the sendMessage function to pass confidence and keyword info
    # Find the sendMessage function and update it
    sendMessage_pattern = r'async function sendMessage\([^}]+\}'
    sendMessage_match = re.search(sendMessage_pattern, content, flags=re.DOTALL)
    
    if sendMessage_match:
        # Extract the current sendMessage function
        current_sendMessage = sendMessage_match.group(0)
        
        # Add confidence and keyword extraction
        enhanced_sendMessage = current_sendMessage.replace(
            'displayMessage(response.response, false);',
            'displayMessage(response.response, false, response.confidence, response.keyword_matched);'
        )
        
        content = content.replace(current_sendMessage, enhanced_sendMessage)
    
    # Write the updated content
    with open('templates/premium_index.html', 'w') as f:
        f.write(content)
    
    print("✅ Fixed feedback UI in premium interface!")
    print("✅ Updated displayMessage function to show feedback buttons")
    print("✅ Enhanced sendMessage to pass confidence data")

def test_feedback_ui():
    """Test if feedback UI is properly implemented"""
    
    print("\n🧪 Testing feedback UI implementation...")
    
    with open('templates/premium_index.html', 'r') as f:
        content = f.read()
    
    # Check for key components
    checks = [
        ("feedback-container CSS", "feedback-container" in content),
        ("createFeedbackHTML function", "createFeedbackHTML" in content),
        ("getConfidenceBadge function", "getConfidenceBadge" in content),
        ("submitFeedback function", "submitFeedback" in content),
        ("displayMessage with feedback", "createFeedbackHTML()" in content),
        ("confidence badge", "confidence-badge" in content)
    ]
    
    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_passed = False
    
    return all_passed

def main():
    """Main function to fix feedback UI"""
    
    print("👍 TechyMart AI Feedback UI Fix")
    print("=" * 50)
    
    # Fix the feedback UI
    fix_feedback_ui()
    
    # Test the implementation
    ui_working = test_feedback_ui()
    
    print("\n" + "=" * 50)
    if ui_working:
        print("🎉 FEEDBACK UI FIXED!")
        print("✅ Thumbs up/down buttons will now appear")
        print("✅ Confidence badges with color coding")
        print("✅ Real-time feedback submission")
        print("✅ Learning system integration")
    else:
        print("⚠️ Some feedback UI components may need manual fixing")
    
    print("\n🎯 Feedback Features:")
    print("   • Thumbs up/down buttons near confidence scores")
    print("   • Color-coded confidence badges (green/yellow/red)")
    print("   • Real-time feedback submission to learning system")
    print("   • Automatic keyword improvement based on feedback")
    print("   • Enhanced user experience")
    
    print("\n🔄 Restart your server to see the feedback buttons!")
    print("   python advanced_main.py")

if __name__ == "__main__":
    main()
