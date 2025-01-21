from chess_pieces import *
from printers import *
import copy


class Match:
    def __init__(self):
        self.populate()
        self.blk_casualties = []
        self.wht_casualties = []
        self.is_wht_turn = True
        self.last_pawn_move = [
            False,  # idx 0 is whether or not last move was a pawn (True or False)
            False,      # idx 1 is if last move by pawn was 2 spaces
            None,   # idx 2 is last pawn that moved (Piece object)
        ]
        self.castle_pieces = []

    def __str__(self):
        string = ''
        string += '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
        string += '*****************\n'
        if self.is_wht_turn:
            string += '      White      \n'
        else:
            string += '      Black      \n'
        string += '*****************\n\n'

        for i in range(DIM + 1):
            if i != DIM:
                string += f'{8 - i} '
            else:
                string += '  '
            for j in range(DIM):
                if i != DIM:
                    next = self.board[i][j]
                    if next.type != '-' and not next.is_white:
                        next = next.type.lower()
                    else:
                        next = next.type
                    string += next + ' '
                else:
                    string += chr(j + ord('a')) + ' '
            string += '\n'
        
        string += '\nBlack Casualties: '
        for i in range(len(self.blk_casualties)):
            string += str(self.blk_casualties[i])
        string += '\nWhite Casualties: '
        for i in range(len(self.wht_casualties)):
            string += str(self.wht_casualties[i])
        
        return string 
    

    # formats the coordinates given by the user for the piece wanting to be moved from chess format to list index format
    # also checks if input is valid input for coordinates
    @staticmethod
    def input_formatter(coords_input):
        coords_input = coords_input.replace(' ', '').lower()
        if len(coords_input) != 2:
            raise Exception('Length of input too long.')
            return None
        rank = coords_input[0]
        file = coords_input[1]
        if not (ord(rank) >= ord('a') and ord(rank) <= ord('h')) or not (int(file) >= 1 and int(file) <= 8):
            raise Exception('Something up with this formatter')
            return None
        coords = []
        coords.append(8 - int(file))
        coords.append(int(ord(rank) - ord('a')))
        return coords

    @staticmethod
    def quitter(coords_input):
        return 'QUIT' in coords_input.upper()
    

    # REMOVE ONCE TESTING IS DONE
    def manual_populate(self):
        for rank in range(DIM):
            new_rank = []
            for file in range(DIM):
                if self.board[rank][file].type != 'K' and self.board[rank][file].type != 'R':
                    self.board[rank][file] = Piece()

    # REMOVE ONCE TESTING IS DONE
    def find_origin_square(self, move_data):
        move_piece_type = move_data[0]
        disambiguation = move_data[1]
        to_square = move_data[2]

        if move_piece_type == 'O-O-O' or move_piece_type == 'O-O':
            coords = Match.input_formatter(disambiguation)
            #print(coords)
            return self.board[coords[0]][coords[1]]

        possible_pieces = []
        for rank in range(DIM):
            for file in range(DIM):
                piece = self.board[rank][file]
                if piece.type != '-':
                    piece.get_valids(self)
                    
                    to_coords = Match.input_formatter(to_square)
                    if piece.type == move_piece_type and piece.is_white == self.is_wht_turn and to_coords in piece.valids:
                        possible_pieces.append(piece)

        if len(possible_pieces) == 0:
            raise Exception('find_origin_square did not properly find piece')
        
        # finds adequate piece using disambiguation if there is one
        if disambiguation != None:
            if len(disambiguation) != 1:
                raise Exception('Improper length of disambiguation.')
            
            valid_pieces = []
            try:
                disambiguation = int(disambiguation)
            except ValueError:      # value error means that disambiguation is a string and thus must be a file
                disambiguation = ord(disambiguation) - ord('a')
                for piece in possible_pieces:
                    if piece.file == disambiguation:
                        valid_pieces.append(piece)
                        
            else:                   # no error means that disambiguation is an integer and thus must be a rank
                disambiguation = 8 - disambiguation
                for piece in possible_pieces:
                    if piece.rank == disambiguation:
                        valid_pieces.append(piece)
            
            if len(valid_pieces) != 1:
                raise Exception('Disambiguation did not work properly.')
            
            return valid_pieces[0]
                    
        return possible_pieces[0]


    def populate(self):
        main_pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

        self.board = []
        for rank in range(DIM):

            is_white = False
            if rank > 1:
                is_white = True

            new_rank = []
            if rank == 0 or rank == 7:
                for file in range(DIM):
                    new_piece = Piece(is_white=is_white, type=main_pieces[file], rank=rank, file=file)
                    if new_piece.type == 'K':
                        if is_white:
                            self.wht_king = new_piece
                        else:
                            self.blk_king = new_piece
                    new_rank.append(new_piece)
            else:
                next = Piece()
                if rank == 1 or rank == 6:
                    next = Piece(is_white=is_white, type='P', rank=rank)
                for file in range(DIM):
                    next.file = file
                    new_rank.append(copy.deepcopy(next))
            self.board.append(new_rank)

        #self.manual_populate()

    
    def update_casualties(self, dest):
        # if not a space, then this is an opponent piece
        if dest.type != '-':
            if dest.is_white:
                self.wht_casualties.append(dest)
            else:
                self.blk_casualties.append(dest)


    # used purely for testing a move to see if it causes a check
    # returns False if move does NOT cause a check
    # returns True if move does cause a check
    def move_cause_check(self, piece, to_coords):
        orig_rank = piece.rank
        orig_file = piece.file
        to_rank = to_coords[0]
        to_file = to_coords[1]


        dest = self.board[to_rank][to_file]

        self.board[orig_rank][orig_file] = Piece()
        self.board[to_rank][to_file] = piece
        piece.rank = to_rank
        piece.file = to_file
        

        did_en_passant = False
        if piece.type == 'P' and abs(to_rank - orig_rank) == 1:
            file_change = to_file - orig_file
            if file_change != 0 and dest.type == '-' and self.board[orig_rank][orig_file + file_change].type == 'P':
                did_en_passant = True
                en_passant_taken_pawn = self.board[orig_rank][orig_file + file_change]
                self.board[orig_rank][orig_file + file_change] = Piece()

        cause_check = False
        if self.in_check(piece.is_white):
            cause_check = True
        
        self.board[to_rank][to_file] = dest
        self.board[orig_rank][orig_file] = piece
        piece.rank = orig_rank
        piece.file = orig_file
        if did_en_passant:
                self.board[orig_rank][orig_file + file_change] = en_passant_taken_pawn


        return cause_check


    # returns 0 if was valid move and successfully completed
    # returns 1 if was invalid move and was not able to completed
    def move(self, piece, to_coords):

        if to_coords not in piece.valids:
            return 1
        
        orig_rank = piece.rank
        orig_file = piece.file
        to_rank = to_coords[0]
        to_file = to_coords[1]
        
        dest = self.board[to_rank][to_file]
        self.update_casualties(dest)

        self.board[piece.rank][piece.file] = Piece()
        self.board[to_rank][to_file] = piece
        piece.rank = to_rank
        piece.file = to_file
        piece.not_moved = False

        if piece.type == 'P':
            self.last_pawn_move[0] = True       # last move was a pawn
            self.last_pawn_move[1] = False      # last move by pawn is 1 space by default
            self.last_pawn_move[2] = piece      # last pawn moved is current moving piece
            if abs(to_rank - orig_rank) == 2:
                self.last_pawn_move[1] = True   # last move by pawn was 2 spaces
            else:
                piece.pawn_promotion(self)

                # checking for en passant and removing piece if so
                file_change = to_file - orig_file
                if file_change != 0 and dest.type == '-' and self.board[orig_rank][orig_file + file_change].type == 'P':
                    self.update_casualties(self.board[orig_rank][orig_file + file_change])
                    self.board[orig_rank][orig_file + file_change] = Piece()


        else:
            self.last_pawn_move[0] = False      # last move was not a pawn
        

        
        if piece.type == 'K' and abs(to_file - orig_file) == 2:
            rook_from_file = 0
            rook_to_file = 3

            if to_file - orig_file == 2:
                rook_from_file = 7
                rook_to_file = 5

            self.board[piece.rank][rook_to_file] = self.board[piece.rank][rook_from_file]
            self.board[piece.rank][rook_to_file].file = rook_to_file
            self.board[piece.rank][rook_to_file].not_moved = False
            self.board[piece.rank][rook_from_file] = Piece()
        
        return 0


    def find_rook(self, find_right_rook, is_white):
        #if piece_type not in ['r', 'k']:
        #    raise Exception(f'find_rook_or_king only takes rooks or kings not \"{piece_type}\"')
        
        rook_file = 0
        if find_right_rook:
            rook_file = 7

        for rank in range(DIM):
            for file in range(DIM):
                piece = self.board[rank][file].type
                if piece.type == 'R' and piece.is_white == is_white:
                    return piece
        return None

    def find_cur_king(self):
        if self.is_wht_turn:
            return self.wht_king
        return self.blk_king
        
    # SEE IF REMOVING CALL PIECE BREAKS ANYTHING
    # determines if board is in check (returns True if in check and False if not)
    def check(self, call_piece):
        # determining if the given piece is the correct color for the turn
        if self.is_wht_turn != call_piece.is_white:
            return False
        
        cur_king = self.find_cur_king()
        
        for rank in range(DIM):
            for file in range(DIM):
                piece = self.board[rank][file]
                if piece.type != '-' and piece.is_white != self.is_wht_turn:
                    piece.get_valids(self)
                    if [cur_king.rank, cur_king.file] in piece.valids:
                        return True
        
        return False

    # ******* IS THE COLOR ARGUMENT NECESSARY??
    # determines if board is in check (returns True if in check and False if not)
    def in_check(self, color):
        if color != self.is_wht_turn:
            return False
        return self.check(self.find_cur_king())
        

    def checkmate_or_stalemate(self):
        for rank in range(DIM):
            for file in range(DIM):
                piece = self.board[rank][file]
                if piece.type != '-' and piece.is_white == self.is_wht_turn:
                    piece.get_valids(self)
                    if len(piece.valids) != 0:
                        return False
        return True
