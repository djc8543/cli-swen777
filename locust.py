from locust import User, task
import subprocess
import time

class HTTPieUser(User):
    @task
    def run_httpie(self):
        start = time.time()
        try:
            subprocess.run(
                ["http", "GET", "http://localhost:5000/get"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            total_time = int((time.time() - start) * 1000)  # ms
            self.environment.events.request.fire(
                request_type="CLI",
                name="HTTPie GET /get",
                response_time=total_time,
                response_length=0,
                exception=None
            )
        except subprocess.CalledProcessError as e:
            total_time = int((time.time() - start) * 1000)
            self.environment.events.request.fire(
                request_type="CLI",
                name="HTTPie GET /get",
                response_time=total_time,
                response_length=0,
                exception=e
            )
