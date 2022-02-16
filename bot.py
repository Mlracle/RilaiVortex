import logging
import time
from os import getenv
from sys import exit

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from main import data, get_items


bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Хэндлер на команду /test1
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="Всего +#% к сопротивлению холоду")
    keyboard.add(button_1)
    button_2 = "Всего +#% к сопротивлению огню"
    keyboard.add(button_2)
    button_3 = "Всего +#% к сопротивлению молнии"
    keyboard.add(button_3)

    await message.answer("Начнем", reply_markup=keyboard)


@dp.message_handler(Text(equals="HeadHunter"))
async def send_data(message: types.Message):
    await message.answer('Пожалуйста подождите...')
    for index, i in enumerate(data):
        explicits = "\n".join(i["explicitMod"])
        card = f'{i["name"]}\n' \
               f'{i["type_name"]}\n' \
               f'{"-" * 60}\n' \
               f'Уровень предмета: {i["itemLevel"]}\n' \
               f'Требует уровень: {i["requirements"]}\n' \
               f'{"-" * 60}\n' \
               f'{i["implicitMod"]}\n' \
               f'{"-" * 60}\n' \
               f'{explicits}' \
               f'{"-" * 60}\n' \
               f'{i["Currency"]}\n'
        if index % 20 == 0:
            time.sleep(3)
        await message.answer(card)


if __name__ == "__main__":
    # Запуск бота
    #get_items()
    executor.start_polling(dp, skip_updates=True)
