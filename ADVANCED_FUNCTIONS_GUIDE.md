# 🚀 Advanced Keyword Management Functions

## 📋 **Complete Function Library**

I've created **19 powerful management functions** for your keyword system. Here's everything you can do:

---

## 🔧 **1. BASIC MANAGEMENT (4 functions)**

### **Add Keywords**
```python
# Single keyword
keyword_manager.add_keyword(
    keyword="student discount",
    category="discounts",
    response="10% student discount available! 🎓",
    priority=9,
    tags=["education", "discount"]
)

# Bulk add multiple keywords
keywords_data = [
    {"keyword": "free shipping", "category": "shipping", "response": "Free shipping on $50+ orders! 📦", "priority": 8},
    {"keyword": "24/7 support", "category": "support", "response": "24/7 customer support available! 🕐", "priority": 9}
]
keyword_manager.bulk_add_keywords(keywords_data)
```

### **Update & Remove Keywords**
```python
# Update existing keyword
keyword_manager.update_keyword(
    keyword="student discount",
    new_response="Amazing 15% student discount! 🎓✨",
    new_priority=10
)

# Remove keyword
keyword_manager.remove_keyword("old_keyword")
```

---

## 🔍 **2. SEARCH & DISCOVERY (3 functions)**

### **Search Keywords**
```python
# Search in all fields
results = keyword_manager.search_keywords("payment", search_in="all")

# Search specific fields
results = keyword_manager.search_keywords("UPI", search_in="response")
results = keyword_manager.search_keywords("shipping", search_in="category")
```

### **Organize by Category**
```python
# List all categories
all_categories = keyword_manager.list_keywords_by_category()

# Get specific category
payment_keywords = keyword_manager.list_keywords_by_category("payment")
```

### **Find Duplicates**
```python
# Find duplicate and similar keywords
duplicates = keyword_manager.find_duplicate_keywords()
for dup in duplicates:
    print(f"⚠️ {dup['type']}: {dup['keyword1']} ↔ {dup['keyword2']}")
```

---

## 📊 **3. ANALYTICS & OPTIMIZATION (4 functions)**

### **Track Performance**
```python
# Track keyword usage
keyword_manager.track_keyword_usage("upi works", "Does UPI work?", success=True)

# Get comprehensive statistics
stats = keyword_manager.get_usage_statistics(top_n=10)
print(f"Total keywords: {stats['total_keywords']}")
print(f"Top performers: {stats['top_keywords']}")
```

### **Performance Analysis**
```python
# Find underperforming keywords
low_performers = keyword_manager.get_low_performing_keywords(
    min_usage=5, 
    max_success_rate=0.6
)

# Get improvement suggestions
suggestions = keyword_manager.suggest_keyword_improvements("problem_keyword")
```

---

## 💾 **4. IMPORT/EXPORT (4 functions)**

### **Backup & Restore**
```python
# Export to JSON (full backup)
keyword_manager.export_keywords_to_json("backup_2024.json")

# Import from JSON
keyword_manager.import_keywords_from_json("backup_2024.json")

# Export to CSV (for Excel editing)
keyword_manager.export_to_csv("keywords_for_editing.csv")

# Import from CSV
keyword_manager.import_from_csv("updated_keywords.csv")
```

---

## 🤖 **5. AUTOMATION (2 functions)**

### **Auto-Optimization**
```python
# Automatically adjust priorities based on performance
optimized_count = keyword_manager.auto_optimize_keywords()
print(f"Optimized {optimized_count} keywords")

# Generate keyword suggestions from user messages
user_messages = [
    "How do I cancel my subscription?",
    "Cancel my account please",
    "I want to cancel service"
]

suggestions = keyword_manager.generate_keyword_suggestions(user_messages)
for suggestion in suggestions:
    print(f"Suggested: '{suggestion['suggested_keyword']}' (frequency: {suggestion['frequency']})")
```

---

## 🧪 **6. TESTING & VALIDATION (2 functions)**

### **Test Coverage**
```python
# Test how well keywords cover user messages
test_messages = [
    "Do you accept UPI?",
    "What's your return policy?",
    "How do I cancel?",
    "Is support available 24/7?"
]

coverage = keyword_manager.test_keyword_coverage(test_messages)
print(f"Coverage: {coverage['coverage_rate']:.1%}")
print(f"Unmatched: {coverage['unmatched']}")
```

### **Validate Quality**
```python
# Check all keywords for issues
issues = keyword_manager.validate_all_keywords()
for issue in issues:
    print(f"⚠️ {issue['keyword']}: {issue['issue']} ({issue['severity']})")
```

---

## 🎯 **PRACTICAL USE CASES**

### **1. E-commerce Store**
```python
# Add product-specific keywords
keyword_manager.add_keyword("iphone 15 price", "products", "iPhone 15 starts at $799! All colors available 📱", 9)
keyword_manager.add_keyword("free returns", "returns", "Free returns within 30 days! 🔄", 8)
keyword_manager.add_keyword("express shipping", "shipping", "Express shipping: 1-2 days for $9.99! ⚡", 8)
```

