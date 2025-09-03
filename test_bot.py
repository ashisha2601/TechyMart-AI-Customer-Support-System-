"""
Test script for TechyMart Customer Support AI Agent
"""

from chatbot import techymart_bot
from order_tracker import order_tracker
from rag_system import rag_system

def test_chatbot():
    print("🤖 Testing TechyMart Customer Support AI Agent")
    print("=" * 50)
    
    # Test cases
    test_messages = [
        "Hello!",
        "What's your return policy?",
        "Where's my order #1234?",
        "Do you offer warranties?",
        "I need help with quantum computing installation",  # Should escalate
        "Thank you so much!",
        "What payment methods do you accept?",
        "My order 5678 status please",
        "How do I contact support?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. User: {message}")
        response = techymart_bot.generate_response(message)
        print(f"   Bot: {response['response']}")
        print(f"   Type: {response['type']}")
        if response.get('escalate'):
            print("   🚨 ESCALATED TO HUMAN")
        print("-" * 30)

def test_order_tracker():
    print("\n🔍 Testing Order Tracker")
    print("=" * 30)
    
    test_orders = [
        "Where is my order #1234?",
        "Check order 5678",
        "Order number 9999 status",
        "What about order #7777?"  # Non-existent order
    ]
    
    for order_query in test_orders:
        print(f"\nQuery: {order_query}")
        result = order_tracker.handle_order_inquiry(order_query)
        if result:
            print(f"Response: {result[:100]}...")
        else:
            print("No order number found")

def test_rag_system():
    print("\n🧠 Testing RAG System")
    print("=" * 25)
    
    test_queries = [
        "return policy",
        "shipping times",
        "warranty coverage",
        "alien technology support"  # Should have low confidence
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        faq, score = rag_system.find_best_answer(query)
        if faq:
            print(f"Match: {faq['question']} (confidence: {score:.3f})")
        else:
            print(f"No good match (confidence: {score:.3f})")

if __name__ == "__main__":
    test_chatbot()
    test_order_tracker()
    test_rag_system()
    
    print("\n🎉 All tests completed!")
    print("\nTo run the web interface:")
    print("python main.py")
    print("Then open: http://localhost:8000")
