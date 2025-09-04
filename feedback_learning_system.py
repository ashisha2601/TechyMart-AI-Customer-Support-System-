"""
Feedback Learning System - AI learns from user feedback to improve keywords
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re

class FeedbackLearningSystem:
    """System that learns from user feedback to improve keyword matching"""
    
    def __init__(self, feedback_file: str = "feedback_data.json"):
        self.feedback_file = feedback_file
        self.feedback_data = self.load_feedback_data()
        self.learning_threshold = 3  # Minimum feedback count to trigger learning
        
    def load_feedback_data(self) -> Dict:
        """Load existing feedback data"""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r') as f:
                    return json.load(f)
            except:
                return {"feedback_history": [], "learned_keywords": {}, "statistics": {}}
        return {"feedback_history": [], "learned_keywords": {}, "statistics": {}}
    
    def save_feedback_data(self):
        """Save feedback data to file"""
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
    
    def record_feedback(self, user_message: str, bot_response: str, 
                       confidence: float, feedback_type: str, keyword_matched: str):
        """Record user feedback for learning"""
        
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message.lower().strip(),
            "bot_response": bot_response,
            "confidence": confidence,
            "feedback_type": feedback_type,  # 'positive' or 'negative'
            "keyword_matched": keyword_matched,
            "message_length": len(user_message),
            "has_emoji": bool(re.search(r'[^\w\s]', user_message))
        }
        
        self.feedback_data["feedback_history"].append(feedback_entry)
        
        # Update statistics
        if "statistics" not in self.feedback_data:
            self.feedback_data["statistics"] = {
                "total_feedback": 0,
                "positive_feedback": 0,
                "negative_feedback": 0,
                "average_confidence": 0.0
            }
        
        stats = self.feedback_data["statistics"]
        stats["total_feedback"] = stats.get("total_feedback", 0) + 1
        
        if feedback_type == "positive":
            stats["positive_feedback"] = stats.get("positive_feedback", 0) + 1
        else:
            stats["negative_feedback"] = stats.get("negative_feedback", 0) + 1
        
        # Update average confidence
        total_conf = sum(entry["confidence"] for entry in self.feedback_data["feedback_history"])
        stats["average_confidence"] = total_conf / len(self.feedback_data["feedback_history"])
        
        self.save_feedback_data()
        
        # Trigger learning if we have enough data
        self.analyze_and_learn()
        
        print(f"📊 Feedback recorded: {feedback_type} for '{user_message[:30]}...'")
    
    def analyze_and_learn(self):
        """Analyze feedback patterns and learn new keywords"""
        
        print("🧠 Analyzing feedback patterns for learning...")
        
        # Group feedback by user message
        message_feedback = {}
        for entry in self.feedback_data["feedback_history"]:
            msg = entry["user_message"]
            if msg not in message_feedback:
                message_feedback[msg] = []
            message_feedback[msg].append(entry)
        
        # Find patterns for learning
        learned_keywords = {}
        
        for message, feedbacks in message_feedback.items():
            if len(feedbacks) >= self.learning_threshold:
                # Analyze feedback pattern
                positive_count = sum(1 for f in feedbacks if f["feedback_type"] == "positive")
                negative_count = sum(1 for f in feedbacks if f["feedback_type"] == "negative")
                total_count = len(feedbacks)
                
                # If mostly positive feedback, this is a good keyword
                if positive_count > negative_count and positive_count >= 2:
                    avg_confidence = sum(f["confidence"] for f in feedbacks) / total_count
                    
                    # Generate response based on successful responses
                    successful_responses = [f["bot_response"] for f in feedbacks if f["feedback_type"] == "positive"]
                    if successful_responses:
                        # Use the most common successful response
                        response_counts = {}
                        for resp in successful_responses:
                            response_counts[resp] = response_counts.get(resp, 0) + 1
                        best_response = max(response_counts, key=response_counts.get)
                        
                        learned_keywords[message] = {
                            "category": "learned",
                            "confidence": min(0.95, avg_confidence + 0.1),  # Boost confidence slightly
                            "response": best_response,
                            "feedback_count": total_count,
                            "positive_ratio": positive_count / total_count,
                            "learned_date": datetime.now().isoformat()
                        }
                        
                        print(f"✅ Learned new keyword: '{message}' (confidence: {learned_keywords[message]['confidence']:.2f})")
                
                # If mostly negative feedback, this needs improvement
                elif negative_count > positive_count and negative_count >= 2:
                    print(f"⚠️ Keyword needs improvement: '{message}' ({negative_count}/{total_count} negative)")
                    self.suggest_keyword_improvements(message, feedbacks)
        
        # Update learned keywords
        if "learned_keywords" not in self.feedback_data:
            self.feedback_data["learned_keywords"] = {}
        
        self.feedback_data["learned_keywords"].update(learned_keywords)
        self.save_feedback_data()
        
        # Apply learned keywords to keyword matcher
        if learned_keywords:
            self.apply_learned_keywords(learned_keywords)
    
    def suggest_keyword_improvements(self, message: str, feedbacks: List[Dict]):
        """Suggest improvements for poorly performing keywords"""
        
        print(f"🔧 Analyzing improvements for: '{message}'")
        
        # Find common patterns in negative feedback
        negative_feedbacks = [f for f in feedbacks if f["feedback_type"] == "negative"]
        
        if negative_feedbacks:
            # Check if responses are too generic
            responses = [f["bot_response"] for f in negative_feedbacks]
            if len(set(responses)) == 1:  # All same response
                print(f"   💡 Suggestion: Response too generic for '{message}'")
            
            # Check confidence levels
            avg_confidence = sum(f["confidence"] for f in negative_feedbacks) / len(negative_feedbacks)
            if avg_confidence < 0.5:
                print(f"   💡 Suggestion: Low confidence ({avg_confidence:.2f}) for '{message}'")
            
            # Check if keyword matching is wrong
            keywords_matched = [f["keyword_matched"] for f in negative_feedbacks]
            if len(set(keywords_matched)) > 1:
                print(f"   💡 Suggestion: Inconsistent keyword matching for '{message}'")
    
    def apply_learned_keywords(self, learned_keywords: Dict):
        """Apply learned keywords to the keyword matcher"""
        
        print("🔄 Applying learned keywords to keyword matcher...")
        
        # Read current keyword matcher
        with open('keyword_matcher.py', 'r') as f:
            content = f.read()
        
        # Extract current exact_phrases
        pattern = r'self\.exact_phrases = \{.*?\n        \}'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # Parse existing phrases
            existing_phrases_str = match.group(0)
            
            # Add learned keywords
            for keyword, data in learned_keywords.items():
                response = data['response'].replace('"', '\\"').replace('\n', '\\n')
                new_phrase = f'            "{keyword}": {{\n'
                new_phrase += f'                "category": "{data["category"]}",\n'
                new_phrase += f'                "confidence": {data["confidence"]},\n'
                new_phrase += f'                "response": "{response}"\n'
                new_phrase += f'            }},\n'
                
                # Insert before the closing brace
                existing_phrases_str = existing_phrases_str.replace('        }', new_phrase + '        }')
            
            # Replace in content
            new_content = content.replace(match.group(0), existing_phrases_str)
            
            # Write updated file
            with open('keyword_matcher.py', 'w') as f:
                f.write(new_content)
            
            print(f"✅ Applied {len(learned_keywords)} learned keywords to keyword matcher!")
    
    def get_learning_statistics(self) -> Dict:
        """Get learning system statistics"""
        
        stats = self.feedback_data.get("statistics", {})
        learned_count = len(self.feedback_data.get("learned_keywords", {}))
        
        return {
            "total_feedback": stats.get("total_feedback", 0),
            "positive_feedback": stats.get("positive_feedback", 0),
            "negative_feedback": stats.get("negative_feedback", 0),
            "satisfaction_rate": (stats.get("positive_feedback", 0) / max(1, stats.get("total_feedback", 1))) * 100,
            "learned_keywords": learned_count,
            "average_confidence": stats.get("average_confidence", 0.0),
            "learning_threshold": self.learning_threshold
        }
    
    def export_learning_report(self) -> str:
        """Export a detailed learning report"""
        
        stats = self.get_learning_statistics()
        learned_keywords = self.feedback_data.get("learned_keywords", {})
        
        report = f"""
