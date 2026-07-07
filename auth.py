import hashlib
import secrets
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import app_config
import sqlite3
import bcrypt

# * AuthV1
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

# * AuthV2

# * Create a SQLite database
conn = sqlite3.connect('/app/data/api_keys.db')
cursor = conn.cursor()

# * Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS api_keys (
                    uid INTEGER PRIMARY KEY AUTOINCREMENT,
                    api_key TEXT NOT NULL
                )''')

# * Check the database have an existing api key
cursor.execute("SELECT COUNT(*) FROM api_keys")
api_key_count = cursor.fetchone()[0]

conn.close()

def Create_API_key_AuthV2(new_key: str = Security(api_key_header)):
    conn = sqlite3.connect('/app/data/api_keys.db')
    cursor = conn.cursor()
    hashed_key = hashlib.sha256(new_key.encode()).hexdigest()
    cursor.execute("INSERT INTO api_keys (api_key) VALUES (?)", (hashed_key,))
    conn.commit()
    conn.close()
    del new_key
    del hashed_key
    return {
        "status": "200",
        "message": "New API Key created successfully",
        "api_key": new_api_key
    }

if api_key_count == 0:
    # * Generate the default API key
    new_api_key = secrets.token_hex(32)
    Create_API_key_AuthV2(new_api_key)
    print(f"Generated default API key: {new_api_key}", flush=True)
    print("Don't forget delete this API Key and generate a new one for security reasons.", flush=True)
else:
    print("API key already exists in the database.")

# * Check the API key from the database
def Check_API_key_AuthV2(entry_key: str = Security(api_key_header)):
    conn = sqlite3.connect('/app/data/api_keys.db')
    cursor = conn.cursor()
    hashed_entry_key = hashlib.sha256(entry_key.encode()).hexdigest()
    cursor.execute("SELECT api_key FROM api_keys WHERE api_key = ?", (hashed_entry_key,))
    in_db_key = cursor.fetchone()
    conn.close()
    if in_db_key is None:
        raise HTTPException(status_code=403, detail="API Key is invalid")
    else:
        return {
            "status": "200",
            "message": "API Key is valid"
     }
    
def Delete_API_key_AuthV2(entry_key: str = Security(api_key_header)):
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

