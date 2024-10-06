# トピックを入力すると、それに関する雑学を返す
# １。トピックから検索ワードを生成
# ２。GooglesearchAPIでそれらを検索
# ３。検索したURLsが返ってくるのでそれをjina readerでスクレイピング
# 結果をLLMでまとめる
import config
from typing import List
from pydantic import BaseModel
from loguru import logger
from jinja2 import Template
from loguru import logger

# debug
import litellm
litellm.set_verbose=True

class Keywords(BaseModel):
    keywords: List[str]
class SearchTopic(BaseModel):
    keyword: str
    fact: str
    word_for_search: str | None = None

class SearchTopicsResponse(BaseModel):
    search_topics: List[SearchTopic]


def generate_search_keywords(keyword: str) -> Keywords:
    """
    トピックに関連する雑学を検索するためのキーワードを生成します。

    引数:
        keyword (str): 検索のベースとなるトピック

    戻り値:
        list[str]: トピックに関連する雑学を検索するためのキーワードのリスト
    """
    assert isinstance(keyword,str)
    keywords = [
        f"{keyword} 雑学",
        f"{keyword} 豆知識",
        f"{keyword} 面白い事実",
        f"{keyword} 意外な情報",
        f"{keyword} トリビア",
        f"{keyword} 歴史",
        f"{keyword} 統計",
        f"{keyword} 秘密",
        f"{keyword} 真実",
        f"{keyword} 逸話",
        f"{keyword} パラドックス"
    ]
    logger.info(f"keywords: {keywords}")
    
    return Keywords(keywords=keywords)



def find_interesting_topics(keywords: Keywords) -> SearchTopicsResponse:
    """
    検索キーワードのリストから、LLMを使用して興味深い事実を検索します。

    引数:
        keywords (List[str]): 検索キーワードのリスト

    戻り値:
        SearchTopicsResponse: LLMの応答
    """
    assert isinstance(keywords,Keywords)
    prompt = f"""
    # 命令
    以下のキーワードリストに関する興味深い具体的な事実を教えてください。英語で思考してください。

    # 検索キーワード:
    {', '.join(keywords.keywords)}

    """
    response = config.client.messages.create(
    response_model=SearchTopicsResponse,
    messages=[
        {"role": "user", "content": prompt},
    ],
    )
    assert isinstance(response,SearchTopicsResponse)
    logger.info(response.model_dump())
    return response


def select_topics(search_topics: SearchTopicsResponse, n: int = 3) -> SearchTopicsResponse:
    """
    LLMを使用して、検索された事実から特に興味深いものを選択します。

    引数:
        search_topics (SearchTopicsResponse): 検索された事実のリスト

    戻り値:
        SearchTopicsResponse: 選択された事実のリスト
    """
    assert isinstance(search_topics,SearchTopicsResponse)
    source = """
    # 命令
    以下の候補の中から、確かな情報で、かつ特に興味深いものを{{n}}個選択してください。
    その上で、選んだ候補についてのWeb検索のためのキーワードを提供してください。
    英語で思考してください。

    候補:
    {% for search_topic in search_topics.search_topics %}
    - {{search_topic.keyword}}: {{search_topic.fact}}
    {% endfor %}
    """
    template = Template(source=source)
    prompt = template.render(search_topics=search_topics,n=n)
    logger.info(prompt)

    response = config.client.messages.create(
    response_model=SearchTopicsResponse,
    messages=[
        {"role": "user", "content": prompt},
    ],
    )
    assert isinstance(response,SearchTopicsResponse)
    return response

def make_search_words(search_topics: SearchTopicsResponse) -> SearchTopicsResponse:
    """
    選択された事実から、Web検索のためのキーワードを生成します。

    引数:
        search_topics (SearchTopicsResponse): 選択された事実のリスト

    戻り値:
        SearchKeywords: Web検索のためのキーワードのリスト
    """
    assert isinstance(search_topics,SearchTopicsResponse)
    assert all(isinstance(search_topic,SearchTopic) for search_topic in search_topics.search_topics)
    assert all(search_topic.word_for_search is None for search_topic in search_topics.search_topics)
    source = """
    # 命令
    以下の検索トピックから、それぞれのWeb検索のためのキーワード(word_for_search)を生成してください。
    英語で思考してください。
    
    # 検索トピック:
    {% for search_topic in search_topics.search_topics %}
        - {{search_topic.keyword}}: {{search_topic.fact}}
    {% endfor %}
    """
    template = Template(source=source)
    prompt = template.render(search_topics=search_topics)
    logger.info(prompt)

    response = config.client.messages.create(
    response_model=SearchTopicsResponse,
    messages=[
        {"role": "user", "content": prompt},
    ],
    )
    assert isinstance(response,SearchTopicsResponse)
    return response

if __name__=="__main__":

    topic = "誕生日"
    keywords = generate_search_keywords(topic)
    logger.info(f"keywords: {keywords}")
    res = find_interesting_topics(keywords)
    logger.info(f"find_interesting_topics: {res}")
    selected_topics = select_topics(res)
    logger.info(f"selected_topics: {selected_topics}")
    search_keywords = make_search_words(selected_topics)
    logger.info(f"search_keywords: {search_keywords}")
