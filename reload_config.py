import os
import uuid
from auth import API_key_check
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
import yaml

def reload_config(security: str = Depends(API_key_check)):
    global UPLOAD_FOLDER, DOMAIN, API_KEY, IMAGE_URL_PREFIX, SUPPORTED_EXTENSIONS
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    UPLOAD_FOLDER = config["settings"]["UPLOAD_FOLDER"]  # * Folder name for uploaded images.
    DOMAIN = config["settings"]["DOMAIN"]  # * your domain name or ip address (yeah ip addrsses work too but name is domain :3)
    API_KEY = config["settings"]["API_KEY"]  # * CHANGE THIS TO STRONG API KEY!!111!1!1!!11!1!1
    IMAGE_URL_PREFIX = config["settings"]["URL_PREFIX"]  # ! not working on reload still need restart the API
    SUPPORTED_EXTENSIONS = config["supported_extensions"]  # * supported image extensions
    return {"status": "200", "message": "Configuration reloaded successfully"}


