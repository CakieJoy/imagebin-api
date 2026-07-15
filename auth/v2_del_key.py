from fastapi import Security,HTTPException
import sqlite3
import hashlib
from fastapi.security import APIKeyHeader


API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def Delete_API_key_AuthV2(entry_key: str = Security(api_key_header), req_permission: str = "a"):
    try:
        conn = sqlite3.connect('/app/data/api_keys.db')
        cursor = conn.cursor()
        hashed_entry_key = hashlib.sha256(entry_key.encode()).hexdigest()
        cursor.execute("DELETE FROM api_keys WHERE api_key = ?", (hashed_entry_key,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="API Key not found")
        else:
            conn.commit()
            conn.close()
            del entry_key
            del hashed_entry_key
            return {
                "status": "200",
                "message": "API Key deleted successfully"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error occurred while deleting API key")