import asyncio
import httpx
import json

async def test_fraud_detection():
    url = "http://127.0.0.1:8000/api/v1/fraud/analyze-message"
    
    # Example 1: High Suspicion Message
    test_case_1 = {
        "message": "URGENT: Your account at SBI is locked. Click here to verify now: http://secure-sbi.phish.com",
        "user_id": "user_001",
        "metadata": {
            "device_token": "mock_token_123",
            "platform": "android"
        }
    }

    # Example 2: Safe Message
    test_case_2 = {
        "message": "Hey, are we still meeting for lunch at 12:30?",
        "user_id": "user_001",
        "metadata": {
            "device_token": "mock_token_123",
            "platform": "android"
        }
    }

    async with httpx.AsyncClient() as client:
        print("🚀 Testing FRAUDULENT message...")
        response1 = await client.post(url, json=test_case_1)
        print(f"Status: {response1.status_code}")
        print(f"Result: {json.dumps(response1.json(), indent=2)}")
        print("-" * 30)

        print("\n✅ Testing SAFE message...")
        response2 = await client.post(url, json=test_case_2)
        print(f"Status: {response2.status_code}")
        print(f"Result: {json.dumps(response2.json(), indent=2)}")
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(test_fraud_detection())
