from logging import config
from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os
import uuid
import yaml
app = FastAPI()
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def API_key_check(entry_key: str = Security(api_key_header)):
    if entry_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key is invalid")
    return {
        "status": "403",
        "message": "API Key is valid"
    }

@app.post("/v1/reload_config")
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


reload_config()  # * Load configuration at startup



if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# * ^ this code checks if the folder exists and if doesnt create the folder


app.mount(IMAGE_URL_PREFIX, StaticFiles(directory=UPLOAD_FOLDER), name="gorseller")

@app.post("/v1/upload")
def upload_image(image: UploadFile = File(...), security: str = Depends(API_key_check)):
    image_extension = os.path.splitext(image.filename)[1]
    
    if image_extension in SUPPORTED_EXTENSIONS:

        image_id = f"{uuid.uuid4()}{image_extension}"

        image_path = os.path.join(UPLOAD_FOLDER, image_id)

        with open(image_path, "wb") as buffer:
            buffer.write(image.file.read())

        access_url = f"http://{DOMAIN}{IMAGE_URL_PREFIX}/{image_id}"
        return {
            "status": "200",
            "image_id": image_id,
            "url": access_url
        }
    else:
        raise HTTPException(status_code=400, detail={"message": "Unsupported file type", "supported_extensions": SUPPORTED_EXTENSIONS})


@app.post("/v1/delete")
def delete_image(image_id: str, security: str = Depends(API_key_check)):
    image_path = os.path.join(UPLOAD_FOLDER, image_id)
    if os.path.exists(image_path):
        os.remove(image_path)
        return {"status": "200", "message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")