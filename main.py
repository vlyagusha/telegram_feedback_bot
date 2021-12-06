import os
import logging
import keyboards as kb

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import IDFilter
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot = Bot(token=os.environ.get("BOT_TOKEN"))
dp = Dispatcher(bot)
CEO_CHAT_ID = os.environ.get("CEO_CHAT_ID")
GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")
feedbacks = {}


@dp.message_handler(IDFilter(chat_id=CEO_CHAT_ID))
async def sniff_ceo_chat(message: types.Message):
    pass


@dp.message_handler(IDFilter(chat_id=GROUP_CHAT_ID))
async def sniff_group_chat(message: types.Message):
    me = await bot.get_me()
    await message.reply(f'''
Добрый день, {message.from_user.full_name}, я бот с обратной связью к руководству.
Напишите мне в личные сообщения, чтобы оставить обратную связь @{me.username}
''')
    await message.delete()


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.reply(f'''
Привет, {message.from_user.full_name}! Я бот с обратной связью к руководству
Вот что я умею:
/help - помощь
''')
    feedbacks[message.from_user.id] = {}
    await message.reply('Выберите участок', reply_markup=kb.zones_kb)


@dp.message_handler(commands=['z'])
async def get_zone(message):
    feedbacks[message.from_user.id].update({'zone': message.get_args()})
    await message.reply('Выберите должность', reply_markup=kb.position_kb)


@dp.message_handler(commands=['p'])
async def get_position(message):
    feedbacks[message.from_user.id].update({'position': message.get_args()})
    await message.reply('Напишите вашу фамилию', reply_markup=kb.blank_kb)


@dp.message_handler()
async def get_text(message):
    if message.from_user.id not in feedbacks:
        feedbacks[message.from_user.id] = {}
        await message.reply('Выберите участок', reply_markup=kb.zones_kb)
        return

    if 'zone' not in feedbacks[message.from_user.id]:
        await message.reply('Выберите участок', reply_markup=kb.zones_kb)
        return

    if 'position' not in feedbacks[message.from_user.id]:
        await message.reply('Выберите должность', reply_markup=kb.position_kb)
        return

    if 'last_name' not in feedbacks[message.from_user.id]:
        feedbacks[message.from_user.id].update({'last_name': message.text})
        await message.reply('Напишите ваше имя', reply_markup=kb.blank_kb)
        return

    if 'first_name' not in feedbacks[message.from_user.id]:
        feedbacks[message.from_user.id].update({'first_name': message.text})
        await message.reply('Напишите ваше отчество', reply_markup=kb.blank_kb)
        return

    if 'middle_name' not in feedbacks[message.from_user.id]:
        feedbacks[message.from_user.id].update({'middle_name': message.text})
        await message.reply('Опишите проблему, которая у вас возникла', reply_markup=kb.blank_kb)
        return

    feedbacks[message.from_user.id].update({'message': message.text})

    await message.reply('''Спасибо за обращение!
Если вы хотите оставить новое обращение, нажмите /start''', reply_markup=kb.blank_kb)

    name = feedbacks[message.from_user.id]['last_name'] + ' ' +\
        feedbacks[message.from_user.id]['first_name'] + ' ' +\
        feedbacks[message.from_user.id]['middle_name']
    await bot.send_message(CEO_CHAT_ID, f'''
Новое сообщение от сотрудника.
Участок: {feedbacks[message.from_user.id]['zone']}
Должность: {feedbacks[message.from_user.id]['position']}
ФИО: {name}
Сообщение: {feedbacks[message.from_user.id]['message']} 
''', reply_markup=kb.blank_kb)
    del feedbacks[message.from_user.id]


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
