import hashlib
import os
import sqlite3
from typing import Annotated

from fastapi import Depends, FastAPI, File, Query, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

import app_config as config
import health
from auth.v2_check_key import Check_API_key_AuthV2
from auth.v2_create_key import Create_API_key_AuthV2
from auth.v2_del_key import Delete_API_key_AuthV2
from auth.v2_update_perms import Update_API_Permissions
from authv1 import API_key_check
from delete import delete_image, delete_image_authv2
from get_images import get_image, get_image_authv2
from key_func import key_func
from upload import upload_image, upload_image_authv2
from uptime import create_start_time

limiter = Limiter(
    key_func=key_func,
    enabled=False if config.DISABLE_RATE_LIMIT else True)

fastapi_kwargs = {}
templates = Jinja2Templates(directory="/app/data/templates")

if config.DISABLE_DOCS:  
    fastapi_kwargs.update({"docs_url": None, "redoc_url": None})
else:
    fastapi_kwargs.update({"docs_url": "/docs", "redoc_url": "/redoc"})

# * Create a SQLite database
conn = sqlite3.connect('/app/data/api_keys.db', timeout=5)
# * Add WAL mode
conn.execute("PRAGMA journal_mode = WAL;")
cursor = conn.cursor()

# * Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS api_keys (
                    uid INTEGER PRIMARY KEY AUTOINCREMENT,
                    api_key TEXT NOT NULL,
                    permissions TEXT NOT NULL
                )''')

# * Check the database have an existing api key
cursor.execute("SELECT COUNT(*) FROM api_keys")
api_key_count = cursor.fetchone()[0]

conn.close()

    
if api_key_count == 0:
    # * Generate the default API key
    new_api_key = "very_secret_key_100_real"
    conn = sqlite3.connect('/app/data/api_keys.db', timeout=5)
    cursor = conn.cursor()
    hashed_key = hashlib.sha256(new_api_key.encode("utf-8")).hexdigest()
    cursor.execute("INSERT INTO api_keys (api_key, permissions) VALUES (?, ?)", (hashed_key, "*"))
    conn.commit()
    cursor.execute("SELECT uid FROM api_keys WHERE api_key = ?", (hashed_key,))
    uid = cursor.fetchone()
    conn.close()
    print(f"Generated default API key: {uid}.{new_api_key}", flush=True)
    print("Don't forget delete this API Key and generate a new one for security reasons.", flush=True)
else:
    print("API key already exists in the database.")

app = FastAPI(**fastapi_kwargs)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# * Create a start time for uptime
create_start_time()


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
async def upload(request: Request, image: Annotated[UploadFile, File(...)], security: str = Depends(API_key_check)):
    return upload_image(image, security)

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




# * Switching AuthV2 after this line

# * Upload Image endpoint with AuthV2
@app.post("/api/v2/upload")
@limiter.limit("5/minute")
async def upload_v2(request: Request, image: Annotated[UploadFile, File(...)], security: str = Depends(Check_API_key_AuthV2(req_permission="upload"))):
    return upload_image_authv2(security, image, req_permission="upload")

# * Delete Image endpoint with AuthV2
@app.delete("/api/v2/delete")
@limiter.limit("5/minute")
async def delete_v2(request: Request, image_id: str, security: str = Depends(Check_API_key_AuthV2(req_permission="delete"))):
    return delete_image_authv2(image_id, security)

# * Get Images endpoint with AuthV2
@app.get("/api/v2/get-images")
@limiter.limit("5/minute")
async def get_images_authv2(request: Request, extension: str = Query(default = ""), security: str = Depends(Check_API_key_AuthV2(req_permission="list"))):
    return get_image_authv2(security, extension)

@app.post("/api/v2/create-api-key")
@limiter.limit("5/minute")
async def create_api_key_v2(request: Request, security: str = Depends(Check_API_key_AuthV2(req_permission="create-key")), new_key_permissions: str = Query()):
    return Create_API_key_AuthV2(new_key_permissions, req_permission="create-key", security=security)

@app.delete("/api/v2/delete-api-key")
@limiter.limit("5/minute")
async def delete_api_key_v2(request: Request, security: str = Depends(Check_API_key_AuthV2(req_permission="delete-key")), entry_key: str = Query()):
    return Delete_API_key_AuthV2(entry_key,security)

@app.post("/api/v2/reload_config")
@limiter.limit("5/minute")
async def reload_config_endpoint_v2(request: Request,security: str = Depends(Check_API_key_AuthV2(req_permission="reload-config"))):
    config.reload_config_authv2(security)

@app.post("/api/v2/update-permissions")
@limiter.limit("5/minute")
async def update_perm_endpoint_v2(request: Request,security: str = Depends(Check_API_key_AuthV2(req_permission="update-permissions")), entry_key: str = Query(),new_permissions: str = Query(),):
    return Update_API_Permissions(entry_key, new_permissions, security=security, req_permission="update-permissions")


@app.get("/api/health")
@limiter.limit("5/minute")
async def health_check(request: Request):
    return health.health_check()


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
    
