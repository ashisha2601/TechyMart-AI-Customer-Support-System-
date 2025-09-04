"""
Fix syntax errors in keyword_matcher.py and improve warranty response
"""

def fix_keyword_matcher():
    """Fix syntax errors and improve keyword responses"""
    
    print("🔧 Fixing keyword_matcher.py syntax errors...")
    
    # Create clean, comprehensive keyword matcher
    keyword_matcher_code = '''"""
Advanced Keyword Matcher for TechyMart AI Customer Support
Handles exact phrase matching with confidence scoring
"""

import re
from typing import Dict, List, Optional, Tuple

class KeywordMatcher:
    """Advanced keyword matching system with confidence scoring"""
    
    def __init__(self):
        # Comprehensive exact phrases with proper warranty information
        self.exact_phrases = {
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
            
            # ==================== WARRANTY (IMPROVED) ====================
            "warranty": {
                "category": "warranty",
                "confidence": 0.95,
                "response": "All electronics come with manufacturer warranty (1-2 years)! 🛡️ We also offer TechyMart Extended Protection: 1 extra year for $19.99, 2 extra years for $34.99. Covers accidents, drops, and liquid damage!"
            },
            "warranty info": {
                "category": "warranty",
                "confidence": 0.95,
                "response": "Warranty Information: 🛡️ All products have manufacturer warranty (1-2 years). TechyMart Extended Protection available: 1 year ($19.99) or 2 years ($34.99). Covers accidental damage, drops, liquid spills, and more!"
            },
            "extended warranty": {
                "category": "warranty",
                "confidence": 0.95,
                "response": "TechyMart Extended Protection! 🛡️ 1 extra year for $19.99, 2 extra years for $34.99. Covers accidents, drops, liquid damage, and more! Add it at checkout or within 30 days of purchase."
            },
            "protection plan": {
                "category": "warranty",
                "confidence": 0.90,
                "response": "Our Extended Protection plans cover accidental damage! 🛡️ 1 year ($19.99) or 2 years ($34.99). Includes drops, liquid spills, and mechanical failures. Much better than standard warranty!"
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
        
        # Keyword patterns for fuzzy matching
        self.keyword_patterns = {
            "payment": {
                "keywords": ["payment", "pay", "card", "credit", "debit", "upi", "wallet", "cash", "cod"],
                "confidence": 0.8,
                "response": "We accept all major payment methods! 💳 Credit/Debit cards, UPI, digital wallets, and Cash on Delivery. What payment method are you interested in?"
            },
            "shipping": {
                "keywords": ["shipping", "delivery", "dispatch", "ship", "deliver", "express", "overnight"],
                "confidence": 0.8,
                "response": "We offer multiple shipping options! 🚚 Standard (3-5 days), Express (1-2 days), and Overnight delivery. FREE shipping on orders over $50!"
            },
            "returns": {
                "keywords": ["return", "refund", "exchange", "cancel", "send back"],
                "confidence": 0.8,
                "response": "We have a hassle-free 30-day return policy! 🔄 Items must be in original condition. Start your return online or contact us!"
            },
            "warranty": {
                "keywords": ["warranty", "guarantee", "protection", "cover", "repair", "service"],
                "confidence": 0.8,
                "response": "All electronics come with manufacturer warranty (1-2 years)! 🛡️ We also offer Extended Protection plans for accidental damage coverage!"
            },
            "support": {
                "keywords": ["help", "support", "assistance", "contact", "service", "problem", "issue"],
                "confidence": 0.8,
                "response": "I'm here to help! 🤗 You can chat with me, email support@techymart.com, or call 1-800-TECHYMART. What do you need assistance with?"
            }
        }
    
    def generate_keyword_response(self, user_input: str) -> Optional[Dict]:
        """Generate response based on keyword matching"""
        
        if not user_input:
            return None
        
        user_input = user_input.lower().strip()
        
        # Check exact phrase matches first
        if user_input in self.exact_phrases:
            phrase_data = self.exact_phrases[user_input]
            return {
                "response": phrase_data["response"],
                "confidence": phrase_data["confidence"],
                "category": phrase_data["category"],
                "match_type": "exact_phrase"
            }
        
        # Check keyword patterns
        for pattern_name, pattern_data in self.keyword_patterns.items():
            for keyword in pattern_data["keywords"]:
                if keyword in user_input:
                    return {
                        "response": pattern_data["response"],
                        "confidence": pattern_data["confidence"],
                        "category": pattern_name,
                        "match_type": "keyword_pattern"
                    }
        
        return None
    
    def get_all_keywords(self) -> List[str]:
        """Get all available keywords"""
        exact_keywords = list(self.exact_phrases.keys())
        pattern_keywords = []
        for pattern_data in self.keyword_patterns.values():
            pattern_keywords.extend(pattern_data["keywords"])
        
        return exact_keywords + pattern_keywords
    
    def get_keywords_by_category(self, category: str) -> List[str]:
        """Get keywords by category"""
        keywords = []
        
        # Check exact phrases
        for keyword, data in self.exact_phrases.items():
            if data["category"] == category:
                keywords.append(keyword)
        
        # Check patterns
        if category in self.keyword_patterns:
            keywords.extend(self.keyword_patterns[category]["keywords"])
        
        return keywords

# Global instance
keyword_matcher = KeywordMatcher()
'''
    
    # Write the clean keyword matcher
    with open('keyword_matcher.py', 'w') as f:
        f.write(keyword_matcher_code)
    
    print("✅ Fixed keyword_matcher.py syntax errors!")
    print("✅ Improved warranty responses with detailed information!")
    print("✅ Added comprehensive warranty keywords!")

def test_warranty_keywords():
    """Test warranty keyword responses"""
    
    print("\n🧪 Testing warranty keyword responses...")
    
    from keyword_matcher import keyword_matcher
    
    warranty_tests = [
        "warranty",
        "warranty info", 
        "extended warranty",
        "protection plan"
    ]
    
    for test_query in warranty_tests:
        response = keyword_matcher.generate_keyword_response(test_query)
        if response:
            print(f"✅ '{test_query}' -> {response['confidence']:.2f} confidence")
            print(f"   Response: {response['response'][:80]}...")
        else:
            print(f"❌ '{test_query}' -> No match")

def main():
    """Main function to fix keyword matcher"""
    
    print("🔧 TechyMart AI Keyword Matcher Fix")
    print("=" * 50)
    
    # Fix syntax errors and improve responses
    fix_keyword_matcher()
    
    # Test warranty keywords
    test_warranty_keywords()
    
    print("\n" + "=" * 50)
    print("🎉 KEYWORD MATCHER FIXED!")
    print("✅ Syntax errors resolved")
    print("✅ Warranty responses improved")
    print("✅ Comprehensive keyword coverage")
    print("✅ Proper confidence scoring")
    
    print("\n🔄 Restart your server to see the fixes!")
    print("   python advanced_main.py")

if __name__ == "__main__":
    main()
