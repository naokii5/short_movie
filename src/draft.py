from jinja2 import Template
import config
from loguru import logger


def make_draft(scrape_data: dict[tuple[str,str]]):
    """
    スクレイピングしたデータを元に、下書きを作成します。

    引数:
        scrape_data (dict[str, list[tuple[str, str]]): スクレイピングしたデータ

    戻り値:
        list[TalkTopic]: 下書きのリスト
    """
    assert isinstance(scrape_data, dict)
    talk_topics = []
    draft = ""
    for keyword, data_with_url in scrape_data.items():
        draft += f"# {keyword}\n\n"
        for data,url in data_with_url:
            draft += f"## {data}\n\n"
            draft += f"[{url}]({url})\n\n"
    source = f"""
    # 命令
    以下のトークスライドをの下書きを参考に、短い動画の台本を作成してください。特定の雑学についての台本を作成してください。
    # トークスライドの下書き
    {{draft}}
    """
    template = Template(source=source)
    prompt = template.render(draft=draft)
    response = config.client.messages.create(
    messages=[
        {"role": "user", "content": prompt},
    ],
    )

    logger.info(response.model_dump())
    return response


if __name__ == "__main__":

    draft = make_draft(scrape_data)
    print(draft)

            

    