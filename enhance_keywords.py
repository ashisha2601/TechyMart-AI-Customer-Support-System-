"""
Keyword Enhancement Script for TechyMart AI
Adds comprehensive keywords across all categories to make the system more responsive
"""

from keyword_manager import keyword_manager
import json

def add_comprehensive_keywords():
    """Add a comprehensive set of keywords to make the system more responsive"""
    
    print("🚀 Adding comprehensive keywords to TechyMart AI...")
    
    # ==================== PAYMENT & BILLING KEYWORDS ====================
    payment_keywords = [
        {
            "keyword": "upi payment",
            "category": "payment",
            "response": "Yes! 🇮🇳 We support UPI payments through Google Pay, PhonePe, Paytm, and all UPI apps. UPI transactions are instant and secure! Just select UPI at checkout.",
            "priority": 9
        },
        {
            "keyword": "credit card",
            "category": "payment", 
            "response": "We accept all major credit cards: Visa, Mastercard, American Express, and Discover. Your payment is secured with 256-bit SSL encryption! 💳",
            "priority": 9
        },
        {
            "keyword": "paypal",
            "category": "payment",
            "response": "Absolutely! You can pay with PayPal for a quick and secure checkout. Just select PayPal as your payment method! 💰",
            "priority": 8
        },
        {
            "keyword": "apple pay",
            "category": "payment",
            "response": "Yes! Apple Pay is available for quick and secure payments on iPhone and Mac. Just look for the Apple Pay button at checkout! 🍎",
            "priority": 8
        },
        {
            "keyword": "google pay",
            "category": "payment",
            "response": "Google Pay is supported! You can use it for both UPI and card payments. Super convenient for Android users! 🤖",
            "priority": 8
        },
        {
            "keyword": "klarna",
            "category": "payment",
            "response": "Yes! We offer Klarna for Buy Now, Pay Later options. Split your purchase into 4 interest-free payments! 💳✨",
            "priority": 7
        },
        {
            "keyword": "afterpay",
            "category": "payment",
            "response": "Afterpay is available! Pay in 4 interest-free installments. Perfect for larger purchases! 💰",
            "priority": 7
        },
        {
            "keyword": "cash on delivery",
            "category": "payment",
            "response": "We offer Cash on Delivery (COD) in select areas! Check availability at checkout. COD orders may have a small additional fee. 💵",
            "priority": 6
        },
        {
            "keyword": "net banking",
            "category": "payment",
            "response": "Net banking is supported! You can pay directly from your bank account through our secure payment gateway. 🏦",
            "priority": 7
        },
        {
            "keyword": "wallet payment",
            "category": "payment",
            "response": "We accept various digital wallets including Paytm, PhonePe, and Amazon Pay! Quick and easy payments! 📱",
            "priority": 6
        }
    ]
    
    # ==================== SHIPPING & DELIVERY KEYWORDS ====================
    shipping_keywords = [
        {
            "keyword": "free shipping",
            "category": "shipping",
            "response": "Yes! We offer FREE shipping on orders over $50! 🚚✨ Standard shipping (3-5 days) is free, or upgrade to Express (1-2 days) for $9.99.",
            "priority": 9
        },
        {
            "keyword": "express delivery",
            "category": "shipping",
            "response": "Express delivery (1-2 business days) is available for $9.99! Perfect when you need your tech goodies fast! ⚡",
            "priority": 8
        },
        {
            "keyword": "overnight shipping",
            "category": "shipping",
            "response": "Overnight delivery is available for $19.99! Order by 2 PM and get it the next business day! 🌙➡️🌅",
            "priority": 8
        },
        {
            "keyword": "international shipping",
            "category": "shipping",
            "response": "We ship internationally! Shipping costs and delivery times vary by country. Contact us for specific rates to your location! 🌍",
            "priority": 7
        },
        {
            "keyword": "tracking number",
            "category": "shipping",
            "response": "You'll get a tracking number via email once your order ships! Use it to track your package in real-time! 📦📱",
            "priority": 8
        },
        {
            "keyword": "delivery time",
            "category": "shipping",
            "response": "Standard: 3-5 business days (FREE over $50), Express: 1-2 days ($9.99), Overnight: Next day ($19.99). We ship Mon-Fri! 📅",
            "priority": 8
        },
        {
            "keyword": "shipping address",
            "category": "shipping",
            "response": "You can change your shipping address within 1 hour of placing your order. After that, contact us and we'll do our best to help! 📍",
            "priority": 7
        },
        {
            "keyword": "weekend delivery",
            "category": "shipping",
            "response": "We don't deliver on weekends, but you can choose Saturday delivery for an additional fee in select areas! 📅",
            "priority": 6
        },
        {
            "keyword": "same day delivery",
            "category": "shipping",
            "response": "Same-day delivery is available in select metro areas for $29.99! Order by 12 PM for same-day delivery! 🚀",
            "priority": 7
        }
    ]
    
    # ==================== RETURNS & EXCHANGES KEYWORDS ====================
    returns_keywords = [
        {
            "keyword": "30 day return",
            "category": "returns",
            "response": "Yes! We have a hassle-free 30-day return policy! Items must be in original condition with tags. Start your return online! 🔄",
            "priority": 9
        },
        {
            "keyword": "return label",
            "category": "returns",
            "response": "We'll email you a prepaid return label! Just print it, attach to your package, and drop it off. Super easy! 📦✉️",
            "priority": 8
        },
        {
            "keyword": "refund time",
            "category": "returns",
            "response": "Refunds typically process within 3-5 business days after we receive your return. You'll get an email confirmation! 💰",
            "priority": 8
        },
        {
            "keyword": "exchange policy",
            "category": "returns",
            "response": "You can exchange items within 30 days! Just start a return and place a new order, or contact us for direct exchange! 🔄",
            "priority": 7
        },
        {
            "keyword": "return shipping cost",
            "category": "returns",
            "response": "Return shipping is FREE! We provide prepaid return labels for all returns. No cost to you! 🆓",
            "priority": 8
        },
        {
            "keyword": "opened box return",
            "category": "returns",
            "response": "Yes! You can return opened items within 30 days if they're in good condition. Electronics need original packaging! 📦",
            "priority": 7
        },
        {
            "keyword": "defective product",
            "category": "returns",
            "response": "If your product is defective, contact us immediately! We'll arrange a free replacement or full refund - your choice! 🔧",
            "priority": 9
        },
        {
            "keyword": "wrong item",
            "category": "returns",
            "response": "If you received the wrong item, we're so sorry! Contact us immediately and we'll send the correct item right away! 📦✅",
            "priority": 9
        }
    ]
    
    # ==================== WARRANTY & PROTECTION KEYWORDS ====================
    warranty_keywords = [
        {
            "keyword": "extended warranty",
            "category": "warranty",
            "response": "We offer TechyMart Extended Protection! 1 extra year for $19.99, 2 extra years for $34.99. Covers accidents, drops, and liquid damage! 🛡️",
            "priority": 9
        },
        {
            "keyword": "manufacturer warranty",
            "category": "warranty",
            "response": "All electronics come with manufacturer warranty (typically 1-2 years). Check your product page for specific warranty details! 📋",
            "priority": 8
        },
        {
            "keyword": "accidental damage",
            "category": "warranty",
            "response": "Our Extended Protection covers accidental damage like drops and liquid spills that manufacturer warranties don't cover! 💧📱",
            "priority": 8
        },
        {
            "keyword": "warranty claim",
            "category": "warranty",
            "response": "To make a warranty claim, contact us with your order number and issue description. We'll guide you through the process! 📞",
            "priority": 7
        },
        {
            "keyword": "repair service",
            "category": "warranty",
            "response": "We offer repair services for items under warranty! Contact us and we'll arrange pickup and repair at no cost to you! 🔧",
            "priority": 7
        }
    ]
    
    # ==================== ACCOUNT & LOGIN KEYWORDS ====================
    account_keywords = [
        {
            "keyword": "create account",
            "category": "account",
            "response": "Creating an account is super easy! Click 'Sign Up' at the top right, enter your email and create a password. You'll get exclusive deals! 👤✨",
            "priority": 8
        },
        {
            "keyword": "forgot password",
            "category": "account",
            "response": "No worries! Click 'Forgot Password' on the login page and we'll send you a reset link to your email! 🔑",
            "priority": 8
        },
        {
            "keyword": "guest checkout",
            "category": "account",
            "response": "Yes! You can shop as a guest without creating an account. Just choose 'Guest Checkout' at the payment page! 🛒",
            "priority": 7
        },
        {
            "keyword": "order history",
            "category": "account",
            "response": "Sign in to your account to view your complete order history, track current orders, and manage your profile! 📋",
            "priority": 7
        },
        {
            "keyword": "wishlist",
            "category": "account",
            "response": "Create a wishlist to save items for later! Sign in to your account and click the heart icon on any product! ❤️",
            "priority": 6
        }
    ]
    
    # ==================== PRODUCT & REVIEWS KEYWORDS ====================
    product_keywords = [
        {
            "keyword": "product reviews",
            "category": "products",
            "response": "Yes! Every product shows verified customer reviews and ratings. We only display reviews from actual customers! ⭐",
            "priority": 8
        },
        {
            "keyword": "product comparison",
            "category": "products",
            "response": "Use our comparison tool to compare up to 4 products side by side! Check specs, prices, and reviews all in one place! 📊",
            "priority": 7
        },
        {
            "keyword": "product availability",
            "category": "products",
            "response": "Check the product page for real-time availability! We update stock levels throughout the day. Out of stock? We'll notify you when it's back! 📦",
            "priority": 7
        },
        {
            "keyword": "product specifications",
            "category": "products",
            "response": "Detailed specifications are on every product page! Scroll down to see full tech specs, dimensions, and features! 📋",
            "priority": 6
        },
        {
            "keyword": "product warranty",
            "category": "products",
            "response": "Warranty information is listed on each product page. Most electronics have 1-2 year manufacturer warranty! 🛡️",
            "priority": 7
        }
    ]
    
    # ==================== SUPPORT & CONTACT KEYWORDS ====================
    support_keywords = [
        {
            "keyword": "customer service",
            "category": "support",
            "response": "We're here to help 24/7! Chat with me, email support@techymart.com, or call 1-800-TECHYMART! 🤗",
            "priority": 9
        },
        {
            "keyword": "live chat",
            "category": "support",
            "response": "You're already using it! I'm your AI assistant. For human support, we have live chat available Mon-Fri 9AM-6PM EST! 💬",
            "priority": 8
        },
        {
            "keyword": "phone support",
            "category": "support",
            "response": "Call us at 1-800-TECHYMART! Our human experts are available Mon-Fri 9AM-6PM EST for complex issues! 📞",
            "priority": 8
        },
        {
            "keyword": "email support",
            "category": "support",
            "response": "Email us at support@techymart.com! We typically respond within 2-4 hours during business hours! 📧",
            "priority": 7
        },
        {
            "keyword": "technical support",
            "category": "support",
            "response": "For technical issues, our specialized tech support team is available Mon-Fri 9AM-6PM EST! They're experts in troubleshooting! 🔧",
            "priority": 8
        }
    ]
    
    # ==================== ORDERS & TRACKING KEYWORDS ====================
    order_keywords = [
        {
            "keyword": "order status",
            "category": "orders",
            "response": "Check your order status by providing your order number! I can look it up for you right now! 📦",
            "priority": 9
        },
        {
            "keyword": "modify order",
            "category": "orders",
            "response": "You can modify orders within 1 hour of placing them! After that, you'll need to process a return. Contact us ASAP! ⚡",
            "priority": 8
        },
        {
            "keyword": "cancel order",
            "category": "orders",
            "response": "Cancel orders within 1 hour of placing them! After that, you'll need to process a return once received. We'll help! ❌",
            "priority": 8
        },
        {
            "keyword": "order confirmation",
            "category": "orders",
            "response": "You'll get an order confirmation email immediately after placing your order! Check your inbox (and spam folder)! 📧",
            "priority": 7
        },
        {
            "keyword": "bulk order",
            "category": "orders",
            "response": "For bulk orders (10+ items), contact our sales team for special pricing and shipping rates! 📦📦📦",
            "priority": 6
        }
    ]
    
    # ==================== PRICING & DEALS KEYWORDS ====================
    pricing_keywords = [
        {
            "keyword": "price match",
            "category": "pricing",
            "response": "We'll match any lower price from major retailers! Contact us with the competitor's link and we'll adjust your price! 💰",
            "priority": 8
        },
        {
            "keyword": "discount code",
            "category": "pricing",
            "response": "Check our promotions page for current discount codes! Sign up for our newsletter to get exclusive deals! 🎟️",
            "priority": 7
        },
        {
            "keyword": "student discount",
            "category": "pricing",
            "response": "Yes! Students get 10% off with valid student ID! Contact us with your student email for verification! 🎓",
            "priority": 7
        },
        {
            "keyword": "bulk discount",
            "category": "pricing",
            "response": "Bulk discounts available for orders of 10+ items! Contact our sales team for custom pricing! 📦💰",
            "priority": 6
        },
        {
            "keyword": "sale items",
            "category": "pricing",
            "response": "Check our Sale section for amazing deals! We update it regularly with clearance and seasonal items! 🏷️",
            "priority": 7
        }
    ]
    
    # ==================== TECHNICAL & TROUBLESHOOTING KEYWORDS ====================
    technical_keywords = [
        {
            "keyword": "setup help",
            "category": "technical",
            "response": "Need setup help? Our technical support team can guide you through installation and configuration! Contact us! 🔧",
            "priority": 8
        },
        {
            "keyword": "compatibility",
            "category": "technical",
            "response": "Check product specifications for compatibility details! Our tech support can help with specific compatibility questions! 🔌",
            "priority": 7
        },
        {
            "keyword": "software update",
            "category": "technical",
            "response": "For software updates, check the manufacturer's website or contact our tech support for guidance! 💻",
            "priority": 6
        },
        {
            "keyword": "driver download",
            "category": "technical",
            "response": "Driver downloads are usually available on the manufacturer's website. Our tech support can help you find the right drivers! 🖥️",
            "priority": 6
        },
        {
            "keyword": "troubleshooting",
            "category": "technical",
            "response": "Our technical support team specializes in troubleshooting! Contact us with your issue and we'll help solve it! 🔍",
            "priority": 8
        }
    ]
    
    # ==================== INDIAN-SPECIFIC KEYWORDS ====================
    indian_keywords = [
        {
            "keyword": "gst",
            "category": "pricing",
            "response": "All prices include GST! You'll see the GST breakdown in your order summary. We're fully GST compliant! 🇮🇳",
            "priority": 7
        },
        {
            "keyword": "emi options",
            "category": "payment",
            "response": "Yes! We offer EMI options through various banks and NBFCs. Check available EMI options at checkout! 💳",
            "priority": 8
        },
        {
            "keyword": "cashback",
            "category": "payment",
            "response": "We offer cashback on select payment methods! Check our promotions page for current cashback offers! 💰",
            "priority": 6
        },
        {
            "keyword": "pin code delivery",
            "category": "shipping",
            "response": "Enter your PIN code at checkout to check delivery availability and estimated delivery time to your area! 📍",
            "priority": 7
        },
        {
            "keyword": "cod charges",
            "category": "payment",
            "response": "COD charges vary by location and order value. Check the exact charges at checkout before placing your order! 💵",
            "priority": 6
        }
    ]
    
    # Combine all keyword categories
    all_keywords = (
        payment_keywords + shipping_keywords + returns_keywords + 
        warranty_keywords + account_keywords + product_keywords + 
        support_keywords + order_keywords + pricing_keywords + 
        technical_keywords + indian_keywords
    )
    
    print(f"📦 Adding {len(all_keywords)} comprehensive keywords...")
    
    # Add all keywords using the keyword manager
    keyword_manager.bulk_add_keywords(all_keywords)
    
    print("✅ All keywords added successfully!")
    return len(all_keywords)

