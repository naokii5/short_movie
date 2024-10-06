import requests
import os
from dotenv import load_dotenv
from loguru import logger
from time import sleep
from draft import Draft
from pydantic import BaseModel
import base64

load_dotenv()
VOICEVOX_URL = os.getenv("VOICEVOX")

class Voices(BaseModel):
    voice_bytes: list[str]

def audio(draft: Draft, speaker: int)->Voices:
    bytes_list = []
    for content in draft.content:
        query_params = {
            "text": content,
            "speaker": speaker}
        query_url = VOICEVOX_URL+"audio_query"
        retries = 3
        for attempt in range(retries):
            try:
                query = requests.post(query_url, params=query_params)
                if not query.status_code==200:
                    logger.info(query.status_code,query.content)
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                if attempt == retries - 1:
                    raise
                sleep(5)

        synthesis_url = VOICEVOX_URL + "synthesis"
        synthesis_params = {
            "speaker": speaker}
        request_body = query.json()
        retries = 3
        for attempt in range(retries):
            try:
                response = requests.post(synthesis_url, params=synthesis_params, json=request_body,timeout=60)
                if not response.status_code==200:
                    logger.info(response.status_code,response.content)
                bytes_list.append(str(base64.b64encode(response.content), 'utf-8'))
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                if attempt == retries - 1:
                    raise
                sleep(5)
    return Voices(voice_bytes=bytes_list)
        

if __name__ == "__main__":
    from draft import Draft
    draft = Draft(keyword="誕生日", content=["誕生日とは、人が生まれた日のことを指します。"])
    voices = audio(draft, 13)
    import base64
    for voice in voices.voice_bytes:
        with open("test_data/test.wav", "wb") as f:
            f.write(base64.b64decode(voice))

 
