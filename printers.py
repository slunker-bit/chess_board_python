from chess_pieces import *

def print_stalemate():
    print('DRAW!')

def print_winner(cur_match):
    if cur_match.is_wht_turn:
        print('BLACK WINS!')
    else:
        print('WHITE WINS!')

def print_check(cur_match):
    if cur_match.is_wht_turn:
        print('WHITE IS IN CHECK')
    else:
        print('BLACK IS IN CHECK')

def print_valids(self):
    for i in range(len(self.valids)):
        print(f'({i+1}): {chr(self.valids[i][1] + ord("a"))}{8 - self.valids[i][0]}')