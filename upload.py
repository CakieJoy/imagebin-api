import os
import uuid
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles

import app_config as config
from auth import API_key_check



def upload_image(image: UploadFile = File(...), security: str = Depends(API_key_check)):
    image_extension = os.path.splitext(image.filename)[1]
    
    if image_extension in config.SUPPORTED_EXTENSIONS:

        image_id = f"{uuid.uuid4()}{image_extension}"

        image_path = os.path.join("/app/data/" + config.UPLOAD_FOLDER, image_id)

        with open(image_path, "wb") as buffer:
            buffer.write(image.file.read())

        access_url = f"http://{config.DOMAIN}{config.IMAGE_URL_PREFIX}/{image_id}"
        return {
            "status": "200",
            "image_id": image_id,
            "url": access_url
        }
    else:
        raise HTTPException(status_code=400, detail={"message": "Unsupported file type", "supported_extensions": config.SUPPORTED_EXTENSIONS})