''' Problem -38 : Tic-Tac-Toe'''
from IPython.display import clear_output
import os
board=[str(i) for i in range (1,9+1)]
def clear_screen():
    try:
        clear_output(wait=True)
    except:
        os.system('cls' if os.name =='nt' else 'clear')
def print_board():
        print(f"{board[0]} | {board[1]} | {board[2]}")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print(f"{board[6]} | {board[7]} | {board[8]}")
def check_winner(mark):
    win_combos=[
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in win_combos:
        if board[a]==board[b]==board[c]==mark:
            return True
    return False        
def is_board_full():
    return all(cell in ('X','O')for cell in board)
def get_move(player_mark):
    while True:
        choice=input(f"Player {player_mark}, move choose(1,9):")
        if not choice.isdigit() or not(1<=int(choice)<=9):
            print("Wrong Input!")
            continue
        idx=int(choice)-1
        if board[idx] in ('X','O'):
            print("Cell is already full")
            continue
        return idx
def play_game():
    current_player='X'
    print_board()
    while True:
        idx=get_move(current_player)
        board[idx]=current_player
        print_board()
        if check_winner(current_player):
            print(f"Player{current_player} Win!")
            break
        if is_board_full():
            print("Draw")
            break
        current_player='O' if current_player=='X' else 'X'
if __name__=="__main__":
    play_game()
        