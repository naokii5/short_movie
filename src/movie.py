from moviepy.editor import AudioFileClip, concatenate_audioclips, ImageClip
import os

def create_movie(folder_path):
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
    final_clip.write_videofile("test_data/output.mp4", fps=24)
    return final_clip

import wave

def get_wav_duration(file_path):
    with wave.open(file_path, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    return duration



if __name__ == "__main__":
    create_movie("test_data")
        # 使用例
    file_path = 'test_data/output.wav'
    duration = get_wav_duration(file_path)
    print(duration)
    print(f"音声の長さ: {duration:.2f}秒")





