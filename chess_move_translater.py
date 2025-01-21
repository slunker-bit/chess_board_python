import re

import csv


def get_game_list():
    file_path = 'chessgames.csv'  # Replace with your actual file path
    unparsed_games = read_moves_from_csv(file_path)

    games = []
    for unparsed_moves in unparsed_games:
        """
        USE THIS IF YOU DONT WANT ANY NONCHECKMATE GAMES TO APPEAR

        if '#' in unparsed_moves[len(unparsed_moves) - 1]:
            parsed_moves = []
            for idx in range(len(unparsed_moves)):
                move = unparsed_moves[idx]
                try:
                    parsed_moves.append(parse_chess_move(move, idx))
                    #print(f"Move: {move}, Parsed: {parse_chess_move(move)}")
                except ValueError as e:
                    print(e)
            games.append(parsed_moves)
        
        """
        parsed_moves = []
        for idx in range(len(unparsed_moves)):
            move = unparsed_moves[idx]
            try:
                parsed_moves.append(parse_chess_move(move, idx))
                #print(f"Move: {move}, Parsed: {parse_chess_move(move)}")
            except ValueError as e:
                print(e)
        games.append(parsed_moves)
    return games

def read_moves_from_csv(file_path):
    """
    Reads the first row of moves from a CSV file and returns a list of moves.
    Stops at the first blank move.

    :param file_path: Path to the CSV file.
    :return: A list of moves from the first row, stopping at the first blank move.
    """
    """
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        
        # Skip the header
        header = next(reader)
        
        # Read the first row of moves (assuming it is the first data row)
        first_row = next(reader, None)
        
        if not first_row:
            return []  # Return an empty list if there's no data row

        moves = []
        
        # Iterate through the row and collect moves until the first blank move
        for move in first_row[1:]:  # Skip the "Result" column
            if not move:  # Stop at the first blank move
                break
            moves.append(move)
        
        return moves
    
    """
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        
        # Skip the header
        header = next(reader)

        games = []
        
        #num_games = 100
        num_games = 400
        for i in range(num_games):
            game = next(reader, None)
            moves = []
            
            # Iterate through the row and collect moves until the first blank move
            for move in game[1:]:  # Skip the "Result" column
                if not move:  # Stop at the first blank move
                    break
                moves.append(move)
            
            games.append(moves)
        return games


def parse_chess_move(move, idx):
    """
    Parses an algebraic chess move and returns the origin and destination squares.
    Handles ambiguous moves, castling, and pawn promotions.

    :param move: A string representing the chess move in algebraic notation.
    :return: A tuple (origin, destination, special), where origin and destination are strings representing squares,
             and special indicates additional information (e.g., "castling" or "promotion").
    """
    # Handle castling
    if move == "O-O":
        #return "e1" if move.isupper() else "e8", "g1" if move.isupper() else "g8", "castling kingside"
        is_white = idx % 2 == 0
        return [move, "e1" if is_white else "e8", "g1" if is_white else "g8", "castling kingside"]
    if move == "O-O-O":
        #return "e1" if move.isupper() else "e8", "c1" if move.isupper() else "c8", "castling queenside"
        is_white = idx % 2 == 0
        return [move, "e1" if is_white else "e8", "c1" if is_white else "c8", "castling queenside"]

    # Regular expression to extract origin, destination, disambiguation, and special notations
    move_pattern = re.compile(r'([NBRQK]?)([a-h]?)([1-8]?)x?([a-h][1-8])(?:=([QRBN]))?')

    match = move_pattern.search(move)
    if match:
        piece = match.group(1)  # Piece type (e.g., N, B, R, Q, K)
        disambiguation_file = match.group(2)  # File (a-h) for disambiguation
        disambiguation_rank = match.group(3)  # Rank (1-8) for disambiguation
        destination = match.group(4)  # Destination square
        promotion = match.group(5)  # Captures promotion piece if present

        # Construct origin if disambiguation is provided
        origin = f"{disambiguation_file}{disambiguation_rank}" if disambiguation_file or disambiguation_rank else None

        special = f"P={promotion}" if promotion else None

        #return piece, origin, destination, special
        if piece == '':
            piece = 'P'
        else:
            piece = piece.upper()
        if '#' in move:
            if special != None:
                special += 'checkmate'
            else:
                special = 'checkmate'
        return [piece, origin, destination, special]

    if 'O-O-O' not in move and 'O-O' not in move:
        raise ValueError(f"Invalid move notation: {move}")

def main():
    # Example usage
    #moves = ["e2e4", "Nf3", "Raxd1", "Nbd2", "e7e8=Q", "O-O", "O-O-O"]
    file_path = 'chessgames.csv'  # Replace with your actual file path
    moves = read_moves_from_csv(file_path)
    parsed_moves = []
    for idx in range(len(moves)):
        move = moves[idx]
        try:
            parsed_moves.append(parse_chess_move(move))
            print(f"Move: {move}, Parsed: {parse_chess_move(move, idx)}")
        except ValueError as e:
            print(e)

    print(parsed_moves)

if __name__ == '__main__':
    main()