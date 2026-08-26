# config.py
import yaml
from fastapi import Security
from fastapi.security import APIKeyHeader


def check_in_config(parent_key: str, child_key: str, default_data: str | bool | list[str]):
    with open("/app/data/config.yaml", "r") as config_file:
        data = yaml.safe_load(config_file)

    if child_key is None:
        if parent_key in data:
            return data.get(parent_key)
        else:
            print(f"Warning: Missing {parent_key} in config.yaml. Using default value: {default_data}", flush=True)
            return default_data
    

    parent = data.get(parent_key, {})

    if child_key in parent:
        return parent.get(child_key)
    else:
        print(f"Warning: Missing {child_key} in config.yaml under {parent_key}. Using default value: {default_data}", flush=True)
        return default_data


def reload_config():
    global UPLOAD_FOLDER, DOMAIN, RAW_API_KEY, IMAGE_URL_PREFIX, SUPPORTED_EXTENSIONS, DISABLE_DOCS, BEHIND_PROXY, DISABLE_RATE_LIMIT, RATE_LIMIT_IP_WL, RATE_LIMIT_API_WL

    UPLOAD_FOLDER = check_in_config("settings", "UPLOAD_FOLDER", "images")
    DOMAIN = check_in_config("settings", "DOMAIN", "localhost:8000")
    RAW_API_KEY = check_in_config("settings", "API_KEY", "my_very_very_secret_api_key")
    IMAGE_URL_PREFIX = check_in_config("settings", "URL_PREFIX", "/images")
    SUPPORTED_EXTENSIONS = check_in_config("supported_extensions", None, [".jpg", ".jpeg", ".png", ".gif"])
    DISABLE_DOCS = check_in_config("settings", "DISABLE_DOCS", True)
    BEHIND_PROXY = check_in_config("settings", "BEHIND_PROXY", True)
    DISABLE_RATE_LIMIT = check_in_config("debug", "DISABLE_RATE_LIMIT", False)

    RATE_LIMIT_IP_WL = check_in_config("rate_limit_ip_whitelist", None, ["127.0.0.1"])
    RATE_LIMIT_API_WL = check_in_config("rate_limit_api_whitelist", None, ["1.my_very_very_secret_api_key"])

    return {"status": "200", "message": "Configuration reloaded successfully"}

reload_config()

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def reload_config_authv2(req_permision: str = "reload-config", security: str = Security(api_key_header)):
    reload_config()