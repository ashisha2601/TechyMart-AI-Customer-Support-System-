"""
TechyMart FAQ Database
Contains company policies and common questions with answers.
"""

FAQ_DATABASE = [
    {
        "category": "shipping",
        "question": "What are your shipping options and delivery times?",
        "answer": "We offer several shipping options: Standard (3-5 business days, FREE on orders $50+), Express (1-2 business days, $9.99), and Overnight ($19.99). We ship Monday-Friday and provide tracking numbers for all orders! 📦✈️",
        "keywords": ["shipping", "delivery", "fast", "overnight", "standard", "express", "time", "how long", "when"]
    },
    {
        "category": "returns",
        "question": "What is your return policy?",
        "answer": "We have a hassle-free 30-day return policy! 🔄 Items must be in original condition with tags attached. Electronics need original packaging. Start a return online or contact us - we'll email you a prepaid return label. Refunds typically process within 3-5 business days of receiving your return.",
        "keywords": ["return", "refund", "exchange", "30 days", "policy", "send back", "don't want"]
    },
    {
        "category": "warranty",
        "question": "Do you offer warranties on products?",
        "answer": "Absolutely! 🛡️ All electronics come with manufacturer warranty (typically 1-2 years). We also offer TechyMart Extended Protection: 1 extra year for $19.99, 2 extra years for $34.99. This covers accidents, drops, and liquid damage that manufacturer warranties don't cover!",
        "keywords": ["warranty", "protection", "guarantee", "broken", "defective", "coverage", "repair"]
    },
    {
        "category": "payment",
        "question": "What payment methods do you accept?",
        "answer": "We accept all major payment methods! 💳 Visa, Mastercard, American Express, Discover, PayPal, Apple Pay, Google Pay, and even Buy Now Pay Later options like Klarna and Afterpay. Your payment info is always secure with 256-bit SSL encryption.",
        "keywords": ["payment", "credit card", "paypal", "apple pay", "google pay", "klarna", "afterpay", "pay"]
    },
    {
        "category": "account",
        "question": "How do I create an account or reset my password?",
        "answer": "Creating an account is super easy! 👤 Click 'Sign Up' at the top right, enter your email and create a password. Forgot your password? No worries! Click 'Forgot Password' on the login page and we'll send you a reset link. You can also shop as a guest if you prefer!",
        "keywords": ["account", "sign up", "register", "password", "forgot", "reset", "login", "guest"]
    },
    {
        "category": "products",
        "question": "Do you have product reviews and ratings?",
        "answer": "Yes! 🌟 Every product page shows verified customer reviews and ratings. We only display reviews from customers who actually purchased the item. You can sort by most helpful, newest, or rating. Your honest feedback helps other customers make great choices!",
        "keywords": ["reviews", "ratings", "feedback", "stars", "comments", "opinions", "quality"]
    },
    {
        "category": "support",
        "question": "How can I contact customer support?",
        "answer": "We're here to help 24/7! 🤗 You can chat with me right here, email us at support@techymart.com, call 1-800-TECHYMART, or use live chat on our website. For complex technical issues, our human experts are available Mon-Fri 9AM-6PM EST.",
        "keywords": ["contact", "support", "help", "phone", "email", "chat", "customer service", "human"]
    },
    {
        "category": "orders",
        "question": "Can I modify or cancel my order?",
        "answer": "If you need to modify or cancel, act fast! ⚡ Orders can be changed within 1 hour of placing them (before they hit our fulfillment center). After that, you'll need to process a return once you receive the item. Contact us ASAP and we'll do our best to help!",
        "keywords": ["modify", "cancel", "change", "order", "stop", "different", "wrong"]
    },
    {
        "category": "pricing",
        "question": "Do you offer price matching?",
        "answer": "We sure do! 💰 We'll match any lower price from major online retailers (Amazon, Best Buy, etc.) on identical items. The competitor must have the item in stock and the price must be current. Just contact us with the competitor's link and we'll adjust your price!",
        "keywords": ["price", "match", "cheaper", "lower", "discount", "beat", "competitor"]
    },
    {
        "category": "technical",
        "question": "What if my product arrives damaged or defective?",
        "answer": "Oh no! 😱 Don't worry, we've got you covered. Contact us immediately with photos of the damage/defect. We'll arrange a free replacement or full refund - your choice! For electronics, we can also connect you with our tech support team for troubleshooting before replacement.",
        "keywords": ["damaged", "defective", "broken", "not working", "replacement", "wrong item"]
    }
]

# Simulated order database
ORDER_DATABASE = {
    "1234": {
        "status": "shipped",
        "tracking": "TM789456123",
        "estimated_delivery": "Tomorrow by 5 PM",
        "items": ["Wireless Headphones", "Phone Case"],
        "location": "Out for delivery in your city"
    },
    "5678": {
        "status": "processing",
        "tracking": None,
        "estimated_delivery": "2-3 business days",
        "items": ["Gaming Mouse", "Keyboard"],
        "location": "Being prepared at our warehouse"
    },
    "9999": {
        "status": "delivered",
        "tracking": "TM123789456",
        "estimated_delivery": "Delivered yesterday",
        "items": ["Smartphone"],
        "location": "Left at front door"
    },
    "1111": {
        "status": "cancelled",
        "tracking": None,
        "estimated_delivery": "N/A",
        "items": ["Tablet"],
        "location": "Order cancelled per customer request"
    }
}
