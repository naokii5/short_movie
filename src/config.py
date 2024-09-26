from dotenv import load_dotenv
import instructor
import google.generativeai as genai
import os

load_dotenv(verbose=True)
google_api_key = os.getenv("GEMINI_API_KEY")
google_cse_id = os.getenv("CUSTOM_ENGINE_ID")
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

client = instructor.from_gemini(
    client=genai.GenerativeModel(
        model_name="models/gemini-1.5-flash-latest",
    ),
    mode=instructor.Mode.GEMINI_JSON,
)