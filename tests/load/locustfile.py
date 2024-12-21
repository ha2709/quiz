from locust import HttpUser, between, task


class QuizUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def create_quiz_and_add_participant(self):
        # Simulate a user logging in, creating a quiz, and adding a participant
        self.client.post("/auth/login", json={"username": "test", "password": "1234"})
        res = self.client.post("/quiz/", json={"quiz_id": None})
        if res.status_code == 200:
            quiz_id = res.json()["quiz_id"]
            self.client.post(f"/quiz/{quiz_id}/participants", json={"user_id": 2})
