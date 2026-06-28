from logging import config
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from auth import API_key_check
from delete import delete_image
from fastapi import FastAPI, Query
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.templating import Jinja2Templates
import os
import app_config as config
from experimantal_get_images import experimantal_get_image
from get_images import get_image
from upload import upload_image
from delete import delete_image
from slowapi.errors import RateLimitExceeded
from get_ip_address import get_ip_address

limiter = Limiter(key_func=get_ip_address)

fastapi_kwargs = {}
templates = Jinja2Templates(directory="/app/data/templates")

if config.DISABLE_DOCS:  
    fastapi_kwargs.update({"docs_url": None, "redoc_url": None})
else:
    fastapi_kwargs.update({"docs_url": "/docs", "redoc_url": "/redoc"})

app = FastAPI(**fastapi_kwargs)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/v1/reload_config")
@limiter.limit("5/minute")
async def reload_config_endpoint(request: Request,security: str = Depends(API_key_check)):
    config.reload_config()
    return  {"status": "200", "message": "Configuration reloaded successfully"}

if not os.path.exists("/app/data/" + config.UPLOAD_FOLDER):
    os.makedirs("/app/data/" + config.UPLOAD_FOLDER)
# * ^ this code checks if the folder exists and if doesnt create the folder


app.mount(config.IMAGE_URL_PREFIX, StaticFiles(directory="/app/data/" + config.UPLOAD_FOLDER), name="images")

# * Upload Image endpoint
@app.post("/v1/upload")
@limiter.limit("5/minute")
async def upload(request: Request, image: UploadFile = File(...), security: str = Depends(API_key_check)):
    return upload_image(image)

# * Delete Image endpoint
@app.delete("/v1/delete")
@limiter.limit("5/minute")
async def delete(request: Request, image_id: str, security: str = Depends(API_key_check)):
    return delete_image(image_id, security)

# * Get Images endpoint
@app.get("/v1/get-images")
@limiter.limit("5/minute")
async def get_images(request: Request, extension: str = Query(default = ""), security: str = Depends(API_key_check)):
    return get_image(security, extension)

# * Get Images endpoint (Experimental)
@app.get("/experimental/get-images")
@limiter.limit("5/minute")
async def get_images(request: Request, extension: str = Query(default=""), security: str = Depends(API_key_check)):
    return experimantal_get_image(extension, security)

@app.exception_handler(404)
async def not_found(request, exc: Exception):
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={"request": request},
            status_code=404
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"detail": "Not Found anything"}
        )
    
