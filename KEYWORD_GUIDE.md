# 🔑 Keyword-Based Response System Guide

## 📋 **Overview**
The keyword system allows your chatbot to respond instantly to specific words or phrases with pre-defined answers. It's faster than AI processing and gives you precise control over responses.

---

## 🚀 **How It Works**

### **3-Layer Response System:**
1. **Keyword Matching** (Fastest) - Exact phrase and keyword pattern matching
2. **RAG/Semantic Search** (Smart) - AI-powered understanding 
3. **Escalation** (Fallback) - Human agent handoff

### **Priority System:**
- **Priority 10**: Exact matches (highest priority)
- **Priority 8-9**: Important keywords 
- **Priority 5-7**: General keywords
- **Priority 1-4**: Low priority/fallback

---

## 💻 **Basic Usage**

### **1. Import the System**
```python
from keyword_matcher import keyword_matcher
```

### **2. Generate Response**
```python
user_message = "Does UPI work?"
response = keyword_matcher.generate_keyword_response(user_message)

if response:
    print(f"Bot: {response['response']}")
    print(f"Confidence: {response['confidence']}")
else:
    print("No keyword match found")
```

### **3. Add Custom Keywords**
```python
keyword_matcher.add_custom_keyword(
    keyword="student discount",
    category="discounts", 
    response="Yes! 10% student discount available! 🎓",
    priority=9
)
```

---

## 🎯 **Adding Keywords - Step by Step**

### **Method 1: Using add_custom_keyword()**
```python
# Simple keyword addition
keyword_matcher.add_custom_keyword(
    keyword="free shipping",           # What user might say
    category="shipping",               # Category for organization
    response="Free shipping on orders above $50! 📦",  # Bot response
    priority=8                         # Priority level (1-10)
)
```

### **Method 2: Direct Pattern Addition**
```python
# Add to keyword_matcher.py file
"custom_pattern": {
    "keywords": ["keyword1", "keyword2", "phrase"],
    "priority": 9,
    "response_type": "direct_answer"
}
```

### **Method 3: Exact Phrase Matching**
```python
# Add to exact_phrases in keyword_matcher.py
"exact phrase": {
    "category": "category_name",
    "confidence": 0.95,
    "response": "Your exact response here"
}
```

---

## 📝 **Examples by Category**

### **Payment Keywords**
```python
# UPI Support
keyword_matcher.add_custom_keyword(
    "upi works", "payment",
    "Yes! UPI payments work perfectly! 🇮🇳 Google Pay, PhonePe, Paytm all supported!", 10
)

# Credit Cards
keyword_matcher.add_custom_keyword(
    "credit card", "payment", 
    "We accept all major credit cards! Visa, Mastercard, Amex, Discover 💳", 9
)

# EMI Options
keyword_matcher.add_custom_keyword(
    "emi available", "payment",
    "0% EMI available on orders above $100! 3-24 months options 💳", 9
)
```

### **Shipping Keywords**
```python
# Fast Delivery
keyword_matcher.add_custom_keyword(
    "same day delivery", "shipping",
    "Same day delivery available in metro cities! Order before 12 PM ⚡", 9
)

# International Shipping  
keyword_matcher.add_custom_keyword(
    "international shipping", "shipping",
    "We ship worldwide! 5-10 business days, customs duties may apply 🌍", 8
)
```

### **Product Keywords**
```python
# Specific Products
keyword_matcher.add_custom_keyword(
    "iphone 15", "products",
    "iPhone 15 available! Starting at $799. All colors in stock! 📱", 9
)

# Categories
keyword_matcher.add_custom_keyword(
    "gaming laptops", "products", 
    "Gaming laptops from ASUS, MSI, Alienware! RTX 4000 series available 🎮", 8
)
```

---

## 🔧 **Advanced Configuration**

### **1. Multi-Language Support**
```python
# Hindi Keywords
keyword_matcher.add_custom_keyword(
    "kya aap hindi me baat kar sakte hain", "language",
    "Haan bilkul! Main Hindi mein baat kar sakta hun! 🇮🇳 Kaise madad kar sakta hun?", 10
)

# Regional Keywords
keyword_matcher.add_custom_keyword(
    "bangalore delivery", "shipping",
    "Bangalore delivery: Same day available! Free delivery above ₹500 🏙️", 9
)
```

### **2. Context-Aware Responses**
```python
# Order-related with action
"track my order": {
    "response_type": "action_required",  # Requires order number
    "priority": 9
}

# Technical issues  
"not working": {
    "response_type": "escalate",  # Auto-escalate to human
    "priority": 8
}
```

