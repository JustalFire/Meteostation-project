import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json

k = "e6a0b01b5cf0014491cb954b85cef04a"
u = "metric" # Нужен для градусов
l = "ru" # Нужен для ответа API

# Список городов: название, id для текущей погоды, широта, долгота
c = {"Таллинн": {"id": 588409, "lat": 59.4370, "lon": 24.7536},"Хельсинки": {"id": 658226, "lat": 60.1699, "lon": 24.9384},"Рига": {"id": 456172, "lat": 56.9496, "lon": 24.1052},"Москва": {"id": 524901, "lat": 55.7558, "lon": 37.6173},"Лондон": {"id": 2643743, "lat": 51.5074, "lon": -0.1278},"Санкт-Петербург": {"id": 498817, "lat": 59.9311, "lon": 30.3609},"Нарва": {"id": 588454, "lat": 59.3772, "lon": 28.1904},}
url = "https://api.openweathermap.org/data/2.5/"

def get_data(u, p):
    q = urllib.parse.urlencode(p)
    full = f"{u}?{q}"
    with urllib.request.urlopen(full) as r:
        d = r.read().decode('utf-8')
    return json.loads(d)

def get_weather(i):
    p = {"id": i, "appid": k, "units": u, "lang": l} #Возвращает строку с текущей погодой для заданного id города
    d = get_data(url + "weather", p)
    # Коды ниже Формируют строку с описанием погоды и основными параметрами
    w = d['weather'][0]['description']
    t = d['main']['temp']
    f = d['main']['feels_like']
    h = d['main']['humidity']
    p = d['main']['pressure']
    return f"{w}, Темп: {t}°C (как {f}°C), Влажн: {h}%, Давл: {p}"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Погода")
        self.geom = "500x400"
        self.geometry(self.geom)
        
        self.c = tk.StringVar()
        self.c.set(list(c.keys())[0])
        self.make_stuff()
    
    def make_stuff(self):
        f = ttk.Frame(self)
        f.pack()
        
        ttk.Label(f, text="Город:").pack()
        ttk.OptionMenu(f, self.c, self.c.get(), *c.keys()).pack()
        
        b = ttk.Button(f, text="Погода сейчас", command=self.show)
        b.pack()
        
        self.t = tk.Text(f)
        self.t.pack()
    
    def show(self): #Обработчик для кнопки ‘Прогноз погоды на сегодня
        n = self.c.get()  # получаем выбранный город
        try:
            w = get_weather(c[n]['id'])
            self.t.delete("1.0", "end") # Этот скрипт очищает предыдущий запрос
            self.t.insert("1.0", f"В {n}:\n{w}")
        except:
            messagebox.showerror("Ошибка", "Данные не найдены")

if __name__ == '__main__':
    a = App()
    a.mainloop()