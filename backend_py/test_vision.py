from google.cloud import vision
from dotenv import load_dotenv

import os

load_dotenv()


print("Using service account:", os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
client = vision.ImageAnnotatorClient()
print("Vision client created OK")
