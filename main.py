from logging import config


from auth import API_key_check
from delete import delete_image
from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.templating import Jinja2Templates
import os
import app_config as config
from upload import upload_image
from delete import delete_image

fastapi_kwargs = {}
templates = Jinja2Templates(directory="/app/data/templates")

if config.DISABLE_DOCS:  
    fastapi_kwargs.update({"docs_url": None, "redoc_url": None})
else:
    fastapi_kwargs.update({"docs_url": "/docs", "redoc_url": "/redoc"})

app = FastAPI(**fastapi_kwargs)


@app.post("/v1/reload_config")
def reload_config_endpoint(security: str = Depends(API_key_check)):
    config.reload_config()
    return  {"status": "200", "message": "Configuration reloaded successfully"}

if not os.path.exists("/app/data/" + config.UPLOAD_FOLDER):
    os.makedirs("/app/data/" + config.UPLOAD_FOLDER)
# * ^ this code checks if the folder exists and if doesnt create the folder


app.mount(config.IMAGE_URL_PREFIX, StaticFiles(directory="/app/data/" + config.UPLOAD_FOLDER), name="images")

@app.post("/v1/upload")
def upload(image: UploadFile = File(...), security: str = Depends(API_key_check)):
    return upload_image(image)


@app.delete("/v1/delete")
def delete(image_id: str, security: str = Depends(API_key_check)):
    return delete_image(image_id, security)


@app.exception_handler(404)
async def not_found(request, exc: Exception):
    return templates.TemplateResponse(
     request=request,
     name="404.html",
     context={"request": request},
     status_code=404
    )