from config import gemini_flash
from typing import Literal

Lang = Literal["English", "Japanese"]

def translate_with_gemini(text: str,inputlang: Lang, outputlang: Lang)->str:
    """
    与えられたテキストを翻訳します。

    Args:
        text (str): 翻訳したいテキスト

    Returns:
        str: 翻訳されたテキスト
    """
    assert isinstance(text, str)
    prompt = f"Translate the following text from {inputlang} to {outputlang}:\n\n{text}"
    response = gemini_flash.generate_content(prompt)
    return response._result.candidates[0].content.parts[0].text

if __name__ == "__main__":
    text = "The birthday paradox is a problem that asks how many people are needed in a room for it to be more likely than not that two of them share a birthday."
    translated_text = translate_with_gemini(text, "English", "Japanese")
    print(translated_text)