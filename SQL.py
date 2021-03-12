from db.models import User, Game, Usergame
from datetime import datetime
import random
import pytz

async def reg_update_user(message):
    user = User.objects.filter(tg_id=message.from_user.id).select_related().first()
    if user is None:
        user = User()
        user.tg_id = message.from_user.id
        user.username = message.from_user.username
        user.first_name = message.from_user.first_name
        user.last_name = message.from_user.last_name
    else:
        user.username = message.from_user.username
        user.first_name = message.from_user.first_name
        user.last_name = message.from_user.last_name
    user.save()

async def get_user_id_name(message):
    user = User.objects.filter(tg_id=message.from_user.id).select_related().first()
    return user.tg_id, user.first_name

async def game_in_progress(message):
    if Game.objects.filter(group_id=message.chat.id).exists():
        return True
    return False

async def register_game(message):
    newgame = Game()
    newgame.group_id = message.chat.id
    newgame.start_message_id = message.message_id
    newgame.start_time = datetime.now()
    newgame.turn = 0
    newgame.chamber_position = random.randrange(0, 7)
    newgame.save()

async def cancel_game(call):
    game = Game.objects.get(group_id=call.message.chat.id)
    Usergame.objects.filter(game=game).delete()
    message_id = game.start_message_id
    game.delete()
    return message_id
    
async def join_game(call):
    user = User.objects.get(tg_id=call.from_user.id)
    game = Game.objects.get(group_id=call.message.chat.id)
    if Usergame.objects.filter(user=user, game=game).exists():
        Usergame.objects.filter(user=user, game=game).delete()
    else:
        usergame = Usergame()
        usergame.user = user
        usergame.game = game
        usergame.status = "alive"
        usergame.randfield = random.randrange(0, 8192)
        usergame.save()

async def registered_players_list(call):
    game = Game.objects.get(group_id=call.message.chat.id)
    if not Usergame.objects.filter(game=game).exists():
        return False
    else:
        player_list = []
        usergames = Usergame.objects.filter(game=game)
        for usergame in usergames:
            player_list.append([usergame.user.tg_id, usergame.user.first_name])
        return player_list

async def registered_players_count(call):
    game = Game.objects.get(group_id=call.message.chat.id)
    return Usergame.objects.filter(game=game).count()

async def start_game(call):
    game = Game.objects.get(group_id=call.message.chat.id)
    game.is_start = True
    game.save()
    return game.start_message_id

async def next_user(call):
    game = Game.objects.get(group_id=call.message.chat.id)
    usergames = Usergame.objects.filter(game=game).order_by('randfield')
    usercount = usergames.count()
    turn = game.turn
    usergame = usergames[turn]
    while usergame.status != 'alive':
        turn += (turn + 1) % usercount
        usergame = usergames[turn]
    game.turn = (turn + 1) % usercount
    game.save()
    return usergame.user.tg_id, usergame.user.first_name

async def set_user_pending(message, user_id):
    user = User.objects.get(tg_id=user_id)
    game = Game.objects.get(group_id=message.chat.id)
    usergame = Usergame.objects.get(game=game, user=user)
    usergame.turn_start_time = datetime.now()
    usergame.is_pending = True
    usergame.pending_message_id = message.message_id
    usergame.save()

async def unset_user_pending(call):
    user = User.objects.get(tg_id=call.from_user.id)
    game = Game.objects.get(group_id=call.message.chat.id)
    usergame = Usergame.objects.get(game=game, user=user)
    usergame.is_pending = False
    usergame.save()


async def shoot(call):
    game = Game.objects.get(group_id=call.message.chat.id)
    if game.chamber_position == 0:
        user = User.objects.get(tg_id=call.from_user.id)
        usergame = Usergame.objects.get(game=game, user=user)
        usergame.status='dead'
        game.chamber_position = random.randrange(0, 7)
        game.save()
        usergame.save()
        return True
    else:
        game.chamber_position = (game.chamber_position + 1) % 7
        game.save()
        return False

async def rotate(call):
    game = Game.objects.get(group_id=call.message.chat.id)
    game.chamber_position = random.randrange(0, 7)
    if game.chamber_position == 0:
        user = User.objects.get(tg_id=call.from_user.id)
        usergame = Usergame.objects.get(game=game, user=user)
        usergame.status='dead'
        game.chamber_position = random.randrange(0, 7)
        game.save()
        usergame.save()
        return True
    else:
        game.chamber_position = (game.chamber_position + 1) % 7
        game.save()
        return False

async def last_standing(call):
    game = Game.objects.get(group_id=call.message.chat.id)
    if Usergame.objects.filter(game=game, status='alive').count() == 1:
        return True
    else: 
        return False

async def endgame(call):
    game = Game.objects.get(group_id=call.message.chat.id)
    winner = Usergame.objects.get(game=game, status='alive')
    Usergame.objects.filter(game=game).delete()
    game.delete()
    return winner.user.tg_id, winner.user.first_name

