import os
import subprocess
import pyttsx3
import pygame
import psutil
import speech_recognition as sr
import requests
import json
import asyncio
import time
import threading

import tkinter as tk
from interface3 import ShowingGif, root
from interface import ShowingGif , root

# Укажите ваш токен Hugging Face
api_key = "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"

# URL для модели на Hugging Face (например, модель GPT-2)
api_url = "https://api-inference.huggingface.co/models/distilgpt2"

headers = {
    "Authorization": f"Bearer {api_key}"
}

# Инициализация Pygame и pyttsx3
pygame.mixer.init()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

# Путь к скриптам
intteliji_path = r"C:\Users\erten\Desktop\Jatvis2\Scripts\IntelijiIdea.ahk"
shazam_path = r"C:\Users\erten\Desktop\Jatvis2\Scripts\Shazam.ahk"
telegram_path = r"C:\Users\erten\Desktop\Jatvis2\Scripts\Telegram.ahk"
calculator_script_path = r"C:\Users\erten\Desktop\Jatvis2\Scripts\Calculator.ahk"
chrome_script_path = r"C:\Users\erten\Desktop\Jatvis2\Scripts\Chrome.ahk"
whatsapp_script_path = r"C:\Users\erten\Desktop\Jatvis2\Scripts\WhatsApp.ahk"
intellij_path = r"C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2024.2.1\bin\idea64.exe"
screenshort_path = r"C:\Users\erten\Desktop\Jatvis2\Scripts\Screnshot.ahk"

# Пути к файлам
greeting_sound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\greeting.mp3'
jarvis_sound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\sound-1_cBqZb05.mp3'
jarvisintroduce = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\jarvis-intro-1.mp3'
connectsound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\jarvis_connected.mp3'
disconnectsound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\jarvis_disconnected.mp3'

# Глобальная переменная для gif_player
gif_player = None
introgif =None

# Асинхронные функции
async def play_music(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

def play_music_paralell(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

def play_greeting_music():
    play_music_paralell(greeting_sound)

def play_introduce_music():
    play_music_paralell(jarvisintroduce)


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

# Синхронная функция для распознавания речи и выполнения команд
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

            # Обработка команд
            for key, action in commands.items():
                if key in command:
                    action()
                    break
            else:
                # Вызов Hugging Face для ответов на вопросы
                asyncio.run(handle_huggingface_command(command))

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from the recognition service: {e}")

# Асинхронная функция для Hugging Face
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
    "what's up": lambda: script(whatsapp_script_path),
    "telegram": lambda: script(telegram_path),
    "shazam": lambda: script(shazam_path),
    "introduce yourself": lambda: asyncio.run(showgifintro()),
    "lock the screen": lambda: os.system("rundll32.exe user32.dll,LockWorkStation"),
    "turn off": lambda: os.system("shutdown /s /t 1"),
    "weather": lambda: asyncio.run(get_weather()),
    "screenshort": lambda: script(screenshort_path),
    "jarvis": lambda: asyncio.run(play_music(jarvis_sound)),
    "taurus": lambda: asyncio.run(play_music(jarvis_sound)),
    "chinese": lambda: asyncio.run(play_music(jarvis_sound))
}






# Запуск скрипта
def script(path):
    subprocess.run([r"C:\Program Files\AutoHotkey\v1.1.37.02\AutoHotkeyU64.exe", path])

def start_showing_gif():
    global gif_player  # Объявляем gif_player как глобальную переменную
    gif_player.show_gif('speak', duration=13000)

def introduce_showing_gif():
    global introgif  # Объявляем gif_player как глобальную переменную
    intro.show_gif('introduce', duration=20000)

async def showgifintro():
    global introgif  # Объявляем gif_player как глобальную переменную
    play_introduce_music()

    gif_lb = tk.Label(root, bg='#000000')
    gif_lb.pack(fill=tk.BOTH, expand=True)

    introgif = ShowingGif(gif_lb, size=(200, 344))
    root.after(0, start_showing_gif)
    root.mainloop()

async def showgif():
    global gif_player  # Объявляем gif_player как глобальную переменную
    play_greeting_music()

    # Запускаем основной цикл Tkinter
    gif_lb = tk.Label(root, bg='#000000')
    gif_lb.pack(fill=tk.BOTH, expand=True)

    gif_player = ShowingGif(gif_lb, size=(200, 344))

    # Используем root.after() для запуска показ GIF
    root.after(0, start_showing_gif)
    root.mainloop()
    gif_player =None


if __name__ == "__main__":
    asyncio.run(showgif())
    # asyncio.run(check_battery())
    # asyncio.run(asyncio.sleep(2))
    # asyncio.run(get_weather())
    main()
