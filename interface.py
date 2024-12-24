import os
import subprocess
import pyttsx3
import pygame
import psutil
import speech_recognition as sr
import requests
import json
import asyncio
import threading
import tkinter as tk
from PIL import Image, ImageTk, ImageFile

# Разрешаем загрузку усеченных изображений
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Инициализация Pygame и pyttsx3
pygame.mixer.init()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

# Пути к файлам и звуковым файлам
jarvis_path = r'C:\Users\erten\Desktop\Jatvis2\Animation\9c046e14e6ca7754d21dcd5c0deceea6.gif'
introduce_path = r'C:\Users\erten\Desktop\Jatvis2\Animation\introduce.gif'
speak_path = r'C:\Users\erten\Desktop\Jatvis2\Animation\speak.gif'


# Инициализация основного окна
root = tk.Tk()
root.geometry('300x200')
root.title('Tkinter Hub')
root.configure(bg='#000000')

# Класс для отображения GIF
class ShowingGif:
    def __init__(self, label, size=(200, 322)):
        self.label = label
        self.gif_frames = []
        self.frame_count = -1
        self.frame_delay = 100
        self.new_size = size
        self.playing = False

    def show_gif(self, text, duration=5000):
        try:
            if text == 'jarvis':
                gif_file = Image.open(jarvis_path)
            elif text == 'introduce':
                gif_file = Image.open(introduce_path)
            elif text == 'speak':
                gif_file = Image.open(speak_path)
            else:
                print("Invalid GIF type specified.")
                return

            self.gif_frames.clear()
            self.frame_count = -1

            for frame in range(gif_file.n_frames):
                gif_file.seek(frame)
                resized_frame = gif_file.copy().resize(self.new_size, Image.LANCZOS)
                self.gif_frames.append(resized_frame)

            self.frame_delay = gif_file.info.get('duration', 100)
            self.playing = True

            self.play_gif()
            root.after(duration, self.stop_gif)
        except FileNotFoundError:
            print("GIF file not found. Please check the file path.")
        except OSError as e:
            print(f"Error loading GIF: {e}")

    def play_gif(self):
        if not self.gif_frames or not self.playing:
            return
        self.frame_count = (self.frame_count + 1) % len(self.gif_frames)
        current_frame = ImageTk.PhotoImage(self.gif_frames[self.frame_count])

        self.label.config(image=current_frame)
        self.label.image = current_frame
        if self.playing:
            root.after(self.frame_delay, self.play_gif)

    def stop_gif(self):
        self.playing = False
        root.destroy()

# Асинхронные функции
async def play_music(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

async def answer_jarvis(text):
    engine.say(text)
    engine.runAndWait()

async def get_weather():
    api_key = "142bc4ff3fc84745f3cbdf5b389a4db5"
    city = "Kaskelen"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        await answer_jarvis(f"Weather in {city}: {temperature}°C. Weather description: {weather_description}")
    else:
        print(f"Error: {data['message']}")

# Синхронная функция для распознавания речи и выполнения команд
def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        with microphone as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language="en-US").lower()
            print(f"You said: {command}")
            if command == "stop":
                break
            elif command == "introduce yourself":
                play_introduce_gif()
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from the recognition service: {e}")

# Функция для запуска introduce GIF
def play_introduce_gif():
    gif_label = tk.Label(root, bg='#000000')
    gif_label.pack(fill=tk.BOTH, expand=True)
    gif_player = ShowingGif(gif_label, size=(200, 344))
    gif_player.show_gif("introduce", duration=5000)

# Запуск программы
if __name__ == "__main__":
    threading.Thread(target=main).start()
    root.mainloop()
