import chess
import chess.polyglot
from random import choice as random_choice


maxDepth = 5
P = 100
N = 320
B = 330
R = 500
Q = 900
K = 20000

piece_values = {
    None: 0,
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 10000,
}

pst = {
    chess.PAWN: [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
    ],
    chess.KNIGHT: [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
    ],
    chess.BISHOP: [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
    ],
    chess.ROOK: [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
    ],
    chess.QUEEN: [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
    ],
    chess.KING: [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
    ],
}
    
def lsb(x: int) -> int:
    return (x & -x).bit_length() - 1

def poplsb(x: int) -> int:
    x &= x - 1
    return x

def eval_side(board: chess.Board, color: chess.Color) -> int:
        # Implement in the future
        # Castling
        # Passed pawns
        # Center control
        # Pins
        
        occupied = board.occupied_co[color]

        material = 0
        psqt = 0

        while occupied:
            square = lsb(occupied)

            piece = board.piece_type_at(square)

            material += piece_values[piece]

            psqt += (
                list(reversed(pst[piece]))[square]
                if color == chess.BLACK
                else pst[piece][square]
            )

            occupied = poplsb(occupied)

        return material + psqt

def evaluate(board: chess.Board) -> int:
    return eval_side(board, board.turn) - eval_side(board, not board.turn)

def getBestMove(board, depth=1, maximizingPlayer=True, alpha=float('-inf'), beta=float('inf')):
    if depth == maxDepth or board.legal_moves.count() == 0:
        score = evaluate(board)
        return score
    
    with chess.polyglot.open_reader("polyglot/polyglot-normal.bin") as reader:
        polyglot = []
        for entry in reader.find_all(board):
            polyglot.append(entry.move)
    
    if maximizingPlayer:
        maxEval = float('-inf')
        for move in board.legal_moves:
            # print(board)
            board.push(move)
            
            eval = getBestMove(board, (depth + 1), False, alpha, beta)
            
            board.pop()
            
            if eval > maxEval:
                maxEval = eval
                bestMove = move
                
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        if depth == 1:
            # if polyglot: 
            #     return random_choice(polyglot)
            # else: 
            return bestMove, maxDepth, maxEval / 100
        else:
            return maxEval
    
    else: 
        minEval = float('inf')
        for move in board.legal_moves:
            # print(board)
            board.push(move)
            
            eval= getBestMove(board, (depth + 1), True, alpha, beta)
            
            board.pop()
            
            if eval < minEval:
                minEval = eval
                bestMove = move
            beta = min(beta, eval)
            
            if beta <= alpha:
                break
            
        if depth == 1:
            # if polyglot: 
            #     return random_choice(polyglot)
            # else: 
            return bestMove, maxDepth, minEval / 100
        else:
            return minEval