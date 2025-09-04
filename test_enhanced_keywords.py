"""
Test script to demonstrate the enhanced keyword system
"""

from keyword_manager import keyword_manager
import time

def test_enhanced_keywords():
    """Test the enhanced keyword system with various queries"""
    
    print("🚀 Testing Enhanced TechyMart AI Keyword System")
    print("=" * 60)
    
    # Test queries covering different categories
    test_queries = [
        # Payment queries
        "Do you accept UPI payment?",
        "Can I pay with credit card?",
        "Is PayPal available?",
        "Do you have Apple Pay?",
        "What about Google Pay?",
        "Do you offer EMI options?",
        
        # Shipping queries
        "Do you have free shipping?",
        "What's your express delivery?",
        "Do you offer overnight shipping?",
        "Can I get same day delivery?",
        "What's the delivery time?",
        
        # Returns queries
        "What's your 30 day return policy?",
        "Do you provide return labels?",
        "How long for refunds?",
        "Can I return opened items?",
        "What if the product is defective?",
        
        # Warranty queries
        "Do you have extended warranty?",
        "What about accidental damage coverage?",
        "How do I make a warranty claim?",
        
        # Account queries
        "How do I create an account?",
        "I forgot my password",
        "Can I checkout as guest?",
        
        # Support queries
        "I need customer service",
        "Can I get phone support?",
        "I have a technical problem",
        "This is not working",
        "I'm confused about something",
        
        # Greeting variations
        "Good morning!",
        "Hey there!",
        "What's up?",
        "😊",
        "👍",
        
        # Indian-specific queries
        "Do you include GST?",
        "What are the COD charges?",
        "Do you deliver to my PIN code?",
        
        # Pricing queries
        "Do you price match?",
        "Any discount codes?",
        "Student discount available?",
        
        # Order queries
        "What's my order status?",
        "Can I modify my order?",
        "How do I cancel an order?",
        
        # Product queries
        "Do you have product reviews?",
        "Is it available in stock?",
        "What are the specifications?"
    ]
    
    print(f"🧪 Testing {len(test_queries)} different queries...")
    print()
    
    successful_matches = 0
    total_queries = len(test_queries)
    
    for i, query in enumerate(test_queries, 1):
        print(f"{i:2d}. Query: '{query}'")
        
        # Test keyword matching
        response = keyword_manager.keyword_matcher.generate_keyword_response(query)
        
        if response and response.get('confidence', 0) > 0.5:
            successful_matches += 1
            confidence = response.get('confidence', 0)
            method = response.get('method', 'unknown')
            print(f"    ✅ MATCHED ({confidence:.2f} confidence, {method})")
            print(f"    📝 Response: {response.get('response', 'N/A')[:80]}...")
        else:
            print(f"    ❌ No keyword match found")
        
        print()
        time.sleep(0.1)  # Small delay for readability
    
    # Calculate success rate
    success_rate = (successful_matches / total_queries) * 100
    
    print("=" * 60)
    print(f"📊 KEYWORD SYSTEM TEST RESULTS:")
    print(f"   • Total queries tested: {total_queries}")
    print(f"   • Successful matches: {successful_matches}")
    print(f"   • Success rate: {success_rate:.1f}%")
    print(f"   • System responsiveness: {'EXCELLENT' if success_rate > 80 else 'GOOD' if success_rate > 60 else 'NEEDS IMPROVEMENT'}")
    
    # Show keyword statistics
    stats = keyword_manager.get_usage_statistics()
    print(f"\n📈 KEYWORD SYSTEM STATISTICS:")
    print(f"   • Total keywords: {stats['total_keywords']}")
    print(f"   • Categories: {len(stats['categories'])}")
    print(f"   • Top categories: {list(stats['categories'].keys())[:5]}")
    
    return success_rate

def show_keyword_categories():
    """Show all available keyword categories"""
    
    print("\n🗂️ AVAILABLE KEYWORD CATEGORIES:")
    print("=" * 40)
    
    categories = keyword_manager.list_keywords_by_category()
    
    for category, keywords in categories.items():
        print(f"📁 {category.upper()} ({len(keywords)} keywords)")
        # Show first few keywords as examples
        examples = [kw['keyword'] for kw in keywords[:3]]
        print(f"   Examples: {', '.join(examples)}")
        if len(keywords) > 3:
            print(f"   ... and {len(keywords) - 3} more")
        print()

if __name__ == "__main__":
    # Run the test
    success_rate = test_enhanced_keywords()
    
    # Show categories
    show_keyword_categories()
    
    print("🎉 Your TechyMart AI system is now much more keyword-rich!")
    print("🌐 Visit http://localhost:8000 to test it live!")
