from select_topic import SearchTopicsResponse
from googleapiclient.discovery import build
import config
import pprint

def topics_URLs(search_topics: SearchTopicsResponse):
    assert isinstance(search_topics, SearchTopicsResponse)
    for search_topic in search_topics.search_topics:
        assert search_topic.word_for_search is not None, "word_for_search is None"

    service = build(
        "customsearch", "v1", developerKey=config.google_api_key
    )
    urls = []
    for search_topic in search_topics.search_topics:
        res = (
            service.cse()
            .list(
                q=search_topic.word_for_search,
                cx=config.google_cse_id,
            )
            .execute()
        )
        urls.append(res)
        pprint.pprint(res)

    return urls

if __name__ == "__main__":
    from loguru import logger
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
    logger.info(f"urls: {urls}")