from fastapi import Header, HTTPException
from . import db

def require_key(authorization: str | None = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing API key")
    key = authorization.split(" ", 1)[1].strip()
    row = db.verify_key(key)
    if not row:
        raise HTTPException(403, "Invalid API key")
    return key
