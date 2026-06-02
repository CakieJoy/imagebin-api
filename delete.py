import os
import uuid

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
import yaml
import app_config as config

from auth import API_key_check  



def delete_image(image_id: str, security: str = Depends(API_key_check)):
    image_path = os.path.join("/app/data/" + config.UPLOAD_FOLDER, image_id)
    if os.path.exists(image_path):
        os.remove(image_path)
        return {"status": "200", "message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")