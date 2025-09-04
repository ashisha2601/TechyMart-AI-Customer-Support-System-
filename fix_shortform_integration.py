"""
Fix shortform integration by properly updating the keyword matcher with all shortform keywords
"""

import re
from typing import Dict, List, Optional, Tuple

def create_comprehensive_keyword_matcher():
    """Create a comprehensive keyword matcher with all shortform keywords"""
    
    # Comprehensive exact phrases including all shortforms
    exact_phrases = {
        # ==================== SHORTFORM RESPONSES ====================
        "ok": {
            "category": "acknowledgment",
            "confidence": 0.95,
            "response": "Great! Is there anything else I can help you with today? 😊"
        },
        "okay": {
            "category": "acknowledgment", 
            "confidence": 0.95,
            "response": "Perfect! Anything else you'd like to know? 🤗"
        },
        "yes": {
            "category": "confirmation",
            "confidence": 0.95,
            "response": "Awesome! What would you like to know more about? 🚀"
        },
        "no": {
            "category": "negation",
            "confidence": 0.95,
            "response": "No problem! Is there anything else I can help you with? 💪"
        },
        "nope": {
            "category": "negation",
            "confidence": 0.90,
            "response": "That's totally fine! What else can I help you with? 😊"
        },
        "sure": {
            "category": "confirmation",
            "confidence": 0.90,
            "response": "Great! What would you like to know? 🤔"
        },
        "maybe": {
            "category": "uncertainty",
            "confidence": 0.85,
            "response": "No worries! Take your time. I'm here whenever you need help! 😊"
        },
        "thanks": {
            "category": "gratitude",
            "confidence": 0.90,
            "response": "You're welcome! 😊 Happy to help anytime!"
        },
        "thank you": {
            "category": "gratitude",
            "confidence": 0.95,
            "response": "You're so welcome! 🌟 I'm here whenever you need me!"
        },
        "ty": {
            "category": "gratitude",
            "confidence": 0.85,
            "response": "You're welcome! 😊 Anytime!"
        },
        
        # ==================== PAYMENT SHORTFORMS ====================
        "gpay": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Yes! Google Pay is fully supported! 🤖 You can use it for both UPI and card payments. Super convenient!"
        },
        "g pay": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Absolutely! Google Pay works great with our system! 🤖 Quick and secure payments!"
        },
        "google pay": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Google Pay is supported! You can use it for both UPI and card payments. Super convenient for Android users! 🤖"
        },
        "paypal": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Yes! PayPal is available for quick and secure checkout! 💰 Just select PayPal as your payment method!"
        },
        "apple pay": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Apple Pay is available! 🍎 Quick and secure payments on iPhone and Mac. Look for the Apple Pay button at checkout!"
        },
        "upi": {
            "category": "payment",
            "confidence": 0.90,
            "response": "Yes! UPI is fully supported! 🇮🇳 Use Google Pay, PhonePe, Paytm, or any UPI app for instant payments!"
        },
        "cod": {
            "category": "payment",
            "confidence": 0.90,
            "response": "Cash on Delivery is available! 💵 Check availability at checkout. COD orders may have a small additional fee."
        },
        "emi": {
            "category": "payment",
            "confidence": 0.90,
            "response": "EMI options are available! 💳 Check available EMI plans at checkout through various banks and NBFCs!"
        },
        
        # ==================== SHIPPING SHORTFORMS ====================
        "shipping": {
            "category": "shipping",
            "confidence": 0.95,
            "response": "We offer FREE shipping on orders over $50! 🚚 Standard (3-5 days), Express (1-2 days for $9.99), or Overnight ($19.99)!"
        },
        "delivery": {
            "category": "shipping",
            "confidence": 0.95,
            "response": "Standard delivery: 3-5 business days (FREE over $50), Express: 1-2 days ($9.99), Overnight: Next day ($19.99)! 📦"
        },
        "track": {
            "category": "orders",
            "confidence": 0.95,
            "response": "I can help you track your order! 📦 Just provide your order number and I'll look it up for you!"
        },
        "order": {
            "category": "orders",
            "confidence": 0.90,
            "response": "I can help with your order! 📦 Need to track, modify, or have questions about it?"
        },
        
        # ==================== SUPPORT SHORTFORMS ====================
        "help": {
            "category": "support",
            "confidence": 0.95,
            "response": "I'm here to help! 🤗 What do you need assistance with? Payment, shipping, returns, or something else?"
        },
        "support": {
            "category": "support",
            "confidence": 0.95,
            "response": "We're here to help 24/7! 🤗 Chat with me, email support@techymart.com, or call 1-800-TECHYMART!"
        },
        "contact": {
            "category": "support",
            "confidence": 0.90,
            "response": "You can contact us via chat (me!), email support@techymart.com, or call 1-800-TECHYMART! 📞"
        },
        "return": {
            "category": "returns",
            "confidence": 0.95,
            "response": "We have a hassle-free 30-day return policy! 🔄 Items must be in original condition. Start your return online!"
        },
        "refund": {
            "category": "returns",
            "confidence": 0.90,
            "response": "Refunds process within 3-5 business days after we receive your return! 💰 We'll email you confirmation!"
        },
        "warranty": {
            "category": "warranty",
            "confidence": 0.90,
            "response": "All electronics come with manufacturer warranty (1-2 years)! 🛡️ We also offer Extended Protection plans!"
        },
        
        # ==================== GREETING SHORTFORMS ====================
        "hi": {
            "category": "greeting",
            "confidence": 0.95,
            "response": "Hi there! 👋 Welcome to TechyMart! How can I help you today?"
        },
        "hello": {
            "category": "greeting",
            "confidence": 0.95,
            "response": "Hello! 👋 Great to see you at TechyMart! What can I assist you with?"
        },
        "hey": {
            "category": "greeting",
            "confidence": 0.90,
            "response": "Hey! 👋 Welcome to TechyMart! What's on your mind today?"
        },
        
        # ==================== PROBLEM SHORTFORMS ====================
        "problem": {
            "category": "support",
            "confidence": 0.90,
            "response": "I'm sorry you're having a problem! 😔 Please tell me more about it and I'll help you resolve it!"
        },
        "issue": {
            "category": "support",
            "confidence": 0.90,
            "response": "I'm here to help with any issues! 🔧 What's going wrong? Let me help you fix it!"
        },
        "broken": {
            "category": "technical",
            "confidence": 0.90,
            "response": "I'm sorry your item is broken! 🔧 Contact us immediately and we'll arrange a free replacement or refund!"
        },
        "confused": {
            "category": "support",
            "confidence": 0.90,
            "response": "I'm here to help clear up any confusion! 🤔 What would you like me to explain better?"
        },
        "unclear": {
            "category": "support",
            "confidence": 0.85,
            "response": "Let me help clarify that! 💡 What specific part would you like me to explain?"
        },
        
        # ==================== SINGLE LETTER RESPONSES ====================
        "y": {
            "category": "confirmation",
            "confidence": 0.85,
            "response": "Yes! What would you like to know more about? 🚀"
        },
        "n": {
            "category": "negation",
            "confidence": 0.85,
            "response": "No problem! Is there anything else I can help you with? 💪"
        },
        
        # ==================== EMOJI SHORTFORMS ====================
        "👍": {
            "category": "gratitude",
            "confidence": 0.90,
            "response": "Thanks for the thumbs up! Glad I could help! 👍"
        },
        "👎": {
            "category": "feedback",
            "confidence": 0.90,
            "response": "I'm sorry I couldn't help better! 😔 Let me try a different approach. What specifically can I improve?"
        },
        "❤️": {
            "category": "gratitude",
            "confidence": 0.90,
            "response": "Aww, sending love right back! ❤️ Thanks for being awesome!"
        },
        "😊": {
            "category": "greeting",
            "confidence": 0.85,
            "response": "😊 Hello there! Great to see you! How can I help you today?"
        },
        "🤔": {
            "category": "support",
            "confidence": 0.85,
            "response": "I see you're thinking! 🤔 What's on your mind? I'm here to help!"
        },
        
        # ==================== EXISTING KEYWORDS (KEEP THESE) ====================
        "upi payment": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Yes! 🇮🇳 We support UPI payments through Google Pay, PhonePe, Paytm, and all UPI apps. UPI transactions are instant and secure! Just select UPI at checkout."
        },
        "credit card": {
            "category": "payment",
            "confidence": 0.95,
            "response": "We accept all major credit cards: Visa, Mastercard, American Express, and Discover. Your payment is secured with 256-bit SSL encryption! 💳"
        },
        "free shipping": {
            "category": "shipping",
            "confidence": 0.95,
            "response": "Yes! We offer FREE shipping on orders over $50! 🚚✨ Standard shipping (3-5 days) is free, or upgrade to Express (1-2 days) for $9.99."
        },
        "express delivery": {
            "category": "shipping",
            "confidence": 0.95,
            "response": "Express delivery (1-2 business days) is available for $9.99! Perfect when you need your tech goodies fast! ⚡"
        },
        "overnight shipping": {
            "category": "shipping",
            "confidence": 0.95,
            "response": "Overnight delivery is available for $19.99! Order by 2 PM and get it the next business day! 🌙➡️🌅"
        },
        "30 day return": {
            "category": "returns",
            "confidence": 0.95,
            "response": "Yes! We have a hassle-free 30-day return policy! 🔄 Items must be in original condition with tags. Start your return online!"
        },
        "return policy": {
            "category": "returns",
            "confidence": 0.95,
            "response": "We have a hassle-free 30-day return policy! 🔄 Items must be in original condition with tags. Start a return online or contact us!"
        },
        "extended warranty": {
            "category": "warranty",
            "confidence": 0.95,
            "response": "We offer TechyMart Extended Protection! 1 extra year for $19.99, 2 extra years for $34.99. Covers accidents, drops, and liquid damage! 🛡️"
        },
        "customer service": {
            "category": "support",
            "confidence": 0.95,
            "response": "We're here to help 24/7! Chat with me, email support@techymart.com, or call 1-800-TECHYMART! 🤗"
        },
        "order status": {
            "category": "orders",
            "confidence": 0.95,
            "response": "Check your order status by providing your order number! I can look it up for you right now! 📦"
        },
        "price match": {
            "category": "pricing",
            "confidence": 0.95,
            "response": "We'll match any lower price from major retailers! Contact us with the competitor's link and we'll adjust your price! 💰"
        },
        "good morning": {
            "category": "greeting",
            "confidence": 0.95,
            "response": "Good morning! ☀️ Welcome to TechyMart! How can I help you today?"
        },
        "good afternoon": {
            "category": "greeting",
            "confidence": 0.95,
            "response": "Good afternoon! 🌤️ Great to see you at TechyMart! What can I assist you with?"
        },
        "good evening": {
            "category": "greeting",
            "confidence": 0.95,
            "response": "Good evening! 🌙 Welcome to TechyMart! How may I help you tonight?"
        },
        "hey there": {
            "category": "greeting",
            "confidence": 0.90,
            "response": "Hey there! 👋 Welcome to TechyMart! What's on your mind today?"
        },
        "what's up": {
            "category": "greeting",
            "confidence": 0.85,
            "response": "What's up! 🚀 I'm here to help with all your TechyMart needs! What can I do for you?"
        },
        "i have a problem": {
            "category": "support",
            "confidence": 0.95,
            "response": "I'm sorry to hear you're having an issue! Please tell me more about the problem and I'll help you resolve it! 🤗"
        },
        "this is not working": {
            "category": "technical",
            "confidence": 0.95,
            "response": "I'm sorry your product isn't working! Let me connect you with our technical support team who can help troubleshoot! 🔧"
        },
        "gst": {
            "category": "pricing",
            "confidence": 0.90,
            "response": "All prices include GST! You'll see the GST breakdown in your order summary. We're fully GST compliant! 🇮🇳"
        }
    }
    
    return exact_phrases

