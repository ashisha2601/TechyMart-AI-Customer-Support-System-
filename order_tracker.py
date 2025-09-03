"""
Order Tracking System - Simulated database lookup for order status
"""

import re
from typing import Optional, Dict
from faq_data import ORDER_DATABASE

class OrderTracker:
    def __init__(self):
        self.orders = ORDER_DATABASE
    
    def extract_order_number(self, text: str) -> Optional[str]:
        """
        Extract order number from user text using regex patterns
        Looks for patterns like: #1234, order 1234, order#1234, etc.
        """
        # Common patterns for order numbers
        patterns = [
            r'#(\d{4,})',  # #1234
            r'order\s*#?(\d{4,})',  # order 1234, order#1234
            r'order\s+number\s*#?(\d{4,})',  # order number 1234
            r'tracking\s*#?(\d{4,})',  # tracking 1234
            r'\b(\d{4,})\b'  # standalone 4+ digit number
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1)
        
        return None
    
    def lookup_order(self, order_number: str) -> Optional[Dict]:
        """
        Look up order details in the simulated database
        """
        return self.orders.get(order_number)
    
    def format_order_status(self, order_data: Dict, order_number: str) -> str:
        """
        Format order information into a friendly response
        """
        status = order_data['status']
        items = ', '.join(order_data['items'])
        
        if status == 'shipped':
            response = f"Great news! 📦 Your order #{order_number} has shipped!\n\n"
            response += f"📱 Items: {items}\n"
            response += f"🚚 Status: {order_data['location']}\n"
            response += f"📍 Estimated delivery: {order_data['estimated_delivery']}\n"
            if order_data['tracking']:
                response += f"📋 Tracking: {order_data['tracking']}\n"
            response += "\nI've checked with our delivery pigeons 🐦 and they confirm it's on the way! 🎉"
            
        elif status == 'processing':
            response = f"Your order #{order_number} is being prepared! 🔧\n\n"
            response += f"📱 Items: {items}\n"
            response += f"🏭 Status: {order_data['location']}\n"
            response += f"📅 Estimated shipping: {order_data['estimated_delivery']}\n"
            response += "\nOur warehouse elves are working hard to get it ready! 🧝‍♂️✨"
            
        elif status == 'delivered':
            response = f"Your order #{order_number} was delivered! 📬\n\n"
            response += f"📱 Items: {items}\n"
            response += f"📍 Delivery location: {order_data['location']}\n"
            response += f"📅 {order_data['estimated_delivery']}\n"
            response += "\nHope you're enjoying your new tech goodies! 🎁"
            
        elif status == 'cancelled':
            response = f"Order #{order_number} was cancelled. 😔\n\n"
            response += f"📱 Items: {items}\n"
            response += f"📋 Reason: {order_data['location']}\n"
            response += "\nIf you need help placing a new order, I'm here for you! 💪"
            
        else:
            response = f"I found your order #{order_number}, but something seems unusual. 🤔\n"
            response += "Let me connect you with a human agent who can provide more details!"
        
        return response
    
    def handle_order_inquiry(self, user_message: str) -> Optional[str]:
        """
        Main function to handle order-related inquiries
        Returns formatted response if order found, None otherwise
        """
        order_number = self.extract_order_number(user_message)
        
        if not order_number:
            return None
        
        order_data = self.lookup_order(order_number)
        
        if not order_data:
            return f"Hmm, I couldn't find order #{order_number} in our system. 🔍\n\nThis could mean:\n• The order number might have a typo\n• It might be an older order (we keep recent orders in my quick-access memory)\n• It could be from a different store\n\nLet me connect you with a human agent who can dig deeper! 🕵️‍♂️"
        
        return self.format_order_status(order_data, order_number)

# Global order tracker instance
order_tracker = OrderTracker()
