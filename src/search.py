from select_topic import SearchTopicsResponse
from googleapiclient.discovery import build
import config
import pprint
import requests
from loguru import logger
import json
from pydantic import BaseModel

class URLText(BaseModel):
    url: str
    text: str

class ScrapeData(BaseModel):
    keyword: str
    data: list[URLText]

class ScrapeDatas(BaseModel):
    scrape_data: list[ScrapeData]

class URLData(BaseModel):
    keyword: str
    urls: list[str]
    meta_data: dict # Google Custom Search APIから取得した結果全体

class URLDatas(BaseModel):
    url_data: list[URLData]

def topics_URLs(search_topics: SearchTopicsResponse) -> URLDatas:
    """
    検索キーワードリストから、Google Custom Search APIを使用して関連するURLを取得します。

    引数:
        search_topics (SearchTopicsResponse): LLMから返された検索トピックのリスト

    戻り値:
        list[URLData]: 検索キーワードと、Google Custom Search APIから取得した結果のリスト
    """
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
                    num=3,
                )
                .execute()
            )
            urls.append(URLData(keyword=search_topic.keyword, urls=[res['items'][i]['link'] for i in range(len(res['items']))], meta_data=res))
            pprint.pprint(res)
        except Exception as e:
            logger.error(f"Error: {e}")

    for i, url_data in enumerate(urls):
        file_path = f"urls/{url_data.keyword}-{i}.json"
        with open(file_path, "w") as f:
            json.dump(url_data.model_dump(by_alias=True), f, indent=4, ensure_ascii=False)
    return URLDatas(url_data=urls)


def scrape_urls(url_datas: URLDatas) -> ScrapeDatas:
    """
    Google Custom Search APIから取得したURLリストから、Jina Readerを使用して関連する情報をスクレイピングします。

    引数:
        url_datas (URLDatas): 検索キーワードと、Google Custom Search APIから取得したURLリスト

    戻り値:
        list[ScrapeData]: スクレイピングされたデータのリスト
    """
    assert isinstance(url_datas, URLDatas)
    assert all(isinstance(url, URLData) for url in url_datas.url_data)
    base_url = 'https://r.jina.ai/'
    headers = {"Authorization": f"Bearer {config.jina_api_key}"}
    scrape_data_dict = {}
    for url_data in url_datas.url_data:
        for target_url in url_data.urls:
            try:
                search_url = base_url+target_url
                
                logger.info(f"url: {search_url}")
                response = requests.get(search_url, headers=headers)
                print(f"type: {type(response)}")
                print(response.text)
                
                scrape_data_dict.setdefault(url_data.keyword, []).append(URLText(url=target_url, text=response.text))
            except Exception as e:
                logger.error(f"Error: {e}")
    for key, url_text_list in scrape_data_dict.items():
        file_path = f"scrape_data/{key}.json"
        with open(file_path, "w") as f:
            json.dump([url_text.model_dump(by_alias=True) for url_text in url_text_list], f, indent=4, ensure_ascii=False)
    
    scrape_data_list = []
    for key, url_text_list in scrape_data_dict.items():
        scrape_data_list.append(ScrapeData(keyword=key, data=url_text_list))
    return ScrapeDatas(scrape_data=scrape_data_list)



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
    # urls = topics_URLs(search_topics)
    urls = URLData(keyword="誕生日", urls=["https://en.wikipedia.org/wiki/Birthday_problem"], meta_data="birthday paradox")
    scrape_urls(urls)