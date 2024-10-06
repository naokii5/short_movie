# トピック入力、検索ワード生成、検索、台本作成、音声合成、画像生成、

from select_topic import generate_search_keywords,find_interesting_topics,select_topics,make_search_words
from search import scrape_urls, topics_URLs
from draft import make_draft
from voice import audio
from image_gen import image_from_draft
from movie import create_movie
import os
import datetime
import json
from typing import Any, Optional

def main(keyword: str):
    keywords = generate_search_keywords(keyword)

    search_topics = find_interesting_topics(keywords)
    chosen_topics = select_topics(search_topics)
    search_topics_with_words = make_search_words(chosen_topics)

    url_datas = topics_URLs(search_topics_with_words)
    scrape_data_list = scrape_urls(url_datas)

    draft = make_draft(scrape_data_list)

    bytes_list = audio(draft, 1) # bytes
    data_images = image_from_draft(draft) # base64

    create_movie(bytes_list, data_images)


def load_data(func: callable, try_num: int = 1):
    today = datetime.date.today()
    folder_name = today.strftime("%Y-%m-%d")
    file_path = f"dev/{folder_name}/try_{try_num}/{func.__name__}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    return None


def save_data(func: callable, *args: Any, try_num: int = 1, **kwargs: Any):
    today = datetime.date.today()
    folder_name = today.strftime("%Y-%m-%d")
    os.makedirs(f"dev/{folder_name}/try_{try_num}", exist_ok=True)
    file_path = f"dev/{folder_name}/try_{try_num}/{func.__name__}.json"
    next = func(*args, **kwargs)
    with open(file_path, "w") as f:
        try:
            json.dump(next, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)
            try:
                json.dump(next.dict(), f, indent=4, ensure_ascii=False)
            except Exception as e:
                json.dump([item.dict() for item in next], f, indent=4, ensure_ascii=False)
    return next

def get_or_save_topics(func: callable, *args: Any, try_num: int = 1, **kwargs: Any) -> Any:
    data: Optional[Any] = load_data(func, try_num)
    return save_data(func, *args, try_num, **kwargs) if data is None else data

def dev_check(keyword: str, try_num: int = 1):
    today = datetime.date.today()
    folder_name = today.strftime("%Y-%m-%d")
    os.makedirs(f"dev/{folder_name}/try_{try_num}", exist_ok=True)
    keywords = get_or_save_topics(generate_search_keywords, keyword, try_num)
    search_topics = get_or_save_topics(find_interesting_topics, keywords, try_num)
    chosen_topics = get_or_save_topics(select_topics, search_topics, try_num)
    search_topics_with_words = get_or_save_topics(make_search_words, chosen_topics, try_num)
    url_datas = get_or_save_topics(topics_URLs, search_topics_with_words, try_num)
    scrape_data_list = get_or_save_topics(scrape_urls, url_datas, try_num)
    draft = get_or_save_topics(make_draft, scrape_data_list, try_num)
    bytes_list = get_or_save_topics(audio, draft, try_num)
    data_images = get_or_save_topics(image_from_draft, draft, try_num)
    create_movie(bytes_list, data_images)


if __name__ == "__main__":
    dev_check("誕生日", 1)






