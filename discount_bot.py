from aiogram import Bot, Dispatcher, executor , types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from salomon_parser import collect_data
from dns_parser import get_page, get_info
from alltime_parser import get_page_time, get_info_time
import json


bot = Bot(token="2081588707:AAHRSpjGaTjzF0SZdZdGI2lzFj9LIH1_VCo", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Кроссовки", "Видеокарты", "Часы"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Товары со скидкой!", reply_markup=keyboard)

@dp.message_handler(Text(equals="Кроссовки"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Собираются данные. Ждите...")

    collect_data()

    with open("result_data.json", encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        card=f"{hlink(item.get('title'), item.get('link'))}\n" \
            f"{hbold('Категория: ')} {item.get('category')}\n" \
            f"{hbold('Прайс: ')} {item.get('price_base')}\n" \
            f"{hbold('Прайс со скидкой: ')} -{item.get('discount_percent')}%: {item.get('price_sale')}"

        await message.answer(card)


@dp.message_handler(Text(equals="Видеокарты"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Собираются данные. Ждите...")

    pagination = get_page()
    get_info(pagination=pagination)


    with open("result_data(videocards).json", encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        card=f"{hlink(item.get('name'), item.get('link'))}\n" \
            f"{hbold('Категория: ')} {item.get('category')}\n" \
            f"{hbold('Прайс: ')} {item.get('price')}"

        await message.answer(card)


@dp.message_handler(Text(equals="Часы"))
async def get_discount_time(message: types.Message):
    await message.answer("Собираются данные. Ждите...")

    pagination = get_page_time(url="https://www.alltime.ru/watch/man/filter/reference:sale/?PAGEN_1=2")
    get_info_time(pagination=pagination)


    with open("result_data(time).json", encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        card=f"{hlink(item.get('name'), item.get('url'))}\n" \
            f"{hbold('Прайс без скидки: ')} {item.get('old_price')}\n" \
            f"{hbold('Прайс со скидкой: ')} {item.get('new_price')}\n" \
            f"{hbold('Cкидка: ')} {item.get('discount')}"

        await message.answer(card)

def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()
