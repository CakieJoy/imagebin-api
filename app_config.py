# config.py
import yaml

UPLOAD_FOLDER = "images"
DOMAIN = "localhost:8000"
RAW_API_KEY = "my_very_very_secret_api_key"
IMAGE_URL_PREFIX = "/images"
SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
DISABLE_DOCS = True

def reload_config():
    global UPLOAD_FOLDER, DOMAIN, RAW_API_KEY, IMAGE_URL_PREFIX, SUPPORTED_EXTENSIONS, DISABLE_DOCS
    
    with open("/app/data/config.yaml", "r") as config_file:
        data = yaml.safe_load(config_file)

    UPLOAD_FOLDER = data["settings"]["UPLOAD_FOLDER"]
    DOMAIN = data["settings"]["DOMAIN"]
    RAW_API_KEY = data["settings"]["API_KEY"]
    IMAGE_URL_PREFIX = data["settings"]["URL_PREFIX"]
    SUPPORTED_EXTENSIONS = data["supported_extensions"]
    DISABLE_DOCS = data["settings"].get("DISABLE_DOCS")
    
    return {"status": "200", "message": "Configuration reloaded successfully"}


reload_config()