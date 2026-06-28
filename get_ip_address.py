import app_config as config
from fastapi import Request
from h11 import Request
from slowapi.util import get_remote_address


def get_ip_address(request: Request):
    if config.BEHIND_PROXY:
        cf_connecting_ip = request.headers.get("CF-Connecting-IP")
        if cf_connecting_ip:
            return cf_connecting_ip
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[-2].strip()
    return get_remote_address(request)