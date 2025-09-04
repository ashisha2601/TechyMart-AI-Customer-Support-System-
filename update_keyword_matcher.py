"""
Update the keyword matcher with comprehensive keywords and improved matching logic
"""

import re
from typing import Dict, List, Optional, Tuple

def create_enhanced_keyword_matcher():
    """Create an enhanced keyword matcher with comprehensive keywords"""
    
    # Comprehensive exact phrases with high confidence
    exact_phrases = {
        # Payment methods
        "upi payment": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Yes! 🇮🇳 We support UPI payments through Google Pay, PhonePe, Paytm, and all UPI apps. UPI transactions are instant and secure! Just select UPI at checkout."
        },
        "upi": {
            "category": "payment", 
            "confidence": 0.90,
            "response": "Yes! 🇮🇳 We support UPI payments through Google Pay, PhonePe, Paytm, and all UPI apps. UPI transactions are instant and secure!"
        },
        "credit card": {
            "category": "payment",
            "confidence": 0.95,
            "response": "We accept all major credit cards: Visa, Mastercard, American Express, and Discover. Your payment is secured with 256-bit SSL encryption! 💳"
        },
        "paypal": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Absolutely! You can pay with PayPal for a quick and secure checkout. Just select PayPal as your payment method! 💰"
        },
        "apple pay": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Yes! Apple Pay is available for quick and secure payments on iPhone and Mac. Just look for the Apple Pay button at checkout! 🍎"
        },
        "google pay": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Google Pay is supported! You can use it for both UPI and card payments. Super convenient for Android users! 🤖"
        },
        "emi": {
            "category": "payment",
            "confidence": 0.90,
            "response": "Yes! We offer EMI options through various banks and NBFCs. Check available EMI options at checkout! 💳"
        },
        "emi options": {
            "category": "payment",
            "confidence": 0.95,
            "response": "Yes! We offer EMI options through various banks and NBFCs. Check available EMI options at checkout! 💳"
        },
        "cash on delivery": {
            "category": "payment",
            "confidence": 0.95,
            "response": "We offer Cash on Delivery (COD) in select areas! Check availability at checkout. COD orders may have a small additional fee. 💵"
        },
        "cod": {
            "category": "payment",
            "confidence": 0.90,
            "response": "We offer Cash on Delivery (COD) in select areas! Check availability at checkout. COD orders may have a small additional fee. 💵"
        },
        
        # Shipping
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
        "same day delivery": {
            "category": "shipping",
            "confidence": 0.95,
            "response": "Same-day delivery is available in select metro areas for $29.99! Order by 12 PM for same-day delivery! 🚀"
        },
        "delivery time": {
            "category": "shipping",
            "confidence": 0.90,
            "response": "Standard: 3-5 business days (FREE over $50), Express: 1-2 days ($9.99), Overnight: Next day ($19.99). We ship Mon-Fri! 📅"
        },
        "tracking number": {
            "category": "shipping",
            "confidence": 0.90,
            "response": "You'll get a tracking number via email once your order ships! Use it to track your package in real-time! 📦📱"
        },
        
        # Returns
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
        "return label": {
            "category": "returns",
            "confidence": 0.90,
            "response": "We'll email you a prepaid return label! Just print it, attach to your package, and drop it off. Super easy! 📦✉️"
        },
        "refund time": {
            "category": "returns",
            "confidence": 0.90,
            "response": "Refunds typically process within 3-5 business days after we receive your return. You'll get an email confirmation! 💰"
        },
        "defective product": {
            "category": "returns",
            "confidence": 0.95,
            "response": "If your product is defective, contact us immediately! We'll arrange a free replacement or full refund - your choice! 🔧"
        },
        
        # Warranty
        "extended warranty": {
            "category": "warranty",
            "confidence": 0.95,
            "response": "We offer TechyMart Extended Protection! 1 extra year for $19.99, 2 extra years for $34.99. Covers accidents, drops, and liquid damage! 🛡️"
        },
        "warranty": {
            "category": "warranty",
            "confidence": 0.90,
            "response": "All electronics come with manufacturer warranty (typically 1-2 years). We also offer Extended Protection plans! 🛡️"
        },
        "accidental damage": {
            "category": "warranty",
            "confidence": 0.90,
            "response": "Our Extended Protection covers accidental damage like drops and liquid spills that manufacturer warranties don't cover! 💧📱"
        },
        
        # Support
        "customer service": {
            "category": "support",
            "confidence": 0.95,
            "response": "We're here to help 24/7! Chat with me, email support@techymart.com, or call 1-800-TECHYMART! 🤗"
        },
        "technical support": {
            "category": "support",
            "confidence": 0.95,
            "response": "For technical issues, our specialized tech support team is available Mon-Fri 9AM-6PM EST! They're experts in troubleshooting! 🔧"
        },
        "phone support": {
            "category": "support",
            "confidence": 0.90,
            "response": "Call us at 1-800-TECHYMART! Our human experts are available Mon-Fri 9AM-6PM EST for complex issues! 📞"
        },
        "live chat": {
            "category": "support",
            "confidence": 0.90,
            "response": "You're already using it! I'm your AI assistant. For human support, we have live chat available Mon-Fri 9AM-6PM EST! 💬"
        },
        
        # Orders
        "order status": {
            "category": "orders",
            "confidence": 0.95,
            "response": "Check your order status by providing your order number! I can look it up for you right now! 📦"
        },
        "modify order": {
            "category": "orders",
            "confidence": 0.90,
            "response": "You can modify orders within 1 hour of placing them! After that, you'll need to process a return. Contact us ASAP! ⚡"
        },
        "cancel order": {
            "category": "orders",
            "confidence": 0.90,
            "response": "Cancel orders within 1 hour of placing them! After that, you'll need to process a return once received. We'll help! ❌"
        },
        
        # Pricing
        "price match": {
            "category": "pricing",
            "confidence": 0.95,
            "response": "We'll match any lower price from major retailers! Contact us with the competitor's link and we'll adjust your price! 💰"
        },
        "discount code": {
            "category": "pricing",
            "confidence": 0.90,
            "response": "Check our promotions page for current discount codes! Sign up for our newsletter to get exclusive deals! 🎟️"
        },
        "student discount": {
            "category": "pricing",
            "confidence": 0.90,
            "response": "Yes! Students get 10% off with valid student ID! Contact us with your student email for verification! 🎓"
        },
        
        # Indian-specific
        "gst": {
            "category": "pricing",
            "confidence": 0.90,
            "response": "All prices include GST! You'll see the GST breakdown in your order summary. We're fully GST compliant! 🇮🇳"
        },
        "pin code delivery": {
            "category": "shipping",
            "confidence": 0.90,
            "response": "Enter your PIN code at checkout to check delivery availability and estimated delivery time to your area! 📍"
        },
        
        # Greetings
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
        
        # Problem expressions
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
        "broken": {
            "category": "technical",
            "confidence": 0.90,
            "response": "I'm sorry your item is broken! Contact us immediately and we'll arrange a free replacement or refund! 🔧"
        },
        "defective": {
            "category": "technical",
            "confidence": 0.90,
            "response": "I'm sorry your item is defective! Contact us immediately and we'll arrange a free replacement or refund! 🔧"
        },
        
        # Confusion
        "confused": {
            "category": "support",
            "confidence": 0.90,
            "response": "I'm here to help clear up any confusion! What would you like me to explain better?"
        },
        "don't understand": {
            "category": "support",
            "confidence": 0.90,
            "response": "No worries! Let me explain that in a different way. What specific part would you like me to clarify?"
        },
        "not sure": {
            "category": "support",
            "confidence": 0.85,
            "response": "That's totally fine! Let me help you figure this out. What are you not sure about?"
        },
        
        # Gratitude
        "thank you": {
            "category": "gratitude",
            "confidence": 0.95,
            "response": "You're very welcome! 😊 I'm here whenever you need help with TechyMart!"
        },
        "thanks": {
            "category": "gratitude",
            "confidence": 0.90,
            "response": "You're welcome! 😊 Happy to help!"
        },
        "love it": {
            "category": "gratitude",
            "confidence": 0.90,
            "response": "That's awesome! I'm so glad you love your purchase! Thanks for choosing TechyMart! ❤️"
        },
        "amazing": {
            "category": "gratitude",
            "confidence": 0.85,
            "response": "Thank you so much! That really means a lot to our team! We're here whenever you need us! 🌟"
        },
        
        # Emojis
        "👍": {
            "category": "gratitude",
            "confidence": 0.90,
            "response": "Thanks for the thumbs up! Glad I could help! 👍"
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
        "😢": {
            "category": "support",
            "confidence": 0.90,
            "response": "I'm sorry you're feeling down! 😢 Let me help make things better. What's wrong?"
        },
        "🎉": {
            "category": "gratitude",
            "confidence": 0.85,
            "response": "🎉 Celebrating with you! Thanks for choosing TechyMart!"
        },
        "🔥": {
            "category": "gratitude",
            "confidence": 0.85,
            "response": "🔥 That's fire! Thanks for the awesome feedback!"
        },
        "💯": {
            "category": "gratitude",
            "confidence": 0.85,
            "response": "💯 You're 100% awesome! Thanks for being a great customer!"
        }
    }
    
    return exact_phrases

