import os
import glob
from fastapi import Depends, HTTPException
import app_config as config
from authv1 import API_key_check

def experimantal_get_image(extension: str, security: str = Depends(API_key_check)):
    images_path = os.path.join("/app/data", config.UPLOAD_FOLDER)
    if extension == "":
        all_images = os.listdir(images_path)
        if all_images == []:
            raise HTTPException(status_code=404, detail="Not found anything")
        else:
            return {
                "status": "200",
                "images-list": all_images,
                "Warning": "This endpoint is stable now please use /v1/get_images endpoint"  
            }
    else: 
        filtered_images = glob.glob(os.path.join(f"*.{extension}"), root_dir=images_path,)
        if filtered_images == []:
            raise HTTPException(status_code=404, detail="Not found anything")
        else:
            return {
                "status": "200",
                "images-list": filtered_images,
                "Warning": "This endpoint is stable now please use /v1/get_images endpoint. Experimantal endpoint will be remove in the future"  
            }
    