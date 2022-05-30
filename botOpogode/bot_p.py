import requests
import datetime
from config import tk_telegram_bot, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor



bot = Bot(token=tk_telegram_bot)
dp = Dispatcher(bot)




@dp.message_handler(commands=["help"])
async def start_help(message: types.Message):
    await message.reply(
        f"Вот что я могу: \n"
        f"Я начинаю работать, при нажатии на команду /start\n"
        f"Тогда тебе  нужно будет написать названия города\n"
        f"И я покажу тебе всю информацию про погоду в этом городе))"
        f"Так что ты тянешь нажимай пиши /start"
    )



@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет!!! Напиши мне название города и я пришлю тебе сводку информации по погоде!")


@dp.message_handler()
async def get_weather(message: types.Message):
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
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

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
        #lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"] - data["sys"]["sunrise"])


        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
        f"Погода в городе: {city}\nТемпература: {cur_weather}C  {wd}\n"
        f"Влажность: {humidity}\nДавление: {pressure} мм. рт.ст\nСкорость ветра: {wind} м/с \n"
        f"Восход солнца: {timetamp_sunrise}\n"
        f"Заход солнца: {timeset_sunrise}\n"
        #f"Продолжительность дня: {timeset_sunrise}\n"
        f"***Хорошего дня***\n"
        f"***Слава Україні***"
        )
    except :
        await message.reply("\U0001F612 *** Проверьте название города *** \U0001F612")

if __name__ == "__main__":
    executor.start_polling(dp)
