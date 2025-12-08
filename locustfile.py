from locust import User, task, between
import subprocess
import time
import os

HTTPIE_CMD = os.getenv("HTTPIE_CMD", "http")
TARGET_URL = os.getenv("HTTPIE_TARGET", "http://localhost:5000/get")


class HTTPieLoadUser(User):
    wait_time = between(0.5, 1.5)
    @task
    def httpie_get(self):
        start = time.perf_counter()

        try:
            subprocess.run(
                [HTTPIE_CMD, "GET", TARGET_URL],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            total_time_ms = (time.perf_counter() - start) * 1000.0
            self.environment.events.request.fire(
                request_type="CLI",           
                name="HTTPie GET",            
                response_time=total_time_ms,  
                response_length=0,            
                exception=None,
            )

        except subprocess.CalledProcessError as e:
            total_time_ms = (time.perf_counter() - start) * 1000.0
            self.environment.events.request.fire(
                request_type="CLI",
                name="HTTPie GET",
                response_time=total_time_ms,
                response_length=0,
                exception=e,                 
            )

        except Exception as e:
            total_time_ms = (time.perf_counter() - start) * 1000.0
            self.environment.events.request.fire(
                request_type="CLI",
                name="HTTPie GET",
                response_time=total_time_ms,
                response_length=0,
                exception=e,
            )
