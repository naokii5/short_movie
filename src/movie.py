from image_gen import DraftImages
from moviepy.editor import AudioFileClip, concatenate_audioclips, ImageClip, VideoClip
import PIL
from PIL import Image, ImageFile
import base64
from io import BytesIO
import tempfile

def add_tiktok_margin(pil_img: ImageFile.ImageFile) -> ImageFile.ImageFile:
    _, height = pil_img.size
    new_width = 1080
    new_height = 1920
    # left = (new_width - width) // 2
    top = (new_height - height) // 2
    result = Image.new(pil_img.mode, (new_width, new_height), (255, 255, 255))
    result.paste(pil_img, (0, top))
    return result

def create_movie(voice_list: list[bytes], draftimages: DraftImages)->VideoClip:
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

    # 写真を読み込んでリサイズ
    image_list = []
    for _,image_b64 in draftimages.content_images:
        image_data = base64.b64decode(image_b64)
        image_bytes = BytesIO(image_data)
        image = Image.open(image_bytes)
        image_resized = add_tiktok_margin(image)
        image_list.append(image_resized)

    # 音声を読み込んで画像と結合
    clips = []
    for voice in voice_list:
        with tempfile.NamedTemporaryFile(delete=True) as temp_audio_file:
        
            temp_audio_file.write(voice)
            temp_audio_file.flush() 

             # 一時ファイルのパスを取得
            temp_audio_file_path = temp_audio_file.name
            
            # AudioFileClipを使って音声を開く
            temp_audio_clip = AudioFileClip(temp_audio_file_path)
            # 音声の長さを取得
            duration = temp_audio_clip.duration
            clips.append((temp_audio_clip, duration))
            temp_audio_clip.close()

    audio_clip = concatenate_audioclips(clips)
    for (audio,duration),image in zip(audio_clip,image_list):
        image_clip = ImageClip(image)
        video_clip = image_clip.set_duration(duration)
        final_clip = video_clip.set_audio(audio)
        final_clip.write_videofile(f"test_data/output_{draftimages.keyword}.mp4", fps=24)
    return final_clip



if __name__ == "__main__":
    ...