### **3. Dynamic Keywords**
```python
# Load from configuration file
import json

def load_keywords_from_config():
    with open('keyword_config.json', 'r') as f:
        config = json.load(f)
    
    for phrase, data in config['exact_phrases'].items():
        keyword_matcher.add_custom_keyword(
            phrase, data['category'], data['response'], 9
        )
```

---

## 📊 **Testing Your Keywords**

### **Test Script**
```python
def test_keywords():
    test_messages = [
        "Does UPI work?",
        "I need same day delivery", 
        "Do you have iPhone 15?",
        "What about EMI options?"
    ]
    
    for message in test_messages:
        print(f"User: {message}")
        response = keyword_matcher.generate_keyword_response(message)
        
        if response:
            print(f"Bot: {response['response']}")
            print(f"Confidence: {response['confidence']}")
        else:
            print("No match found")
        print("-" * 30)

test_keywords()
```

---

## 🎨 **Best Practices**

### **1. Keyword Selection**
- ✅ Use common phrases customers actually say
- ✅ Include variations and misspellings
- ✅ Add regional/local terms
- ❌ Don't use overly technical terms
- ❌ Avoid too generic keywords

### **2. Response Quality**
- ✅ Keep responses helpful and specific
- ✅ Include relevant emojis for personality  
- ✅ Provide next steps or actions
- ❌ Don't make responses too long
- ❌ Avoid confusing or contradictory info

### **3. Priority Management**
- **Priority 10**: Brand-specific, exact matches
- **Priority 9**: Important customer queries
- **Priority 8**: Product/service specific
- **Priority 7**: General support topics
- **Priority 6-**: Less critical keywords

### **4. Testing Strategy**
```python
# Test different variations
test_variations = [
    "UPI works?",
    "Does UPI work?", 
    "UPI payment available?",
    "Can I pay with UPI?",
    "UPI supported?"
]
```

---

## 🔄 **Integration with Main Bot**

### **In your main chatbot code:**
```python
def generate_response(self, user_message: str):
    # Step 1: Try keyword matching (fastest)
    keyword_response = keyword_matcher.generate_keyword_response(user_message)
    if keyword_response:
        return keyword_response
    
    # Step 2: Try semantic search (AI)
    semantic_response = rag_system.find_best_answer(user_message)
    if semantic_response:
        return semantic_response
    
    # Step 3: Escalate to human
    return self.escalate_to_human()
```

---

## 📈 **Performance Tips**

### **1. Optimize for Speed**
- Put most common keywords at higher priority
- Use exact phrase matching for frequent queries
- Keep keyword lists organized by category

### **2. Monitor and Improve**
```python
# Get statistics
stats = keyword_matcher.get_keyword_statistics()
print(f"Total keywords: {stats['total_keywords']}")
print(f"Categories: {stats['categories']}")

# Track which keywords are being matched
def log_keyword_match(keyword, user_message):
    print(f"Matched '{keyword}' for: {user_message}")
```

---

## 🛠️ **Quick Setup Commands**

### **1. Test Current System**
```bash
python keyword_examples.py
```

### **2. Add New Keywords**
```bash
python add_keywords.py
```

### **3. Check Integration**
```bash
python test_bot.py
```

---

## 🎯 **Common Use Cases**

### **E-commerce Keywords**
- Payment methods: "credit card", "paypal", "upi", "cod"
- Shipping: "free shipping", "express delivery", "tracking"
- Returns: "return policy", "refund", "exchange"
- Products: "iphone", "laptop", "headphones"

### **Support Keywords** 
- Technical: "not working", "broken", "error"
- Account: "login problem", "password reset"
- Orders: "cancel order", "modify order", "order status"

### **Regional Keywords**
- India: "upi", "paytm", "cod", "emi"
- US: "credit score", "financing", "zip code"
- Global: "international shipping", "customs"

---

## 🚀 **Ready-to-Use Examples**

Copy and paste these into your system:

```python
# Popular payment keywords
payment_keywords = [
    ("upi works", "Yes! UPI payments supported! Google Pay, PhonePe, Paytm 🇮🇳"),
    ("credit card accepted", "All major credit cards accepted! Visa, Mastercard, Amex 💳"),
    ("paypal available", "PayPal payments available! Secure and instant 🛡️"),
    ("buy now pay later", "BNPL options: Klarna, Afterpay, Sezzle available! 💰")
]

for keyword, response in payment_keywords:
    keyword_matcher.add_custom_keyword(keyword, "payment", response, 9)
```

---

**🎉 Your keyword system is now ready! Start adding keywords that matter to your customers and watch your bot respond instantly and accurately!**

