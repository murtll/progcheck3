from random import randint
from time import sleep
from datetime import datetime
from threading import Thread

from fightergame import Field, Shelly, Bull, Piper
from dbworker import DbWorker

def effects():
    colors = ['\033[91m', '\033[93m']
    phrases = ['BOOM!', 'BANG!']
    endc = '\033[0m'

    while True:
        print(colors[randint(0, len(colors) - 1)] + phrases[randint(0, len(phrases) - 1)] + endc)
        sleep(randint(1, 2))

if __name__ == '__main__':
    db = DbWorker()
    
    winners = db.get_all_winners()

    if len(winners) == 0:
        print('There were no winners yet.\n')
    else:
        print('Previous winners:')
        for i, current_winner in enumerate(winners):
            date = datetime.fromtimestamp(current_winner.date).strftime('%Y-%m-%d %H:%M:%S')
            print(f'{current_winner.id} | {current_winner.name} | {date}')
        print('\n')

    field = Field(100, 100)

    try:
        player1 = Piper(2, field)
        player2 = Bull(2, field)
    except:
        print('Can`t initialize players')
        exit(0)

    effect_thread = Thread(target = effects, daemon=True)
    effect_thread.start()

    while len(field.characters) > 1:
        for c in field.characters:
            c.update()
            c.move(randint(-1, 1), randint(-1, 1))
            c.attack()
            sleep(1)
            print('')

    winner = field.characters[0]

    print('The winner is ', winner.name.upper(), '!')
    db.add_winner(winner.name, int(datetime.timestamp(datetime.now())))