🧠 TechyMart AI Learning System Report
=====================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 Overall Statistics:
   • Total Feedback: {stats['total_feedback']}
   • Positive Feedback: {stats['positive_feedback']}
   • Negative Feedback: {stats['negative_feedback']}
   • Satisfaction Rate: {stats['satisfaction_rate']:.1f}%
   • Average Confidence: {stats['average_confidence']:.2f}
   • Learned Keywords: {stats['learned_keywords']}

🎯 Learned Keywords:
"""
        
        for keyword, data in learned_keywords.items():
            report += f"   • '{keyword}': {data['confidence']:.2f} confidence ({data['feedback_count']} feedback)\n"
        
        report += f"""
🔧 Learning Configuration:
   • Learning Threshold: {self.learning_threshold} feedbacks
   • Auto-apply Keywords: Yes
   • Continuous Learning: Active

💡 Recent Learning Activity:
"""
        
        # Show recent feedback
        recent_feedback = self.feedback_data.get("feedback_history", [])[-5:]
        for entry in recent_feedback:
            report += f"   • {entry['timestamp'][:19]}: {entry['feedback_type']} for '{entry['user_message'][:30]}...'\n"
        
        return report

def create_enhanced_feedback_endpoint():
    """Create enhanced feedback endpoint with learning capabilities"""
    
    print("🔄 Creating enhanced feedback endpoint with learning...")
    
    # Read current advanced_main.py
    with open('advanced_main.py', 'r') as f:
        content = f.read()
    
    # Import the learning system
    import_statement = """
