"""
Add comprehensive shortform recognition to the TechyMart AI system
"""

from keyword_manager import keyword_manager
import json

def add_shortform_keywords():
    """Add comprehensive shortform keywords and context-aware responses"""
    
    print("🔤 Adding shortform recognition to TechyMart AI...")
    
    # Comprehensive shortform keywords
    shortform_keywords = [
        # Simple responses
        {
            "keyword": "ok",
            "category": "acknowledgment",
            "response": "Great! Is there anything else I can help you with today? 😊",
            "priority": 8
        },
        {
            "keyword": "okay",
            "category": "acknowledgment", 
            "response": "Perfect! Anything else you'd like to know? 🤗",
            "priority": 8
        },
        {
            "keyword": "yes",
            "category": "confirmation",
            "response": "Awesome! What would you like to know more about? 🚀",
            "priority": 8
        },
        {
            "keyword": "no",
            "category": "negation",
            "response": "No problem! Is there anything else I can help you with? 💪",
            "priority": 8
        },
        {
            "keyword": "nope",
            "category": "negation",
            "response": "That's totally fine! What else can I help you with? 😊",
            "priority": 7
        },
        {
            "keyword": "sure",
            "category": "confirmation",
            "response": "Great! What would you like to know? 🤔",
            "priority": 8
        },
        {
            "keyword": "maybe",
            "category": "uncertainty",
            "response": "No worries! Take your time. I'm here whenever you need help! 😊",
            "priority": 7
        },
        {
            "keyword": "thanks",
            "category": "gratitude",
            "response": "You're very welcome! 😊 Happy to help anytime!",
            "priority": 8
        },
        {
            "keyword": "thank you",
            "category": "gratitude",
            "response": "You're so welcome! 🌟 I'm here whenever you need me!",
            "priority": 9
        },
        {
            "keyword": "ty",
            "category": "gratitude",
            "response": "You're welcome! 😊 Anytime!",
            "priority": 7
        },
        
        # Payment shortforms
        {
            "keyword": "gpay",
            "category": "payment",
            "response": "Yes! Google Pay is fully supported! 🤖 You can use it for both UPI and card payments. Super convenient!",
            "priority": 9
        },
        {
            "keyword": "g pay",
            "category": "payment",
            "response": "Absolutely! Google Pay works great with our system! 🤖 Quick and secure payments!",
            "priority": 9
        },
        {
            "keyword": "google pay",
            "category": "payment",
            "response": "Google Pay is supported! You can use it for both UPI and card payments. Super convenient for Android users! 🤖",
            "priority": 9
        },
        {
            "keyword": "paypal",
            "category": "payment",
            "response": "Yes! PayPal is available for quick and secure checkout! 💰 Just select PayPal as your payment method!",
            "priority": 9
        },
        {
            "keyword": "apple pay",
            "category": "payment",
            "response": "Apple Pay is available! 🍎 Quick and secure payments on iPhone and Mac. Look for the Apple Pay button at checkout!",
            "priority": 9
        },
        {
            "keyword": "upi",
            "category": "payment",
            "response": "Yes! UPI is fully supported! 🇮🇳 Use Google Pay, PhonePe, Paytm, or any UPI app for instant payments!",
            "priority": 9
        },
        {
            "keyword": "cod",
            "category": "payment",
            "response": "Cash on Delivery is available! 💵 Check availability at checkout. COD orders may have a small additional fee.",
            "priority": 8
        },
        {
            "keyword": "emi",
            "category": "payment",
            "response": "EMI options are available! 💳 Check available EMI plans at checkout through various banks and NBFCs!",
            "priority": 8
        },
        
        # Shipping shortforms
        {
            "keyword": "shipping",
            "category": "shipping",
            "response": "We offer FREE shipping on orders over $50! 🚚 Standard (3-5 days), Express (1-2 days for $9.99), or Overnight ($19.99)!",
            "priority": 9
        },
        {
            "keyword": "delivery",
            "category": "shipping",
            "response": "Standard delivery: 3-5 business days (FREE over $50), Express: 1-2 days ($9.99), Overnight: Next day ($19.99)! 📦",
            "priority": 9
        },
        {
            "keyword": "track",
            "category": "orders",
            "response": "I can help you track your order! 📦 Just provide your order number and I'll look it up for you!",
            "priority": 9
        },
        {
            "keyword": "order",
            "category": "orders",
            "response": "I can help with your order! 📦 Need to track, modify, or have questions about it?",
            "priority": 8
        },
        
        # Support shortforms
        {
            "keyword": "help",
            "category": "support",
            "response": "I'm here to help! 🤗 What do you need assistance with? Payment, shipping, returns, or something else?",
            "priority": 9
        },
        {
            "keyword": "support",
            "category": "support",
            "response": "We're here to help 24/7! 🤗 Chat with me, email support@techymart.com, or call 1-800-TECHYMART!",
            "priority": 9
        },
        {
            "keyword": "contact",
            "category": "support",
            "response": "You can contact us via chat (me!), email support@techymart.com, or call 1-800-TECHYMART! 📞",
            "priority": 8
        },
        
        # Return/Warranty shortforms
        {
            "keyword": "return",
            "category": "returns",
            "response": "We have a hassle-free 30-day return policy! 🔄 Items must be in original condition. Start your return online!",
            "priority": 9
        },
        {
            "keyword": "refund",
            "category": "returns",
            "response": "Refunds process within 3-5 business days after we receive your return! 💰 We'll email you confirmation!",
            "priority": 8
        },
        {
            "keyword": "warranty",
            "category": "warranty",
            "response": "All electronics come with manufacturer warranty (1-2 years)! 🛡️ We also offer Extended Protection plans!",
            "priority": 9
        },
        
        # Greeting shortforms
        {
            "keyword": "hi",
            "category": "greeting",
            "response": "Hi there! 👋 Welcome to TechyMart! How can I help you today?",
            "priority": 8
        },
        {
            "keyword": "hello",
            "category": "greeting",
            "response": "Hello! 👋 Great to see you at TechyMart! What can I assist you with?",
            "priority": 8
        },
        {
            "keyword": "hey",
            "category": "greeting",
            "response": "Hey! 👋 Welcome to TechyMart! What's on your mind today?",
            "priority": 7
        },
        
        # Problem shortforms
        {
            "keyword": "problem",
            "category": "support",
            "response": "I'm sorry you're having a problem! 😔 Please tell me more about it and I'll help you resolve it!",
            "priority": 8
        },
        {
            "keyword": "issue",
            "category": "support",
            "response": "I'm here to help with any issues! 🔧 What's going wrong? Let me help you fix it!",
            "priority": 8
        },
        {
            "keyword": "broken",
            "category": "technical",
            "response": "I'm sorry your item is broken! 🔧 Contact us immediately and we'll arrange a free replacement or refund!",
            "priority": 9
        },
        
        # Confusion shortforms
        {
            "keyword": "confused",
            "category": "support",
            "response": "I'm here to help clear up any confusion! 🤔 What would you like me to explain better?",
            "priority": 8
        },
        {
            "keyword": "unclear",
            "category": "support",
            "response": "Let me help clarify that! 💡 What specific part would you like me to explain?",
            "priority": 7
        },
        
        # Single letter responses (context-aware)
        {
            "keyword": "y",
            "category": "confirmation",
            "response": "Yes! What would you like to know more about? 🚀",
            "priority": 6
        },
        {
            "keyword": "n",
            "category": "negation",
            "response": "No problem! Is there anything else I can help you with? 💪",
            "priority": 6
        },
        
        # Emoji shortforms
        {
            "keyword": "👍",
            "category": "gratitude",
            "response": "Thanks for the thumbs up! Glad I could help! 👍",
            "priority": 7
        },
        {
            "keyword": "👎",
            "category": "feedback",
            "response": "I'm sorry I couldn't help better! 😔 Let me try a different approach. What specifically can I improve?",
            "priority": 8
        },
        {
            "keyword": "❤️",
            "category": "gratitude",
            "response": "Aww, sending love right back! ❤️ Thanks for being awesome!",
            "priority": 7
        },
        {
            "keyword": "😊",
            "category": "greeting",
            "response": "😊 Hello there! Great to see you! How can I help you today?",
            "priority": 6
        },
        {
            "keyword": "🤔",
            "category": "support",
            "response": "I see you're thinking! 🤔 What's on your mind? I'm here to help!",
            "priority": 6
        }
    ]
    
    print(f"📦 Adding {len(shortform_keywords)} shortform keywords...")
    
    # Add all shortform keywords
    keyword_manager.bulk_add_keywords(shortform_keywords)
    
    print("✅ Shortform keywords added successfully!")
    return len(shortform_keywords)

