"""
RAG (Retrieval-Augmented Generation) System for FAQ matching
Uses simple embedding similarity for finding relevant answers.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from faq_data import FAQ_DATABASE

class SimpleRAGSystem:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
        self.faq_vectors = None
        self.faqs = FAQ_DATABASE
        self._build_index()
    
    def _build_index(self):
        """Build TF-IDF vectors for all FAQ entries"""
        # Combine question, answer, and keywords for better matching
        texts = []
        for faq in self.faqs:
            combined_text = f"{faq['question']} {faq['answer']} {' '.join(faq['keywords'])}"
            texts.append(combined_text)
        
        self.faq_vectors = self.vectorizer.fit_transform(texts)
    
    def find_best_answer(self, query: str, threshold: float = 0.1) -> Tuple[Dict, float]:
        """
        Find the most relevant FAQ answer for a given query
        
        Args:
            query: User's question
            threshold: Minimum similarity score to consider a match
            
        Returns:
            Tuple of (best_faq_dict, similarity_score)
        """
        # Vectorize the query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.faq_vectors)[0]
        
        # Find best match
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score >= threshold:
            return self.faqs[best_idx], best_score
        else:
            return None, best_score
    
    def get_category_faqs(self, category: str) -> List[Dict]:
        """Get all FAQs for a specific category"""
        return [faq for faq in self.faqs if faq['category'] == category]
    
    def search_by_keywords(self, keywords: List[str]) -> List[Dict]:
        """Search FAQs by specific keywords"""
        results = []
        for faq in self.faqs:
            if any(keyword.lower() in [k.lower() for k in faq['keywords']] for keyword in keywords):
                results.append(faq)
        return results

# Global RAG system instance
rag_system = SimpleRAGSystem()
