"""
Advanced RAG System with Sentence Transformers and Vector Database
High-end semantic search with proper embeddings and context awareness
"""

import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict, Tuple, Optional
from faq_data import FAQ_DATABASE
import json
import os
from datetime import datetime

class AdvancedRAGSystem:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize with a high-quality sentence transformer model"""
        print("🧠 Loading advanced AI model...")
        self.model = SentenceTransformer(model_name)
        
        # Initialize ChromaDB for vector storage
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="techymart_faqs",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.faqs = FAQ_DATABASE
        self.conversation_context = []
        self.user_preferences = {}
        
        # Build or load the vector index
        self._initialize_vector_database()
        print("✅ Advanced RAG system ready!")
    
    def _initialize_vector_database(self):
        """Initialize the vector database with FAQ embeddings"""
        # Check if we already have embeddings
        existing_count = self.collection.count()
        
        if existing_count == 0:
            print("🔄 Building vector database...")
            self._build_vector_index()
        else:
            print(f"📚 Loaded {existing_count} existing FAQ embeddings")
    
    def _build_vector_index(self):
        """Build embeddings for all FAQ entries"""
        documents = []
        metadatas = []
        ids = []
        
        for i, faq in enumerate(self.faqs):
            # Create rich document text combining all fields
            doc_text = f"""
            Question: {faq['question']}
            Answer: {faq['answer']}
            Category: {faq['category']}
            Keywords: {', '.join(faq['keywords'])}
            """
            
            documents.append(doc_text.strip())
            metadatas.append({
                "category": faq['category'],
                "question": faq['question'],
                "answer": faq['answer'],
                "keywords": json.dumps(faq['keywords']),
                "created_at": datetime.now().isoformat()
            })
            ids.append(f"faq_{i}")
        
        # Generate embeddings and store in ChromaDB
        embeddings = self.model.encode(documents).tolist()
        
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Built vector index with {len(documents)} FAQ entries")
    
    def find_best_answer(self, query: str, n_results: int = 3, threshold: float = 0.7) -> Tuple[Optional[Dict], float, List[Dict]]:
        """
        Advanced semantic search with context awareness
        
        Args:
            query: User's question
            n_results: Number of similar results to retrieve
            threshold: Minimum similarity threshold
            
        Returns:
            Tuple of (best_match, confidence_score, all_results)
        """
        # Enhance query with conversation context
        enhanced_query = self._enhance_query_with_context(query)
        
        # Search the vector database
        results = self.collection.query(
            query_texts=[enhanced_query],
            n_results=n_results
        )
        
        if not results['distances'][0]:
            return None, 0.0, []
        
        # Convert ChromaDB results to our format
        all_matches = []
        for i, (distance, metadata) in enumerate(zip(results['distances'][0], results['metadatas'][0])):
            confidence = 1 - distance  # Convert distance to similarity
            
            match = {
                'question': metadata['question'],
                'answer': metadata['answer'],
                'category': metadata['category'],
                'keywords': json.loads(metadata['keywords']),
                'confidence': confidence
            }
            all_matches.append(match)
        
        # Get the best match
        best_match = all_matches[0] if all_matches else None
        best_confidence = all_matches[0]['confidence'] if all_matches else 0.0
        
        # Update conversation context
        self._update_context(query, best_match, best_confidence)
        
        if best_confidence >= threshold:
            return best_match, best_confidence, all_matches
        else:
            return None, best_confidence, all_matches
    
    def _enhance_query_with_context(self, query: str) -> str:
        """Enhance query with conversation context for better matching"""
        if not self.conversation_context:
            return query
        
        # Add recent context (last 2 exchanges)
        recent_context = self.conversation_context[-2:]
        context_text = " ".join([ctx.get('query', '') for ctx in recent_context])
        
        return f"{context_text} {query}"
    
    def _update_context(self, query: str, match: Optional[Dict], confidence: float):
        """Update conversation context for better future matching"""
        context_entry = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'match_found': match is not None,
            'confidence': confidence,
            'category': match['category'] if match else None
        }
        
        self.conversation_context.append(context_entry)
        
        # Keep only last 10 exchanges
        if len(self.conversation_context) > 10:
            self.conversation_context = self.conversation_context[-10:]
    
    def get_conversation_insights(self) -> Dict:
        """Get insights about the current conversation"""
        if not self.conversation_context:
            return {"status": "new_conversation"}
        
        categories = [ctx['category'] for ctx in self.conversation_context if ctx['category']]
        avg_confidence = np.mean([ctx['confidence'] for ctx in self.conversation_context])
        
        return {
            "total_queries": len(self.conversation_context),
            "categories_discussed": list(set(categories)),
            "average_confidence": avg_confidence,
            "recent_category": categories[-1] if categories else None,
            "escalation_likely": avg_confidence < 0.6
        }
    
    def get_smart_suggestions(self, query: str) -> List[str]:
        """Get smart follow-up suggestions based on query and context"""
        insights = self.get_conversation_insights()
        
        # Base suggestions
        suggestions = [
            "What's your return policy?",
            "Do you offer warranties?",
            "What payment methods do you accept?",
            "How can I track my order?"
        ]
        
        # Context-aware suggestions
        if insights.get('recent_category') == 'shipping':
            suggestions = [
                "What are your delivery options?",
                "Can I change my shipping address?",
                "Do you offer express delivery?",
                "What if my package is delayed?"
            ]
        elif insights.get('recent_category') == 'returns':
            suggestions = [
                "How do I start a return?",
                "What items can't be returned?",
                "How long do refunds take?",
                "Can I exchange instead of return?"
            ]
        elif 'order' in query.lower():
            suggestions = [
                "Where's my order #1234?",
                "Can I modify my order?",
                "How do I cancel an order?",
                "What's the order status?"
            ]
        
        return suggestions[:4]  # Return top 4 suggestions

# Global advanced RAG system instance
try:
    advanced_rag = AdvancedRAGSystem()
except Exception as e:
    print(f"⚠️ Advanced RAG system unavailable: {e}")
    print("🔄 Falling back to basic RAG system...")
    from rag_system import rag_system as advanced_rag