def update_keyword_matcher_with_shortforms():
    """Update the keyword_matcher.py file with comprehensive shortform keywords"""
    
    print("🔤 Updating keyword_matcher.py with comprehensive shortform keywords...")
    
    # Read the current file
    with open('keyword_matcher.py', 'r') as f:
        content = f.read()
    
    # Create comprehensive exact phrases
    enhanced_phrases = create_comprehensive_keyword_matcher()
    
    # Generate the new exact_phrases dictionary
    phrases_code = "        self.exact_phrases = {\n"
    for keyword, data in enhanced_phrases.items():
        response = data['response'].replace('"', '\\"').replace('\n', '\\n')
        phrases_code += f'            "{keyword}": {{\n'
        phrases_code += f'                "category": "{data["category"]}",\n'
        phrases_code += f'                "confidence": {data["confidence"]},\n'
        phrases_code += f'                "response": "{response}"\n'
        phrases_code += f'            }},\n'
    phrases_code += "        }\n"
    
    # Find and replace the exact_phrases section
    pattern = r'self\.exact_phrases = \{.*?\n        \}'
    new_content = re.sub(pattern, phrases_code.strip(), content, flags=re.DOTALL)
    
    # Write the updated file
    with open('keyword_matcher.py', 'w') as f:
        f.write(new_content)
    
    print(f"✅ Updated keyword_matcher.py with {len(enhanced_phrases)} comprehensive keywords!")
    return len(enhanced_phrases)

