from dotenv import load_dotenv
import instructor
import google.generativeai as genai
from openai import OpenAI
import os

load_dotenv(verbose=True)
google_api_key = os.getenv("GEMINI_API_KEY")
google_cse_id = os.getenv("CUSTOM_ENGINE_ID")
jina_api_key = os.getenv("JINA_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")
# litellmで制御したかったが、バグるため一旦純正の方法に切り替える
# client = instructor.patch(
#     Router(
#         model_list=[
#             {
#                 "model_name": "gemini-1.5-pro-latest",  
#                 "litellm_params": {  # params for litellm completion/embedding call - e.g.: https://github.com/BerriAI/litellm/blob/62a591f90c99120e1a51a8445f5c3752586868ea/litellm/router.py#L111
#                     "model": "gemini/gemini-1.5-pro-latest",
#                     "api_key": os.getenv("GEMINI_API_KEY")
#                 },
#             }
#         ]
#     )
# )

 
genai.configure(api_key=google_api_key)
gemini_flash= genai.GenerativeModel("gemini-1.5-flash-latest")

openai_client = OpenAI(api_key=openai_api_key)

client = instructor.from_gemini(
client=genai.GenerativeModel(
    model_name="models/gemini-1.5-flash-latest",
),
mode=instructor.Mode.GEMINI_JSON,
)