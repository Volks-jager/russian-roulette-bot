from aiogram import types
from strings import button
import aiogram

def keyboard_remove():
    keyboard = types.ReplyKeyboardRemove()
    return keyboard

def inline_keyboard_remove():
    keyboard = types.InlineKeyboardMarkup()
    return keyboard

def game_dialog_keyboard(message):
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(text=button('ru', 'join_game'), callback_data='join'))
    keyboard.add(aiogram.types.InlineKeyboardButton(text=button('ru', 'start_game'), callback_data='start'),
                 aiogram.types.InlineKeyboardButton(text=button('ru', 'cancel_game'), callback_data='cancel'))
    return keyboard

def turn_keyboard(user_id):
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(text=button('ru', 'shoot'), callback_data=f'shoot|{user_id}'),
                 aiogram.types.InlineKeyboardButton(text=button('ru', 'rotate'), callback_data=f'rotate|{user_id}'))
    return keyboard
