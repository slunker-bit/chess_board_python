import os
from chess_pieces import *
from chess_move_translater import *
from printers import *
from match_class import Match
from printers import *


def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')



def main():
    cur_match = Match()
    while True:
        print(cur_match)
        while True:
            if cur_match.in_check(cur_match.is_wht_turn):
                if cur_match.checkmate_or_stalemate():
                    #checkmate
                    print_winner(cur_match)
                    return 0
                print_check(cur_match)
            else:
                if cur_match.checkmate_or_stalemate():
                    #stalemate
                    print_stalemate()
                    return 0
            print('\n\nType QUIT to quit the game.\n')
            coords = input('piece: ')

            if Match.quitter(coords):
                return 0
            coords = Match.input_formatter(coords)
            if coords != None:
                piece = cur_match.board[coords[0]][coords[1]]
                break

        if piece.is_white == cur_match.is_wht_turn:
            valids = piece.get_valids(cur_match)
            print('\n****************')
            print(f'({piece}): {chr(piece.file + ord("a"))}{DIM - piece.rank}')
            print('****************')
            print_valids(piece)
            print('****************\n')

            invalid_move = True
            if len(piece.valids) != 0:
                while invalid_move:
                    print('\nType QUIT to choose another piece.')
                    move_to = input('move to: ')
                    if Match.quitter(move_to):
                        break
                    move_coords = Match.input_formatter(move_to)
                    if move_coords != None:
                        invalid_move = cur_match.move(piece, move_coords)
                        if not invalid_move:
                            cur_match.is_wht_turn = not cur_match.is_wht_turn
        else:
            cur_color = 'Black'
            if cur_match.is_wht_turn:
                cur_color = 'White'
            print(f'Select the current color: {cur_color}')

if __name__ == '__main__':
    main()