def add_common_phrases():
    """Add common customer phrases and variations"""
    
    print("🗣️ Adding common customer phrases...")
    
    common_phrases = [
        # Greeting variations
        {"keyword": "good morning", "category": "greeting", "response": "Good morning! ☀️ Welcome to TechyMart! How can I help you today?", "priority": 8},
        {"keyword": "good afternoon", "category": "greeting", "response": "Good afternoon! 🌤️ Great to see you at TechyMart! What can I assist you with?", "priority": 8},
        {"keyword": "good evening", "category": "greeting", "response": "Good evening! 🌙 Welcome to TechyMart! How may I help you tonight?", "priority": 8},
        {"keyword": "hey there", "category": "greeting", "response": "Hey there! 👋 Welcome to TechyMart! What's on your mind today?", "priority": 7},
        {"keyword": "what's up", "category": "greeting", "response": "What's up! 🚀 I'm here to help with all your TechyMart needs! What can I do for you?", "priority": 6},
        
        # Question variations
        {"keyword": "do you have", "category": "products", "response": "I'd be happy to help you find what you're looking for! Can you tell me more about the specific product?", "priority": 7},
        {"keyword": "is it available", "category": "products", "response": "Let me check availability for you! What specific product are you interested in?", "priority": 7},
        {"keyword": "how much does it cost", "category": "pricing", "response": "I can help you with pricing! Which product are you asking about?", "priority": 7},
        {"keyword": "when will it be back in stock", "category": "products", "response": "I can check stock status for you! What product are you looking for?", "priority": 7},
        
        # Problem expressions
        {"keyword": "i have a problem", "category": "support", "response": "I'm sorry to hear you're having an issue! Please tell me more about the problem and I'll help you resolve it! 🤗", "priority": 8},
        {"keyword": "this is not working", "category": "technical", "response": "I'm sorry your product isn't working! Let me connect you with our technical support team who can help troubleshoot! 🔧", "priority": 8},
        {"keyword": "i'm not satisfied", "category": "support", "response": "I'm sorry you're not satisfied! Let me help make this right. What specifically can we improve?", "priority": 8},
        {"keyword": "this is broken", "category": "technical", "response": "I'm sorry your item is broken! Contact us immediately and we'll arrange a free replacement or refund! 🔧", "priority": 9},
        
        # Urgency expressions
        {"keyword": "i need this urgently", "category": "shipping", "response": "I understand you need this urgently! We offer Express (1-2 days) and Overnight delivery options! ⚡", "priority": 8},
        {"keyword": "asap", "category": "shipping", "response": "Got it! For ASAP delivery, we have Express (1-2 days) and Overnight options available! 🚀", "priority": 7},
        {"keyword": "emergency", "category": "support", "response": "I understand this is urgent! Let me connect you with our priority support team right away! 🚨", "priority": 9},
        
        # Positive expressions
        {"keyword": "love it", "category": "gratitude", "response": "That's awesome! I'm so glad you love your purchase! Thanks for choosing TechyMart! ❤️", "priority": 6},
        {"keyword": "amazing service", "category": "gratitude", "response": "Thank you so much! That really means a lot to our team! We're here whenever you need us! 🌟", "priority": 6},
        {"keyword": "you're the best", "category": "gratitude", "response": "Aww, you're the best too! Thanks for being such a great customer! 🤗", "priority": 5},
        
        # Confusion expressions
        {"keyword": "i don't understand", "category": "support", "response": "No worries! Let me explain that in a different way. What specific part would you like me to clarify?", "priority": 7},
        {"keyword": "confused", "category": "support", "response": "I'm here to help clear up any confusion! What would you like me to explain better?", "priority": 7},
        {"keyword": "not sure", "category": "support", "response": "That's totally fine! Let me help you figure this out. What are you not sure about?", "priority": 6}
    ]
    
    keyword_manager.bulk_add_keywords(common_phrases)
    print(f"✅ Added {len(common_phrases)} common phrases!")
    return len(common_phrases)

