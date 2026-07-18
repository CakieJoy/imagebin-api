from fastapi import Security,HTTPException
import sqlite3
import hashlib
from fastapi.security import APIKeyHeader


API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def Delete_API_key_AuthV2(entry_key: str, req_permission: str = "a", security: str = Security(api_key_header)):
    try:
        uid_part, key_part = entry_key.split('.', 1)
        conn = sqlite3.connect('/app/data/api_keys.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM api_keys WHERE uid = ?", (uid_part,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="API Key not found")
        else:
            conn.commit()
            conn.close()
            del entry_key
            del key_part
            del uid_part
            return {
                "status": "200",
                "message": "API Key deleted successfully"
            }
    except Exception as e:
        print(f"Error deleting API key: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail="Error occurred while deleting API key")