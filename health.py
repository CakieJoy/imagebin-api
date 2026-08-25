import time
from uptime import get_uptime


def health_check():
    response_time = time.time()
    return {
        "timestamp": response_time,
        "uptimeSeconds": get_uptime()
    }