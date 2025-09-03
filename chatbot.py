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
        self.escalation_threshold = 0.25  # Similarity threshold for FAQ matching
        self.conversation_context = []
        
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
            
            # Add helpful follow-up
            followups = [
                "\n\nAnything else I can help clarify? 🤔",
                "\n\nHope that helps! Let me know if you need more details! 😊",
                "\n\nDoes this answer your question, or would you like me to elaborate? 💭",
                "\n\nFeel free to ask if you need more info! I'm full of TechyMart knowledge! 🧠"
            ]
            
            response += random.choice(followups)
            
            return {
                'response': response,
                'type': 'faq_answer',
                'category': best_faq['category'],
                'confidence': similarity_score,
                'escalate': False
            }
        
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
