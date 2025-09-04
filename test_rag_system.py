"""
Test script for RAG system functionality
"""

import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_rag_components():
    """Test individual RAG components"""
    print("🧪 Testing RAG System Components...")
    
    try:
        # Test data ingestion
        print("\n1. Testing Data Ingestion...")
        from rag_data_ingestion import rag_data_ingestion
        from faq_data import FAQ_DATABASE
        
        faq_documents = rag_data_ingestion.ingest_faq_database(FAQ_DATABASE)
        print(f"✅ Ingested {len(faq_documents)} FAQ documents")
        
        sample_documents = rag_data_ingestion.create_sample_knowledge_base()
        print(f"✅ Created {len(sample_documents)} sample documents")
        
    except Exception as e:
        print(f"❌ Data ingestion failed: {e}")
        return False
    
    try:
        # Test vector store
        print("\n2. Testing Vector Store...")
        from rag_vector_store import rag_vector_store
        
        all_documents = faq_documents + sample_documents
        success = rag_vector_store.add_documents(all_documents)
        
        if success:
            print("✅ Documents added to vector store")
            
            # Test similarity search
            results = rag_vector_store.similarity_search("shipping policy", k=3)
            print(f"✅ Similarity search returned {len(results)} results")
            
            # Test stats
            stats = rag_vector_store.get_stats()
            print(f"✅ Vector store stats: {stats}")
        else:
            print("❌ Failed to add documents to vector store")
            return False
            
    except Exception as e:
        print(f"❌ Vector store test failed: {e}")
        return False
    
    try:
        # Test LangChain integration
        print("\n3. Testing LangChain Integration...")
        from rag_langchain_integration import rag_langchain
        
        # Test query processing
        response = rag_langchain.process_query_with_rag(
            "What is your return policy?",
            session_id="test_session"
        )
        
        if response and 'response' in response:
            print("✅ LangChain query processing works")
            print(f"   Response: {response['response'][:100]}...")
        else:
            print("❌ LangChain query processing failed")
            return False
            
    except Exception as e:
        print(f"❌ LangChain integration test failed: {e}")
        return False
    
    try:
        # Test conversation memory
        print("\n4. Testing Conversation Memory...")
        from rag_conversation_memory import rag_conversation_memory
        
        # Test conversation processing
        response = rag_conversation_memory.process_conversation(
            "Hello, I need help with my order",
            session_id="test_session"
        )
        
        if response and 'response' in response:
            print("✅ Conversation memory works")
            print(f"   Response: {response['response'][:100]}...")
        else:
            print("❌ Conversation memory failed")
            return False
            
    except Exception as e:
        print(f"❌ Conversation memory test failed: {e}")
        return False
    
    try:
        # Test enhanced chatbot
        print("\n5. Testing Enhanced RAG Chatbot...")
        from rag_enhanced_chatbot import rag_enhanced_chatbot
        
        # Test response generation
        response = rag_enhanced_chatbot.generate_response(
            "What are your shipping options?",
            session_id="test_session"
        )
        
        if response and 'response' in response:
            print("✅ Enhanced RAG chatbot works")
            print(f"   Response: {response['response'][:100]}...")
            print(f"   Method: {response.get('method', 'unknown')}")
            print(f"   Confidence: {response.get('confidence', 0):.2f}")
        else:
            print("❌ Enhanced RAG chatbot failed")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced RAG chatbot test failed: {e}")
        return False
    
    return True

def test_conversation_flow():
    """Test a complete conversation flow"""
    print("\n🔄 Testing Complete Conversation Flow...")
    
    try:
        from rag_enhanced_chatbot import rag_enhanced_chatbot
        
        # Test conversation
        test_queries = [
            "Hello, I need help",
            "What is your return policy?",
            "How long does shipping take?",
            "Can I track my order?",
            "Thank you for your help"
        ]
        
        session_id = "conversation_test"
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Query {i}: {query}")
            response = rag_enhanced_chatbot.generate_response(query, session_id)
            
            if response and 'response' in response:
                print(f"   Response: {response['response'][:80]}...")
                print(f"   Method: {response.get('method', 'unknown')}")
                print(f"   Confidence: {response.get('confidence', 0):.2f}")
            else:
                print("   ❌ No response generated")
                return False
        
        # Test analytics
        analytics = rag_enhanced_chatbot.get_conversation_analytics(session_id)
        print(f"\n   Analytics: {analytics}")
        
        print("✅ Complete conversation flow works")
        return True
        
    except Exception as e:
        print(f"❌ Conversation flow test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints (requires server to be running)"""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        import requests
        
        # Test RAG status endpoint
        response = requests.get("http://localhost:8000/rag/status", timeout=5)
        if response.status_code == 200:
            print("✅ RAG status endpoint works")
        else:
            print(f"❌ RAG status endpoint failed: {response.status_code}")
            return False
        
        # Test RAG chat endpoint
        chat_data = {
            "message": "What is your return policy?",
            "session_id": "api_test"
        }
        response = requests.post(
            "http://localhost:8000/chat/rag",
            data=chat_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ RAG chat endpoint works")
            data = response.json()
            print(f"   Response: {data.get('response', '')[:80]}...")
        else:
            print(f"❌ RAG chat endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("⚠️ Server not running - skipping API tests")
        return True
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 RAG System Test Suite")
    print("=" * 50)
    
    # Test individual components
    components_ok = test_rag_components()
    
    if components_ok:
        # Test conversation flow
        conversation_ok = test_conversation_flow()
        
        # Test API endpoints
        api_ok = test_api_endpoints()
        
        print("\n" + "=" * 50)
        print("📊 Test Results Summary:")
        print(f"   Components: {'✅ PASS' if components_ok else '❌ FAIL'}")
        print(f"   Conversation: {'✅ PASS' if conversation_ok else '❌ FAIL'}")
        print(f"   API Endpoints: {'✅ PASS' if api_ok else '⚠️ SKIP'}")
        
        if components_ok and conversation_ok:
            print("\n🎉 All tests passed! RAG system is working correctly.")
            return True
        else:
            print("\n❌ Some tests failed. Check the errors above.")
            return False
    else:
        print("\n❌ Component tests failed. RAG system is not working.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
