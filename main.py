import os
import requests
import random
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from gtts import gTTS

# Функция для получения рандомного видео с Pexels
def get_random_video(api_key, query="sea"):
    headers = {
        "Authorization": api_key
    }
    response = requests.get(f"https://api.pexels.com/videos/search?query={query}&per_page=1&page={random.randint(1, 10)}", headers=headers)
    response.raise_for_status()  # Проверка на успешность запроса
    video_url = response.json()["videos"][0]["video_files"][0]["link"]
    video_data = requests.get(video_url)
    with open("random_video.mp4", "wb") as video_file:
        video_file.write(video_data.content)
    return "random_video.mp4"

# Функция для получения рандомного факта
def get_random_fact():
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    response.raise_for_status()  # Проверка на успешность запроса
    fact = response.json()["text"]
    return fact

# Функция для озвучивания текста
def text_to_speech(text, filename="fact.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# Основная функция для создания видео
def create_video(video_file, audio_file, output_file="final_video.mp4"):
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)

    # Создаем CompositeVideoClip, чтобы добавить аудио к видео
    final_clip = CompositeVideoClip([video_clip.set_audio(audio_clip)])
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

# Параметры API Pexels
PEXELS_API_KEY = "GhNiX6aABCvIYZJuRJjmda802epYvvWxxGlg3NNZdUGS9jTLdyeLdhbV"

# Получаем рандомное видео
video_file = get_random_video(PEXELS_API_KEY)

# Получаем рандомный факт
fact = get_random_fact()

# Озвучиваем факт
audio_file = text_to_speech(fact)

# Создаем финальное видео
create_video(video_file, audio_file)
