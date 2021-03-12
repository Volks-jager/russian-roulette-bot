import aiogram
import asyncio
from aiogram import types
from main import bot
from keyboards import keyboard_remove, inline_keyboard_remove, game_dialog_keyboard, turn_keyboard
from config import ADMIN_LIST, DB
from strings import string
from SQL import *

async def db_handler(message):
    if message.from_user.id in ADMIN_LIST:
        db = open(DB, 'rb')
        await bot.send_document(chat_id=message.chat.id, document=db)
        db.close()
    else:
        await bot.send_message(chat_id=message.chat.id, text=string('ru', '404'))

async def start_handler(message):
    await reg_update_user(message)
    await bot.send_message(chat_id=message.chat.id, text=string('ru', 'greetings'))

async def groupadd_handler(message):
    await bot.send_message(chat_id=message.chat.id, text=string('ru', 'group_greetings'))

async def newgame_handler(message):
    if not await game_in_progress(message):
        msg = await bot.send_message(chat_id=message.chat.id, 
                                text=string('ru', 'game_dialog_noplayers'), 
                                reply_markup=game_dialog_keyboard(message))
        await register_game(msg)
    else:
        await bot.send_message(chat_id=message.chat.id, text=string('ru', 'game_in_progress'))

async def wrong_chat_handler(message):
    await bot.send_message(chat_id=message.chat.id, text=string('ru', 'wrong_chat'))

async def cancel_game_handler(call):
    member = await bot.get_chat_member(call.message.chat.id, call.from_user.id)
    if member.is_chat_admin():
        msg_id = await cancel_game(call)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id= msg_id, 
                                text=string('ru', 'game_cancelled').format(call.from_user.id, call.from_user.first_name if call.from_user.first_name else "noname"), 
                                reply_markup = inline_keyboard_remove(), parse_mode='HTML')
    else:
        await bot.answer_callback_query(call.id, text=string('ru', 'not_admin_alert'), show_alert=True)

async def join_game_handler(call):
    await reg_update_user(call)
    await join_game(call)
    registered_players = await registered_players_list(call)
    if registered_players:
        player_list = ''
        for player in registered_players:
            player_list += '-<a href="tg://user?id={}">{}</a>\n'.format(player[0], player[1] if player[1] else "noname")
        text = string('ru', 'game_dialog').format(player_list)
    else:
        text = string('ru', 'game_dialog_noplayers')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=game_dialog_keyboard(call.message), parse_mode='HTML')

async def start_game_handler(call):
    member = await bot.get_chat_member(call.message.chat.id, call.from_user.id)
    if member.is_chat_admin():
        if await registered_players_count(call) > 1:
            msg_id = await start_game(call)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id= msg_id, 
                                    text=string('ru', 'game_started').format(call.from_user.id, call.from_user.first_name if call.from_user.first_name else "noname"), 
                                    reply_markup = inline_keyboard_remove(), parse_mode='HTML')
            await next_turn(call)
        else:
            await bot.answer_callback_query(call.id, text=string('ru', 'not_enough_players'), show_alert=True)
    else:
        await bot.answer_callback_query(call.id, text=string('ru', 'not_admin_alert'), show_alert=True)

async def next_turn(call):
    user_id, name = await next_user(call)
    keyboard = turn_keyboard(user_id)
    msg = await bot.send_message(chat_id=call.message.chat.id, text=string('ru', 'turn_text').format(user_id, name), reply_markup=keyboard, parse_mode='HTML')
    await set_user_pending(msg, user_id)

async def shoot_handler(call):
    data = call.data.split('|')
    user = data[1]
    if int(user) == call.from_user.id:
        await unset_user_pending(call)
        user_id, name = await get_user_id_name(call) 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, 
                        text=string('ru', 'shoot').format(call.from_user.id, call.from_user.first_name if call.from_user.first_name else "noname"), 
                        reply_markup = inline_keyboard_remove(), parse_mode='HTML')
        await asyncio.sleep(1,5)
        if await shoot(call):
            await bot.send_message(chat_id=call.message.chat.id, text=string('ru', 'dead').format(user_id, name), parse_mode='HTML')
            if await last_standing(call):
                user_id, name = await endgame(call)
                await bot.send_message(chat_id=call.message.chat.id, text=string('ru', 'endgame').format(user_id, name), parse_mode='HTML')
            else:
                await asyncio.sleep(1,5)
                await next_turn(call)
        else:
            await bot.send_message(chat_id=call.message.chat.id, text=string('ru', 'alive').format(user_id, name), parse_mode='HTML')
            await asyncio.sleep(1,5)
            await next_turn(call)
    else:
        await bot.answer_callback_query(call.id, text=string('ru', 'not_your_turn'), show_alert=True)

async def rotate_handler(call):
    data = call.data.split('|')
    user = data[1]
    if int(user) == call.from_user.id:
        await unset_user_pending(call)
        user_id, name = await get_user_id_name(call) 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, 
                        text=string('ru', 'rotate').format(call.from_user.id, call.from_user.first_name if call.from_user.first_name else "noname"), 
                        reply_markup = inline_keyboard_remove(), parse_mode='HTML')
        await asyncio.sleep(1,5)
        if await rotate(call):
            await bot.send_message(chat_id=call.message.chat.id, text=string('ru', 'dead').format(user_id, name), parse_mode='HTML')
            if await last_standing(call):
                user_id, name = await endgame(call)
                await bot.send_message(chat_id=call.message.chat.id, text=string('ru', 'endgame').format(user_id, name), parse_mode='HTML')
            else:
                await asyncio.sleep(1,5)
                await next_turn(call)
        else:
            await bot.send_message(chat_id=call.message.chat.id, text=string('ru', 'alive').format(user_id, name), parse_mode='HTML')
            await asyncio.sleep(1,5)
            await next_turn(call)
    else:
        await bot.answer_callback_query(call.id, text=string('ru', 'not_your_turn'), show_alert=True)




