import time

def create_start_time():
    global start_time
    start_time = int(time.time() * 1000)  # * Store start time in ms

def get_start_time():
    return start_time

def get_uptime():
    return int(time.time() * 1000) - start_time