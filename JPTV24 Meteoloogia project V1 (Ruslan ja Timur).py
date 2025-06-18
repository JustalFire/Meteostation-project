import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import urllib.request
import urllib.parse
import json

# Конфигурация
API_KEY = "e6a0b01b5cf0014491cb954b85cef04a" # Сам API ключ
UNITS = "metric"  # Нужен для градусов 
LANG = "ru"      # Нужен для ответа API

"""
Снизу используются все локации для показа погоды и дополнительной инфы
"""

# Список городов: название, id для текущей погоды, широта, долгота
LOCATIONS = {"Таллинн":       {"id": 588409,  "lat": 59.4370, "lon": 24.7536}, "Хельсинки":     {"id": 658226,  "lat": 60.1699, "lon": 24.9384}, "Рига":          {"id": 456172,  "lat": 56.9496, "lon": 24.1052}, "Москва":        {"id": 524901,  "lat": 55.7558, "lon": 37.6173}, "Лондон":        {"id": 2643743,"lat": 51.5074, "lon": -0.1278}, "Санкт-Петербург": {"id": 498817, "lat": 59.9311, "lon": 30.3609}, "Кохтла-Ярве (Временно не работает)":    {"id": 588063,  "lat": 59.3589, "lon": 27.2731}, "Йыхви (Временно не работает)":         {"id": 588096,  "lat": 59.3565, "lon": 27.4160}, "Нарва":         {"id": 588454,  "lat": 59.3772, "lon": 28.1904},}
BASE_URL = "https://api.openweathermap.org/data/2.5/"


def fetch_json(url, params):
    """Кодирует парамерты а также делает GET запрос"""
    query = urllib.parse.urlencode(params)  # кодирует параметры в строку
    full_url = f"{url}?{query}"          # формирует полный URL запроса
    with urllib.request.urlopen(full_url) as response:
        data = response.read().decode('utf-8')
    return json.loads(data)                 


def get_current_weather(city_id):
    """Возвращает строку с текущей погодой для заданного id города"""
    params = {"id": city_id, "appid": API_KEY, "units": UNITS, "lang": LANG}
    d = fetch_json(BASE_URL + "weather", params) 
    # Коды ниже Формируют строку с описанием погоды и основными параметрами
    desc = d['weather'][0]['description'].title()
    temp = d['main']['temp']
    feels = d['main']['feels_like']
    hum = d['main']['humidity']
    pres = d['main']['pressure']
    return f"{desc}, Темп: {temp}°C (ощущается {feels}°C), Влажн.: {hum}%, Давл.: {pres} hPa"

class WeatherApp(tk.Tk):
    """Вот тут находится основное окно для приложение и его настройки """
    def __init__(self):
        super().__init__()
        self.title("Метеостанция (By Ruslan and Timur)")
        self.geometry("500x400")

        # Переменная для выбранного города
        self.city_var = tk.StringVar(value=list(LOCATIONS.keys())[0])
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=10)   #Вот тут были добавлены отступы для красоты и удобства
        frame.pack(fill=tk.BOTH, expand=True)

        
        ttk.Label(frame, text="Выберите город:").pack(anchor=tk.W)
        ttk.OptionMenu(frame, self.city_var, self.city_var.get(), *LOCATIONS.keys()).pack(fill=tk.X)

        # Кнопки для запроса погоды
        btnframe = ttk.Frame(frame)
        btnframe.pack(pady=10)
        ttk.Button(btnframe, text="Прогноз погоды на сегодня", command=self.show_current).pack(side=tk.LEFT, padx=5)
       
        # Текстовое поле для вывода результатов
        self.text = tk.Text(frame, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=True)

    def show_current(self):
        """Обработчик для кнопки ‘Прогноз погоды на сегодня’"""
        city = self.city_var.get()                # получаем выбранный город
        try:
            info = get_current_weather(LOCATIONS[city]['id'])
            self.text.delete(1.0, tk.END)         # Этот скрипт очищает предыдущий запрос
            self.text.insert(tk.END, f"Погода в {city}:\n{info}")
        except Exception as e:
            messagebox.showerror("Ошибка", "Данные не найдены")

if __name__ == '__main__':
    app = WeatherApp()
    app.mainloop()
