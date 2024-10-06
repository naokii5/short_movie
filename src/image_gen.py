from config import openai_client, gemini_flash
from draft import Draft
from pydantic import BaseModel
from loguru import logger

class DraftImages(BaseModel):
    keyword: str
    content_images: list[tuple[str, bytes]]

def image_prompt(content: str)->str:
    """
    下書きを元に画像生成のプロンプトを作成します。

    Args:
        content (str): 下書きの文章

    Returns:
        str: 画像生成のプロンプト
    """
    assert isinstance(content, str)
    prompt = f"""
    以下の文章を出している間に表示されるアニメ風画像はどんな構図のものがいいでしょうか？英語で思考してください。
    文章：{content}
    """
    try:
      im_prompt = gemini_flash.generate_content(prompt)
      logger.info(f"im_prompt: {im_prompt._result.candidates[0].content.parts[0].text}")
    except Exception as e:
      print(e)

    return im_prompt._result.candidates[0].content.parts[0].text

    

def image_from_draft(draft: Draft)->DraftImages:
    """
    下書きを元に画像を生成します。

    Args:
        draft (Draft): 下書き

    Returns:
        list[dict]: 生成された画像のリスト
    """
    assert isinstance(draft, Draft)
    content_images = []
    for content in draft.content:
        prompt = image_prompt(content)
        image = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024", # ['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024'] 
            response_format="b64_json",
        )
        content_images.append((content, image.data[0].b64_json))
    return DraftImages(keyword=draft.keyword, content_images=content_images)

if __name__ == "__main__":
    from draft import Draft
    import base64
    draft = Draft(keyword="誕生日", content=["The birthday paradox is a problem that asks how many people are needed in a room for it to be more likely than not that two of them share a birthday."])
    draft_images = image_from_draft(draft)
    # print(draft_images)
    print("done generating images")
    for i, (content, image) in enumerate(draft_images.content_images):
        with open(f"test_data/output_{i}.png", "wb") as f:
            f.write(base64.b64decode(image))

      