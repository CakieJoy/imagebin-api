import os
from fastapi import Depends, HTTPException
import app_config as config
from auth import API_key_check

def get_image(security: str = Depends(API_key_check)):
    images_path = os.path.join("/app/data/" + config.UPLOAD_FOLDER)
    images = os.listdir(images_path)
    if images == []:
        raise HTTPException(status_code=404, detail="Not found anything")
    else:
        return {
            "status": "200",
            "images-list": images}