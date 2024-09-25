# トピックを入力すると、それに関する雑学を返す
# １。トピックから検索ワードを生成
# ２。GooglesearchAPIでそれらを検索
# ３。検索したURLsが返ってくるのでそれをjina readerでスクレイピング
# 結果をLLMでまとめる


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
    ]
    
    return keywords

from typing import List
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])

def find_interesting_topics(keywords: List[str], n: int = 3) -> List[str]:
    """
    検索キーワードのリストから、Geminiを使用して最も興味を惹きそうなトピックをn個探します。

    引数:
        keywords (List[str]): 検索キーワードのリスト
        n (int): 返すトピックの数（デフォルトは3）

    戻り値:
        List[str]: 最も興味深いと判断されたトピックのリスト
    """
    model = GenerativeModel('gemini-pro')
    prompt = f"""
    以下の検索キーワードリストから、最も興味深く、人々の注目を集めそうなトピックを{n}個選んでください。
    選んだトピックには、簡単な理由も付け加えてください。

    検索キーワード:
    {', '.join(keywords)}

    回答は以下の形式で提供してください：
    1. [トピック]: [選んだ理由]
    2. [トピック]: [選んだ理由]
    3. [トピック]: [選んだ理由]
    """

    response = model.generate_content(prompt)
    topics = [line.split(':')[0].strip() for line in response.text.split('\n') if line.strip()]

    return topics[:n]
