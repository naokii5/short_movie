import config
from loguru import logger
from search import ScrapeData
from pydantic import BaseModel

class TalkScript(BaseModel):
    title: str
    content: str

def make_draft(scrape_data_list: list[ScrapeData]) -> str:
    """
    スクレイピングしたデータを元に、下書きを作成します。

    引数:
        scrape_data (dict[str, list[tuple[str, str]]): スクレイピングしたデータ

    戻り値:
        str: 動画の台本
    """
    assert all(isinstance(scrape_data, ScrapeData) for scrape_data in scrape_data_list)
    draft = ""
    for scrape_data in scrape_data_list:
        draft += f"# {scrape_data.keyword}\n\n"
        for data in scrape_data.data:
            draft += f"## {data.url}\n\n{data.text}\n\n"
    logger.info(f"draft: {draft}")
    # jinja2を使うとdraftが読み込まれないので、f-stringを使う
    source = f"""
    # 命令
    以下の内容を参考に、小学生でもなんとなく分かる短い動画の台本を作成してください。
    動画は淡々とした語り口で進行し、視聴者に知識を提供することを目的としていますが、ときには面白いエピソードを交えても構いません。
    また、情報源の全てを使う必要はありません。必要な情報を選んで使ってください。
    # 情報源
    """
    prompt = source + draft
    logger.info(f"prompt: {prompt}")
    # instructorを使うとなぜかエラーが出るので、config.gemini_flashを使う
    response = config.gemini_flash.generate_content(prompt)

    logger.info(f"response: {response})")
    
    return response._result.candidates[0].content.parts[0].text


if __name__ == "__main__":
    from search import URLData, scrape_urls
    urls = [URLData(keyword="誕生日", urls=["https://en.wikipedia.org/wiki/Birthday_problem"], meta_data="birthday paradox")]
    scrape_data = scrape_urls(urls)
    draft = make_draft(scrape_data)
    # print(draft)

            

    