def add_context_aware_responses():
    """Add context-aware responses for better understanding"""
    
    print("🧠 Adding context-aware response patterns...")
    
    # Context patterns for better understanding
    context_patterns = [
        {
            "keyword": "ok after payment info",
            "category": "context_acknowledgment",
            "response": "Perfect! You're all set with payment info! 💳 Is there anything else about your order I can help with?",
            "priority": 9
        },
        {
            "keyword": "ok after shipping info", 
            "category": "context_acknowledgment",
            "response": "Great! You're all set with shipping details! 📦 Need help with anything else?",
            "priority": 9
        },
        {
            "keyword": "no after help offer",
            "category": "context_negation",
            "response": "No worries at all! 😊 I'm here whenever you need help. Have a great day!",
            "priority": 8
        },
        {
            "keyword": "yes after help offer",
            "category": "context_confirmation", 
            "response": "Awesome! What else can I help you with? 🚀",
            "priority": 8
        }
    ]
    
    keyword_manager.bulk_add_keywords(context_patterns)
    print(f"✅ Added {len(context_patterns)} context-aware patterns!")
    return len(context_patterns)

def main():
    """Main function to add shortform recognition"""
    
    print("🔤 TechyMart AI Shortform Enhancement Tool")
    print("=" * 50)
    
    # Add shortform keywords
    shortform_count = add_shortform_keywords()
    
    # Add context-aware responses
    context_count = add_context_aware_responses()
    
    total_added = shortform_count + context_count
    
    print("\n" + "=" * 50)
    print(f"🎉 SHORTFORM ENHANCEMENT COMPLETE!")
    print(f"📊 Shortform keywords added: {shortform_count}")
    print(f"📊 Context patterns added: {context_count}")
    print(f"📊 Total enhancements: {total_added}")
    print(f"🎯 System now understands shortforms like 'ok', 'gpay', 'no', 'yes'!")
    
    # Show statistics
    stats = keyword_manager.get_usage_statistics()
    print(f"\n📈 Updated system stats:")
    print(f"   • Total keywords: {stats['total_keywords']}")
    print(f"   • Categories: {len(stats['categories'])}")
    
    # Export updated keywords
    backup_file = keyword_manager.export_keywords_to_json()
    print(f"💾 Keywords backed up to: {backup_file}")
    
    print("\n🔄 Restart your server to see the enhanced shortform recognition!")
    print("   python advanced_main.py")

if __name__ == "__main__":
    main()