from feedback_learning_system import FeedbackLearningSystem
"""
    
    # Add import if not already present
    if "from feedback_learning_system import" not in content:
        content = content.replace("from fastapi import", import_statement + "from fastapi import")
    
    # Initialize learning system
    init_learning = """
# Initialize feedback learning system
feedback_learner = FeedbackLearningSystem()
"""
    
    # Add initialization after imports
    if "feedback_learner" not in content:
        content = content.replace("app = FastAPI(", init_learning + "\napp = FastAPI(")
    
    # Enhanced feedback endpoint
    enhanced_feedback_endpoint = '''
@app.post("/feedback")
async def submit_feedback(request: Request):
    """Handle user feedback for AI responses with learning capabilities"""
    try:
        data = await request.json()
        
        # Record feedback with learning system
        feedback_learner.record_feedback(
            user_message=data.get('user_message', ''),
            bot_response=data.get('bot_response', ''),
            confidence=data.get('confidence', 0.0),
            feedback_type=data.get('feedback_type', ''),
            keyword_matched=data.get('keyword_matched', '')
        )
        
        # Get updated statistics
        stats = feedback_learner.get_learning_statistics()
        
        return JSONResponse(content={
            "status": "success",
            "message": "Feedback recorded and learning system updated",
            "feedback_id": datetime.now().isoformat(),
            "learning_stats": stats
        })
        
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.get("/feedback/stats")
async def get_feedback_stats():
    """Get comprehensive feedback and learning statistics"""
    try:
        stats = feedback_learner.get_learning_statistics()
        return JSONResponse(content=stats)
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.get("/feedback/learning-report")
async def get_learning_report():
    """Get detailed learning system report"""
    try:
        report = feedback_learner.export_learning_report()
        return JSONResponse(content={"report": report})
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.post("/feedback/force-learn")
async def force_learning():
    """Force the learning system to analyze and learn from feedback"""
    try:
        feedback_learner.analyze_and_learn()
        stats = feedback_learner.get_learning_statistics()
        return JSONResponse(content={
            "status": "success",
            "message": "Learning analysis completed",
            "stats": stats
        })
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
'''
    
    # Replace the existing feedback endpoint
    pattern = r'@app\.post\("/feedback"\).*?(?=@app\.|if __name__)'
    new_content = re.sub(pattern, enhanced_feedback_endpoint, content, flags=re.DOTALL)
    
    # Write updated file
    with open('advanced_main.py', 'w') as f:
        f.write(new_content)
    
    print("✅ Enhanced feedback endpoint with learning capabilities created!")

def test_learning_system():
    """Test the learning system with sample feedback"""
    
    print("🧪 Testing feedback learning system...")
    
    # Initialize learning system
    learner = FeedbackLearningSystem()
    
    # Simulate some feedback
    test_feedbacks = [
        ("ok", "Great! Is there anything else I can help you with today? 😊", 0.95, "positive", "ok"),
        ("ok", "Great! Is there anything else I can help you with today? 😊", 0.95, "positive", "ok"),
        ("ok", "Great! Is there anything else I can help you with today? 😊", 0.95, "positive", "ok"),
        ("gpay", "Yes! Google Pay is fully supported! 🤖", 0.95, "positive", "gpay"),
        ("gpay", "Yes! Google Pay is fully supported! 🤖", 0.95, "positive", "gpay"),
        ("gpay", "Yes! Google Pay is fully supported! 🤖", 0.95, "positive", "gpay"),
        ("bad keyword", "I'm not sure what you mean", 0.3, "negative", "bad keyword"),
        ("bad keyword", "I'm not sure what you mean", 0.3, "negative", "bad keyword"),
        ("bad keyword", "I'm not sure what you mean", 0.3, "negative", "bad keyword"),
    ]
    
    print("📝 Recording test feedback...")
    for user_msg, bot_resp, conf, feedback_type, keyword in test_feedbacks:
        learner.record_feedback(user_msg, bot_resp, conf, feedback_type, keyword)
    
    # Get statistics
    stats = learner.get_learning_statistics()
    print(f"\n📊 Learning Statistics:")
    print(f"   • Total Feedback: {stats['total_feedback']}")
    print(f"   • Positive: {stats['positive_feedback']}")
    print(f"   • Negative: {stats['negative_feedback']}")
    print(f"   • Satisfaction Rate: {stats['satisfaction_rate']:.1f}%")
    print(f"   • Learned Keywords: {stats['learned_keywords']}")
    
    # Export report
    report = learner.export_learning_report()
    print(f"\n📋 Learning Report:")
    print(report)
    
    return learner

def main():
    """Main function to implement feedback learning system"""
    
    print("🧠 TechyMart AI Feedback Learning System")
    print("=" * 50)
    
    # Create enhanced feedback endpoint
    create_enhanced_feedback_endpoint()
    
    # Test the learning system
    learner = test_learning_system()
    
    print("\n" + "=" * 50)
    print("🎉 FEEDBACK LEARNING SYSTEM IMPLEMENTED!")
    print("✅ AI now learns from user feedback")
    print("✅ Automatic keyword improvement")
    print("✅ Continuous learning and adaptation")
    print("✅ Feedback analytics and reporting")
    print("✅ Smart keyword suggestions")
    
    print("\n🎯 Learning Features:")
    print("   • Records all user feedback (thumbs up/down)")
    print("   • Analyzes feedback patterns automatically")
    print("   • Learns new keywords from positive feedback")
    print("   • Identifies problematic keywords from negative feedback")
    print("   • Auto-applies learned keywords to the system")
    print("   • Provides detailed learning reports")
    print("   • Continuous improvement based on user behavior")
    
    print("\n📊 New API Endpoints:")
    print("   • POST /feedback - Enhanced feedback with learning")
    print("   • GET /feedback/stats - Learning statistics")
    print("   • GET /feedback/learning-report - Detailed report")
    print("   • POST /feedback/force-learn - Force learning analysis")
    
    print("\n🔄 Restart your server to activate the learning system!")
    print("   python advanced_main.py")

if __name__ == "__main__":
    main()
