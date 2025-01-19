from fastapi import Header, HTTPException

def authenticate_request(token: str = Header(...)):
    if token != "your_static_token":
        raise HTTPException(status_code=401, detail="Unauthorized")
