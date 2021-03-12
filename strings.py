STRINGS = {
    'ru': {
        '404': 'У тебя недостаточно прав для выполнения данной команды!',
        'greetings': 'Это бот для игры в русскую рулетку. Играть необходимо с несколькими игроками, потому добавь бота в группу, после чего отправь команду /newgame тоб начать игру.',
        'group_greetings': 'Привет, это бот для игры в русскую рулетку!\n'
                           'В качестве "игрового поля" выступает семизарядный револьвер системы Нагана, состоявший на вооружении армии Российской империи.\n'
                           'Правила игры простые: Последний выживший- победитель!\n'
                           'Для начала игры, отправь /newgame',
        'game_in_progress': 'В группе уже есть активная игра!',
        'game_dialog_noplayers': 'Начата регистрация в игру!\n'
                                 'Время регистрации- 5 минут\n'
                                 'Досрочно начать либо отменить игру могут администраторы группы.',
        'game_dialog': 'Начата регистрация в игру!\n'
                       'Время регистрации- 5 минут\n'
                       'Досрочно начать либо отменить игру могут администраторы группы.\n'
                       '\n'
                       'Зарегистрированные игроки:\n{}',
        'not_admin_alert': 'Только администраторы группы могут выполнять это действие!',
        'game_cancelled': 'Игра отменена пользователем <a href="tg://user?id={}">{}</a>',
        'game_started': 'Игра начата пользователем <a href="tg://user?id={}">{}</a>',
        'turn_text': 'Очередь игрока <a href="tg://user?id={}">{}</a>!\nСтреляешь сразу или крутишь барабан?\nВремя хода-30 сек.',
        'not_enough_players': 'Для начала игры необходимо минимум 2 игрока!',
        'wrong_chat': 'Это бот для игры в группах! Добавь бота в группу с другими игроками и повтори команду для начала игры.',
        'not_your_turn': 'Сейчас не твой ход!',
        'shoot': 'Игрок <a href="tg://user?id={}">{}</a> берет револьвер и нажимает на курок, не вращая барабан...',
        'rotate': 'Игрок <a href="tg://user?id={}">{}</a> раскручивает барабан, и среляет сразу как тот остановится...',
        'dead': 'Игрок <a href="tg://user?id={}">{}</a> застрелился!\n/F',
        'alive': 'Ударник спустился, но ничего не произошло! <a href="tg://user?id={}">{}</a> остался жив.',
        'endgame': 'Игра завершена!\n'
                   'Победитель- <a href="tg://user?id={}">{}</a>\n'
                   '\n'
                   'Начать новую игру: /newgame',
        'game_cancelled_timeout': 'Время на регистрацию вышло, но собрать достаточно игроков не удалось. Игра отменена!',
        'game_started_timeout': 'Время регистрации окончено, игра начинается!',
        'shoot_timeout': '<a href="tg://user?id={}">{}</a> слишком долго раздумывал, что надоело игроку <a href="tg://user?id={}">{}</a>, потому тот выхватил самозарядный ПМ и застрелил <a href="tg://user?id={}">{}</a>\n/F'
    }
}

BUTTONS = {
    'ru': {
        'join_game': 'Присоединиться/Выйти',
        'start_game': 'Начать игру',
        'cancel_game': 'Отменить игру',
        'shoot': 'Выстрелить',
        'rotate': 'Вращать',
    }
}

def string(language, string_key):
    return STRINGS.get(language).get(string_key)

def button(language, button_key):
    return BUTTONS.get(language).get(button_key)