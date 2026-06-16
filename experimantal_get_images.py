import os
import glob
from fastapi import Depends
import app_config as config
from auth import API_key_check

def experimantal_get_image(extension: str, security: str = Depends(API_key_check)):
    images_path = os.path.join("/app/data", config.UPLOAD_FOLDER)
    if extension == "":
        all_images = os.listdir(images_path)
        return {"status": "200", "images-list": all_images}
    else:    
        filtered_images = glob.glob(os.path.join(images_path, f"*.{extension}"))
        return {"status": "200", "images-list": filtered_images}
    