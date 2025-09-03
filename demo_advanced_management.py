"""
Demo of Advanced Keyword Management Functions
Shows all the powerful management features available
"""

from keyword_manager import keyword_manager

def demo_basic_management():
    """Demo basic keyword management functions"""
    print("🔧 BASIC MANAGEMENT FUNCTIONS")
    print("=" * 40)
    
    # 1. Add single keyword
    print("\n1️⃣ Adding Single Keywords:")
    keyword_manager.add_keyword(
        keyword="free trial",
        category="pricing",
        response="Yes! We offer a 7-day free trial with full access to all features! 🆓 No credit card required!",
        priority=9,
        tags=["trial", "pricing", "promotion"]
    )
    
    # 2. Bulk add keywords
    print("\n2️⃣ Bulk Adding Keywords:")
    bulk_keywords = [
        {
            "keyword": "mobile app",
            "category": "products",
            "response": "Our mobile app is available on iOS and Android! 📱 Download from App Store or Google Play!",
            "priority": 8,
            "tags": ["mobile", "app"]
        },
        {
            "keyword": "24/7 support",
            "category": "support",
            "response": "Yes! We provide 24/7 customer support via chat, email, and phone! 🕐 Always here to help!",
            "priority": 9,
            "tags": ["support", "24/7"]
        },
        {
            "keyword": "data security",
            "category": "security",
            "response": "Your data is 100% secure! 🔒 We use bank-level encryption, SOC2 compliance, and regular security audits!",
            "priority": 8,
            "tags": ["security", "encryption"]
        }
    ]
    
    keyword_manager.bulk_add_keywords(bulk_keywords)
    
    # 3. Update existing keyword
    print("\n3️⃣ Updating Keywords:")
    keyword_manager.update_keyword(
        keyword="free trial",
        new_response="Amazing! We offer a 14-day free trial with premium features! 🆓✨ Start today!",
        new_priority=10
    )

def demo_search_discovery():
    """Demo search and discovery functions"""
    print("\n🔍 SEARCH & DISCOVERY FUNCTIONS")
    print("=" * 40)
    
    # 1. Search keywords
    print("\n1️⃣ Searching Keywords:")
    results = keyword_manager.search_keywords("support", search_in="all")
    for result in results[:3]:
        print(f"   • {result['keyword']} ({result['category']}) - {result['response'][:50]}...")
    
    # 2. List by category
    print("\n2️⃣ Keywords by Category:")
    categories = keyword_manager.list_keywords_by_category()
    for category, keywords in list(categories.items())[:3]:
        print(f"   📂 {category}: {len(keywords)} keywords")
        for kw in keywords[:2]:
            print(f"      • {kw['keyword']} (Priority: {kw['priority']})")
    
    # 3. Find duplicates
    print("\n3️⃣ Finding Duplicates:")
    duplicates = keyword_manager.find_duplicate_keywords()
    if duplicates:
        for dup in duplicates[:3]:
            print(f"   ⚠️ {dup['type']}: '{dup['keyword1']}' ↔ '{dup['keyword2']}'")
    else:
        print("   ✅ No duplicates found!")

def demo_analytics():
    """Demo analytics and optimization functions"""
    print("\n📊 ANALYTICS & OPTIMIZATION")
    print("=" * 35)
    
    # Simulate some usage data
    print("\n1️⃣ Simulating Usage Data:")
    test_usage = [
        ("free trial", "Do you have free trial?", True),
        ("mobile app", "Where can I download the app?", True),
        ("24/7 support", "Is support available 24/7?", True),
        ("data security", "How secure is my data?", False),  # Simulate failure
        ("free trial", "Can I try it for free?", True),
    ]
    
    for keyword, message, success in test_usage:
        keyword_manager.track_keyword_usage(keyword, message, success)
        print(f"   📈 Tracked: '{keyword}' - {'✅' if success else '❌'}")
    
    # 2. Get usage statistics
    print("\n2️⃣ Usage Statistics:")
    stats = keyword_manager.get_usage_statistics(top_n=5)
    print(f"   • Total Keywords: {stats['total_keywords']}")
    print(f"   • Total Matches: {stats['total_matches']}")
    print("   • Top Keywords:", list(stats['top_keywords'].keys())[:3])
    print("   • Categories:", list(stats['categories'].keys())[:3])
    
    # 3. Performance analysis
    print("\n3️⃣ Performance Analysis:")
    low_performers = keyword_manager.get_low_performing_keywords(min_usage=1, max_success_rate=0.8)
    if low_performers:
        for performer in low_performers[:2]:
            print(f"   ⚠️ {performer['keyword']}: {performer['success_rate']:.1%} success rate")
    
    # 4. Keyword suggestions
    print("\n4️⃣ Improvement Suggestions:")
    if low_performers:
        suggestions = keyword_manager.suggest_keyword_improvements(low_performers[0]['keyword'])
        print(f"   🔧 For '{suggestions['keyword']}':")
        for suggestion in suggestions['suggestions'][:2]:
            print(f"      • {suggestion}")

