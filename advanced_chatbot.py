"""
Advanced TechyMart Customer Support AI Agent
Enhanced with context awareness, personality adaptation, and intelligent routing
"""

import random
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from advanced_rag import advanced_rag
from order_tracker import order_tracker

class AdvancedTechyMartBot:
    def __init__(self):
        self.name = "TechBot Pro"
        self.version = "2.0"
        self.escalation_threshold = 0.7  # Higher threshold for better quality
        self.conversation_sessions = {}
        
        # Enhanced personality system
        self.personality_modes = {
            'professional': {
                'greetings': [
                    "Good day! I'm TechBot Pro, your advanced AI assistant at TechyMart. How may I assist you today?",
                    "Welcome to TechyMart! I'm your dedicated AI support specialist. What can I help you with?",
                    "Hello! TechBot Pro here, ready to provide you with expert assistance. How can I help?"
                ],
                'escalation': [
                    "I'll connect you with our specialized human expert who can provide detailed assistance.",
                    "Let me transfer you to our senior support specialist for personalized help.",
                    "I'm routing this to our expert team who can give you the comprehensive support you deserve."
                ]
            },
            'friendly': {
                'greetings': [
                    "Hey there! 👋 Welcome to TechyMart! I'm TechBot Pro, your super-smart AI buddy. What's up?",
                    "Hi! 🤖 TechBot Pro at your service! Ready to help you with anything tech-related (and beyond)!",
                    "Hello and welcome! 🌟 I'm your upgraded AI assistant - think of me as your tech-savvy best friend!"
                ],
                'escalation': [
                    "You know what? This deserves the VIP treatment! 🌟 Let me get our human experts involved!",
                    "I want to make sure you get perfect help! Bringing in our specialist team! 🚀",
                    "Time for the A-team! 💪 Our human experts will take amazing care of you!"
                ]
            }
        }
        
        self.current_personality = 'friendly'  # Default personality
        
        # Advanced response templates
        self.response_enhancers = {
            'confidence_boosters': [
                "I'm confident this will help: ",
                "Here's exactly what you need to know: ",
                "Perfect question! Let me give you the complete answer: "
            ],
            'empathy_phrases': [
                "I understand that can be frustrating. ",
                "I totally get why you'd want to know about this. ",
                "That's a really important question. "
            ],
            'follow_ups': [
                "\n\nIs there anything specific about this you'd like me to explain further?",
                "\n\nWould you like me to help you with the next steps?",
                "\n\nAny other questions about this topic?"
            ]
        }
    
    def initialize_session(self, session_id: str) -> Dict:
        """Initialize a new conversation session with user profiling"""
        if session_id not in self.conversation_sessions:
            self.conversation_sessions[session_id] = {
                'created_at': datetime.now().isoformat(),
                'message_count': 0,
                'topics_discussed': [],
                'user_satisfaction': None,
                'preferred_personality': 'friendly',
                'escalation_count': 0,
                'successful_resolutions': 0
            }
        return self.conversation_sessions[session_id]
    
    def detect_user_intent(self, message: str) -> Dict[str, any]:
        """Advanced intent detection with confidence scoring"""
        message_lower = message.lower()
        
        # Intent patterns with confidence scores
        intents = {
            'greeting': {
                'patterns': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'start'],
                'confidence': 0.0
            },
            'order_inquiry': {
                'patterns': ['order', 'package', 'delivery', 'shipped', 'tracking', 'where is', 'status'],
                'confidence': 0.0
            },
            'complaint': {
                'patterns': ['problem', 'issue', 'broken', 'not working', 'disappointed', 'angry'],
                'confidence': 0.0
            },
            'compliment': {
                'patterns': ['thank', 'thanks', 'great', 'awesome', 'helpful', 'amazing'],
                'confidence': 0.0
            },
            'technical_support': {
                'patterns': ['install', 'setup', 'configure', 'troubleshoot', 'error', 'bug'],
                'confidence': 0.0
            }
        }
        
        # Calculate confidence for each intent
        words = message_lower.split()
        for intent_name, intent_data in intents.items():
            matches = sum(1 for pattern in intent_data['patterns'] if pattern in message_lower)
            intents[intent_name]['confidence'] = matches / len(words) if words else 0
        
        # Find best intent
        best_intent = max(intents.items(), key=lambda x: x[1]['confidence'])
        
        return {
            'intent': best_intent[0],
            'confidence': best_intent[1]['confidence'],
            'all_intents': intents
        }
    
    def adapt_personality(self, session_data: Dict, intent_data: Dict):
        """Dynamically adapt personality based on user interaction"""
        # Switch to professional mode for complaints or technical issues
        if intent_data['intent'] in ['complaint', 'technical_support']:
            self.current_personality = 'professional'
        # Use friendly mode for general inquiries
        elif intent_data['intent'] in ['greeting', 'compliment']:
            self.current_personality = 'friendly'
    
    def generate_enhanced_response(self, user_message: str, session_id: str = "default") -> Dict[str, any]:
        """
        Advanced response generation with context awareness and personality adaptation
        """
        # Initialize session
        session_data = self.initialize_session(session_id)
        session_data['message_count'] += 1
        
        # Detect user intent
        intent_data = self.detect_user_intent(user_message)
        
        # Adapt personality
        self.adapt_personality(session_data, intent_data)
        
        # Handle different intents
        if intent_data['intent'] == 'greeting' and len(user_message.split()) <= 3:
            return self._handle_greeting(session_data)
        
        if intent_data['intent'] == 'compliment':
            return self._handle_compliment(session_data)
        
        # Check for order inquiries first (agentic action)
        if intent_data['intent'] == 'order_inquiry' or 'order' in user_message.lower():
            order_response = order_tracker.handle_order_inquiry(user_message)
            if order_response:
                session_data['successful_resolutions'] += 1
                return {
                    'response': self._enhance_response(order_response, 'order_tracking'),
                    'type': 'order_tracking',
                    'escalate': False,
                    'confidence': 0.95,
                    'suggestions': ["Can I help with anything else about your order?", "Would you like to track another order?"],
                    'intent': intent_data
                }
        
        # Try advanced RAG system
        best_faq, confidence, all_matches = advanced_rag.find_best_answer(user_message)
        
        if best_faq and confidence >= self.escalation_threshold:
            # Enhance the FAQ response
            enhanced_answer = self._enhance_faq_response(best_faq, confidence, session_data)
            session_data['successful_resolutions'] += 1
            session_data['topics_discussed'].append(best_faq['category'])
            
            return {
                'response': enhanced_answer,
                'type': 'faq_answer',
                'category': best_faq['category'],
                'confidence': confidence,
                'escalate': False,
                'suggestions': advanced_rag.get_smart_suggestions(user_message),
                'intent': intent_data,
                'alternative_matches': [match['question'] for match in all_matches[1:3]]
            }
        
        # Escalate with enhanced context
        session_data['escalation_count'] += 1
        escalation_response = self._generate_smart_escalation(user_message, confidence, session_data, intent_data)
        
        return {
            'response': escalation_response,
            'type': 'escalation',
            'escalate': True,
            'confidence': confidence,
            'suggestions': ["Can I help with something else while you wait?"],
            'intent': intent_data
        }
    
    def _handle_greeting(self, session_data: Dict) -> Dict[str, any]:
        """Handle greeting with personality-aware response"""
        personality = self.personality_modes[self.current_personality]
        greeting = random.choice(personality['greetings'])
        
        # Add session context for returning users
        if session_data['message_count'] > 1:
            greeting += " Welcome back! How else can I help you today?"
        
        return {
            'response': greeting,
            'type': 'greeting',
            'escalate': False,
            'suggestions': advanced_rag.get_smart_suggestions("help"),
            'intent': {'intent': 'greeting', 'confidence': 1.0}
        }
    
    def _handle_compliment(self, session_data: Dict) -> Dict[str, any]:
        """Handle compliments with personality-aware gratitude"""
        if self.current_personality == 'professional':
            responses = [
                "Thank you for your kind words. I'm here to provide excellent service. How else may I assist you?",
                "I appreciate your feedback. Is there anything else I can help you with today?",
                "Thank you. I'm committed to providing you with the best possible support. What else can I do for you?"
            ]
        else:
            responses = [
                "Aww, that totally made my circuits happy! 💖 What else can I help you with?",
                "You're the best! 🌟 I'm here whenever you need more TechyMart magic!",
                "That means so much to me! 🤗 Ready to tackle your next question!"
            ]
        
        return {
            'response': random.choice(responses),
            'type': 'gratitude',
            'escalate': False,
            'suggestions': ["Is there anything else I can help with?"],
            'intent': {'intent': 'compliment', 'confidence': 1.0}
        }
    
    def _enhance_faq_response(self, faq: Dict, confidence: float, session_data: Dict) -> str:
        """Enhance FAQ responses with personality and context"""
        base_answer = faq['answer']
        
        # Add confidence booster
        if confidence > 0.9:
            prefix = random.choice(self.response_enhancers['confidence_boosters'])
        else:
            prefix = random.choice(self.response_enhancers['empathy_phrases'])
        
        # Add follow-up
        follow_up = random.choice(self.response_enhancers['follow_ups'])
        
        return f"{prefix}{base_answer}{follow_up}"
    
    def _enhance_response(self, response: str, response_type: str) -> str:
        """Add personality enhancements to any response"""
        if response_type == 'order_tracking':
            if self.current_personality == 'friendly':
                return response  # Order responses already have personality
            else:
                # Make it more professional
                return response.replace('🐦', '').replace('🧝‍♂️✨', '').replace('Great news!', 'Your order status:')
        
        return response
    
    def _generate_smart_escalation(self, user_message: str, confidence: float, session_data: Dict, intent_data: Dict) -> str:
        """Generate intelligent escalation messages based on context"""
        personality = self.personality_modes[self.current_personality]
        base_escalation = random.choice(personality['escalation'])
        
        # Add context-specific information
        context_additions = []
        
        if intent_data['intent'] == 'technical_support':
            context_additions.append("Our technical specialists will provide expert troubleshooting assistance.")
        elif intent_data['intent'] == 'complaint':
            context_additions.append("Our customer care team will ensure your concerns are fully addressed.")
        elif 'billing' in user_message.lower():
            context_additions.append("Our billing specialists will resolve this promptly.")
        
        # Add escalation reason
        if confidence < 0.3:
            context_additions.append("Your question requires specialized knowledge that our human experts can provide.")
        else:
            context_additions.append("While I found some relevant information, a human agent can give you more detailed assistance.")
        
        full_response = base_escalation
        if context_additions:
            full_response += "\n\n" + " ".join(context_additions)
        
        return full_response
    
    def get_session_analytics(self, session_id: str) -> Dict:
        """Get analytics for a conversation session"""
        if session_id not in self.conversation_sessions:
            return {"error": "Session not found"}
        
        session = self.conversation_sessions[session_id]
        insights = advanced_rag.get_conversation_insights()
        
        return {
            **session,
            **insights,
            "success_rate": session['successful_resolutions'] / max(session['message_count'], 1),
            "escalation_rate": session['escalation_count'] / max(session['message_count'], 1)
        }

# Global advanced chatbot instance
advanced_bot = AdvancedTechyMartBot()
