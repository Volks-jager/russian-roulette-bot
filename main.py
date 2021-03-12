import sys
sys.dont_write_bytecode = True
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from db.models import *
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import aiogram
import asyncio
from aiogram import types, executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandHelp, CommandStart
from config import BOT_TOKEN
from handlers import *

bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)

@dp.message_handler(commands=['db'])
async def db_cmd(message: types.Message):
    await db_handler(message)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await start_handler(message)

@dp.message_handler(content_types=["new_chat_members"])
async def groupadd(message: types.Message):
    if message.new_chat_members[0].id == 1543437848:
        await groupadd_handler(message)

@dp.message_handler(commands=["newgame"])
async def newgame(message: types.Message):
    if message.chat.id < 0:
        await newgame_handler(message)
    else:
        await wrong_chat_handler(message)

@dp.callback_query_handler(lambda call: True)
async def query_handler(call):
    if 'join' in call.data:
        await join_game_handler(call)
    if 'start' in call.data:
        await start_game_handler(call)
    if 'cancel' in call.data:
        await cancel_game_handler(call)
    if 'shoot' in call.data:
        await shoot_handler(call)
    if 'rotate' in call.data:
        await rotate_handler(call)
    
from autostarter import scheduler
async def on_startup(dp):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup = on_startup)
