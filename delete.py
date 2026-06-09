import os
import uuid

from fastapi import Depends, HTTPException
import app_config as config

from auth import API_key_check  



def delete_image(image_id: str, security: str = Depends(API_key_check)):
    image_path = os.path.join("/app/data/" + config.UPLOAD_FOLDER, image_id)
    if os.path.exists(image_path):
        os.remove(image_path)
        return {"status": "200", "message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")