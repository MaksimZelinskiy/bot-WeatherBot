import requests
import datetime
from pprint import pprint
from config import open_weather_token


def get_weather(city, open_weather_token):
    
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"}


    
    
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри сам в окно, не могу понять, что там происходит((!"

        humidity= data["main"]["humidity"]
        pressure = data ["main"]["pressure"]
        wind = data["wind"]["speed"]
        timetamp_sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]) #рассвет
        timeset_sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) #рассвет
        #lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - (data["sys"]["sunrise"])


        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
        f"Погода в городе: {city}\nТемпература: {cur_weather}C  {wd}\n"
        f"Влажность: {humidity}\nДавление: {pressure} мм. рт.ст\nСкорость ветра: {wind} м/с \n"
        f"Восход солнца: {timetamp_sunrise}\n"
        f"Заход солнца: {timeset_sunrise}\n"
        f"Хорошего дня"
        )
    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def main():
    city = input("Введите свой город: ")
    get_weather(city, open_weather_token)


if __name__ == "__main__":
    main()