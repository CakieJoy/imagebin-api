import glob
import os
from fastapi import Depends, HTTPException
import app_config as config
from auth import API_key_check

def get_image(security: str = Depends(API_key_check), extension: str = ""):
    images_path = os.path.join("/app/data", config.UPLOAD_FOLDER)
    if extension == "":
        all_images = os.listdir(images_path)
        if all_images == []:
            raise HTTPException(status_code=404, detail="Not found anything")
        else:
            return {"status": "200", "images-list": all_images}
    else: 
        filtered_images = glob.glob(os.path.join(f"*.{extension}"), root_dir=images_path,)
        if filtered_images == []:
            raise HTTPException(status_code=404, detail="Not found anything")
        else:
            return {"status": "200", "images-list": filtered_images}