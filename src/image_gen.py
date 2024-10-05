from openai import OpenAI
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_key = os.environ.get("OPENAI_API_KEY")


client = OpenAI(api_key=api_key)

a = client.images.generate(
  model="dall-e-3",
  prompt="誕生日のパラドックス",
  n=1,
  size="1024x1024"
)
print(a)