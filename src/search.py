# トピックを入力すると、それに関する雑学を返す
# １。トピックから検索ワードを生成
# ２。GooglesearchAPIでそれらを検索
# ３。検索したURLsが返ってくるのでそれをjina readerでスクレイピング
# 結果をLLMでまとめる
import config as config
from typing import List
from litellm import completion

# debug
import litellm
litellm.set_verbose=True

gemini_api_key = config.gemini_api_key
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
        f"意外 {topic} 真実",
        f"{topic} 逸話",
        f"{topic} パラドックス"
    ]
    
    return keywords



def find_interesting_topics(keywords: List[str], model:str = "gemini/gemini-1.5-pro-latest") -> str:
    """
    検索キーワードのリストから、LLMを使用して雑学を検索します。

    引数:
        keywords (List[str]): 検索キーワードのリスト

    戻り値:
        str: LLMの応答
    """
    model = model
    prompt = f"""
    # 命令
    以下のキーワードリストに関する興味深い具体的な事実を教えてください。英語で思考して日本語で答えてください。

    # 検索キーワード:
    {', '.join(keywords)}

    # 解答形式：
    1. [キーワード]: [詳細]
    2. [キーワード]: [詳細]
    3. [キーワード]: [詳細]
    ...
    n. [キーワード]: [詳細]
    """

    response = completion(
    model=model, 
    messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__=="__main__":
    print("hey")
    topic = "誕生日"
    keywords = generate_search_keywords(topic)
    response = find_interesting_topics(keywords)
    print(response)
