"""
Examples of how to use the keyword-based response system
Run this to see how keyword matching works and add custom responses
"""

from keyword_matcher import keyword_matcher

def demonstrate_keyword_matching():
    """Demonstrate how keyword matching works"""
    
    print("🔍 Keyword Matching System Demo")
    print("=" * 40)
    
    # Test messages with different keyword patterns
    test_messages = [
        "UPI works?",
        "What payment methods do you accept?",
        "I want to return this item",
        "Where is my order #1234?", 
        "My product is broken",
        "Hello there!",
        "shipping information please",
        "warranty details"
    ]
    
    for message in test_messages:
        print(f"\n📝 User: {message}")
        
        # Get keyword match
        response = keyword_matcher.generate_keyword_response(message)
        
        if response:
            print(f"🤖 Bot: {response['response'][:100]}...")
            print(f"   Type: {response['type']}")
            print(f"   Confidence: {response.get('confidence', 'N/A')}")
            if response.get('matched_keywords'):
                print(f"   Matched Keywords: {response['matched_keywords']}")
        else:
            print("❌ No keyword match found")
        
        print("-" * 30)

def add_custom_keywords():
    """Examples of adding custom keyword responses"""
    
    print("\n➕ Adding Custom Keywords")
    print("=" * 30)
    
    # Add custom responses for specific queries
    custom_keywords = [
        {
            "keyword": "student discount",
            "category": "discounts",
            "response": "Yes! We offer a 10% student discount! 🎓 Just verify your student email through SheerID at checkout. Valid for all products except sale items.",
            "priority": 9
        },
        {
            "keyword": "bulk order", 
            "category": "sales",
            "response": "Great! For bulk orders (10+ items), we offer special pricing! 📦 Contact our B2B team at bulk@techymart.com or call 1-800-BULK-TM for a custom quote.",
            "priority": 9
        },
        {
            "keyword": "gift card",
            "category": "payment", 
            "response": "We have digital gift cards available! 🎁 Choose from $25, $50, $100, or custom amounts. They're delivered instantly via email and never expire!",
            "priority": 8
        }
    ]
    
    # Add the custom keywords
    for item in custom_keywords:
        keyword_matcher.add_custom_keyword(
            keyword=item["keyword"],
            category=item["category"], 
            response=item["response"],
            priority=item["priority"]
        )
        print(f"✅ Added: '{item['keyword']}' → {item['category']}")
    
    # Test the new keywords
    print("\n🧪 Testing Custom Keywords:")
    test_custom = [
        "Do you have student discount?",
        "I need to place a bulk order", 
        "Can I buy a gift card?"
    ]
    
    for message in test_custom:
        print(f"\n📝 User: {message}")
        response = keyword_matcher.generate_keyword_response(message)
        if response:
            print(f"🤖 Bot: {response['response']}")
        else:
            print("❌ No match")

def show_keyword_statistics():
    """Show keyword system statistics"""
    
    print("\n📊 Keyword System Statistics")
    print("=" * 35)
    
    stats = keyword_matcher.get_keyword_statistics()
    
    print(f"Total Patterns: {stats['total_patterns']}")
    print(f"Total Exact Phrases: {stats['total_exact_phrases']}")
    print(f"Total Keywords: {stats['total_keywords']}")
    print(f"Categories: {', '.join(stats['categories'])}")

def create_keyword_config():
    """Create a configuration file for easy keyword management"""
    
    keyword_config = {
        "exact_phrases": {
            "upi works": {
                "category": "payment",
                "response": "Yes! UPI payments work perfectly! 🇮🇳 Use Google Pay, PhonePe, Paytm, or any UPI app. Instant and secure!"
            },
            "cod available": {
                "category": "payment", 
                "response": "Cash on Delivery is available! 💵 COD fee is ₹50 for orders under ₹500. Free COD on orders above ₹500!"
            },
            "emi options": {
                "category": "payment",
                "response": "Yes! We offer EMI options! 💳 0% EMI on orders above ₹5000 with major credit cards. 3-24 months available!"
            }
        },
        "keyword_patterns": {
            "india_specific": {
                "keywords": ["india", "indian", "rupees", "inr", "delhi", "mumbai", "bangalore"],
                "response": "We serve customers across India! 🇮🇳 Free shipping above ₹500, COD available, and local customer support in Hindi/English!"
            },
            "mobile_apps": {
                "keywords": ["mobile app", "android app", "ios app", "download app"],
                "response": "Download our mobile app! 📱 Available on Google Play Store and Apple App Store. Get exclusive app-only deals!"
            }
        }
    }
    
    import json
    with open('/Users/ashishasharma/Desktop/AGI/keyword_config.json', 'w') as f:
        json.dump(keyword_config, f, indent=2)
    
    print("💾 Created keyword_config.json for easy management!")

if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_keyword_matching()
    add_custom_keywords() 
    show_keyword_statistics()
    create_keyword_config()
    
    print("\n🎉 Keyword system demo complete!")
    print("\nTo use in your chatbot:")
    print("1. Import: from keyword_matcher import keyword_matcher")
    print("2. Use: response = keyword_matcher.generate_keyword_response(user_message)")
    print("3. Add custom: keyword_matcher.add_custom_keyword(keyword, category, response)")
