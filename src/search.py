# トピックを入力すると、それに関する雑学を返す
# １。トピックから検索ワードを生成
# ２。GooglesearchAPIでそれらを検索
# ３。検索したURLsが返ってくるのでそれをjina readerでスクレイピング
# 結果をLLMでまとめる
import config
from typing import List
from pydantic import BaseModel
from loguru import logger

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
    検索キーワードのリストから、LLMを使用して雑学を検索します。

    引数:
        keywords (List[str]): 検索キーワードのリスト

    戻り値:
        str: LLMの応答
    """
    prompt = f"""
    # 命令
    以下のキーワードリストに関する興味深い具体的な事実を教えてください。英語で出力してください。

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

if __name__=="__main__":
    topic = "誕生日"
    keywords = generate_search_keywords(topic)
    response = find_interesting_topics(keywords)
    print(response)

