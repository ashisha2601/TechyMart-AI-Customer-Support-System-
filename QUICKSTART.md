# 🚀 Quick Start Guide - TechyMart Customer Support AI

## Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the system:**
   ```bash
   python test_bot.py
   ```

3. **Try the command-line demo:**
   ```bash
   python demo.py
   ```

4. **Launch the web interface:**
   ```bash
   python main.py
   ```
   Then open: http://localhost:8000

## 🎯 Features Demonstrated

### ✅ FAQ Answering (RAG System)
- **Try:** "What's your return policy?"
- **Try:** "Do you offer warranties?"
- **Try:** "What payment methods do you accept?"

### ✅ Order Tracking (Agentic Action)
- **Try:** "Where's my order #1234?"
- **Try:** "Check order 5678 status"
- **Try:** "Order number 9999 please"

### ✅ Smart Escalation
- **Try:** "I need help with quantum computing"
- **Try:** "My flux capacitor is broken"
- **Try:** "Advanced neural network debugging"

### ✅ Friendly Personality
- Emojis and humor throughout responses
- "Delivery pigeons" and "warehouse elves" references
- Warm, helpful tone with escalations

## 📊 Test Order Numbers

- `#1234` - Shipped (out for delivery)
- `#5678` - Processing (being prepared)
- `#9999` - Delivered (yesterday)
- `#1111` - Cancelled
- `#7777` - Not found (triggers helpful error message)

## 🏗️ Architecture

```
chatbot.py          # Main bot logic & personality
├── rag_system.py   # FAQ matching with TF-IDF
├── order_tracker.py # Simulated order database
├── faq_data.py     # Company policies & order data
└── main.py         # FastAPI web application
```

## 🎨 Customization

- **Add more FAQs:** Edit `faq_data.py`
- **Adjust personality:** Modify responses in `chatbot.py`
- **Change escalation threshold:** Update `escalation_threshold` in `chatbot.py`
- **Add more order data:** Extend `ORDER_DATABASE` in `faq_data.py`

## 🌟 What Makes This Special

1. **Beginner-Friendly:** Uses simple TF-IDF instead of complex embeddings
2. **But Still Interesting:** Implements proper RAG architecture
3. **Agentic Actions:** Actual function calls for order lookup
4. **Smart Escalation:** Confidence-based handoff to humans
5. **Great UX:** Beautiful web interface with real-time chat
6. **Personality Plus:** Engaging, funny responses that users love

Enjoy your AI customer support agent! 🤖✨
