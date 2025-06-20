import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json

API_KEY = "e6a0b01b5cf0014491cb954b85cef04a"
UNITS = "metric"
LANG = "ru"


CITIES = {
    "Таллинн": {"id": 588409, "lat": 59.4370, "lon": 24.7536},
    "Хельсинки": {"id": 658226, "lat": 60.1699, "lon": 24.9384},
    "Рига": {"id": 456172, "lat": 56.9496, "lon": 24.1052},
    "Москва": {"id": 524901, "lat": 55.7558, "lon": 37.6173},
    "Лондон": {"id": 2643743, "lat": 51.5074, "lon": -0.1278},
    "Санкт-Петербург": {"id": 498817, "lat": 59.9311, "lon": 30.3609},
    "Нарва": {"id": 588454, "lat": 59.3772, "lon": 28.1904},
}
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def get_data(url, params):
    """
    Получает данные от API через HTTP-запрос
    param url URL API-конечной точки
    param params Параметры запроса
    return JSON-объект с данными
    """
    #Формирует строку запроса из параметров
    query = urllib.parse.urlencode(params)
    #Собирает полный URL с параметрами
    full_url = f"{url}?{query}"
    
    #Выполняет HTTP-запрос
    with urllib.request.urlopen(full_url) as res:
        #Читает и декодирует ответ
        data = res.read().decode('utf-8')
    
    #Преобразует JSON строку в объект Python
    return json.loads(data)

def get_weather(city_id):
    """
    Получает текущую погоду для указанного города
    param city_id ID города в OpenWeatherMap
    return Форматированная строка с данными о погоде
    """
    #Параметры для запроса текущей погоды
    params = {
        "id": city_id,
        "appid": API_KEY,
        "units": UNITS,
        "lang": LANG  
    }
    
   
    data = get_data(BASE_URL + "weather", params)
    
    #Извлекает нужные данные из JSON ответа
    desc = data['weather'][0]['description']
    temp = data['main']['temp']
    feels = data['main']['feels_like'] 
    hum = data['main']['humidity'] #Влажность (%)
    press = data['main']['pressure'] 
    
    #Форматирует результат в читаемую строку
    return (
        f"{desc}, \nТемп: {temp}°C (ощущаеться как: {feels}°C), "
        f"\nВлажность: {hum}%, \nДавление: {press} АТМ"
    )

class WeatherApp(tk.Tk):
    """Главное окно приложения для отображения погоды"""
    
    def __init__(self):
        super().__init__()
        self.title("Meteostation Project by Ruslan and Timur")
        self.geometry("500x400")
        
        #Переменная для выбранного города
        self.city_var = tk.StringVar()
        #Устанавливает первый город по умолчанию
        self.city_var.set(list(CITIES.keys())[0])
        self.create_ui()
    
    def create_ui(self):
        """Создает пользовательский интерфейс"""
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Город:").pack(pady=5)
        
        #Выпадающий список для выбора города
        city_menu = ttk.OptionMenu(
            frame,
            self.city_var,          #Привязанная переменная
            self.city_var.get(),    #Изначально заданный город
            *CITIES.keys()          #Города которые можно выбрать
        )
        city_menu.pack(pady=5)
        
        #Кнопка для запроса погоды
        btn = ttk.Button(
            frame,
            text="Погода сейчас",       #Текст кнопки
            command=self.show_weather   #Обработчик клика
        )
        btn.pack(pady=10)
        
        #Текстовое поле для вывода погоды
        self.weather_txt = tk.Text(
            frame, 
            height=8,
            width=50
        )
        self.weather_txt.pack(pady=10)
    
    def show_weather(self):
        """Обработчик для отображения текущей погоды"""
        #Получает выбранный город
        city = self.city_var.get()
        
        try:
            #Получает ID города из словаря
            city_id = CITIES[city]["id"]
            #Запрашивает данные о погоде
            weather_info = get_weather(city_id)
            
            #Очищает текстовое поле
            self.weather_txt.delete("1.0", tk.END)
            #Вставляет отформатированные данные
            self.weather_txt.insert(
                "1.0", 
                f"Погода в {city}:\n{weather_info}"
            )
        except Exception as e:
            #бработка ошибок с показом сообщения
            messagebox.showerror(
                "Ошибка", 
                f"Ошибка данных: {str(e)}"
            )

#Точка входа в приложение
if __name__ == '__main__':
    app = WeatherApp()  #Создаёт прилоение
    app.mainloop()      #Запускает обработку