def update_keyword_matcher_file():
    """Update the keyword_matcher.py file with enhanced keywords"""
    
    print("🔄 Updating keyword_matcher.py with enhanced keywords...")
    
    # Read the current file
    with open('keyword_matcher.py', 'r') as f:
        content = f.read()
    
    # Create enhanced exact phrases
    enhanced_phrases = create_enhanced_keyword_matcher()
    
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
    import re
    pattern = r'self\.exact_phrases = \{.*?\n        \}'
    new_content = re.sub(pattern, phrases_code.strip(), content, flags=re.DOTALL)
    
    # Write the updated file
    with open('keyword_matcher.py', 'w') as f:
        f.write(new_content)
    
    print(f"✅ Updated keyword_matcher.py with {len(enhanced_phrases)} enhanced keywords!")
    return len(enhanced_phrases)

def test_updated_keywords():
    """Test the updated keyword system"""
    
    print("\n🧪 Testing updated keyword system...")
    
    # Import the updated keyword matcher
    from keyword_matcher import keyword_matcher
    
    test_queries = [
        "Do you accept UPI payment?",
        "Can I pay with credit card?",
        "Is PayPal available?",
        "Do you have free shipping?",
        "What's your express delivery?",
        "Do you offer overnight shipping?",
        "What's your 30 day return policy?",
        "Do you have extended warranty?",
        "I need customer service",
        "What's my order status?",
        "Do you price match?",
        "Do you include GST?",
        "Do you offer EMI options?",
        "Good morning!",
        "Hey there!",
        "I have a problem",
        "I'm confused",
        "Thank you!",
        "👍",
        "🤔"
    ]
    
    successful_matches = 0
    
    for query in test_queries:
        response = keyword_matcher.generate_keyword_response(query)
        if response and response.get('confidence', 0) > 0.5:
            successful_matches += 1
            print(f"✅ '{query}' -> {response.get('confidence', 0):.2f} confidence")
        else:
            print(f"❌ '{query}' -> No match")
    
    success_rate = (successful_matches / len(test_queries)) * 100
    print(f"\n📊 Success rate: {success_rate:.1f}% ({successful_matches}/{len(test_queries)})")
    
    return success_rate

if __name__ == "__main__":
    print("🚀 TechyMart AI Keyword Matcher Enhancement")
    print("=" * 50)
    
    # Update the keyword matcher file
    keyword_count = update_keyword_matcher_file()
    
    # Test the updated system
    success_rate = test_updated_keywords()
    
    print("\n" + "=" * 50)
    print(f"🎉 ENHANCEMENT COMPLETE!")
    print(f"📊 Keywords added: {keyword_count}")
    print(f"📈 Success rate: {success_rate:.1f}%")
    print(f"🎯 System is now much more responsive!")
    
    print("\n🔄 Restart your server to see the enhanced system in action!")
    print("   python advanced_main.py")
