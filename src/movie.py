from moviepy.editor import AudioFileClip, concatenate_audioclips, ImageClip
import os
from moviepy.video.fx.resize import resize
from PIL import Image, ImageFile

def add_tiktok_margin(pil_img: ImageFile.ImageFile) -> ImageFile.ImageFile:
    width, height = pil_img.size
    new_width = 1080
    new_height = 1920
    # left = (new_width - width) // 2
    top = (new_height - height) // 4
    result = Image.new(pil_img.mode, (new_width, new_height), (255, 255, 255))
    result.paste(pil_img, (0, top))
    return result

def create_movie(folder_path):
    import PIL
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
    clips = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):
            filepath = os.path.join(folder_path, filename)
            clip = AudioFileClip(filepath)
            clips.append(clip)

    audio_clip = concatenate_audioclips(clips)
    # 静止画と音声ファイルを読み込む
    image_clip = ImageClip("test_data/ai_character07_surprise.png")
    # 静止画クリップの長さを音声の長さに合わせる
    video_clip = image_clip.set_duration(audio_clip.duration)
    # 音声を動画に追加
    final_clip = video_clip.set_audio(audio_clip)
    try:
        video_resized = resize(final_clip,newsize=(1080, 1920))
    except Exception as e:
        print(e)
    video_resized.write_videofile("test_data/output2.mp4", fps=24)
    return video_resized

import wave

def get_wav_duration(file_path):
    with wave.open(file_path, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    return duration



if __name__ == "__main__":
    # create_movie("test_data")
        # 使用例
    # file_path = 'test_data/output.wav'
    # duration = get_wav_duration(file_path)
    # print(duration)
    # print(f"音声の長さ: {duration:.2f}秒")

    from PIL import Image

    im = Image.open('test_data/ai_character07_surprise.png')
    im_new = add_tiktok_margin(im)
    im_new.save('test_data/ai_character07_surprise_margin.png')





