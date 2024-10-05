import requests
import os
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path
from draft import Draft
load_dotenv()
VOICEVOX_URL = os.getenv("VOICEVOX")

def audio(draft: Draft, speaker: int)->list[bytes]:
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
        response = requests.post(synthesis_url, params=synthesis_params, json=request_body,timeout=60)
        if not response.status_code==200:
            logger.info(response.status_code,response.content)
        bytes_list.append(response.content)
    return bytes_list
        

if __name__ == "__main__":
    # from search import URLData, scrape_urls
    # from draft import make_draft
    # urls = [URLData(keyword="誕生日", urls=["https://en.wikipedia.org/wiki/Birthday_problem"], meta_data="birthday paradox")]
    # scrape_data = scrape_urls(urls)
    # draft = make_draft(scrape_data)

    # with open("sample.txt","w") as f:
    #     f.write(draft)
    from draft import Draft
    draft = Draft(keyword="誕生日", content=["誕生日のパラドックスとは","誕生日が同じ人が何人いるかを求める問題です。"])
    output_path = Path("test_data/output.wav")
    bytes_list = audio(draft, 1)
    for i, bytes_ in enumerate(bytes_list):
        with open(f"test_data/output_{i}.wav", "wb") as f:
            f.write(bytes_)
 
