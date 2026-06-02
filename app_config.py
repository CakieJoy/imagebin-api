# config.py
import yaml

UPLOAD_FOLDER = None
DOMAIN = None
API_KEY = None
IMAGE_URL_PREFIX = None
SUPPORTED_EXTENSIONS = None

def reload_config():
    global UPLOAD_FOLDER, DOMAIN, API_KEY, IMAGE_URL_PREFIX, SUPPORTED_EXTENSIONS
    
    with open("/app/data/config.yaml", "r") as config_file:
        data = yaml.safe_load(config_file)

    UPLOAD_FOLDER = data["settings"]["UPLOAD_FOLDER"]
    DOMAIN = data["settings"]["DOMAIN"]
    API_KEY = data["settings"]["API_KEY"]
    IMAGE_URL_PREFIX = data["settings"]["URL_PREFIX"]
    SUPPORTED_EXTENSIONS = data["supported_extensions"]
    
    return {"status": "200", "message": "Configuration reloaded successfully"}


reload_config()