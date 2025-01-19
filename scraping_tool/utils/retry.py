import time

def retry_request(request_func, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return request_func()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e