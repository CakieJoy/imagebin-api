import sqlite3
import bcrypt
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader


API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def Check_API_key_AuthV2(req_permission: str):
    def dependecy(entry_key: str = Security(api_key_header)):
        try:
            uid_part, key_part = entry_key.split('.', 1)
        except ValueError:
            raise HTTPException(status_code=403, detail="API Key is invalid")
        conn = sqlite3.connect('/app/data/api_keys.db')
        cursor = conn.cursor()
        byte_entry_key = key_part.encode('utf-8')
        cursor.execute("SELECT api_key FROM api_keys WHERE uid = ?", (uid_part,))
        in_db_key = cursor.fetchone()
        cursor.execute("SELECT permissions FROM api_keys WHERE api_key = ?", (in_db_key[0],))
        permissions = cursor.fetchone()
        conn.close()
        if permissions is not None:
            if req_permission not in permissions[0]:
                raise HTTPException(status_code=403, detail="API Key does not have the required permission")

        if bcrypt.checkpw(byte_entry_key, in_db_key[0]) is False:
            raise HTTPException(status_code=403, detail="API Key is invalid")
        else:
            return {
                "status": "200",
                "message": "API Key is valid"
        }
    return dependecy