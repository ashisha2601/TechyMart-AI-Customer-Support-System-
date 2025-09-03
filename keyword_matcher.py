"""
Enhanced Keyword-Based Response System
Provides precise control over bot responses based on specific keywords and phrases
"""

import re
from typing import Dict, List, Optional, Tuple
from faq_data import FAQ_DATABASE

class KeywordMatcher:
    def __init__(self):
        self.faq_data = FAQ_DATABASE
        
        # Enhanced keyword patterns with priorities
        self.keyword_patterns = {
            # High Priority Keywords (exact matches first)
            "payment_methods": {
                "keywords": ["payment methods", "how to pay", "payment options", "credit card", "paypal", "apple pay"],
                "priority": 10,
                "response_type": "direct_answer"
            },
            "shipping_info": {
                "keywords": ["shipping", "delivery", "how long", "when will it arrive", "tracking"],
                "priority": 10,
                "response_type": "direct_answer"
            },
            "warranty_info": {
                "keywords": ["warranty", "guarantee", "protection", "broken", "defective"],
                "priority": 10,
                "response_type": "direct_answer"
            },
            "return_policy": {
                "keywords": ["return", "refund", "send back", "don't want", "exchange"],
                "priority": 10,
                "response_type": "direct_answer"
            },
            
            # Medium Priority Keywords (partial matches)
            "order_tracking": {
                "keywords": ["order", "track", "where is", "status", "package"],
                "priority": 8,
                "response_type": "action_required"  # Needs order number
            },
            "technical_support": {
                "keywords": ["not working", "broken", "error", "problem", "issue", "help"],
                "priority": 7,
                "response_type": "escalate"
            },
            
            # Greeting Keywords
            "greetings": {
                "keywords": ["hello", "hi", "hey", "good morning", "good afternoon"],
                "priority": 5,
                "response_type": "greeting"
            }
        }
        
        # Exact phrase matching for better accuracy
        self.exact_phrases = {
            "upi works": {
                "category": "payment",
                "confidence": 0.95,
                "response": "Great question about UPI! 🇮🇳 Yes, we do support UPI payments through our Indian payment gateway. You can use Google Pay, PhonePe, Paytm, or any UPI-enabled app. UPI transactions are instant and secure with 256-bit encryption. Would you like me to walk you through the checkout process?"
            },
            "payment methods": {
                "category": "payment", 
                "confidence": 0.98,
                "response": None  # Use FAQ database response
            },
            "return policy": {
                "category": "returns",
                "confidence": 0.98,
                "response": None
            }
        }
    
    def find_keyword_match(self, user_message: str) -> Optional[Dict]:
        """
        Find the best keyword match with priority-based scoring
        """
        message_lower = user_message.lower().strip()
        
        # Step 1: Check for exact phrase matches first
        exact_match = self._check_exact_phrases(message_lower)
        if exact_match:
            return exact_match
        
        # Step 2: Check keyword patterns with scoring
        best_match = None
        best_score = 0
        
        for pattern_name, pattern_data in self.keyword_patterns.items():
            score = self._calculate_keyword_score(message_lower, pattern_data)
            
            if score > best_score:
                best_score = score
                best_match = {
                    "pattern": pattern_name,
                    "score": score,
                    "priority": pattern_data["priority"],
                    "response_type": pattern_data["response_type"],
                    "matched_keywords": self._get_matched_keywords(message_lower, pattern_data["keywords"])
                }
        
        # Only return if score is above threshold
        if best_score >= 3:  # Minimum threshold
            return best_match
        
        return None
    
    def _check_exact_phrases(self, message: str) -> Optional[Dict]:
        """Check for exact phrase matches"""
        for phrase, data in self.exact_phrases.items():
            if phrase in message:
                if data["response"]:
                    return {
                        "type": "exact_phrase",
                        "category": data["category"],
                        "confidence": data["confidence"],
                        "response": data["response"]
                    }
                else:
                    # Find FAQ response
                    faq_response = self._find_faq_by_category(data["category"])
                    if faq_response:
                        return {
                            "type": "exact_phrase",
                            "category": data["category"],
                            "confidence": data["confidence"],
                            "response": faq_response["answer"]
                        }
        return None
    
    def _calculate_keyword_score(self, message: str, pattern_data: Dict) -> float:
        """Calculate keyword matching score"""
        keywords = pattern_data["keywords"]
        priority = pattern_data["priority"]
        
        # Count exact keyword matches
        exact_matches = sum(1 for keyword in keywords if keyword in message)
        
        # Count partial matches (word boundaries)
        partial_matches = 0
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', message):
                partial_matches += 1
        
        # Calculate weighted score
        base_score = (exact_matches * 2) + partial_matches
        weighted_score = base_score * (priority / 10)
        
        return weighted_score
    
    def _get_matched_keywords(self, message: str, keywords: List[str]) -> List[str]:
        """Get list of keywords that matched"""
        matched = []
        for keyword in keywords:
            if keyword in message:
                matched.append(keyword)
        return matched
    
    def _find_faq_by_category(self, category: str) -> Optional[Dict]:
        """Find FAQ entry by category"""
        for faq in self.faq_data:
            if faq["category"] == category:
                return faq
        return None
    
    def generate_keyword_response(self, user_message: str) -> Optional[Dict]:
        """
        Generate response based on keyword matching
        """
        keyword_match = self.find_keyword_match(user_message)
        
        if not keyword_match:
            return None
        
        # Handle different response types
        if keyword_match.get("type") == "exact_phrase":
            return {
                "response": keyword_match["response"],
                "type": "keyword_match",
                "confidence": keyword_match["confidence"],
                "category": keyword_match["category"],
                "method": "exact_phrase"
            }
        
        response_type = keyword_match["response_type"]
        
        if response_type == "direct_answer":
            return self._generate_direct_answer(keyword_match)
        elif response_type == "action_required":
            return self._generate_action_response(keyword_match, user_message)
        elif response_type == "escalate":
            return self._generate_escalation_response(keyword_match)
        elif response_type == "greeting":
            return self._generate_greeting_response()
        
        return None
    
    def _generate_direct_answer(self, match: Dict) -> Dict:
        """Generate direct FAQ answer"""
        pattern = match["pattern"]
        
        # Map patterns to categories
        category_map = {
            "payment_methods": "payment",
            "shipping_info": "shipping", 
            "warranty_info": "warranty",
            "return_policy": "returns"
        }
        
        category = category_map.get(pattern)
        if category:
            faq = self._find_faq_by_category(category)
            if faq:
                return {
                    "response": faq["answer"],
                    "type": "keyword_match",
                    "confidence": min(match["score"] / 10, 0.95),
                    "category": category,
                    "method": "keyword_pattern",
                    "matched_keywords": match["matched_keywords"]
                }
        
        return None
    
    def _generate_action_response(self, match: Dict, message: str) -> Dict:
        """Generate response that requires additional action"""
        if match["pattern"] == "order_tracking":
            # Check if order number is present
            order_pattern = r'#?(\d{4,})'
            order_match = re.search(order_pattern, message)
            
            if order_match:
                return {
                    "response": f"Let me track order #{order_match.group(1)} for you! 📦",
                    "type": "order_tracking",
                    "confidence": 0.9,
                    "action": "track_order",
                    "order_number": order_match.group(1)
                }
            else:
                return {
                    "response": "I'd be happy to help track your order! Could you please provide your order number? It usually starts with # followed by 4 or more digits. 📦",
                    "type": "keyword_match",
                    "confidence": 0.8,
                    "category": "orders",
                    "action_required": "order_number"
                }
        
        return None
    
    def _generate_escalation_response(self, match: Dict) -> Dict:
        """Generate escalation response"""
        return {
            "response": "I understand you're having a technical issue. Let me connect you with our technical support team who can provide specialized assistance! 🔧",
            "type": "escalation",
            "confidence": 0.7,
            "escalate": True,
            "reason": "technical_support"
        }
    
    def _generate_greeting_response(self) -> Dict:
        """Generate greeting response"""
        greetings = [
            "Hello! 👋 Welcome to TechyMart! I'm here to help with any questions about orders, returns, warranties, or anything else!",
            "Hi there! 🌟 Great to see you at TechyMart! How can I assist you today?",
            "Hey! 🤖 TechBot Pro here, ready to help with all your TechyMart needs!"
        ]
        
        import random
        return {
            "response": random.choice(greetings),
            "type": "greeting",
            "confidence": 0.95
        }
    
    def add_custom_keyword(self, keyword: str, category: str, response: str, priority: int = 5):
        """
        Add custom keyword response dynamically
        """
        pattern_name = f"custom_{keyword.replace(' ', '_')}"
        self.keyword_patterns[pattern_name] = {
            "keywords": [keyword],
            "priority": priority,
            "response_type": "direct_answer"
        }
        
        # Add to exact phrases for precise matching
        self.exact_phrases[keyword] = {
            "category": category,
            "confidence": 0.9,
            "response": response
        }
    
    def get_keyword_statistics(self) -> Dict:
        """Get statistics about keyword patterns"""
        stats = {
            "total_patterns": len(self.keyword_patterns),
            "total_exact_phrases": len(self.exact_phrases),
            "categories": set(),
            "total_keywords": 0
        }
        
        for pattern_data in self.keyword_patterns.values():
            stats["total_keywords"] += len(pattern_data["keywords"])
        
        for faq in self.faq_data:
            stats["categories"].add(faq["category"])
        
        stats["categories"] = list(stats["categories"])
        return stats

# Global keyword matcher instance
keyword_matcher = KeywordMatcher()
