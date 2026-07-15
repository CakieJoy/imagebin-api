import os

from fastapi import Depends, HTTPException
import app_config as config

from authv1 import API_key_check
from auth.v2_check_key import Check_API_key_AuthV2


def delete_image(image_id: str, security: str = Depends(API_key_check)):
    image_path = os.path.join("/app/data/" + config.UPLOAD_FOLDER, image_id)
    if os.path.exists(image_path):
        os.remove(image_path)
        return {"status": "200", "message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    

def delete_image_authv2(image_id: str, security: str = Depends(Check_API_key_AuthV2(req_permission="w"))):
    image_path = os.path.join("/app/data/" + config.UPLOAD_FOLDER, image_id)
    if os.path.exists(image_path):
        os.remove(image_path)
        return {"status": "200", "message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")