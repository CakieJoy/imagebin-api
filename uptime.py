import time

def create_start_time():
    global start_time
    start_time = time.time()

def get_start_time():
    return start_time

def get_uptime():
    return int(time.time() - start_time)