def demo_import_export():
    """Demo import/export functions"""
    print("\n💾 IMPORT/EXPORT FUNCTIONS")
    print("=" * 30)
    
    # 1. Export to JSON
    print("\n1️⃣ Exporting to JSON:")
    json_file = keyword_manager.export_keywords_to_json("demo_keywords.json")
    
    # 2. Export to CSV
    print("\n2️⃣ Exporting to CSV:")
    csv_file = keyword_manager.export_to_csv("demo_keywords.csv")
    
    print(f"   📄 Files created: {json_file}, {csv_file}")

def demo_automation():
    """Demo automation functions"""
    print("\n🤖 AUTOMATION FUNCTIONS")
    print("=" * 25)
    
    # 1. Auto-optimize keywords
    print("\n1️⃣ Auto-Optimization:")
    optimized_count = keyword_manager.auto_optimize_keywords()
    print(f"   🔧 Optimized {optimized_count} keywords based on performance")
    
    # 2. Generate suggestions from user messages
    print("\n2️⃣ Keyword Suggestions from User Messages:")
    sample_messages = [
        "How do I cancel my subscription?",
        "What is your refund policy?",
        "Can I cancel anytime?",
        "Is there a cancellation fee?",
        "How to delete my account?",
        "Subscription cancellation process"
    ]
    
    suggestions = keyword_manager.generate_keyword_suggestions(sample_messages)
    print("   💡 Suggested new keywords:")
    for suggestion in suggestions[:3]:
        print(f"      • '{suggestion['suggested_keyword']}' (freq: {suggestion['frequency']})")

def demo_testing_validation():
    """Demo testing and validation functions"""
    print("\n🧪 TESTING & VALIDATION")
    print("=" * 25)
    
    # 1. Test keyword coverage
    print("\n1️⃣ Testing Keyword Coverage:")
    test_messages = [
        "Do you have a free trial?",
        "Is there a mobile app?",
        "How secure is my data?",
        "What about customer support?",
        "Can I get a refund?",  # This might not match
    ]
    
    coverage = keyword_manager.test_keyword_coverage(test_messages)
    print(f"   📊 Coverage: {coverage['coverage_rate']:.1%} ({coverage['matched']}/{coverage['total_messages']})")
    print(f"   ✅ Matched: {len(coverage['matches'])} messages")
    print(f"   ❌ Unmatched: {coverage['unmatched']}")
    
    # 2. Validate all keywords
    print("\n2️⃣ Keyword Validation:")
    issues = keyword_manager.validate_all_keywords()
    if issues:
        print(f"   ⚠️ Found {len(issues)} issues:")
        for issue in issues[:3]:
            print(f"      • {issue['keyword']}: {issue['issue']} ({issue['severity']})")
    else:
        print("   ✅ All keywords validated successfully!")

def show_available_functions():
    """Show all available management functions"""
    print("\n📋 ALL AVAILABLE MANAGEMENT FUNCTIONS")
    print("=" * 45)
    
    functions = {
        "Basic Management": [
            "add_keyword(keyword, category, response, priority, tags)",
            "bulk_add_keywords(keywords_data)",
            "remove_keyword(keyword)",
            "update_keyword(keyword, new_response, new_priority, new_category)"
        ],
        "Search & Discovery": [
            "search_keywords(query, search_in='all')",
            "list_keywords_by_category(category=None)",
            "find_duplicate_keywords()",
        ],
        "Analytics & Optimization": [
            "track_keyword_usage(keyword, user_message, success)",
            "get_usage_statistics(top_n=10)",
            "get_low_performing_keywords(min_usage, max_success_rate)",
            "suggest_keyword_improvements(keyword)"
        ],
        "Import/Export": [
            "export_keywords_to_json(filename)",
            "import_keywords_from_json(filename)",
            "export_to_csv(filename)",
            "import_from_csv(filename)"
        ],
        "Automation": [
            "auto_optimize_keywords()",
            "generate_keyword_suggestions(user_messages)"
        ],
        "Testing & Validation": [
            "test_keyword_coverage(test_messages)",
            "validate_all_keywords()"
        ]
    }
    
    for category, funcs in functions.items():
        print(f"\n🔧 {category}:")
        for func in funcs:
            print(f"   • keyword_manager.{func}")

def main():
    """Run all demos"""
    print("🚀 ADVANCED KEYWORD MANAGEMENT DEMO")
    print("=" * 50)
    
    # Run all demos
    demo_basic_management()
    demo_search_discovery()
    demo_analytics()
    demo_import_export()
    demo_automation()
    demo_testing_validation()
    show_available_functions()
    
    print("\n🎉 Demo completed! All functions are ready to use!")
    print("\n💡 Quick Start:")
    print("   from keyword_manager import keyword_manager")
    print("   keyword_manager.add_keyword('hello', 'greeting', 'Hi there! 👋')")
    print("   stats = keyword_manager.get_usage_statistics()")

if __name__ == "__main__":
    main()

