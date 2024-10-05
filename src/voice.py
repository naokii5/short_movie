import requests
import os
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path

load_dotenv()
VOICEVOX_URL = os.getenv("VOICEVOX")

def audio(text: str, speaker: int, output_path: Path):
    extension = output_path.suffix
    assert extension == ".wav", f"拡張子が{extension}です。拡張子は.wavにしてください。"

    query_params = {
        "text": text,
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
    
    with open(output_path, "wb") as f:
        f.write(response.content)

if __name__ == "__main__":
    # from search import URLData, scrape_urls
    # from draft import make_draft
    # urls = [URLData(keyword="誕生日", urls=["https://en.wikipedia.org/wiki/Birthday_problem"], meta_data="birthday paradox")]
    # scrape_data = scrape_urls(urls)
    # draft = make_draft(scrape_data)

    # with open("sample.txt","w") as f:
    #     f.write(draft)
    with open("test_data/sample.txt", "r") as f:
        draft = f.read().splitlines()[:4]
        draft = "\n".join(draft)
    output_path = Path("test_data/output.wav")
    audio(draft, 0, output_path)
    logger.info(f"音声ファイルを{output_path}に保存しました。")
    requests.get(VOICEVOX_URL)
