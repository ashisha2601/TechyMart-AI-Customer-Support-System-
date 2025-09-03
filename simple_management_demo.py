"""
Simple Demo of Advanced Keyword Management Functions
Shows the most useful management features
"""

from keyword_manager import keyword_manager

def main():
    print("🚀 ADVANCED KEYWORD MANAGEMENT FUNCTIONS")
    print("=" * 50)
    
    # 1. BASIC MANAGEMENT
    print("\n🔧 1. BASIC MANAGEMENT")
    print("-" * 25)
    
    print("✅ Adding keywords:")
    keyword_manager.add_keyword(
        keyword="student discount",
        category="discounts", 
        response="Yes! 10% student discount with valid student ID! 🎓",
        priority=9
    )
    
    keyword_manager.add_keyword(
        keyword="bulk pricing",
        category="pricing",
        response="Bulk discounts available for 10+ items! Contact sales team! 📦",
        priority=8
    )
    
    # 2. SEARCH & DISCOVERY
    print("\n🔍 2. SEARCH & DISCOVERY")
    print("-" * 25)
    
    print("🔎 Searching for 'discount' keywords:")
    results = keyword_manager.search_keywords("discount")
    for result in results[:2]:
        print(f"   • {result['keyword']} → {result['response'][:50]}...")
    
    # 3. ANALYTICS
    print("\n📊 3. ANALYTICS & TRACKING")
    print("-" * 30)
    
    # Simulate usage
    keyword_manager.track_keyword_usage("student discount", "Do you have student discounts?", True)
    keyword_manager.track_keyword_usage("bulk pricing", "What about bulk orders?", True)
    keyword_manager.track_keyword_usage("student discount", "Any student deals?", False)
    
    stats = keyword_manager.get_usage_statistics(top_n=3)
    print(f"📈 Total Keywords: {stats['total_keywords']}")
    print(f"📈 Total Matches: {stats['total_matches']}")
    print(f"📈 Top Keywords: {list(stats['top_keywords'].keys())}")
    
    # 4. EXPORT/IMPORT
    print("\n💾 4. EXPORT/IMPORT")
    print("-" * 20)
    
    json_file = keyword_manager.export_keywords_to_json("backup_keywords.json")
    print(f"💾 Exported to: {json_file}")
    
    # 5. AUTOMATION
    print("\n🤖 5. AUTOMATION")
    print("-" * 15)
    
    # Generate suggestions from user messages
    sample_messages = [
        "How do I cancel subscription?",
        "Cancel my account please",
        "I want to cancel service",
        "Cancellation policy info"
    ]
    
    suggestions = keyword_manager.generate_keyword_suggestions(sample_messages)
    print("💡 Auto-suggested keywords from user messages:")
    for suggestion in suggestions[:3]:
        print(f"   • '{suggestion['suggested_keyword']}' (appeared {suggestion['frequency']} times)")
    
    # 6. TESTING
    print("\n🧪 6. TESTING & VALIDATION")
    print("-" * 25)
    
    test_messages = [
        "Do you have student discounts?",
        "What about bulk pricing?", 
        "Is there a mobile app?",
        "How secure is my data?"
    ]
    
    coverage = keyword_manager.test_keyword_coverage(test_messages)
    print(f"📊 Keyword Coverage: {coverage['coverage_rate']:.1%}")
    print(f"✅ Matched {coverage['matched']}/{coverage['total_messages']} messages")
    if coverage['unmatched']:
        print(f"❌ Unmatched: {coverage['unmatched']}")
    
    print("\n" + "=" * 50)
    print("🎉 DEMO COMPLETE!")
    print("\n💡 ALL AVAILABLE FUNCTIONS:")
    
    functions = [
        "📝 keyword_manager.add_keyword(keyword, category, response, priority)",
        "📦 keyword_manager.bulk_add_keywords(keywords_list)",
        "🔍 keyword_manager.search_keywords(query)",
        "📊 keyword_manager.get_usage_statistics()",
        "📈 keyword_manager.track_keyword_usage(keyword, message, success)",
        "💾 keyword_manager.export_keywords_to_json(filename)",
        "📥 keyword_manager.import_keywords_from_json(filename)",
        "🤖 keyword_manager.auto_optimize_keywords()",
        "💡 keyword_manager.generate_keyword_suggestions(messages)",
        "🧪 keyword_manager.test_keyword_coverage(test_messages)",
        "🔧 keyword_manager.validate_all_keywords()",
        "❌ keyword_manager.remove_keyword(keyword)",
        "✏️ keyword_manager.update_keyword(keyword, new_response=None)",
        "📋 keyword_manager.list_keywords_by_category(category=None)",
        "🔍 keyword_manager.find_duplicate_keywords()",
        "📉 keyword_manager.get_low_performing_keywords()",
        "💡 keyword_manager.suggest_keyword_improvements(keyword)",
        "📊 keyword_manager.export_to_csv(filename)",
        "📥 keyword_manager.import_from_csv(filename)"
    ]
    
    print("\n🛠️ USAGE EXAMPLES:")
    for func in functions:
        print(f"   {func}")
    
    print("\n🚀 QUICK START:")
    print("   from keyword_manager import keyword_manager")
    print("   keyword_manager.add_keyword('hello', 'greeting', 'Hi there! 👋', 9)")
    print("   stats = keyword_manager.get_usage_statistics()")
    print("   keyword_manager.export_keywords_to_json('backup.json')")

if __name__ == "__main__":
    main()

