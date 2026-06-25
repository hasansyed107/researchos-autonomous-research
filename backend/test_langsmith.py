from dotenv import load_dotenv
load_dotenv()

from langsmith import traceable
import time


@traceable
def hello():
    return "ResearchOS"


print(hello())

time.sleep(5)