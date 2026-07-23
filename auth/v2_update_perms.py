from fastapi import Security, HTTPException
import sqlite3
from fastapi.security import APIKeyHeader
import bcrypt

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def Update_API_Permissions(entry_key: str, new_permissions: str, req_permission: str = "a", security: str = Security(api_key_header)):
    try:
        uid_part, key_part = entry_key.split('.', 1)
    except ValueError:
        raise HTTPException(status_code=403, detail="API Key is invalid")

    conn = sqlite3.connect('/app/data/api_keys.db')
    cursor = conn.cursor()
    # * Checks entry key avalible in db
    cursor.execute("SELECT api_key FROM api_keys WHERE uid = ?", (uid_part,))
    if cursor.fetchone():
        # * if key in the db
        pass
    else:
        # * if key not exist in the db
        raise HTTPException(status="404", detail="Entry key not found.")

