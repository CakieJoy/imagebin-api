import hashlib

from fastapi import Request
from slowapi.util import get_remote_address

import app_config as config


def key_func(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key:
        if api_key in config.RATE_LIMIT_API_WL:
            return None
        else:
            return hashlib.sha256(api_key.encode('utf-8')).hexdigest()
    else:
        if config.BEHIND_PROXY:
            cf_connecting_ip = request.headers.get("CF-Connecting-IP")
            if cf_connecting_ip:
                if cf_connecting_ip in config.RATE_LIMIT_IP_WL:
                    return None
                else:
                    return cf_connecting_ip
            x_forwarded_for = request.headers.get("X-Forwarded-For")
            if x_forwarded_for:
                if x_forwarded_for.split(",")[-2].strip() in config.RATE_LIMIT_IP_WL:
                    return None
                else:
                    return x_forwarded_for.split(",")[-2].strip()
    return get_remote_address(request)