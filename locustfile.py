from locust import HttpUser, task


class TrafficTest(HttpUser):

    @task
    def test_landing_api(self):
        self.client.get("/hospital/v1/hospitals/home")
