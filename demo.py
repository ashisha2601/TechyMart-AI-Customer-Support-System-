"""
Interactive demo of the TechyMart Customer Support AI Agent
Run this for a command-line chat experience
"""

from chatbot import techymart_bot
import sys

def main():
    print("🤖 Welcome to TechyMart Customer Support!")
    print("=" * 45)
    print(techymart_bot.get_conversation_starter())
    print("\n💡 Try these example queries:")
    print("   • 'Where's my order #1234?'")
    print("   • 'What's your return policy?'") 
    print("   • 'Do you offer warranties?'")
    print("   • 'I need help with quantum physics'")
    print("\nType 'quit' to exit")
    print("=" * 45)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🤖 TechBot: Thanks for chatting! Have a great day! 👋")
                break
            
            if not user_input:
                continue
                
            # Get bot response
            response = techymart_bot.generate_response(user_input)
            
            print(f"\n🤖 TechBot: {response['response']}")
            
            # Show escalation notice
            if response.get('escalate'):
                print("\n🚨 [SYSTEM] This query has been escalated to a human agent")
            
            # Show confidence for debugging
            if 'confidence' in response:
                print(f"   [Debug: confidence={response['confidence']:.3f}, type={response['type']}]")
                
        except KeyboardInterrupt:
            print("\n\n🤖 TechBot: Goodbye! 👋")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Let me try to help you anyway! 🤔")

if __name__ == "__main__":
    main()