### **2. SaaS Platform**
```python
# Add service-related keywords  
keyword_manager.add_keyword("api limits", "technical", "API limits: 10K requests/month on free plan, unlimited on pro! 🔌", 8)
keyword_manager.add_keyword("sso integration", "features", "SSO integration available on enterprise plans! 🔐", 7)
keyword_manager.add_keyword("data export", "features", "Export your data anytime in CSV, JSON, or XML format! 📊", 8)
```

### **3. Customer Support**
```python
# Add support-specific keywords
keyword_manager.add_keyword("escalate to human", "support", "Connecting you to our human support team! 👨‍💻", 10)
keyword_manager.add_keyword("ticket status", "support", "Check your ticket status in the support portal! 🎫", 8)
keyword_manager.add_keyword("priority support", "support", "Priority support available for premium customers! ⭐", 7)
```

---

## 📈 **ADVANCED WORKFLOWS**

### **1. Daily Maintenance**
```python
# Daily keyword maintenance routine
def daily_keyword_maintenance():
    # 1. Check performance
    low_performers = keyword_manager.get_low_performing_keywords()
    
    # 2. Auto-optimize
    keyword_manager.auto_optimize_keywords()
    
    # 3. Backup
    keyword_manager.export_keywords_to_json(f"daily_backup_{datetime.now().strftime('%Y%m%d')}.json")
    
    # 4. Validate
    issues = keyword_manager.validate_all_keywords()
    
    return {
        'low_performers': len(low_performers),
        'issues_found': len(issues),
        'backup_created': True
    }
```

### **2. Analytics Dashboard**
```python
# Create analytics dashboard data
def get_keyword_dashboard():
    stats = keyword_manager.get_usage_statistics(top_n=10)
    coverage = keyword_manager.test_keyword_coverage(recent_user_messages)
    
    return {
        'total_keywords': stats['total_keywords'],
        'total_matches': stats['total_matches'],
        'top_keywords': stats['top_keywords'],
        'coverage_rate': coverage['coverage_rate'],
        'categories': stats['categories']
    }
```

### **3. Keyword Optimization Pipeline**
```python
# Automated keyword optimization
def optimize_keywords_pipeline(user_messages):
    # 1. Generate suggestions from user messages
    suggestions = keyword_manager.generate_keyword_suggestions(user_messages)
    
    # 2. Find gaps in coverage
    coverage = keyword_manager.test_keyword_coverage(user_messages)
    
    # 3. Identify low performers
    low_performers = keyword_manager.get_low_performing_keywords()
    
    # 4. Auto-optimize existing keywords
    keyword_manager.auto_optimize_keywords()
    
    return {
        'new_suggestions': suggestions,
        'coverage_gaps': coverage['unmatched'],
        'optimization_candidates': low_performers
    }
```

---

## 🎨 **BEST PRACTICES**

### **1. Keyword Naming**
- ✅ Use natural language: "upi works" not "upi_payment_method"
- ✅ Include variations: "free trial", "trial version", "test account"
- ✅ Add regional terms: "UPI", "Paytm", "PhonePe" for India

### **2. Priority System**
- **Priority 10**: Brand-specific, exact matches
- **Priority 9**: High-value customer queries
- **Priority 8**: Product/service specific
- **Priority 7**: General support topics
- **Priority 6-**: Nice-to-have keywords

### **3. Performance Monitoring**
```python
# Weekly performance review
def weekly_keyword_review():
    stats = keyword_manager.get_usage_statistics()
    low_performers = keyword_manager.get_low_performing_keywords(min_usage=10)
    
    # Focus on keywords used 10+ times with <70% success rate
    for performer in low_performers:
        suggestions = keyword_manager.suggest_keyword_improvements(performer['keyword'])
        print(f"📊 {performer['keyword']}: {suggestions['suggestions']}")
```

---

## 🚀 **QUICK IMPLEMENTATION GUIDE**

### **Step 1: Import**
```python
from keyword_manager import keyword_manager
```

### **Step 2: Add Your Keywords**
```python
# Add your most important keywords first
important_keywords = [
    ("upi payment", "payment", "UPI payments fully supported! 🇮🇳", 10),
    ("free shipping", "shipping", "Free shipping on orders $50+! 📦", 9),
    ("return policy", "returns", "30-day hassle-free returns! 🔄", 9),
    ("customer support", "support", "24/7 support available! 🤝", 8)
]

for keyword, category, response, priority in important_keywords:
    keyword_manager.add_keyword(keyword, category, response, priority)
```

### **Step 3: Monitor & Optimize**
```python
# Regular monitoring
stats = keyword_manager.get_usage_statistics()
keyword_manager.auto_optimize_keywords()
keyword_manager.export_keywords_to_json("backup.json")
```

---

## 🎉 **SUMMARY**

You now have **19 powerful functions** for complete keyword management:

- **📝 4 Basic Management** - Add, update, remove, bulk operations
- **🔍 3 Search & Discovery** - Find, organize, detect duplicates  
- **📊 4 Analytics** - Track usage, performance analysis, optimization
- **💾 4 Import/Export** - Backup, restore, CSV editing
- **🤖 2 Automation** - Auto-optimize, generate suggestions
- **🧪 2 Testing** - Coverage testing, quality validation

Your keyword system is now **enterprise-grade** with comprehensive management capabilities! 🚀✨

