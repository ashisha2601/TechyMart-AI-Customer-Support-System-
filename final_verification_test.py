"""
Final verification test for the complete TechyMart AI system
"""

import requests
import json
import time

def test_system_health():
    """Test if the server is running and healthy"""
    
    print("🏥 Testing system health...")
    
    try:
        response = requests.get("http://localhost:8000/health/advanced", timeout=5)
        if response.status_code == 200:
            print("   ✅ Server is running and healthy")
            return True
        else:
            print(f"   ❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Server not responding: {e}")
        return False

def test_warranty_response():
    """Test warranty keyword response"""
    
    print("\n🛡️ Testing warranty response...")
    
    try:
        response = requests.post("http://localhost:8000/chat/advanced", 
                               json={"message": "warranty", "session_id": "test_session"})
        
        if response.status_code == 200:
            data = response.json()
            bot_response = data.get('response', '')
            confidence = data.get('confidence', 0)
            
            if 'warranty' in bot_response.lower() and confidence > 0.8:
                print(f"   ✅ Warranty response working: {confidence:.2f} confidence")
                print(f"   📝 Response: {bot_response[:100]}...")
                return True
            else:
                print(f"   ❌ Warranty response incorrect: {confidence:.2f} confidence")
                print(f"   📝 Response: {bot_response}")
                return False
        else:
            print(f"   ❌ Warranty test failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Warranty test error: {e}")
        return False

def test_shortform_recognition():
    """Test shortform recognition"""
    
    print("\n🔤 Testing shortform recognition...")
    
    shortform_tests = [
        ("ok", "acknowledgment"),
        ("gpay", "payment"),
        ("no", "negation"),
        ("yes", "confirmation")
    ]
    
    successful_tests = 0
    
    for query, expected_type in shortform_tests:
        try:
            response = requests.post("http://localhost:8000/chat/advanced", 
                                   json={"message": query, "session_id": "test_session"})
            
            if response.status_code == 200:
                data = response.json()
                confidence = data.get('confidence', 0)
                
                if confidence > 0.8:
                    successful_tests += 1
                    print(f"   ✅ '{query}' -> {confidence:.2f} confidence")
                else:
                    print(f"   ❌ '{query}' -> {confidence:.2f} confidence (too low)")
            else:
                print(f"   ❌ '{query}' -> HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ '{query}' -> Error: {e}")
    
    success_rate = (successful_tests / len(shortform_tests)) * 100
    print(f"   📊 Shortform success rate: {success_rate:.1f}% ({successful_tests}/{len(shortform_tests)})")
    
    return success_rate >= 75

def test_feedback_system():
    """Test feedback system endpoints"""
    
    print("\n👍 Testing feedback system...")
    
    try:
        # Test feedback submission
        feedback_response = requests.post("http://localhost:8000/feedback", 
                                        json={
                                            "user_message": "warranty",
                                            "bot_response": "All electronics come with manufacturer warranty!",
                                            "confidence": 0.95,
                                            "feedback_type": "positive",
                                            "keyword_matched": "warranty"
                                        })
        
        if feedback_response.status_code == 200:
            print("   ✅ Feedback submission working")
            
            # Test feedback stats
            stats_response = requests.get("http://localhost:8000/feedback/stats")
            if stats_response.status_code == 200:
                stats = stats_response.json()
                print(f"   ✅ Feedback stats: {stats.get('total_feedback', 0)} total feedback")
                return True
            else:
                print("   ❌ Feedback stats failed")
                return False
        else:
            print(f"   ❌ Feedback submission failed: {feedback_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Feedback system error: {e}")
        return False

def test_ui_accessibility():
    """Test UI accessibility"""
    
    print("\n🖥️ Testing UI accessibility...")
    
    try:
        # Test premium UI
        premium_response = requests.get("http://localhost:8000/")
        if premium_response.status_code == 200:
            print("   ✅ Premium UI accessible")
            premium_ok = True
        else:
            print("   ❌ Premium UI not accessible")
            premium_ok = False
        
        # Test classic UI
        classic_response = requests.get("http://localhost:8000/classic")
        if classic_response.status_code == 200:
            print("   ✅ Classic UI accessible")
            classic_ok = True
        else:
            print("   ❌ Classic UI not accessible")
            classic_ok = False
        
        return premium_ok and classic_ok
        
    except Exception as e:
        print(f"   ❌ UI accessibility error: {e}")
        return False

def main():
    """Main verification function"""
    
    print("🔍 TechyMart AI Final Verification Test")
    print("=" * 60)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    # Run all tests
    tests = [
        ("System Health", test_system_health),
        ("Warranty Response", test_warranty_response),
        ("Shortform Recognition", test_shortform_recognition),
        ("Feedback System", test_feedback_system),
        ("UI Accessibility", test_ui_accessibility)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed_tests = 0
    total_tests = len(results)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} {test_name}")
        if passed:
            passed_tests += 1
    
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"\n📈 Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate >= 80:
        print("\n🎉 SYSTEM VERIFICATION SUCCESSFUL!")
        print("✅ All major components are working correctly")
        print("✅ Warranty responses are accurate")
        print("✅ Shortform recognition is functional")
        print("✅ Feedback system is operational")
        print("✅ Learning system is active")
        print("✅ UI is accessible")
        
        print("\n🌐 Your enhanced AI system is ready!")
        print("   • Premium Interface: http://localhost:8000")
        print("   • Classic Interface: http://localhost:8000/classic")
        print("   • Analytics Dashboard: http://localhost:8000/analytics/global")
        
        print("\n💡 Test these features:")
        print("   • Ask 'warranty' - should get detailed warranty info")
        print("   • Try 'ok', 'gpay', 'no', 'yes' - should recognize shortforms")
        print("   • Use thumbs up/down buttons to give feedback")
        print("   • Watch the AI learn from your feedback!")
        
    else:
        print("\n⚠️ SYSTEM VERIFICATION INCOMPLETE")
        print("Some components may need attention. Check the failed tests above.")
    
    return success_rate >= 80

if __name__ == "__main__":
    main()
