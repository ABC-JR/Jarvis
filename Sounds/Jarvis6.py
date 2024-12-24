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
from PIL import Image, ImageTk

pygame.mixer.init()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

jarvis_path_animation = r'C:\Users\erten\Desktop\Jatvis2\Animation\9c046e14e6ca7754d21dcd5c0deceea6.gif'
introduce_path_animation = r'C:\Users\erten\Desktop\Jatvis2\Animation\introducing.gif'
speak_path_animation = r'C:\Users\erten\Desktop\Jatvis2\Animation\speak.gif'

# Инициализация основного окна
root = tk.Tk()
root.geometry('300x200')
root.title('Tkinter Hub')
root.configure(bg='#000000')

# Укажите ваш токен Hugging Face
api_key = "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"

# URL для модели на Hugging Face (например, модель GPT-2)
api_url = "https://api-inference.huggingface.co/models/distilgpt2"
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Пути к файлам и звуковым файлам
greeting_sound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\greeting.mp3'
jarvis_sound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\sound-1_cBqZb05.mp3'
jarvisintroduce = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\jarvis-intro-1.mp3'
connectsound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\jarvis_connected.mp3'
disconnectsound = 'C:\\Users\\erten\\Desktop\\Jatvis2\\Sounds\\jarvis_disconnected.mp3'

# Глобальная переменная для gif_player
gif_frames = []
frame_count = 0
playing = False
frame_delay = 100  # Default frame delay


# Асинхронные функции
async def play_music(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()


async def play_greeting_music():
    await play_music(greeting_sound)


async def play_introduce_music():
    await play_music(jarvisintroduce)


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
                asyncio.gather(showgif('speak', duration=10000), handle_huggingface_command(command))
                # asyncio.run(handle_huggingface_command(command))

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
    "new project": lambda: os.startfile(
        r"C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2024.2.1\bin\idea64.exe"),
    "time": lambda: asyncio.run(answer_jarvis(f"The current time is {time.strftime('%I:%M %p', time.localtime())}")),
    "what's up": lambda: script(r"C:\Users\erten\Desktop\Jatvis2\Scripts\WhatsApp.ahk"),
    "telegram": lambda: script(r"C:\Users\erten\Desktop\Jatvis2\Scripts\Telegram.ahk"),
    "shazam": lambda: script(r"C:\Users\erten\Desktop\Jatvis2\Scripts\Shazam.ahk"),
    "introduce yourself": lambda: asyncio.run(introgif()),
    "lock the screen": lambda: os.system("rundll32.exe user32.dll,LockWorkStation"),
    "turn off": lambda: os.system("shutdown /s /t 1"),
    "weather": lambda: asyncio.run(get_weather()),
    "screenshort": lambda: script(r"C:\Users\erten\Desktop\Jatvis2\Scripts\Screnshot.ahk"),
    "jarvis": lambda: asyncio.run(jarvissoundparalel()),
    "taurus": lambda: asyncio.run(jarvissoundparalel()),
    "chinese": lambda: asyncio.run(jarvissoundparalel())
}


def script(path):
    subprocess.run([r"C:\Program Files\AutoHotkey\v1.1.37.02\AutoHotkeyU64.exe", path])


async def introgif():
    # Параллельно работают GIF и музыка
    await asyncio.gather(showgif('introduce', duration=20000), play_introduce_music())

async def jarvissoundparalel():
    await asyncio.gather(showgif('jarvis', duration=3000), play_music(jarvis_sound))

async def speakfirst():
    await asyncio.gather(showgif('speak' , duration=18000) , play_greeting_music())




async def showgif(text, duration=5000):
    try:
        if text == 'jarvis':
            gif_file = Image.open(jarvis_path_animation)
        elif text == 'introduce':
            gif_file = Image.open(introduce_path_animation)
        elif text == 'speak':
            gif_file = Image.open(speak_path_animation)

        else:
            print("Invalid GIF type specified.")
            return

        gif_frames.clear()
        for frame in range(gif_file.n_frames):
            gif_file.seek(frame)
            resized_frame = gif_file.copy().resize((300, 200), Image.LANCZOS)
            gif_frames.append(resized_frame)

        global playing
        playing = True

        for _ in range(duration // frame_delay):
            if not playing:
                break
            play_gif()
            root.update()  # Обновляем интерфейс
            await asyncio.sleep(frame_delay / 1000.0)  # Convert milliseconds to seconds

    except FileNotFoundError:
        print("GIF file not found. Please check the file path.")
    except OSError as e:
        print(f"Error loading GIF: {e}")


def play_gif():
    global frame_count
    if not gif_frames:
        return
    frame_count = (frame_count + 1) % len(gif_frames)
    current_frame = ImageTk.PhotoImage(gif_frames[frame_count])

    # Обновляем изображение в виджете Tkinter
    label.config(image=current_frame)
    label.image = current_frame


def stop_gif():
    global playing
    playing = False


if __name__ == "__main__":
    label = tk.Label(root)
    label.pack()
    asyncio.run(speakfirst())

    asyncio.run(check_battery())
    asyncio.run(asyncio.sleep(2))  # Задержка перед началом распознавания
    threading.Thread(target=main).start()

    root.protocol("WM_DELETE_WINDOW", stop_gif)  # Остановка GIF при закрытии окна
    root.mainloop()
