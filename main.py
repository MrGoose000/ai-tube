import os
import requests
import random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx.resize import resize
from moviepy.audio.fx.all import volumex
from elevenlabs import generate, save

# Функция для получения рандомного видео с Pexels
def get_random_video(api_key, query="sea"):
    headers = {
        "Authorization": api_key
    }
    response = requests.get(f"https://api.pexels.com/videos/search?query={query}&per_page=1&page={random.randint(1, 10)}", headers=headers)
    response.raise_for_status()
    video_url = response.json()["videos"][0]["video_files"][0]["link"]
    video_data = requests.get(video_url)
    with open("random_video.mp4", "wb") as video_file:
        video_file.write(video_data.content)
    return "random_video.mp4"

# Функция для получения рандомного факта
def get_random_fact():
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    response.raise_for_status()
    fact = response.json()["text"]
    return fact

# Функция для озвучивания текста с использованием elevenlabs
def text_to_speech_elevenlabs(text, api_key, filename="fact.mp3"):
    audio = generate(text=text, api_key=api_key, voice="Rachel")
    save(audio, filename)
    return filename

# Функция для создания вертикального видео с текстом
def create_video(video_file, audio_file, text, output_file="final_video.mp4"):
    # Загружаем видео и аудио
    video_clip = VideoFileClip(video_file).resize((1080, 1920))
    audio_clip = volumex(AudioFileClip(audio_file), 1.5)

    # Создаем текстовый клип
    text_clip = TextClip(text, fontsize=70, color='white', size=video_clip.size, method='caption', align='center')
    text_clip = text_clip.set_duration(audio_clip.duration).set_position('center')

    # Композиция видео и текста
    final_clip = CompositeVideoClip([video_clip.set_audio(audio_clip), text_clip.set_start(0).set_duration(audio_clip.duration)])
    final_clip = final_clip.set_duration(audio_clip.duration)
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

# Параметры API
PEXELS_API_KEY = "GhNiX6aABCvIYZJuRJjmda802epYvvWxxGlg3NNZdUGS9jTLdyeLdhbV"
ELEVENLABS_API_KEY = "9d9d2a1f204cbedc80a0cfc4d96711ba"

# Получаем рандомное видео
video_file = get_random_video(PEXELS_API_KEY)

# Получаем рандомный факт
fact = get_random_fact()

# Добавляем паузы для увеличения времени озвучивания до 15 секунд
fact_with_pauses = ". ".join(fact.split()) + ". " * 10

# Озвучиваем факт с использованием elevenlabs
audio_file = text_to_speech_elevenlabs(fact_with_pauses, ELEVENLABS_API_KEY)

# Создаем финальное видео
create_video(video_file, audio_file, fact)
