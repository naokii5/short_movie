import requests
import os
from dotenv import load_dotenv
from loguru import logger
from time import sleep
from pathlib import Path
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
        query = requests.post(query_url, params=query_params)

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
    ...
 
