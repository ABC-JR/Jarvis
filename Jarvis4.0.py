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

from Jarvis import intellij_path
from interface import ShowingGif, root

# Инициализация Pygame и pyttsx3
pygame.mixer.init()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

# Установите пути к вашим GIF-файлам и звуковым файлам
greeting_sound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\greeting.mp3'
jarvis_sound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\sound-1_cBqZb05.mp3'
jarvisintroduce = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\jarvis-intro-1.mp3'
connectsound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\jarvis_connected.mp3'
disconnectsound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\jarvis_disconnected.mp3'

# Инициализация API Hugging Face
api_key = "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"
api_url = "https://api-inference.huggingface.co/models/distilgpt2"
headers = {"Authorization": f"Bearer {api_key}"}

# Глобальные переменные для GIF
gif_player = None
gif_player_intro = None

# Асинхронные функции
async def play_music(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

def play_music_parallel(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

def play_greeting_music():
    play_music_parallel(greeting_sound)

def play_introduce_music():
    play_music_parallel(jarvisintroduce)

async def answer_jarvis(text):
    engine.say(text)
    engine.runAndWait()

async def check_battery():
    battery = psutil.sensors_battery()
    percent = battery.percent
    plugged = battery.power_plugged
    status = "Connect" if plugged else "Disconnect"

    if status == "Connect":
        print("connected")
        await play_music(connectsound)
    elif status == "Disconnect":
        print("disconnected")
        await play_music(disconnectsound)

async def ask_huggingface(question):
    payload = {"inputs": question}
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data[0]["generated_text"]
    else:
        return f"Error: {response.status_code}, {response.text}"

async def get_weather():
    api_key = "142bc4ff3fc84745f3cbdf5b389a4db5"
    city = "Kaskelen"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        print(f"Weather in {city}: {temperature}°C")
        print(f"Weather description: {weather_description}")
        await answer_jarvis(f"Weather in {city}: {temperature}°C. Weather description: {weather_description}")
    else:
        print(f"Error: {data['message']}")

# Основная функция для распознавания речи и выполнения команд
def main():
    while True:
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        with microphone as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language="en-US").lower()
            print(f"You said: {command}")
            if command == "stop":
                break

            for key, action in commands.items():
                if key in command:
                    action()
                    break
            else:
                asyncio.run(handle_huggingface_command(command))

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from the recognition service: {e}")

async def handle_huggingface_command(command):
    answer_from_huggingface = await ask_huggingface(command)
    print(f"Hugging Face ответил: {answer_from_huggingface}")
    await answer_jarvis(answer_from_huggingface)

# Команды и функции
commands = {
    "chrome": lambda: os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    "calculator": lambda: os.system("calc.exe"),
    "new project": lambda: os.startfile(intellij_path),
    "time": lambda: asyncio.run(answer_jarvis(f"The current time is {time.strftime('%I:%M %p', time.localtime())}")),
    "weather": lambda: asyncio.run(get_weather()),
    "introduce yourself": lambda: asyncio.run(introgif())
}

def start_main_thread():
    main_thread = threading.Thread(target=main)
    main_thread.start()

async def showgif():
    global gif_player
    play_greeting_music()

    gif_lb = tk.Label(root, bg='#000000')
    gif_lb.pack(fill=tk.BOTH, expand=True)

    gif_player = ShowingGif(gif_lb, size=(200, 344))
    root.after(0, lambda: gif_player.show_gif('speak', duration=13000))
    root.mainloop()

def start_tkinter_loop():
    asyncio.run(showgif())

if __name__ == "__main__":
    start_main_thread()
    start_tkinter_loop()
