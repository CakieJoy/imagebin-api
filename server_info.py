import os

import app_config as config


def get_app_version():
    return os.getenv("APP_VERSION", "dontknown")


def server_info():
    return {
        "name": config.INSTANCE_NAME,
        "description": config.INSTANCE_DESCRIPTION,
        "version": get_app_version(),
        "environment": config.ENVIRONMENT,
        "email": config.INSTANCE_EMAIL,
        "domain": config.DOMAIN,
        "url_prefix": config.IMAGE_URL_PREFIX,
        "supported_extensions": config.SUPPORTED_EXTENSIONS,
    }