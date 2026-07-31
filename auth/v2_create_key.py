from fastapi import Security,HTTPException
import sqlite3
from fastapi.security import APIKeyHeader
import hashlib
import secrets

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def Create_API_key_AuthV2(new_key_permissions: str, req_permission: str = "a", security: str = Security(api_key_header)):
    try:
        # If youre a good osu player you can see 727 in this secret
        new_key = secrets.token_hex(32)
        conn = sqlite3.connect('/app/data/api_keys.db')
        cursor = conn.cursor()
        hashed_key = hashlib.sha256(new_key.encode("utf-8")).hexdigest()
        cursor.execute("INSERT INTO api_keys (api_key, permissions) VALUES (?, ?)", (hashed_key, new_key_permissions))
        conn.commit()
        cursor.execute("SELECT uid FROM api_keys WHERE api_key = ?", (hashed_key,))
        uid = cursor.fetchone()[0]
        conn.close()
        del hashed_key
        return {
            "status": "200",
            "message": "New API Key created successfully",
            "api_key": f"{uid}.{new_key}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
