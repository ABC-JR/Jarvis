import tkinter as tk
from PIL import Image, ImageTk, ImageFile
import threading

# Разрешаем загрузку усеченных изображений
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Указываем пути к GIF-файлам (обновите пути в соответствии с вашей системой)
jarvis_path = r'C:\Users\erten\Desktop\Jatvis2\Animation\9c046e14e6ca7754d21dcd5c0deceea6.gif'
introduce_path = r'C:\Users\erten\Desktop\Jatvis2\Animation\introduce.gif'
speak_path = r'C:\Users\erten\Desktop\Jatvis2\Animation\speak.gif'


class ShowingGif:
    def __init__(self, label, size=(200, 322)):
        self.label = label
        self.gif_frames = []
        self.frame_count = -1
        self.frame_delay = 100  # Устанавливаем значение по умолчанию
        self.new_size = size    # Задаем размер кадров
        self.playing = False    # Флаг для отслеживания состояния воспроизведения

    def show_gif(self, text, duration=5000):
        try:
            # Выбор GIF-файла
            if text == 'jarvis':
                gif_file = Image.open(jarvis_path)
            elif text == 'introduce':
                gif_file = Image.open(introduce_path)
            elif text == 'speak':
                gif_file = Image.open(speak_path)
            else:
                print("Invalid GIF type specified.")
                return

            # Обнуляем список кадров и фрейм
            self.gif_frames.clear()
            self.frame_count = -1

            # Заполнение списка кадрами GIF с изменением их размера
            for frame in range(gif_file.n_frames):
                gif_file.seek(frame)
                resized_frame = gif_file.copy().resize(self.new_size, Image.LANCZOS)
                self.gif_frames.append(resized_frame)

            # Получение задержки между кадрами
            self.frame_delay = gif_file.info.get('duration', 100)  # По умолчанию 100 мс, если нет значения
            self.playing = True  # Включаем флаг воспроизведения

            # Запускаем воспроизведение GIF
            self.play_gif()

            # Останавливаем GIF и закрываем окно через указанное время
            self.label.after(duration, self.stop_gif)
        except FileNotFoundError:
            print("GIF file not found. Please check the file path.")
        except OSError as e:
            print(f"Error loading GIF: {e}")

    def play_gif(self):
        if not self.gif_frames or not self.playing:
            return  # Остановка, если неактивно

        # Переход к следующему кадру
        self.frame_count = (self.frame_count + 1) % len(self.gif_frames)
        current_frame = ImageTk.PhotoImage(self.gif_frames[self.frame_count])

        # Обновление метки с GIF
        self.label.config(image=current_frame)
        self.label.image = current_frame  # Сохраняем ссылку на изображение

        # Показать следующий кадр через указанную задержку, только если продолжается воспроизведение
        if self.playing:
            self.label.after(self.frame_delay, self.play_gif)

    def stop_gif(self):
        self.playing = False  # Останавливаем воспроизведение
        self.label.config(image='')  # Очищаем изображение


class GIFController:
    def __init__(self, gif_player):
        self.gif_player = gif_player

    def start_gif(self, gif_type, duration=5000):
        threading.Thread(target=lambda: self.gif_player.show_gif(gif_type, duration), daemon=True).start()
