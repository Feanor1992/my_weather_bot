import os
import math
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from background import keep_alive

bot = Bot(token='6113855922:AAGSuKb-pdwUNAhj-h8hfMjWaAgxvv0n-Rs')
dispatcher = Dispatcher(bot)


# create start command
@dispatcher.message_handler(commands=['start'])
async def star_command(message: types.Message):
    await message.reply('Hi! Write the name of the city and I will send You a weather report')


# create def that reacts to city names and get weather report
@dispatcher.message_handler()
async def get_weather(message: types.Message):
    try:
        #chat_id = message.chat.id
        city_name = message.text
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&land=en&units=metric&appid=7aebca778cfc8d1c00c3cadbb7166870')
        data = response.json()
        city = data['name']
        current_temperature = data['main']['temp']
        feels_like_temperature = data['main']['feels_like']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']

        # get sunrise and sunset time in the city
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        # return day length in the city
        day_length = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        # add weather description with emoji
        description_with_emoji = {
            'Clear': 'Clear \U00002600',
            'Clouds': 'Clouds \U00002601',
            'Rain': 'Rain \U00002614',
            'Drizzle': 'Drizzle \U00002614',
            'Thunderstorm': 'Thunderstorm \U000026A1',
            'Snow': 'Snow \U0001F328'
                    'Mist:' 'Mist \U0001F32B'
        }

        # get weather description
        weather_description = data['weather'][0]['main']
        if weather_description in description_with_emoji:
            wd = description_with_emoji[weather_description]
        else:
            wd = 'Something outside of window'

        # return data to users
        await message.reply(
            f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\nWeather in {city}\nTemperature: {current_temperature}°C\nFeels like: {feels_like_temperature}\n'
            f'{wd}\nPressure: {math.ceil(pressure / 1.333)} mb\nHumidity: {humidity}%\nWind: {wind} m/s\n'
            f'Sunrise: {sunrise}\nSunset: {sunset}\nDay Length: {day_length}\n'
            f'Have a nice day!'
            )
    except:
        await message.reply('OOOOOPS! Please, check city name!')


if __name__ == '__main__':
    # using method executor from aiogram.utils asking
    # Dispatcher expect command /start
    executor.start_polling(dispatcher)

keep_alive()
bot.polling(non_stop=True, interval=0)