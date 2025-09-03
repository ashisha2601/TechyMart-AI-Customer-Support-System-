"""
Easy way to add new keywords and responses to your chatbot
Just run this script to add new keyword-based responses
"""

from keyword_matcher import keyword_matcher

def add_keywords_for_upi():
    """Add specific responses for UPI and Indian payment methods"""
    
    # UPI-related keywords
    keyword_matcher.add_custom_keyword(
        keyword="upi works",
        category="payment",
        response="Yes! UPI payments work perfectly! 🇮🇳 We support all UPI apps like Google Pay, PhonePe, Paytm, and BHIM. Payments are instant and secure with 256-bit encryption!",
        priority=10
    )
    
    keyword_matcher.add_custom_keyword(
        keyword="paytm",
        category="payment", 
        response="Absolutely! Paytm is fully supported! 💙 You can pay using Paytm wallet, UPI via Paytm, or Paytm Postpaid. All transactions are secure and instant!",
        priority=9
    )
    
    keyword_matcher.add_custom_keyword(
        keyword="google pay",
        category="payment",
        response="Yes! Google Pay works great! 🟢 Use GPay for instant UPI payments. Just scan the QR code or enter our UPI ID at checkout. Super fast and secure!",
        priority=9
    )
    
    keyword_matcher.add_custom_keyword(
        keyword="phonepe", 
        category="payment",
        response="PhonePe is fully supported! 💜 Pay instantly using PhonePe UPI or wallet. We also accept PhonePe Switch payments. Quick, easy, and secure!",
        priority=9
    )

def add_indian_specific_keywords():
    """Add India-specific responses"""
    
    keyword_matcher.add_custom_keyword(
        keyword="cod available",
        category="payment",
        response="Yes! Cash on Delivery (COD) is available across India! 💵 COD charges: ₹40 for orders under ₹500, FREE COD for orders ₹500+. Available in 19,000+ pin codes!",
        priority=9
    )
    
    keyword_matcher.add_custom_keyword(
        keyword="emi options",
        category="payment", 
        response="EMI options available! 💳 0% EMI on orders above ₹3,000 with major credit cards. Choose 3, 6, 9, 12, 18, or 24 months. Also available with Bajaj Finserv and ZestMoney!",
        priority=9
    )
    
    keyword_matcher.add_custom_keyword(
        keyword="delivery time india",
        category="shipping",
        response="India Delivery Times: 🇮🇳\n• Metro Cities: 1-2 days\n• Tier 2 Cities: 2-4 days\n• Tier 3 Cities: 3-7 days\n• Remote Areas: 5-10 days\nFree shipping on orders above ₹500!",
        priority=9
    )

def add_product_specific_keywords():
    """Add product-specific responses"""
    
    keyword_matcher.add_custom_keyword(
        keyword="mobile phones",
        category="products",
        response="We have the latest mobile phones! 📱 iPhone, Samsung, OnePlus, Xiaomi, Realme, and more. All phones come with manufacturer warranty, free delivery, and easy EMI options!",
        priority=8
    )
    
    keyword_matcher.add_custom_keyword(
        keyword="laptops",
        category="products", 
        response="Huge laptop collection! 💻 Dell, HP, Lenovo, ASUS, Acer, MacBook, and gaming laptops. Free installation support, extended warranty options, and 0% EMI available!",
        priority=8
    )
    
    keyword_matcher.add_custom_keyword(
        keyword="headphones",
        category="products",
        response="Premium headphones available! 🎧 Sony, Bose, JBL, Audio-Technica, Sennheiser. Wired, wireless, noise-cancelling, and gaming headsets. 30-day return guarantee!",
        priority=8
    )

def add_support_keywords():
    """Add customer support related keywords"""
    
    keyword_matcher.add_custom_keyword(
        keyword="customer care number",
        category="support",
        response="Customer Care: 📞\n• Toll-Free: 1800-123-TECH (8324)\n• WhatsApp: +91-98765-43210\n• Email: support@techymart.com\n• Live Chat: Available 24/7\n• Hindi Support: Available 9 AM - 9 PM",
        priority=9
    )
    
    keyword_matcher.add_custom_keyword(
        keyword="cancel order",
        category="orders",
        response="You can cancel your order easily! ⏰\n• Before shipping: Cancel instantly in 'My Orders'\n• After shipping: Refuse delivery for full refund\n• Need help? Call 1800-123-TECH or use live chat!",
        priority=9
    )
    
    keyword_matcher.add_custom_keyword(
        keyword="track order",
        category="orders", 
        response="Track your order easily! 📦\n• SMS/Email: Automatic updates sent\n• Website: Login → My Orders → Track\n• WhatsApp: Send order number to +91-98765-43210\n• App: Real-time tracking with delivery partner details",
        priority=9
    )

def test_new_keywords():
    """Test the newly added keywords"""
    
    print("🧪 Testing New Keywords")
    print("=" * 25)
    
    test_messages = [
        "Does UPI work?",
        "I want to pay with Paytm",
        "Is COD available?", 
        "What are EMI options?",
        "Do you sell mobile phones?",
        "Customer care number please",
        "How to cancel my order?"
    ]
    
    for message in test_messages:
        print(f"\n📝 User: {message}")
        response = keyword_matcher.generate_keyword_response(message)
        
        if response:
            print(f"🤖 Bot: {response['response'][:80]}...")
            print(f"   Confidence: {response.get('confidence', 'N/A')}")
        else:
            print("❌ No keyword match")

def main():
    """Add all keywords and test them"""
    
    print("➕ Adding Keywords to TechyMart Bot")
    print("=" * 35)
    
    # Add different categories of keywords
    add_keywords_for_upi()
    print("✅ Added UPI payment keywords")
    
    add_indian_specific_keywords()
    print("✅ Added India-specific keywords")
    
    add_product_specific_keywords()  
    print("✅ Added product keywords")
    
    add_support_keywords()
    print("✅ Added support keywords")
    
    # Test the keywords
    test_new_keywords()
    
    print("\n🎉 All keywords added successfully!")
    print("\n💡 Pro Tips:")
    print("1. Higher priority (8-10) = more likely to match")
    print("2. Use exact phrases for precise responses")
    print("3. Add multiple variations of the same keyword")
    print("4. Test your keywords before deploying")

if __name__ == "__main__":
    main()
