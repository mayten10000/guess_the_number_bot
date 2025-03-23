from aiogram import F, Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import random

Bot_token = ""

bot = Bot(Bot_token)
dp = Dispatcher()

attempts = 0


user = {
    'in_game': False,
    'secret_number': None,
    'attempts': None,
    'total_games': None,
    'wins': 0
}

def get_random() -> int:
    random_int = random.randint(0,100)
    return random_int

@dp.message(CommandStart())
async def greeting(message: Message):
    await message.answer("Привет, я бот угадай число!")

@dp.message(Command(commands='stat'))
async def statistics(message: Message):
    await message.answer(f'Количество выигранных игр {user["wins"]}. Количество всего сыгранных игр {user["total_games"]}')

@dp.message(Command(commands='cancel'))
async def cancel_game(message: Message):
    if user['in_game']:
        user['in_game'] = False
        await message.answer("Мы закончили игру")
    else:
        await message.answer("Мы и не играли")

@dp.message(Command(commands='help'))
async def helper_command(message: Message):
    await message.answer("Игра угадай число. Я загадываю рандом число от 0 до 100, ты угадываешь или не угадываешь")

@dp.message(F.text.lower().in_(['сыграем', 'го']))
async def positive_answer(message: Message):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random()
        user['attempts'] = attempts
        await message.answer("Я загадал число от 1 до 100")
    else:
        await message.answer("Пока мы играем, мы не можем начать новую. Нажми /cancel")

@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def processing(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            user['in_game'] = False
            user['secret_number'] = None
            user['attempts'] = None
            user['total_games'] += 1
            user['wins'] += 1
            await message.answer("Вы угадали, поздравляюЮ сыграем ещё?")
        elif int(message.text) > user['secret_number']:
            user['attempts'] -= 1
            await message.answer("Моё число меньше")
        elif int(message.text) < user['secret_number']:
            user['attempts'] -= 1
            await message.answer("Моё число больше")
        if user[attempts] == 0:
            user['in_game'] = False
            user['total_games'] += 1
            await message.answer("Ходы закончились. Вы проиграли, сыграем ещё?")
    else:
        await message.answer("Мы ещё не в игре")

@dp.message(Command(commands='proccessing_out'))
async def process_out(message: Message):
    if user['in_game']:
        await message.answer("Ты в игре")
    else:
        await message.answer("Напиши сыграем или го")


if __name__ == '__main__':
    dp.run_polling(bot)