def add_emoji_keywords():
    """Add emoji-based keywords for modern communication"""
    
    print("😊 Adding emoji-based keywords...")
    
    emoji_keywords = [
        {"keyword": "👍", "category": "gratitude", "response": "Thanks for the thumbs up! Glad I could help! 👍", "priority": 5},
        {"keyword": "❤️", "category": "gratitude", "response": "Aww, sending love right back! ❤️ Thanks for being awesome!", "priority": 5},
        {"keyword": "😊", "category": "greeting", "response": "😊 Hello there! Great to see you! How can I help you today?", "priority": 6},
        {"keyword": "🤔", "category": "support", "response": "I see you're thinking! 🤔 What's on your mind? I'm here to help!", "priority": 6},
        {"keyword": "😢", "category": "support", "response": "I'm sorry you're feeling down! 😢 Let me help make things better. What's wrong?", "priority": 7},
        {"keyword": "🎉", "category": "gratitude", "response": "🎉 Celebrating with you! Thanks for choosing TechyMart!", "priority": 5},
        {"keyword": "🔥", "category": "gratitude", "response": "🔥 That's fire! Thanks for the awesome feedback!", "priority": 5},
        {"keyword": "💯", "category": "gratitude", "response": "💯 You're 100% awesome! Thanks for being a great customer!", "priority": 5}
    ]
    
    keyword_manager.bulk_add_keywords(emoji_keywords)
    print(f"✅ Added {len(emoji_keywords)} emoji keywords!")
    return len(emoji_keywords)

def main():
    """Main function to enhance the keyword system"""
    
    print("🚀 TechyMart AI Keyword Enhancement Tool")
    print("=" * 50)
    
    # Add comprehensive keywords
    total_keywords = 0
    total_keywords += add_comprehensive_keywords()
    total_keywords += add_common_phrases()
    total_keywords += add_emoji_keywords()
    
    print("\n" + "=" * 50)
    print(f"🎉 KEYWORD ENHANCEMENT COMPLETE!")
    print(f"📊 Total keywords added: {total_keywords}")
    print(f"🎯 System is now much more responsive!")
    
    # Show statistics
    stats = keyword_manager.get_usage_statistics()
    print(f"\n📈 Current system stats:")
    print(f"   • Total keywords: {stats['total_keywords']}")
    print(f"   • Categories: {len(stats['categories'])}")
    
    # Export updated keywords
    backup_file = keyword_manager.export_keywords_to_json()
    print(f"💾 Keywords backed up to: {backup_file}")
    
    print("\n🔄 Restart your server to see the enhanced keyword system in action!")
    print("   python advanced_main.py")

if __name__ == "__main__":
    main()
