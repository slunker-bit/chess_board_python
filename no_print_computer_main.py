from chess_pieces import *
from chess_move_translater import *
from printers import *
from match_class import Match
from printers import *

import time


move_idx = 0

def main(game, game_num):
    cur_match = Match()
    cur_match.moves = game
    move_idx = 0
    while True:
        while True:
            if cur_match.in_check(cur_match.is_wht_turn):
                if cur_match.checkmate_or_stalemate():
                    #checkmate
                    print(f'({num_game}) row {game_num}: ', end='')
                    print_winner(cur_match)
                    return 0
            else:
                if cur_match.checkmate_or_stalemate():
                    #stalemate
                    print(f'({num_game}) row {game_num}: ', end='')
                    print_stalemate()
                    return 0
            cur_match.cur_move = cur_match.moves[move_idx]
            coords = ''

            if Match.quitter(coords):
                return 0
            coords = [0,0]
            piece = cur_match.find_origin_square(cur_match.moves[move_idx])
            coords[0] = piece.rank
            coords[1] = piece.file
            if coords != None:
                piece = cur_match.board[coords[0]][coords[1]]
                break

        if piece.is_white == cur_match.is_wht_turn:
            valids = piece.get_valids(cur_match)

            invalid_move = True
            if len(piece.valids) != 0:
                while invalid_move:
                    move_to = cur_match.moves[move_idx][2]
                    move_idx += 1
                    move_coords = Match.input_formatter(move_to)
                    if Match.quitter(move_to):
                        break
                    elif move_coords != None:
                        invalid_move = cur_match.move(piece, move_coords)
                        if not invalid_move:
                            cur_match.is_wht_turn = not cur_match.is_wht_turn
        


num_game = 1

if __name__ == '__main__':

    start = time.time()

    unparsed_games = read_moves_from_csv('chessgames.csv')
    games = get_game_list()
    for game_idx in range(50):
        moves = games[game_idx]
        special = moves[len(moves)-1][3]
        if special != None and 'checkmate' in moves[len(moves)-1][3]:
            game_start = time.time()
            main(moves, game_idx + 2)
            game_end = time.time()
            print(f'Game {num_game} took {game_end-game_start} seconds.\n')

            num_game += 1
    
    end = time.time()
    length = end - start

    print(f'It took {length} seconds for {num_game-1} games.')