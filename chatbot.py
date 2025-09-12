"""
TechyMart Customer Support AI Agent
Main chatbot logic with personality and conversation flow
"""

import random
from typing import Dict, List, Optional
from rag_system import rag_system
from order_tracker import order_tracker
from keyword_matcher import keyword_matcher

class TechyMartBot:
    def __init__(self):
        self.name = "TechBot"
        self.escalation_threshold = 0.15  # Lower threshold for better FAQ matching
        self.conversation_context = []
        self.user_declined_help = False  # Track if user declined help
        
        # Friendly greetings and responses
        self.greetings = [
            "Hey there! 👋 Welcome to TechyMart! I'm TechBot, your friendly digital assistant. How can I help you today?",
            "Hi! 🤖 I'm TechBot from TechyMart support. Ready to help you with anything tech-related (and some non-tech stuff too)!",
            "Hello and welcome! 🌟 TechBot here - think of me as your personal shopping sidekick. What's on your mind?",
            "Hey! 🎉 TechBot at your service! Whether it's about orders, returns, or just chatting about cool gadgets, I'm here for you!"
        ]
        
        self.escalation_messages = [
            "I'm still learning 🤖, so let me connect you with one of our amazing human agents who can help you better!",
            "This one's got me scratching my digital head! 🤔 I'll escalate this to a human expert right away.",
            "You know what? You deserve the VIP treatment! 🌟 Let me get a human agent to give you personalized help.",
            "I want to make sure you get the perfect answer! Let me bring in a human colleague who specializes in this area. 👨‍💻👩‍💻"
        ]
        
        self.thinking_responses = [
            "Let me check that for you... 🔍",
            "Searching my knowledge base... 🧠",
            "Consulting the TechyMart wisdom archives... 📚",
            "Let me dig into that... ⚡"
        ]
    
    def detect_greeting(self, message: str) -> bool:
        """Detect if message is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'start', 'help']
        return any(greeting in message.lower() for greeting in greetings)
    
    def detect_gratitude(self, message: str) -> bool:
        """Detect if message expresses gratitude"""
        thanks = ['thank', 'thanks', 'appreciate', 'helpful', 'great', 'awesome', 'perfect']
        return any(thank in message.lower() for thank in thanks)
    
    def detect_decline(self, message: str) -> bool:
        """Detect if user is declining help or saying no"""
        decline_words = ['no', 'nope', 'not now', 'later', 'no thanks', 'no thank you', 'i\'m good', 'i\'m fine', 'all set', 'nothing', 'none']
        return any(decline in message.lower().strip() for decline in decline_words)
    
    def detect_order_inquiry(self, message: str) -> bool:
        """Detect if message is asking about an order"""
        order_keywords = ['order', 'package', 'delivery', 'shipped', 'tracking', 'where is', 'when will']
        return any(keyword in message.lower() for keyword in order_keywords)
    
    def generate_response(self, user_message: str) -> Dict[str, any]:
        """
        Main response generation logic
        Returns dict with response text and metadata
        """
        user_message = user_message.strip()
        
        # Handle greetings
        if self.detect_greeting(user_message) and len(user_message.split()) <= 3:
            return {
                'response': random.choice(self.greetings),
                'type': 'greeting',
                'escalate': False
            }
        
        # Handle gratitude
        if self.detect_gratitude(user_message):
            if self.user_declined_help:
                gratitude_responses = [
                    "You're so welcome! 😊",
                    "Aww, that made my circuits happy! 💖",
                    "That's what I'm here for! 🤗",
                    "Glad I could help! 🌟"
                ]
            else:
                gratitude_responses = [
                    "You're so welcome! 😊 Happy to help! Anything else I can do for you?",
                    "Aww, that made my circuits happy! 💖 Is there anything else you'd like to know?",
                    "That's what I'm here for! 🤗 Feel free to ask me anything else about TechyMart!",
                    "Glad I could help! 🌟 I'm always here if you need more assistance!"
                ]
            return {
                'response': random.choice(gratitude_responses),
                'type': 'gratitude',
                'escalate': False
            }
        
        # Handle decline/no responses
        if self.detect_decline(user_message):
            self.user_declined_help = True
            decline_responses = [
                "No problem at all! 😊 I'll be here whenever you need me.",
                "Got it! 👍 I'm here if you change your mind.",
                "All good! 😌 Feel free to reach out anytime.",
                "Understood! 🤝 I'll be around when you need help."
            ]
            return {
                'response': random.choice(decline_responses),
                'type': 'acknowledgment',
                'escalate': False,
                'confidence': 0.9
            }
        
        # Reset decline flag if user asks for something new (not just "no")
        if not self.detect_decline(user_message) and self.user_declined_help:
            self.user_declined_help = False
        
        # Step 1: Try keyword-based matching first (fastest and most precise)
        keyword_response = keyword_matcher.generate_keyword_response(user_message)
        if keyword_response:
            # Handle special actions
            if keyword_response.get('action') == 'track_order':
                order_response = order_tracker.handle_order_inquiry(user_message)
                if order_response:
                    keyword_response['response'] = order_response
            
            return keyword_response
        
        # Step 2: Check for order inquiries (agentic action)
        if self.detect_order_inquiry(user_message):
            order_response = order_tracker.handle_order_inquiry(user_message)
            if order_response:
                return {
                    'response': order_response,
                    'type': 'order_tracking',
                    'escalate': False
                }
        
        # Step 3: Try RAG system for FAQ matching (semantic understanding)
        best_faq, similarity_score = rag_system.find_best_answer(user_message, self.escalation_threshold)
        
        if best_faq and similarity_score >= self.escalation_threshold:
            # Add some personality to the FAQ answer
            personality_prefixes = [
                "Great question! ",
                "I've got you covered! ",
                "Here's the scoop: ",
                "Let me break this down for you: ",
                "Perfect timing for this question! "
            ]
            
            response = random.choice(personality_prefixes) + best_faq['answer']
            
            # Add helpful follow-up only if user hasn't declined help
            if not self.user_declined_help:
                followups = [
                    "\n\nAnything else I can help clarify? 🤔",
                    "\n\nHope that helps! Let me know if you need more details! 😊",
                    "\n\nDoes this answer your question, or would you like me to elaborate? 💭",
                    "\n\nFeel free to ask if you need more info! I'm full of TechyMart knowledge! 🧠"
                ]
                response += random.choice(followups)
            else:
                # Simple acknowledgment without asking for more
                response += "\n\nHope that helps! 😊"
            
            return {
                'response': response,
                'type': 'faq_answer',
                'category': best_faq['category'],
                'confidence': similarity_score,
                'escalate': False
            }
        
        # Try to provide a helpful response based on keywords before escalating
        helpful_responses = self._get_helpful_fallback_response(user_message)
        if helpful_responses:
            return helpful_responses
        
        # If we can't handle it, escalate politely
        escalation_response = random.choice(self.escalation_messages)
        
        # Add context-specific escalation messages
        if 'technical' in user_message.lower() or 'broken' in user_message.lower():
            escalation_response += "\n\nOur tech specialists are standing by to help troubleshoot! 🔧"
        elif 'billing' in user_message.lower() or 'charge' in user_message.lower():
            escalation_response += "\n\nOur billing experts will sort this out quickly! 💳"
        elif 'complaint' in user_message.lower() or 'problem' in user_message.lower():
            escalation_response += "\n\nOur customer care team will make sure everything gets resolved! 🤝"
        
        return {
            'response': escalation_response,
            'type': 'escalation',
            'escalate': True,
            'confidence': similarity_score
        }
    
    def _get_helpful_fallback_response(self, user_message: str) -> Dict:
        """Provide helpful fallback responses based on common patterns"""
        message_lower = user_message.lower()
        
        # Payment-related queries
        if any(word in message_lower for word in ['payment', 'pay', 'card', 'credit', 'debit', 'upi', 'wallet']):
            return {
                'response': "We accept all major payment methods! 💳 Credit/Debit cards, UPI, digital wallets, PayPal, Apple Pay, Google Pay, and Buy Now Pay Later options. Your payment is secure with 256-bit SSL encryption!",
                'type': 'payment_info',
                'escalate': False,
                'confidence': 0.8
            }
        
        # Shipping-related queries
        if any(word in message_lower for word in ['shipping', 'delivery', 'dispatch', 'when', 'how long']):
            return {
                'response': "We offer multiple shipping options! 🚚 Standard (3-5 days, FREE over $50), Express (1-2 days, $9.99), and Overnight ($19.99). We provide tracking numbers for all orders!",
                'type': 'shipping_info',
                'escalate': False,
                'confidence': 0.8
            }
        
        # Return-related queries
        if any(word in message_lower for word in ['return', 'refund', 'exchange', 'send back']):
            return {
                'response': "We have a hassle-free 30-day return policy! 🔄 Items must be in original condition with tags. Start your return online or contact us for a prepaid return label!",
                'type': 'return_info',
                'escalate': False,
                'confidence': 0.8
            }
        
        # Warranty-related queries
        if any(word in message_lower for word in ['warranty', 'guarantee', 'protection', 'broken', 'defective']):
            return {
                'response': "All electronics come with manufacturer warranty (1-2 years)! 🛡️ We also offer TechyMart Extended Protection: 1 extra year for $19.99, 2 extra years for $34.99. Covers accidents, drops, and liquid damage!",
                'type': 'warranty_info',
                'escalate': False,
                'confidence': 0.8
            }
        
        # Contact/support queries
        if any(word in message_lower for word in ['contact', 'support', 'help', 'phone', 'email', 'call']):
            return {
                'response': "We're here to help 24/7! 🤗 Chat with me, email support@techymart.com, or call 1-800-TECHYMART. For complex issues, our human experts are available Mon-Fri 9AM-6PM EST!",
                'type': 'support_info',
                'escalate': False,
                'confidence': 0.8
            }
        
        # Product-related queries
        if any(word in message_lower for word in ['product', 'item', 'review', 'rating', 'quality', 'specs']):
            return {
                'response': "I'd be happy to help with product information! 🌟 We have detailed specs, verified customer reviews, and ratings for all products. What specific item are you interested in?",
                'type': 'product_info',
                'escalate': False,
                'confidence': 0.7
            }
        
        return None
    
    def get_conversation_starter(self) -> str:
        """Get a conversation starter message"""
        starters = [
            "I can help you with:\n• 📦 Order tracking and delivery info\n• 🔄 Returns and refunds\n• 🛡️ Warranty and protection plans\n• 💳 Payment and account questions\n• 🛒 Product info and reviews\n\nWhat would you like to know?",
            "Popular questions I can answer:\n• \"Where's my order #1234?\"\n• \"What's your return policy?\"\n• \"Do you offer warranties?\"\n• \"What payment methods do you accept?\"\n\nOr ask me anything else! 😊",
            "I'm here to help with all things TechyMart! Whether you need to track an order, understand our policies, or just want to chat about cool tech, I've got you covered! 🚀\n\nWhat's on your mind?"
        ]
        return random.choice(starters)

# Global chatbot instance
techymart_bot = TechyMartBot()
