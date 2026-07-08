from logging import config
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from auth import API_key_check, Check_API_key_AuthV2, Create_API_key_AuthV2, Delete_API_key_AuthV2
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
from upload import upload_image, upload_image_authv2
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

# * Upload Image endpoint with AuthV1
@app.post("/v1/upload")
@limiter.limit("5/minute")
async def upload(request: Request, image: UploadFile = File(...), security: str = Depends(API_key_check)):
    return upload_image(image)

# * Delete Image endpoint with AuthV1
@app.delete("/v1/delete")
@limiter.limit("5/minute")
async def delete(request: Request, image_id: str, security: str = Depends(API_key_check)):
    return delete_image(image_id, security)

# * Get Images endpoint with AuthV1
@app.get("/v1/get-images")
@limiter.limit("5/minute")
async def get_images(request: Request, extension: str = Query(default = ""), security: str = Depends(API_key_check)):
    return get_image(security, extension)

# * Get Images endpoint (Experimental) with AuthV1
@app.get("/experimental/get-images")
@limiter.limit("5/minute")
async def get_images(request: Request, extension: str = Query(default=""), security: str = Depends(API_key_check)):
    return experimantal_get_image(extension, security)

# * Upload Image endpoint with AuthV2
@app.post("/v2/upload")
@limiter.limit("5/minute")
async def upload(request: Request, image: UploadFile = File(...), security: str = Depends(Check_API_key_AuthV2(req_permission="w"))):
    return upload_image_authv2(security, image, req_permission="w")

# * Delete Image endpoint with AuthV2
@app.delete("/v2/delete")
@limiter.limit("5/minute")
async def delete(request: Request, image_id: str, security: str = Depends(Check_API_key_AuthV2)):
    return delete_image(image_id, security)

# * Get Images endpoint with AuthV2
@app.get("/v2/get-images")
@limiter.limit("5/minute")
async def get_images(request: Request, extension: str = Query(default = ""), security: str = Depends(Check_API_key_AuthV2)):
    return get_image(security, extension)

@app.post("/v2/create-api-key")
@limiter.limit("5/minute")
async def create_api_key(request: Request, security: str = Depends(Check_API_key_AuthV2(req_permission="a")), new_key: str = Query(), new_key_permissions: str = Query()):
    return Create_API_key_AuthV2(new_key,new_key_permissions, req_permission="a", security=security)

@app.post("/v2/delete-api-key")
@limiter.limit("5/minute")
async def delete_api_key(request: Request, security: str = Depends(Check_API_key_AuthV2), entry_key: str = Query()):
    return Delete_API_key_AuthV2(entry_key,security)


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
    
