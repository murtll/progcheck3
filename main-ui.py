from random import randint
from time import sleep
from datetime import datetime
from threading import Thread
from tkinter import *

from fightergame import Field, Shelly, Bull, Piper
from dbworker import DbWorker

winner_name = None

class PlayerInfoFrame(Frame):
    def __init__(self, parent, player):
        super().__init__(parent)
        self.canvas = Canvas(self, height=20, width=20)
        self.canvas.create_rectangle(0, 0, 20, 20, fill=player.color, outline='black')
        self.info_var = StringVar()
        self.info_var.set(f'{player.name}\nHP: {player.health}\nPos: {player.x}, {player.y}\nCap: {int(player.capacity)}')
        self.info_label = Label(self, textvariable=self.info_var)

        self.canvas.grid(row=1, column=1)
        self.info_label.grid(row=1, column=2)

def play():
    global winner_name
    global frame

    field = Field(400, 400)

    try:
        if piper_var.get():
            player1 = Piper(2, field)
        if bull_var.get():
            player2 = Bull(2, field)
        if shelly_var.get():
            player3 = Shelly(2, field)
    except:
        print('Can`t initialize players')
        ui.destroy()
        exit(1)

    if len(field.characters) < 2:
        choose_fighter_label.configure(foreground='red')
        sleep(0.5)
        choose_fighter_label.configure(foreground='white')
        exit(1)

    winners_label.destroy()
    start_game_button.destroy()
    shelly_checkbox.destroy()
    bull_checkbox.destroy()
    piper_checkbox.destroy()
    choose_fighter_label.destroy()

    info_frame = Frame(frame)
    player_infos = []

    for i, c in enumerate(field.characters):
        player_info_frame = PlayerInfoFrame(info_frame, c)
        player_infos.append(player_info_frame)
        player_info_frame.grid(column=i, row=1)

    canvas = Canvas(frame, height=field.height + 100, width=field.width + 100, bg='#7e7e6e')

    info_frame.grid(column=1, row=1)
    canvas.grid(column=1, row=2)

    while len(field.characters) > 1:
        for i, c in enumerate(field.characters):
            c.update()
            c.move(randint(-1, 1), randint(-1, 1))

            player_info_frame = player_infos[i]
            player_info_frame.info_var.set(f'{c.name}\nHP: {c.health}\nPos: {c.x}, {c.y}\nCap: {int(c.capacity)}')

            canvas.delete(canvas.find_withtag(c.name))
            canvas.delete(canvas.find_withtag(f'{c.name}-attack'))
            canvas.create_rectangle(c.x - 15 + 50, c.y - 15 + 50, c.x + 15 + 50, c.y + 15 + 50, fill=c.color, outline='', tags=c.name)
            canvas.create_oval(c.x - c.attack_distance + 50, c.y - c.attack_distance + 50, c.x + c.attack_distance + 50, c.y + c.attack_distance + 50, outline='#00ff00' if c.capacity > 2 else '#ffff00' if c.capacity > 1  else '#ff0000', tags=f'{c.name}-attack')
            
            print('')
            sleep(0.3)

        for i, c in enumerate(field.characters):
            field_chars_old = field.characters.copy()
            attacked = c.attack()

            player_info_frame = player_infos[i]
            player_info_frame.info_var.set(f'{c.name}\nHP: {c.health}\nPos: {c.x}, {c.y}\nCap: {int(c.capacity)}')

            if attacked:
                canvas.delete(canvas.find_withtag(c.name))
                canvas.delete(canvas.find_withtag(attacked.name))

                line = canvas.create_polygon(c.x + 50, c.y + 50, attacked.x + 50 - 1000 // c.attack_distance, attacked.y + 50 - 1000 // c.attack_distance, attacked.x + 50 + 1000 // c.attack_distance, attacked.y + 50 + 1000 // c.attack_distance, fill=c.color)

                attacker_rect = canvas.create_rectangle(c.x - 15 + 50, c.y - 15 + 50, c.x + 15 + 50, c.y + 15 + 50, fill='white', outline='')
                attacked_rect = canvas.create_rectangle(attacked.x - 15 + 50, attacked.y - 15 + 50, attacked.x + 15 + 50, attacked.y + 15 + 50, fill='red', outline='')
                sleep(0.2)
                
                canvas.delete(attacker_rect)
                canvas.delete(attacked_rect)
                canvas.delete(line)

                canvas.create_rectangle(c.x - 15 + 50, c.y - 15 + 50, c.x + 15 + 50, c.y + 15 + 50, fill=c.color, outline='', tags=c.name)

                if attacked.health <= 0:
                    idx = field_chars_old.index(attacked)
                    attacked_info = player_infos[idx]
                    
                    attacked_info.info_var.set(f'{attacked.name} ☠\nHP: 0\nPos: {attacked.x}, {attacked.y}\nCap: {int(attacked.capacity)}')
                    attacked_info.canvas.delete('all')
                    attacked_info.canvas.create_rectangle(0, 0, 20, 20, fill='black', outline='black')
                    
                    canvas.create_rectangle(attacked.x - 15 + 50, attacked.y - 15 + 50, attacked.x + 15 + 50, attacked.y + 15 + 50, fill='black', outline='', tags=attacked.name)
                    canvas.delete(canvas.find_withtag(f'{attacked.name}-attack'))

                    player_infos.remove(attacked_info)
                else:
                    canvas.create_rectangle(attacked.x - 15 + 50, attacked.y - 15 + 50, attacked.x + 15 + 50, attacked.y + 15 + 50, fill=attacked.color, outline='', tags=attacked.name)

            print('')

    winner = field.characters[0]

    player_infos[0].info_var.set(f'{winner.name.upper()} ⚜\nHP: {winner.health}\nPos: {winner.x}, {winner.y}\nCap: {int(winner.capacity)}')

    winner_str = f'The winner is {winner.name.upper()}!'

    winner_label = Label(frame, text=winner_str, foreground=winner.color)
    exit_button = Button(frame, text='Exit', command=lambda: ui.destroy())

    winner_label.grid(row=3, column=1)
    exit_button.grid(row=4, column=1)

    winner_name = winner.name

def start_game_thread():
    game_thread = Thread(target=play, daemon=True)
    game_thread.start()

if __name__ == '__main__':
    ui = Tk()
    ui.geometry('500x650')
    ui.title('Bubble Kvas')

    frame = Frame(ui)

    db = DbWorker()
    
    winners = db.get_all_winners()
    winners_str = ''

    if len(winners) == 0:
        winners_str = 'There were no winners yet.'
    else:
        winners_str = 'Previous winners:\n'
        for i in range(len(winners) - 1, 0, -1):
            current_winner = winners[i]
            date = datetime.fromtimestamp(current_winner.date).strftime('%Y-%m-%d %H:%M:%S')
            winners_str += f'{date} - {current_winner.name}\n'

    winners_label = Label(frame, text=winners_str)
    start_game_button = Button(frame, text='Start new game', command=start_game_thread)

    shelly_var = BooleanVar()
    bull_var = BooleanVar()
    piper_var = BooleanVar()

    shelly_checkbox = Checkbutton(frame, text='Shelly', variable=shelly_var, onvalue=True)
    bull_checkbox = Checkbutton(frame, text='Bull', variable=bull_var, onvalue=True)
    piper_checkbox = Checkbutton(frame, text='Piper', variable=piper_var, onvalue=True)
    choose_fighter_label = Label(frame, text='Choose your fighters (at least 2)', pady=5)

    frame.place(relx=.5, rely=.5, anchor="center")
    winners_label.grid(column=1, row=1, columnspan=3)
    choose_fighter_label.grid(column=1, row=2, columnspan=3)
    shelly_checkbox.grid(column=1, row=3)
    bull_checkbox.grid(column=2, row=3)
    piper_checkbox.grid(column=3, row=3)
    start_game_button.grid(column=1, row=4, columnspan=3)

    ui.mainloop()

    if winner_name:
        db.add_winner(winner_name, int(datetime.timestamp(datetime.now())))