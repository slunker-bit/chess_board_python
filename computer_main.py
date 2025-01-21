from chess_pieces import *
from chess_move_translater import *
from printers import *
from match_class import Match
from printers import *

DIM = 8


move_idx = 0

def main(game, game_num):
    cur_match = Match()
    #cur_match.moves = games[game_idx]
    cur_match.moves = game
    move_idx = 0
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
            #print(f'algebraic move: {cur_match.moves[move_idx]}')
            cur_match.cur_move = cur_match.moves[move_idx]
            coords = ''

            if Match.quitter(coords):
                return 0
            #coords = input_formatter(coords)
            coords = [0,0]
            piece = cur_match.find_origin_square(cur_match.moves[move_idx])
            print(f'piece: ({piece})-{chr(piece.file + ord("a"))}{DIM - piece.rank}')
            if piece == None:
                for move in cur_match.moves:
                    print(move)
            coords[0] = piece.rank
            coords[1] = piece.file
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
                    #move_to = input('move to: ')
                    move_to = cur_match.moves[move_idx][2]
                    move_idx += 1
                    move_coords = Match.input_formatter(move_to)
                    print(f'move to: ({piece})-{chr(move_coords[1] + ord("a"))}{DIM - move_coords[0]}')
                    #print(move_coords)
                    if Match.quitter(move_to):
                        break
                    elif move_coords != None:
                        invalid_move = cur_match.move(piece, move_coords)
                        if not invalid_move:
                            cur_match.is_wht_turn = not cur_match.is_wht_turn
        else:
            cur_color = 'Black'
            if cur_match.is_wht_turn:
                cur_color = 'White'
            print(f'Select the current color: {cur_color}')
        


num_game = 1

if __name__ == '__main__':
    unparsed_games = read_moves_from_csv('chessgames.csv')
    games = get_game_list()
    for game_idx in range(300):
        moves = games[game_idx]
        special = moves[len(moves)-1][3]
        if special != None and 'checkmate' in moves[len(moves)-1][3]:
            main(moves, game_idx + 2)
            num_game += 1