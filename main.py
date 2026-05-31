from logging import config
from auth import API_key_check
from delete import delete_image
from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os
import app_config as config
from upload import upload_image
from delete import delete_image

app = FastAPI()


@app.post("/v1/reload_config")
def reload_config_endpoint(security: str = Depends(API_key_check)):
    config.reload_config()
    return  {"status": "200", "message": "Configuration reloaded successfully"}




if not os.path.exists(config.UPLOAD_FOLDER):
    os.makedirs(config.UPLOAD_FOLDER)
# * ^ this code checks if the folder exists and if doesnt create the folder


app.mount(config.IMAGE_URL_PREFIX, StaticFiles(directory=config.UPLOAD_FOLDER), name="images")

@app.post("/v1/upload")
def upload(file: UploadFile = File(...), security: str = Depends(API_key_check)):
    return upload_image(file)


@app.post("/v1/delete")
def delete(image_id: str, security: str = Depends(API_key_check)):
    return delete_image(image_id, security)