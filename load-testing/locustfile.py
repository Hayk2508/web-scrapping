from locust import HttpUser, task, between


class LoadTestUser(HttpUser):

    @task
    def load_test_endpoint(self):
        self.client.get(
            "/api/parsers/parse/?url=https://preply.com/en/tutor-signup&parse_type=images"
        )
