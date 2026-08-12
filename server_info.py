import app_config as config


def server_info():
    return {
        "name": config.INSTANCE_NAME,
        "description": config.INSTANCE_DESCRIPTION,
        "email": config.INSTANCE_EMAIL,
        "domain": config.DOMAIN,
        "url_prefix": config.IMAGE_URL_PREFIX,
        "supported_extensions": config.SUPPORTED_EXTENSIONS,
    }