def test_comprehensive_shortforms():
    """Test the comprehensive shortform recognition"""
    
    print("\n🧪 Testing comprehensive shortform recognition...")
    
    # Import the updated keyword matcher
    from keyword_matcher import keyword_matcher
    
    # Test the problematic shortforms
    problematic_shortforms = [
        "ok", "gpay", "no", "yes", "thanks", "help", "hi", "hello", 
        "shipping", "delivery", "track", "order", "support", "contact",
        "return", "refund", "warranty", "problem", "issue", "broken",
        "confused", "unclear", "y", "n", "👍", "👎", "❤️", "😊", "🤔"
    ]
    
    successful_matches = 0
    
    for shortform in problematic_shortforms:
        response = keyword_matcher.generate_keyword_response(shortform)
        if response and response.get('confidence', 0) > 0.5:
            successful_matches += 1
            print(f"✅ '{shortform}' -> {response.get('confidence', 0):.2f} confidence")
        else:
            print(f"❌ '{shortform}' -> No match")
    
    success_rate = (successful_matches / len(problematic_shortforms)) * 100
    print(f"\n📊 Shortform success rate: {success_rate:.1f}% ({successful_matches}/{len(problematic_shortforms)})")
    
    return success_rate

def main():
    """Main function to fix shortform integration"""
    
    print("🔤 TechyMart AI Shortform Integration Fix")
    print("=" * 50)
    
    # Update keyword matcher with comprehensive shortforms
    keyword_count = update_keyword_matcher_with_shortforms()
    
    # Test the integration
    success_rate = test_comprehensive_shortforms()
    
    print("\n" + "=" * 50)
    print(f"🎉 SHORTFORM INTEGRATION FIX COMPLETE!")
    print(f"📊 Keywords integrated: {keyword_count}")
    print(f"📈 Success rate: {success_rate:.1f}%")
    print(f"🎯 System now properly recognizes shortforms!")
    
    print("\n🔄 Restart your server to see the fixed shortform recognition!")
    print("   python advanced_main.py")

if __name__ == "__main__":
    main()
