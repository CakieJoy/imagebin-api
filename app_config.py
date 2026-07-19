# config.py
from fastapi import Security
from fastapi.security import APIKeyHeader
import yaml

UPLOAD_FOLDER = "images"
DOMAIN = "localhost:8000"
RAW_API_KEY = "my_very_very_secret_api_key"
IMAGE_URL_PREFIX = "/images"
SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
DISABLE_DOCS = True
BEHIND_PROXY = True

def reload_config():
    global UPLOAD_FOLDER, DOMAIN, RAW_API_KEY, IMAGE_URL_PREFIX, SUPPORTED_EXTENSIONS, DISABLE_DOCS, BEHIND_PROXY
    
    with open("/app/data/config.yaml", "r") as config_file:
        data = yaml.safe_load(config_file)

    settings = data.get("settings", {})

    UPLOAD_FOLDER = settings.get("UPLOAD_FOLDER", "images")
    DOMAIN = settings.get("DOMAIN", "localhost:8000")
    RAW_API_KEY = settings.get("API_KEY", "my_very_very_secret_api_key")
    IMAGE_URL_PREFIX = settings.get("URL_PREFIX", "/images")
    SUPPORTED_EXTENSIONS = data.get("supported_extensions", [".jpg", ".jpeg", ".png", ".gif"])
    DISABLE_DOCS = settings.get("DISABLE_DOCS", True)
    BEHIND_PROXY = settings.get("BEHIND_PROXY", True)

    return {"status": "200", "message": "Configuration reloaded successfully"}

reload_config()

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def reload_config_authv2(req_permision: str = "a", security: str = Security(api_key_header)):
    global UPLOAD_FOLDER, DOMAIN, RAW_API_KEY, IMAGE_URL_PREFIX, SUPPORTED_EXTENSIONS, DISABLE_DOCS, BEHIND_PROXY
    
    with open("/app/data/config.yaml", "r") as config_file:
        data = yaml.safe_load(config_file)

    UPLOAD_FOLDER = data["settings"]["UPLOAD_FOLDER"]
    DOMAIN = data["settings"]["DOMAIN"]
    RAW_API_KEY = data["settings"]["API_KEY"]
    IMAGE_URL_PREFIX = data["settings"]["URL_PREFIX"]
    SUPPORTED_EXTENSIONS = data["supported_extensions"]
    DISABLE_DOCS = data["settings"].get("DISABLE_DOCS")
    BEHIND_PROXY = data["settings"].get("BEHIND_PROXY") 
    
    return {"status": "200", "message": "Configuration reloaded successfully"}