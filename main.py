from random import randint
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font

from numpy import pad
root = Tk()
root.title('Tic-Tac-Toe')
win_x = root.winfo_rootx() + 300
win_y = root.winfo_rooty() + 300
root.resizable(width=False, height=False)
root.geometry(f'+{win_x}+{win_y}')

global popup
popup = Toplevel(root)
popup.title('Board Game')
popup.resizable(width=False, height=False)
popup.geometry(f'+{win_x+380}+{win_y}')
popup.withdraw()

FONT = Font(family='Bahnschrift', size=16)
player_character = ''
ai_character = ''
positions = ['-' for _ in range(9)]
pos_buttons = []
turn = 0
turns = 0
game_over = False
winner = ''

for i in range(5,8):
    Grid.rowconfigure(root, i, weight=1)
for i in range(0,3):
    Grid.columnconfigure(root, i, weight=1)

def check_continue():
    for pos in positions:
        if pos == '-':
            return True
    return False

def check_win(pos, character):
    winning_condition = 3*character
    if pos[0] + pos[1] + pos[2] == winning_condition or \
        pos[3] + pos[4] + pos[5] == winning_condition or \
        pos[6] + pos[7] + pos[8] == winning_condition or \
        pos[0] + pos[3] + pos[6] == winning_condition or \
        pos[1] + pos[4] + pos[7] == winning_condition or \
        pos[2] + pos[5] + pos[8] == winning_condition or \
        pos[0] + pos[4] + pos[8] == winning_condition or \
        pos[2] + pos[4] + pos[6] == winning_condition:
            return True

def check_game_over(pos):
    global game_over
    global winner
    global win_label

    def game_over_message(character):
        if player_character == character:
            messagebox.showinfo(title="Congratulations!", message="You are not stupid!")
        else:
            messagebox.showinfo(title="Fcking noob!", message="You lost to a badly coded ai")

    if check_win(pos, '✖'):
            game_over = True
            winner = '✖'
            game_over_message(winner)

    elif check_win(pos, 'Ｏ'):
            game_over = True
            winner = 'Ｏ'
            game_over_message(winner)

    else:
        if check_continue():
            game_over = False
        else:
            game_over = True
            messagebox.showinfo(title="It's a draw!", message="How could you get a draw againt a simple AI ????")

    return game_over

def minimax(positions, is_maximizing):
    if check_win(positions, ai_character):
        return 1
    elif check_win(positions, player_character):
        return -1
    elif not check_continue:
        return 0
    
    if is_maximizing:
        best_score = -1000
        for pos in range(len(positions)):
            if positions[pos] == '-':
                positions[pos] = ai_character
                score = minimax(positions, False)
                positions[pos] = '-'
                if score > best_score:
                    best_score = score
        
        return best_score

    else:
        best_score = 1000
        for pos in range(len(positions)):
            if positions[pos] == '-':
                positions[pos] = player_character
                score = minimax(positions, True)
                positions[pos] = '-'
                if score < best_score:
                    best_score = score
        return best_score

def ai_turn():
    global turn
    global turns
    global game_over
    while turn == 0 and turns < 9 and game_over == False:
        if turns == 0:
            best_move = randint(0,8)

        else:    
            best_score = -1000
            best_move = 0

            for pos in range(len(positions)):
                if positions[pos] == '-':
                    positions[pos] = ai_character
                    score = minimax(positions, False)
                    positions[pos] = '-'
                    if score > best_score:
                        best_score = score
                        best_move = pos
            
        positions[best_move] = ai_character
        pos_buttons[best_move]['text'] = positions[best_move]
        game_over = check_game_over(positions)
        turn = 1
        turns += 1

def player_pos(position):
    global turn
    global turns
    global game_over
    global winner
    if turn == 1 and turns < 9 and game_over == False:
        if positions[position] == '-':
            # if turns >= 8:
            #     winner = ''
            #     game_over = True
            #     messagebox.showinfo(title="It's a draw!", message="How could you get a draw againt a simple AI ????")
            positions[position] = player_character
            pos_buttons[position]['text'] = positions[position]
            game_over = check_game_over(positions)
            turn = 0
            turns += 1
            ai_turn()
    
def draw_board():
    global positions
    global turn
    global turns
    global game_over
    game_over = False
    turn = 0
    turns = 0
    positions = ['-' for _ in range(9)]
    win_label.config(text='')
    win_label.grid_remove()
    
    
    for button in pos_buttons:
        button['text'] = '-'
    
    global start_button
    start_button['state'] = DISABLED
    c,  r = 0, 5
    for j in range(9):
        if c>2: 
            c=0
            r+=1
        pos_buttons[j].grid(row=r, column=c, sticky='nesw')
        c += 1
    ai_turn()

def xo_select(x):
    global player_character
    global ai_character
    player_character = x
    ai_character = 'Ｏ' if player_character == '✖' else '✖'

    for j in range(9):
        pos_buttons[j].grid_remove()

    global popup
    popup.deiconify()
    player_label = Label(popup, text=f'You have selected {player_character}', font=FONT)
    player_label.grid(row=3, column=0, columnspan= 3, padx=10, pady=(20,0))
    
    global start_button
    start_button = Button(popup, text='Start!', command=draw_board, font=FONT)
    start_button.grid(row=4, column=0, columnspan=3, padx=10, pady=30)
    start_button['state'] = NORMAL

#Simple widget definition
main_label = Label(root, text='Welcome to Tic-Tac-Toe', font=FONT)
player_select_label = Label(root, text='Select a character to play as!', font=FONT)
win_label = Label(root, font=FONT)

#Simple widget placement
main_label.grid(row=0, column=0, columnspan= 3, padx=10, pady=10)
player_select_label.grid(row=1, column=0, columnspan= 3, padx=10, pady=1)

#Position_buttons definition
for j in range(9):
    pos_buttons.append(Button(popup, text=positions[j], command=lambda j=j: player_pos(j), 
                                    font=FONT, height= 3, width=7))

#x & o buttons definition and placement
xo_buttons = {}
xo_options = {'✖': 0, 'Ｏ':2}
for i in xo_options.keys():
    def func(x=i):
        return xo_select(x)
    
    xo_buttons[i] = Button(root, text= i, command= func, font=FONT)
    xo_buttons[i].grid(row=2, column = xo_options[i], sticky='ew', padx=10, pady=5)

def on_closing():
    for j in range(9):
        pos_buttons[j].grid_remove()
    popup.withdraw()


popup.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()



