import os
import asyncio
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile
from ai_chat import chat, generate_image, search

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_modes: dict[int, str] = {}


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="💬 ИИ ЧАТ"))
    builder.add(types.KeyboardButton(text="🎨 РАСМ"))
    builder.add(types.KeyboardButton(text="🔍 ҶУСТУҶӮ"))
    return builder.as_markup(resize_keyboard=True)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Салом! Тугмаи поёнро зер кунед:", reply_markup=get_main_keyboard())


@dp.message(lambda message: message.text == "💬ИИ ЧАТ")
async def say_hello(message: types.Message):
    user_modes[message.from_user.id] = 'chat'
    await message.answer('Режими ИИ фаъол аст. Саволтанро нависед')


@dp.message(lambda message: message.text == "🎨РАСМ")
async def say_hello(message: types.Message):
    user_modes[message.from_user.id] = 'image'
    await message.answer('Чӣ расм тасвир кардан лозим? Промптро пурра нависед:')


@dp.message(lambda message: message.text == "🔍ҶУСТУҶӮ")
async def say_hello(message: types.Message):
    user_modes[message.from_user.id] = 'search'
    await message.answer('Чиро ҷустуҷӯ кардан лозим аст? Нависед:')


@dp.message()
async def ai_response(message: types.Message):
    if user_modes[message.from_user.id] == 'chat':
        await message.answer('Фикр карда истодаам...')
        answer = chat(message.from_user.id, message.text)
        await message.answer(answer)

    elif user_modes[message.from_user.id] == 'image':
        await message.answer('🎨 Расми шуморо тайёр карда истодаем...')
        await message.answer('Ин тахминан 30 сония вақт мегирад')
        try:
            filename = generate_image(message.from_user.id, message.text)
            photo = FSInputFile(filename)
            await message.answer_photo(photo, caption="Марҳамат расми шумо")
        except openai.BadRequestError:
            await message.answer('Ин расм ҳуқуқи авториро нарушат мекунад')
    elif user_modes[message.from_user.id] == 'search':
        await message.answer('Дар ҷустуҷӯ🔍...')
        result = search(message.text)
        await message.answer(result)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
