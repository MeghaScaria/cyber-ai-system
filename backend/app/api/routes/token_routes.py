from fastapi import APIRouter

router = APIRouter()

# Temporary storage (later DB)
user_tokens = {}

@router.post("/save-token")
def save_token(data: dict):
    user_id = data.get("user_id")
    token = data.get("device_token")

    user_tokens[user_id] = token

    print(f"🔥 Saved token for {user_id}: {token}")

    return {"status": "token saved"}