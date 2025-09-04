"""
Script to properly integrate enhanced keywords with the keyword matcher
"""

from keyword_manager import keyword_manager
from keyword_matcher import keyword_matcher
import json

def integrate_enhanced_keywords():
    """Integrate the enhanced keywords from keyword_manager into keyword_matcher"""
    
    print("🔗 Integrating enhanced keywords with keyword matcher...")
    
    # Get all keywords from keyword manager
    all_keywords = keyword_manager.keyword_matcher.exact_phrases.copy()
    
    print(f"📊 Found {len(all_keywords)} keywords to integrate...")
    
    # Add keywords to the main keyword matcher
    integrated_count = 0
    
    for keyword, data in all_keywords.items():
        if keyword not in keyword_matcher.exact_phrases:
            keyword_matcher.exact_phrases[keyword] = data
            integrated_count += 1
            print(f"✅ Integrated: '{keyword}' -> {data.get('category', 'unknown')}")
    
    print(f"\n🎉 Successfully integrated {integrated_count} new keywords!")
    
    # Update keyword patterns with new categories
    new_patterns = {
        "upi_payment": {
            "keywords": ["upi", "upi payment", "google pay", "phonepe", "paytm"],
            "priority": 9,
            "response_type": "direct_answer"
        },
        "credit_card": {
            "keywords": ["credit card", "visa", "mastercard", "amex", "discover"],
            "priority": 9,
            "response_type": "direct_answer"
        },
        "paypal": {
            "keywords": ["paypal", "pay pal"],
            "priority": 8,
            "response_type": "direct_answer"
        },
        "apple_pay": {
            "keywords": ["apple pay", "applepay"],
            "priority": 8,
            "response_type": "direct_answer"
        },
        "free_shipping": {
            "keywords": ["free shipping", "free delivery", "no shipping cost"],
            "priority": 9,
            "response_type": "direct_answer"
        },
        "express_delivery": {
            "keywords": ["express delivery", "express shipping", "fast delivery", "quick delivery"],
            "priority": 8,
            "response_type": "direct_answer"
        },
        "overnight_shipping": {
            "keywords": ["overnight", "overnight shipping", "next day delivery", "same day delivery"],
            "priority": 8,
            "response_type": "direct_answer"
        },
        "return_policy_30": {
            "keywords": ["30 day return", "30-day return", "return policy", "return within 30"],
            "priority": 9,
            "response_type": "direct_answer"
        },
        "extended_warranty": {
            "keywords": ["extended warranty", "extra warranty", "additional protection", "accidental damage"],
            "priority": 9,
            "response_type": "direct_answer"
        },
        "customer_service": {
            "keywords": ["customer service", "support", "help", "assistance", "contact"],
            "priority": 9,
            "response_type": "direct_answer"
        },
        "order_status": {
            "keywords": ["order status", "track order", "where is my order", "order tracking"],
            "priority": 9,
            "response_type": "action_required"
        },
        "price_match": {
            "keywords": ["price match", "match price", "lower price", "competitor price"],
            "priority": 8,
            "response_type": "direct_answer"
        },
        "gst": {
            "keywords": ["gst", "tax", "taxes included", "gst included"],
            "priority": 7,
            "response_type": "direct_answer"
        },
        "emi": {
            "keywords": ["emi", "emi options", "installments", "monthly payment"],
            "priority": 8,
            "response_type": "direct_answer"
        },
        "cod": {
            "keywords": ["cod", "cash on delivery", "pay on delivery"],
            "priority": 7,
            "response_type": "direct_answer"
        },
        "greeting_morning": {
            "keywords": ["good morning", "morning", "gm"],
            "priority": 8,
            "response_type": "greeting"
        },
        "greeting_afternoon": {
            "keywords": ["good afternoon", "afternoon", "ga"],
            "priority": 8,
            "response_type": "greeting"
        },
        "greeting_evening": {
            "keywords": ["good evening", "evening", "ge"],
            "priority": 8,
            "response_type": "greeting"
        },
        "greeting_casual": {
            "keywords": ["hey there", "what's up", "hi there", "hello there"],
            "priority": 7,
            "response_type": "greeting"
        },
        "problem_expressions": {
            "keywords": ["i have a problem", "this is not working", "broken", "defective", "not working"],
            "priority": 8,
            "response_type": "escalate"
        },
        "confusion": {
            "keywords": ["confused", "don't understand", "not sure", "unclear"],
            "priority": 7,
            "response_type": "support"
        },
        "gratitude": {
            "keywords": ["thank you", "thanks", "love it", "amazing", "great", "awesome"],
            "priority": 6,
            "response_type": "gratitude"
        },
        "emoji_positive": {
            "keywords": ["👍", "❤️", "😊", "🎉", "🔥", "💯"],
            "priority": 5,
            "response_type": "gratitude"
        },
        "emoji_thinking": {
            "keywords": ["🤔", "😢"],
            "priority": 6,
            "response_type": "support"
        }
    }
    
    # Add new patterns to keyword matcher
    for pattern_name, pattern_data in new_patterns.items():
        if pattern_name not in keyword_matcher.keyword_patterns:
            keyword_matcher.keyword_patterns[pattern_name] = pattern_data
            print(f"✅ Added pattern: {pattern_name}")
    
    print(f"\n🎯 Total patterns in system: {len(keyword_matcher.keyword_patterns)}")
    print(f"🎯 Total exact phrases: {len(keyword_matcher.exact_phrases)}")
    
    return integrated_count

def test_integrated_keywords():
    """Test the integrated keyword system"""
    
    print("\n🧪 Testing integrated keyword system...")
    
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
    print("🚀 TechyMart AI Keyword Integration Tool")
    print("=" * 50)
    
    # Integrate keywords
    integrated_count = integrate_enhanced_keywords()
    
    # Test the integration
    success_rate = test_integrated_keywords()
    
    print("\n" + "=" * 50)
    print(f"🎉 INTEGRATION COMPLETE!")
    print(f"📊 Keywords integrated: {integrated_count}")
    print(f"📈 Success rate: {success_rate:.1f}%")
    print(f"🎯 System is now much more responsive!")
    
    print("\n🔄 Restart your server to see the enhanced system in action!")
    print("   python advanced_main.py")
