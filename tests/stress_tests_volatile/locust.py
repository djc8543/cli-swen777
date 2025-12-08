from locust import HttpUser, task

class LoadUser(HttpUser):
    @task
    def load_test(self):
        self.client.get("/")
