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
# debug
import litellm
litellm.set_verbose=True

class SearchWord(BaseModel):
    keyword: str
    fact: str

class SearchTopicsResponse(BaseModel):
    search_words: List[SearchWord]

def generate_search_keywords(topic: str) -> list[str]:
    """
    トピックに関連する雑学を検索するためのキーワードを生成します。

    引数:
        topic (str): 検索のベースとなるトピック

    戻り値:
        list[str]: トピックに関連する雑学を検索するためのキーワードのリスト
    """
    assert isinstance(topic,str)
    keywords = [
        f"{topic} 雑学",
        f"{topic} 豆知識",
        f"{topic} 面白い事実",
        f"{topic} 意外な情報",
        f"{topic} トリビア",
        f"{topic} 歴史",
        f"{topic} 統計",
        f"{topic} 秘密",
        f"{topic} 真実",
        f"{topic} 逸話",
        f"{topic} パラドックス"
    ]
    
    return keywords



def find_interesting_topics(keywords: List[str]) -> str:
    """
    検索キーワードのリストから、LLMを使用して興味深い事実を検索します。

    引数:
        keywords (List[str]): 検索キーワードのリスト

    戻り値:
        SearchTopicsResponse: LLMの応答
    """
    assert isinstance(keywords,list)
    prompt = f"""
    # 命令
    以下のキーワードリストに関する興味深い具体的な事実を教えてください。英語で思考してください。

    # 検索キーワード:
    {', '.join(keywords)}

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


def select_topics(search_topics: SearchTopicsResponse) -> str:
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
    以下の候補の中から、確かな情報で、かつ特に興味深いものを3つ選択してください。
    英語で思考してください。

    候補:
    {% for search_word in search_topics.search_words %}
    - {{search_word.keyword}}: {{search_word.fact}}
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
    res = find_interesting_topics(keywords)
    print(res)

    print(select_topics(res))
