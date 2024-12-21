import os
import random
import sys

from locust import HttpUser, between, task

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)
from tests.e2e.test_quiz_e2e import test_app
from tests.utils.string import generate_random_string


class QuizUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def create_quiz_and_add_participant(self):
        # Headers for the requests
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Generate random username and password
        random_username = generate_random_string()
        random_password = generate_random_string()

        # Step 1: Register a new user
        register_response = self.client.post(
            "/register",
            params={"username": random_username, "password": random_password},
            headers=headers,
        )
        print(
            35,
            register_response.json(),
            register_response.status_code,
            type(register_response.status_code),
            register_response.status_code != 200,
        )
        if register_response.status_code != 200:
            print(f"Failed to register user: {random_username}")
            return

        print(f"User registered: {random_username}")

        # Step 2: Login the user to get a token
        login_response = self.client.post(
            "/auth/token",
            data={"username": random_username, "password": random_password},
            headers=headers,
        )
        print(54, login_response.status_code)
        if login_response.status_code != 200:
            print(f"Failed to login user: {random_username}")
            return

        token = login_response.json().get("data", {}).get("access_token")
        if not token:
            print("Failed to retrieve token")
            return

        print(f"User logged in: {random_username}")
        auth_headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

        # Add authorization header
        # auth_headers = {**headers, "Authorization": f"Bearer {token}"}

        # Step 3: Create a new quiz
        random_quiz_id = str(random.randint(10000, 99999))
        create_quiz_response = self.client.post(
            "/quiz/",
            json={"quiz_id": random_quiz_id},
            headers=auth_headers,
        )
        print(76, create_quiz_response.json())
        if create_quiz_response.status_code != 200:
            print(f"Failed to create quiz for user: {random_username}")
            return

        quiz_id = create_quiz_response.json().get("data", {}).get("quiz_id")
        if not quiz_id:
            print("Failed to retrieve quiz ID")
            return

        print(f"Quiz created: {quiz_id}")

        # Step 4: Add a participant to the quiz
        add_participant_response = self.client.post(
            f"/quiz/{quiz_id}/participants",
            json={"user_id": random.randint(1, 100)},
            headers=auth_headers,
        )

        if add_participant_response.status_code == 200:
            print(f"Participant added to quiz {quiz_id}")
        else:
            print(f"Failed to add participant to quiz {quiz_id}")
