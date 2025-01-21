DIM = 8

class Piece:
    def __init__(self, is_white=None, type='-', rank=None, file=None):
        self.is_white = is_white
        self.type = type
        self.rank = rank
        self.file = file
        self.not_moved = True
        self.valids = []


    def __str__(self):
        if not self.is_white:
            return self.type.lower()
        return self.type


    def in_bounds(self, rank, file):
        return rank >= 0 and rank <= 7 and file >= 0 and file <= 7
    

    def stop_check(self, cur_match):
        new_valids = []

        for valid_move in self.valids:
            if not cur_match.move_cause_check(self, valid_move):
                new_valids.append(valid_move)
        self.valids = new_valids
    
    
    # returns a list of valid moves that player can make with selected piece
    def get_valids(self, cur_match):
        self.valids = []
        movement_rules = {
            'P': self.pawn_valids,
            'N': self.knight_valids,
            'K': self.king_valids,
            'R': self.shared_planes,
            'B': self.shared_planes,
            'Q': self.shared_planes,
        }
        return movement_rules[self.type](cur_match)
    
    def is_opp(self, other_piece):
        if other_piece.type == '-' or (self.is_white == other_piece.is_white):
            return False
        return True
    
    def add_valid(self, cur_match, rank, file):
        if not self.in_bounds(rank, file):
            return True    # should break loop
        
        bool_is_opp = self.is_opp(cur_match.board[rank][file])
        if cur_match.board[rank][file].type == '-' or bool_is_opp:
            self.valids.append([rank, file])
            if not bool_is_opp:
                return False    # don't break loop
        
        return True    # should break loop
    
    # direction is integer for file change ... so 1 for right and -1 for left
    def can_en_passant(self, cur_match, direction):
        potential_pawn = cur_match.board[self.rank][self.file + direction]

        # return position eligibility (see Match class notes for idx meanings of last_pawn_move list)
        return cur_match.last_pawn_move[0] and cur_match.last_pawn_move[1] and cur_match.last_pawn_move[2] == potential_pawn
    
    def pawn_promotion(self, cur_match):
        prom_options = ['Q', 'R', 'B', 'K']
        last_rank = 0
        if not cur_match.is_wht_turn:
            last_rank = 7
            for i in range(len(prom_options)):
                prom_options[i] = prom_options[i].lower()

        if self.rank != last_rank or cur_match.in_check(self.is_white):
            return
        
        invalid_answer = True
        while invalid_answer:
                                                                # ONLY FOR TESTING WITH PRERAN GAMES
            # can pawn promotion prevent a check? (the act of promoting a pawn to something else)
            # remove 2nd element (cur_match.cur_move[3] != None) and check with game on row 9 of chessgames.csv to find bug
            if cur_match.cur_move != None and cur_match.cur_move[3] == None:
                return
            # remove 2nd element (cur_match.cur_move[3] != None) and check with game on row 9 of chessgames.csv to find bug
            if cur_match.cur_move != None and cur_match.cur_move[3] != None and '=' in cur_match.cur_move[3]:
                choice = cur_match.cur_move[3][2]
                if not cur_match.is_wht_turn:
                    choice = choice.lower()
            else:
                choice = input(f'\nPromote pawn to one of the following: {prom_options[0]}, {prom_options[1]}, {prom_options[2]}, {prom_options[3]}').replace(' ', '')
            if choice in prom_options:
                invalid_answer = False
        
        cur_match.board[self.rank][self.file] = Piece(is_white=self.is_white, type=choice.upper(), rank=self.rank, file=self.file)


    def pawn_valids(self, cur_match):
        rank_change = 1
        if self.is_white:
            rank_change = -1

        if cur_match.board[self.rank + rank_change][self.file].type == '-':
            can_attempt_two = not self.add_valid(cur_match, self.rank + rank_change, self.file)
            if self.not_moved and can_attempt_two and cur_match.board[self.rank + rank_change * 2][self.file].type == '-':
                self.add_valid(cur_match, self.rank + rank_change * 2, self.file)


        # attack another piece
        if self.in_bounds(self.rank + rank_change, self.file - 1) and self.is_opp(cur_match.board[self.rank + rank_change][self.file - 1]):
            self.add_valid(cur_match, self.rank + rank_change, self.file - 1)
        if self.in_bounds(self.rank + rank_change, self.file + 1) and self.is_opp(cur_match.board[self.rank + rank_change][self.file + 1]):
            self.add_valid(cur_match, self.rank + rank_change, self.file + 1)

        # en passant
        if self.in_bounds(self.rank + rank_change, self.file + 1) and self.can_en_passant(cur_match, 1):
            self.add_valid(cur_match, self.rank + rank_change, self.file + 1)

        if self.in_bounds(self.rank + rank_change, self.file + 1) and self.can_en_passant(cur_match, -1):
            self.add_valid(cur_match, self.rank + rank_change, self.file - 1)


        # remove moves that cause checks
        self.stop_check(cur_match)


    def knight_valids(self, cur_match):
        # 2d array of position changes for knight
        # idx 0 array is rank changes
        # idx 1 array is file changes
        changes = [
            [-1, -2, -2, -1, 1, 2, 2, 1],
            [-2, -1, 1, 2, 2, 1, -1, -2]
        ]

        for i in range(len(changes[0])):
            rank = self.rank + changes[0][i]
            file = self.file + changes[1][i]
            self.add_valid(cur_match, rank, file)

        
        # remove moves that cause checks
        self.stop_check(cur_match)
        

    def can_castle(self, cur_match, change):
        last_file = 0       # last_file means the leftmost or rightmost file, with leftmost of 0 being default
        if change == 1:     # if change is positive, then rightmost file of 7 is last_file
            last_file = 7

        # ensuring all squares in between king and rook are empty
        file = self.file + change
        while file != last_file:
            piece_type = cur_match.board[self.rank][file].type

            if piece_type != '-':
                return False
            
            file += change

        for i in range(1, 3):
            to_coords = [self.rank, self.file + change * i]
            if cur_match.move_cause_check(self, to_coords):
                return False

        return True

        

        
    def king_valids(self, cur_match):

        for rank in range(self.rank - 1, self.rank + 2):
            for file in range(self.file - 1, self.file + 2):
                #if self.in_bounds(rank, file) and not (rank == self.rank and file == self.file) and not cur_match.move_cause_check(self, [rank, file]):
                if self.in_bounds(rank, file) and not (rank == self.rank and file == self.file):
                    self.add_valid(cur_match, rank, file)
        
        if self.is_white == cur_match.is_wht_turn and self.not_moved:
            
            rook_rank = 0       # black rook rank
            if self.is_white:
                rook_rank = 7   # white rook rank

            left_rook = cur_match.board[rook_rank][0]
            if left_rook.type == 'R' and left_rook.not_moved and self.can_castle(cur_match, -1):
                self.add_valid(cur_match, self.rank, self.file - 2)
            
            right_rook = cur_match.board[rook_rank][7]
            if right_rook.type == 'R' and right_rook.not_moved and self.can_castle(cur_match, 1):
                self.add_valid(cur_match, self.rank, self.file + 2)
            
        self.stop_check(cur_match)



        

    def shared_planes(self, cur_match):
        change = [-1, 1]    #
        SIZE_CHANGE = 2     #

        for i in range(SIZE_CHANGE):
            for j in range(SIZE_CHANGE):
                if self.type == 'R' or self.type == 'Q':
                    rank = self.rank
                    file = self.file
                    while True:
                        if i == 0:
                            rank += change[j]
                        else:
                            file += change[j]
                        break_loop = self.add_valid(cur_match, rank, file)
                        if break_loop:
                            break
                if self.type == 'B' or self.type == 'Q':
                    rank = self.rank
                    file = self.file
                    while True:
                        rank += change[i]
                        file += change[j]
                        break_loop = self.add_valid(cur_match, rank, file)
                        if break_loop:
                            break
        
        # remove moves that cause checks
        self.stop_check(cur_match)
