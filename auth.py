import os
import uuid
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
import yaml
import app_config


API_KEY = app_config.API_KEY  


API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def API_key_check(entry_key: str = Security(api_key_header)):
    if entry_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key is invalid")
    return {
        "status": "403",
        "message": "API Key is valid"
    }