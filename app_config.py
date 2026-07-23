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

    missing_settings = []

    if "UPLOAD_FOLDER" in settings:
        UPLOAD_FOLDER = settings.get("UPLOAD_FOLDER")
    else:
        missing_settings.append("UPLOAD_FOLDER")
        UPLOAD_FOLDER = "images"

    if "DOMAIN" in settings:
        DOMAIN = settings.get("DOMAIN")
    else:
        missing_settings.append("DOMAIN")
        DOMAIN = "localhost:8000"

    if "API_KEY" in settings:
        RAW_API_KEY = settings.get("API_KEY")
    else:
        missing_settings.append("API_KEY")
        RAW_API_KEY = "my_very_very_secret_api_key"

    if "URL_PREFIX" in settings:
        IMAGE_URL_PREFIX = settings.get("URL_PREFIX")
    else:
        missing_settings.append("URL_PREFIX")
        IMAGE_URL_PREFIX = "/images"

    if "SUPPORTED_EXTENSIONS" in data:
        SUPPORTED_EXTENSIONS = data["SUPPORTED_EXTENSIONS"]
    else:
        missing_settings.append("SUPPORTED_EXTENSIONS")
        SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]

    if "DISABLE_DOCS" in settings:
        DISABLE_DOCS = settings.get("DISABLE_DOCS")
    else:
        missing_settings.append("DISABLE_DOCS")
        DISABLE_DOCS = True

    if "BEHIND_PROXY" in settings:
        BEHIND_PROXY = settings.get("BEHIND_PROXY")
    else:
        missing_settings.append("BEHIND_PROXY")
        BEHIND_PROXY = True
    if missing_settings:
        print(f"Warning: Missing settings in config.yaml: {', '.join(missing_settings)}. Using default values.", flush=True)

    return {"status": "200", "message": "Configuration reloaded successfully"}

reload_config()

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def reload_config_authv2(req_permision: str = "a", security: str = Security(api_key_header)):
    global UPLOAD_FOLDER, DOMAIN, RAW_API_KEY, IMAGE_URL_PREFIX, SUPPORTED_EXTENSIONS, DISABLE_DOCS, BEHIND_PROXY
    
    with open("/app/data/config.yaml", "r") as config_file:
        data = yaml.safe_load(config_file)

    settings = data.get("settings", {})

    missing_settings = []

    if "UPLOAD_FOLDER" in settings:
        UPLOAD_FOLDER = settings.get("UPLOAD_FOLDER")
    else:
        missing_settings.append("UPLOAD_FOLDER")
        UPLOAD_FOLDER = "images"

    if "DOMAIN" in settings:
        DOMAIN = settings.get("DOMAIN")
    else:
        missing_settings.append("DOMAIN")
        DOMAIN = "localhost:8000"

    if "API_KEY" in settings:
        RAW_API_KEY = settings.get("API_KEY")
    else:
        missing_settings.append("API_KEY")
        RAW_API_KEY = "my_very_very_secret_api_key"

    if "URL_PREFIX" in settings:
        IMAGE_URL_PREFIX = settings.get("URL_PREFIX")
    else:
        missing_settings.append("URL_PREFIX")
        IMAGE_URL_PREFIX = "/images"

    if "SUPPORTED_EXTENSIONS" in data:
        SUPPORTED_EXTENSIONS = data["SUPPORTED_EXTENSIONS"]
    else:
        missing_settings.append("SUPPORTED_EXTENSIONS")
        SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]

    if "DISABLE_DOCS" in settings:
        DISABLE_DOCS = settings.get("DISABLE_DOCS")
    else:
        missing_settings.append("DISABLE_DOCS")
        DISABLE_DOCS = True

    if "BEHIND_PROXY" in settings:
        BEHIND_PROXY = settings.get("BEHIND_PROXY")
    else:
        missing_settings.append("BEHIND_PROXY")
        BEHIND_PROXY = True
    if missing_settings:
        print(f"Warning: Missing settings in config.yaml: {', '.join(missing_settings)}. Using default values.", flush=True)

    return {"status": "200", "message": "Configuration reloaded successfully"}