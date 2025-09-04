"""
Test script to verify shortform recognition is working properly
"""

from keyword_manager import keyword_manager

def test_shortform_recognition():
    """Test the enhanced shortform recognition system"""
    
    print("🔤 Testing TechyMart AI Shortform Recognition")
    print("=" * 60)
    
    # Test shortform queries
    shortform_tests = [
        # Simple responses
        ("ok", "acknowledgment"),
        ("okay", "acknowledgment"),
        ("yes", "confirmation"),
        ("no", "negation"),
        ("nope", "negation"),
        ("sure", "confirmation"),
        ("maybe", "uncertainty"),
        ("thanks", "gratitude"),
        ("thank you", "gratitude"),
        ("ty", "gratitude"),
        
        # Payment shortforms
        ("gpay", "payment"),
        ("g pay", "payment"),
        ("google pay", "payment"),
        ("paypal", "payment"),
        ("apple pay", "payment"),
        ("upi", "payment"),
        ("cod", "payment"),
        ("emi", "payment"),
        
        # Shipping shortforms
        ("shipping", "shipping"),
        ("delivery", "shipping"),
        ("track", "orders"),
        ("order", "orders"),
        
        # Support shortforms
        ("help", "support"),
        ("support", "support"),
        ("contact", "support"),
        ("return", "returns"),
        ("refund", "returns"),
        ("warranty", "warranty"),
        
        # Greeting shortforms
        ("hi", "greeting"),
        ("hello", "greeting"),
        ("hey", "greeting"),
        
        # Problem shortforms
        ("problem", "support"),
        ("issue", "support"),
        ("broken", "technical"),
        ("confused", "support"),
        ("unclear", "support"),
        
        # Single letter responses
        ("y", "confirmation"),
        ("n", "negation"),
        
        # Emoji shortforms
        ("👍", "gratitude"),
        ("👎", "feedback"),
        ("❤️", "gratitude"),
        ("😊", "greeting"),
        ("🤔", "support")
    ]
    
    print(f"🧪 Testing {len(shortform_tests)} shortform queries...")
    print()
    
    successful_matches = 0
    total_tests = len(shortform_tests)
    
    for i, (query, expected_category) in enumerate(shortform_tests, 1):
        print(f"{i:2d}. Query: '{query}' (Expected: {expected_category})")
        
        # Test keyword matching
        response = keyword_manager.keyword_matcher.generate_keyword_response(query)
        
        if response and response.get('confidence', 0) > 0.5:
            successful_matches += 1
            confidence = response.get('confidence', 0)
            method = response.get('method', 'unknown')
            actual_response = response.get('response', 'N/A')[:60] + '...' if len(response.get('response', '')) > 60 else response.get('response', 'N/A')
            
            print(f"    ✅ MATCHED ({confidence:.2f} confidence, {method})")
            print(f"    📝 Response: {actual_response}")
        else:
            print(f"    ❌ No keyword match found")
        
        print()
    
    # Calculate success rate
    success_rate = (successful_matches / total_tests) * 100
    
    print("=" * 60)
    print(f"📊 SHORTFORM RECOGNITION TEST RESULTS:")
    print(f"   • Total queries tested: {total_tests}")
    print(f"   • Successful matches: {successful_matches}")
    print(f"   • Success rate: {success_rate:.1f}%")
    print(f"   • System responsiveness: {'EXCELLENT' if success_rate > 90 else 'GOOD' if success_rate > 70 else 'NEEDS IMPROVEMENT'}")
    
    # Test specific problematic cases
    print(f"\n🎯 TESTING SPECIFIC PROBLEMATIC CASES:")
    problematic_cases = [
        "ok",
        "gpay", 
        "no",
        "yes",
        "thanks",
        "help"
    ]
    
    for case in problematic_cases:
        response = keyword_manager.keyword_matcher.generate_keyword_response(case)
        if response and response.get('confidence', 0) > 0.5:
            print(f"   ✅ '{case}' -> {response.get('confidence', 0):.2f} confidence")
        else:
            print(f"   ❌ '{case}' -> No match")
    
    return success_rate

def show_shortform_categories():
    """Show shortform categories and examples"""
    
    print(f"\n🗂️ SHORTFORM CATEGORIES:")
    print("=" * 40)
    
    categories = keyword_manager.list_keywords_by_category()
    
    shortform_categories = [
        'acknowledgment', 'confirmation', 'negation', 'uncertainty', 'gratitude',
        'payment', 'shipping', 'orders', 'support', 'returns', 'warranty',
        'greeting', 'technical', 'feedback'
    ]
    
    for category in shortform_categories:
        if category in categories:
            keywords = categories[category]
            print(f"📁 {category.upper()} ({len(keywords)} keywords)")
            # Show first few keywords as examples
            examples = [kw['keyword'] for kw in keywords[:3]]
            print(f"   Examples: {', '.join(examples)}")
            if len(keywords) > 3:
                print(f"   ... and {len(keywords) - 3} more")
            print()

if __name__ == "__main__":
    # Run the test
    success_rate = test_shortform_recognition()
    
    # Show categories
    show_shortform_categories()
    
    print("🎉 Shortform recognition test complete!")
    print("🌐 Visit http://localhost:8000 to test it live!")
    print("💡 Try queries like: 'ok', 'gpay', 'no', 'yes', 'thanks'")
