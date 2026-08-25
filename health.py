import time

from uptime import get_uptime


def health_check():
    response_time = int(time.time() * 1000)  # * Store response time in ms
    return {
        "timestamp": response_time,
        "uptimeSeconds": get_uptime() // 1000
    }