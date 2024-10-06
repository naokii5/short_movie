from image_gen import DraftImages
from moviepy.editor import AudioFileClip, concatenate_audioclips, ImageClip, VideoClip, concatenate_videoclips, VideoFileClip,CompositeVideoClip
import PIL
from PIL import Image, ImageFile
import base64
from io import BytesIO
import tempfile
from voice import Voices
import numpy as np
import os

def add_tiktok_margin(pil_img: ImageFile.ImageFile) -> ImageFile.ImageFile:
    _, height = pil_img.size
    new_width = 1080
    new_height = 1920
    # left = (new_width - width) // 2
    top = (new_height - height) // 2
    result = Image.new(pil_img.mode, (new_width, new_height), (255, 255, 255))
    result.paste(pil_img, (0, top))
    return result

def create_movie(voices: Voices, draftimages: DraftImages)->VideoClip:
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
    durations = []
    for voice_str in voices.voice_bytes:
        voice = base64.b64decode(voice_str)

        with tempfile.NamedTemporaryFile(delete=True, suffix=".m4a") as temp_audio_file:
            temp_audio_file.write(voice)
            temp_audio_file.flush()
            temp_audio_file_path = temp_audio_file.name
            temp_audio_clip = AudioFileClip(temp_audio_file_path)
            duration = temp_audio_clip.duration
            clips.append(temp_audio_clip)
            durations.append(duration)


    video_clips = []
    for audio,duration,image in zip(clips,durations,image_list):
        image_array = np.array(image)
        image_clip = ImageClip(image_array)
        video_clip = image_clip.set_duration(duration)
        video_sound_clip = video_clip.set_audio(audio)
        video_clips.append(video_sound_clip)
        video_sound_clip.close()
        
    final_clip = concatenate_videoclips(video_clips)

    final_clip.write_videofile(f"test_data/output_{draftimages.keyword.replace(' ', '_')}.mp4",fps=24)
    print("output file created")
    print(f"duration: {final_clip.duration}")
    # print(f"audio duration: {audio_clip.duration}")
    final_clip.close()
    return 



if __name__ == "__main__":
    ...





