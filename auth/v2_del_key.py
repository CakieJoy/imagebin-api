from fastapi import Security,HTTPException
import sqlite3
import hashlib
from fastapi.security import APIKeyHeader


API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# todo: add try-catch and try delete non existing key
def Delete_API_key_AuthV2(entry_key: str = Security(api_key_header), req_permission: str = "a"):
    conn = sqlite3.connect('/app/data/api_keys.db')
    cursor = conn.cursor()
    hashed_entry_key = hashlib.sha256(entry_key.encode()).hexdigest()
    cursor.execute("DELETE FROM api_keys WHERE api_key = ?", (hashed_entry_key,))
    conn.commit()
    conn.close()
    del entry_key
    del hashed_entry_key
    return {
        "status": "200",
        "message": "API Key deleted successfully"
    }