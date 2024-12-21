import random
import string


# Helper function to generate a random string
def generate_random_string(length=7):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
