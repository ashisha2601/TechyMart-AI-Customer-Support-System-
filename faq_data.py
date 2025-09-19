"""
TechyMart FAQ Database
Contains frequently asked questions and answers for the customer support system
"""

FAQ_DATABASE = [
    {
        "question": "What is your return policy?",
        "answer": "We offer a 30-day return policy for most items. Electronics have a 14-day return window. Items must be in original condition with tags. Free return shipping for defective items!",
        "category": "returns",
        "keywords": ["return", "refund", "exchange", "policy"]
    },
    {
        "question": "How long does delivery take?",
        "answer": "Standard delivery takes 3-5 business days, express delivery takes 1-2 business days. We also offer same-day delivery in select cities.",
        "category": "delivery",
        "keywords": ["delivery", "shipping", "time", "when"]
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, Apple Pay, Google Pay, and bank transfers. All payments are secure and encrypted!",
        "category": "payment",
        "keywords": ["payment", "credit card", "paypal", "apple pay", "google pay"]
    },
    {
        "question": "How can I track my order?",
        "answer": "You can track your order by logging into your account and going to 'My Orders', or by using the tracking number we sent to your email.",
        "category": "delivery",
        "keywords": ["track", "order", "status", "where"]
    },
    {
        "question": "What is your warranty policy?",
        "answer": "Most products come with a 1-year manufacturer warranty. Extended warranties are available for electronics. Check your product page for specific warranty details.",
        "category": "warranty",
        "keywords": ["warranty", "guarantee", "repair", "defective"]
    },
    {
        "question": "How can I contact customer support?",
        "answer": "You can reach us at: Phone: 1-800-TECHY-HELP, Email: support@techymart.com, Live Chat: Available 24/7 on our website, or visit our store locations!",
        "category": "support",
        "keywords": ["contact", "support", "help", "phone", "email"]
    },
    {
        "question": "Do you offer international shipping?",
        "answer": "Yes! We ship worldwide. International shipping costs and delivery times vary by country. Check our shipping calculator for specific rates.",
        "category": "delivery",
        "keywords": ["international", "worldwide", "shipping", "overseas"]
    },
    {
        "question": "Can I change or cancel my order?",
        "answer": "You can modify or cancel your order within 1 hour of placing it if it hasn't been processed yet. After that, you'll need to return it using our return policy.",
        "category": "orders",
        "keywords": ["change", "cancel", "modify", "order"]
    },
    {
        "question": "What are your store hours?",
        "answer": "Our stores are open Monday-Friday 9AM-9PM, Saturday 10AM-8PM, and Sunday 11AM-6PM. Online support is available 24/7!",
        "category": "support",
        "keywords": ["hours", "store", "open", "time"]
    },
    {
        "question": "How do I create an account?",
        "answer": "Click 'Sign Up' on our website, enter your email and create a password. You'll receive a confirmation email to verify your account.",
        "category": "account",
        "keywords": ["account", "sign up", "register", "create"]
    }
]

ORDER_DATABASE = {
    "1234": {
        "order_id": "TM789456123",
        "status": "Shipped",
        "items": ["Wireless Headphones", "Phone Case"],
        "tracking": "On the way",
        "estimated_delivery": "Tomorrow"
    },
    "5678": {
        "order_id": "TM456789012",
        "status": "Processing",
        "items": ["Gaming Mouse", "Keyboard"],
        "tracking": "Being prepared",
        "estimated_delivery": "In 2-3 days"
    },
    "9999": {
        "order_id": "TM123789456",
        "status": "Delivered",
        "items": ["Smart Watch"],
        "tracking": "Delivered",
        "estimated_delivery": "Delivered yesterday"
    },
    "1111": {
        "order_id": "TM987654321",
        "status": "Cancelled",
        "items": ["Laptop Stand"],
        "tracking": "N/A",
        "estimated_delivery": "Order cancelled"
    }
}