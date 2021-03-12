import aioschedule
import asyncio
import random
from db.models import User, Game, Usergame
from datetime import datetime, timedelta
from strings import string
from keyboards import inline_keyboard_remove, turn_keyboard
from main import bot

async def startgames():
    games_to_start = Game.objects.filter(start_time__lt = (datetime.now() - timedelta(seconds=300)), is_start=False)
    for game in games_to_start:
        usergames_count = Usergame.objects.filter(game=game).count()
        if usergames_count < 2:
            await bot.edit_message_text(chat_id=game.group_id, message_id=game.start_message_id, 
                                text=string('ru', 'game_cancelled_timeout'),
                                reply_markup = inline_keyboard_remove(), parse_mode='HTML')
            Usergame.objects.filter(game=game).delete()
            game.delete()
        else:
            await bot.edit_message_text(chat_id=game.group_id, message_id=game.start_message_id, 
                                text=string('ru', 'game_started_timeout'),
                                reply_markup = inline_keyboard_remove(), parse_mode='HTML')
            
            usergames = Usergame.objects.filter(game=game).order_by('randfield')
            usercount = usergames.count()
            usergame = usergames[0]
            game.turn = (game.turn + 1) % usercount
            game.is_start = True
            game.save()

            keyboard = turn_keyboard(usergame.user.tg_id)
            msg = await bot.send_message(chat_id=game.group_id, 
                text=string('ru', 'turn_text').format(usergame.user.tg_id, usergame.user.first_name if usergame.user.first_name else 'noname'), 
                reply_markup=keyboard, parse_mode='HTML'
            )

            usergame.turn_start_time = datetime.now()
            usergame.is_pending = True
            usergame.pending_message_id = msg.message_id
            usergame.save()


async def user_timeout():
    usergames = Usergame.objects.filter(turn_start_time__lt=(datetime.now() - timedelta(seconds=30)), is_pending = True)
    for usergame in usergames:
        killer_arr = Usergame.objects.filter(game=usergame.game, status='alive').exclude(pk=usergame.pk)
        killer = random.choice(killer_arr)
        await bot.edit_message_text(chat_id=usergame.game.group_id, message_id=usergame.pending_message_id,
                    text=string('ru', 'shoot_timeout').format(usergame.user.tg_id, usergame.user.first_name if usergame.user.first_name else "noname", killer.user.tg_id, killer.user.first_name if usergame.user.first_name else "noname", usergame.user.tg_id, usergame.user.first_name if usergame.user.first_name else "noname"), 
                    reply_markup = inline_keyboard_remove(), parse_mode='HTML')
        usergame.status = 'dead'
        usergame.save()

        if Usergame.objects.filter(game=usergame.game, status='alive').count() == 1:
            winner = Usergame.objects.get(game=usergame.game, status='alive')
            Usergame.objects.filter(game=usergame.game).delete()
            usergame.game.delete()
            await bot.send_message(chat_id=usergame.game.group_id, text=string('ru', 'endgame').format(winner.user.tg_id, winner.user.first_name), parse_mode='HTML')
        else:
            await asyncio.sleep(1,5)
            game = usergame.game
            usergames = Usergame.objects.filter(game=game).order_by('randfield')
            usercount = usergames.count()
            usergame = usergames[game.turn]
            while usergame.status != 'alive':
                game.turn = (game.turn + 1) % usercount
                usergame = usergames[game.turn]
            game.turn = (game.turn + 1) % usercount
            game.save()

            keyboard = turn_keyboard(usergame.user.tg_id)
            msg = await bot.send_message(chat_id=game.group_id, 
                text=string('ru', 'turn_text').format(usergame.user.tg_id, usergame.user.first_name if usergame.user.first_name else 'noname'), 
                reply_markup=keyboard, parse_mode='HTML'
            )

            usergame.turn_start_time = datetime.now()
            usergame.is_pending = True
            usergame.pending_message_id = msg.message_id
            usergame.save()
            

async def scheduler():
    aioschedule.every(15).seconds.do(startgames)
    aioschedule.every(5).seconds.do(user_timeout)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
