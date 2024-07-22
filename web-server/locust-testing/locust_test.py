from locust import HttpUser, task, between


class LoadTestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_test_endpoint(self):
        self.client.get("/api/parsed-objects/")
