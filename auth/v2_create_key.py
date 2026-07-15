from fastapi import Security,HTTPException
import sqlite3
from fastapi.security import APIKeyHeader
import bcrypt


API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# todo: add try-catch
def Create_API_key_AuthV2(new_key: str, new_key_permissions: str, req_permission: str = "a", security: str = Security(api_key_header)):
    conn = sqlite3.connect('/app/data/api_keys.db')
    cursor = conn.cursor()
    byte_key = new_key.encode('utf-8')
    hashed_key = bcrypt.hashpw(byte_key, bcrypt.gensalt())
    cursor.execute("INSERT INTO api_keys (api_key, permissions) VALUES (?, ?)", (hashed_key, new_key_permissions))
    conn.commit()
    cursor.execute("SELECT uid FROM api_keys WHERE api_key = ?", (hashed_key,))
    uid = cursor.fetchone()[0]
    conn.close()
    del hashed_key
    return {
        "status": "200",
        "message": "New API Key created successfully",
        "api_key": f"{uid}.{new_key}",
    }