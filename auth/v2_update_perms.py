from fastapi import Security, HTTPException
import sqlite3
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def Update_API_Permissions(entry_key: str, new_permissions: str, req_permission: str = "a", security: str = Security(api_key_header)):
    try:
        uid_part, key_part = entry_key.split('.', 1)
    except ValueError:
        raise HTTPException(status_code=403, detail="API Key is invalid")

    conn = sqlite3.connect('/app/data/api_keys.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE api_keys SET permissions = ? WHERE uid = ?", (new_permissions, uid_part))
    conn.commit()
    if cursor.rowcount == 0:
        # * if key not exist in the db
        conn.close()
        raise HTTPException(status_code=404, detail="Entry key not found.")
    else:
        return {
            "status": "200",
            "message": "Permission changed successfully"
        }
    

