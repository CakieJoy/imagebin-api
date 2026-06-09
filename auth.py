import hashlib
import secrets
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import app_config


RAW_API_KEY = app_config.RAW_API_KEY
HASHED_API_KEY = hashlib.sha256(RAW_API_KEY.encode()).hexdigest()

del RAW_API_KEY
del app_config.RAW_API_KEY


API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def API_key_check(entry_key: str = Security(api_key_header)):
    HASHED_ENTRY_KEY = hashlib.sha256(entry_key.encode()).hexdigest()
    del entry_key
    if not secrets.compare_digest(HASHED_ENTRY_KEY, HASHED_API_KEY):
        raise HTTPException(status_code=403, detail="API Key is invalid")
    return {
        "status": "200",
        "message": "API Key is valid"
    }