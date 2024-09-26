from select_topic import SearchTopicsResponse
from googleapiclient.discovery import build
import config
import pprint
import requests
from loguru import logger
import json

def topics_URLs(search_topics: SearchTopicsResponse) -> list[tuple[str,dict]]:
    assert isinstance(search_topics, SearchTopicsResponse)
    for search_topic in search_topics.search_topics:
        assert search_topic.word_for_search is not None, "word_for_search is None"

    service = build(
        "customsearch", "v1", developerKey=config.google_api_key
    )
    urls = []
    for search_topic in search_topics.search_topics:
        try:
            res = (
                service.cse()
                .list(
                    q=search_topic.word_for_search,
                    cx=config.google_cse_id,
                )
                .execute()
            )
            urls.append((search_topic.keyword,res))
            pprint.pprint(res)
        except Exception as e:
            logger.error(f"Error: {e}")

    logger.info(urls)

    for i, url in enumerate(urls):
        file_path = f"urls/{i}{url[0]}.json"
        with open(file_path, "w") as f:
            json.dump(url[1], f, indent=4, ensure_ascii=False)
    return urls


def scrape_urls(urls: list[tuple[str,dict]]):
    base_url = 'https://r.jina.ai/'
    headers = {"Authorization": f"Bearer {config.jina_api_key}"}
    scrape_data = []
    for url in urls:
        try:
            target_url = url[1]['items'][0]['link']
            search_url = base_url+target_url
            
            logger.info(f"url: {search_url}")
            response = requests.get(search_url, headers=headers)
            print(f"type: {type(response)}")

            print(response.text)
            scrape_data.append((url[0],response.text))
        except Exception as e:
            logger.error(f"Error: {e}")
    for i, (keyword, data) in enumerate(scrape_data):
        file_path = f"scrape_data/{i}_{keyword}.json"
        with open(file_path, "w") as f:
            json.dump({"keyword": keyword, "data": data}, f, indent=4, ensure_ascii=False)
    return scrape_data



if __name__ == "__main__":

    search_topics = SearchTopicsResponse(
        search_topics=[
            {
                "keyword": "誕生日",
                "fact": "誕生日のパラドックス",
                "word_for_search": "birthday paradox",
            }
        ]
    )
    urls = topics_URLs(search_topics)
    scrape_urls(urls)