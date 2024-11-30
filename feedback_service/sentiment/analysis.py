import time
import random

# mock function
def analyze(feedback):
    time.sleep(5)
    return random.choice(["positive", "neutral", "negative"])

# mock function
def extract_keywords(feedback):
    time.sleep(5)
    return ["example", "mock", "keywords"]