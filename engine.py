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

pst = {
        'P': (   0,   0,   0,   0,   0,   0,   0,   0,
                78,  83,  86,  73, 102,  82,  85,  90,
                7,  29,  21,  44,  40,  31,  44,   7,
                -17,  16,  -2,  15,  14,   0,  15, -13,
                -26,   3,  10,   9,   6,   1,   0, -23,
                -22,   9,   5, -11, -10,  -2,   3, -19,
                -31,   8,  -7, -37, -36, -14,   3, -31,
                0,   0,   0,   0,   0,   0,   0,   0),
        'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
                -3,  -6, 100, -36,   4,  62,  -4, -14,
                10,  67,   1,  74,  73,  27,  62,  -2,
                24,  24,  45,  37,  33,  41,  25,  17,
                -1,   5,  31,  21,  22,  35,   2,   0,
                -18,  10,  13,  22,  18,  15,  11, -14,
                -23, -15,   2,   0,   2,   0, -23, -20,
                -74, -23, -26, -24, -19, -35, -22, -69),
        'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
                -11,  20,  35, -42, -39,  31,   2, -22,
                -9,  39, -32,  41,  52, -10,  28, -14,
                25,  17,  20,  34,  26,  25,  15,  10,
                13,  10,  17,  23,  17,  16,   0,   7,
                14,  25,  24,  15,   8,  25,  20,  15,
                19,  20,  11,   6,   7,   6,  20,  16,
                -7,   2, -15, -12, -14, -15, -10, -10),
        'R': (  35,  29,  33,   4,  37,  33,  56,  50,
                55,  29,  56,  67,  55,  62,  34,  60,
                19,  35,  28,  33,  45,  27,  25,  15,
                0,   5,  16,  13,  18,  -4,  -9,  -6,
                -28, -35, -16, -21, -13, -29, -46, -30,
                -42, -28, -42, -25, -25, -35, -26, -46,
                -53, -38, -31, -26, -29, -43, -44, -53,
                -30, -24, -18,   5,  -2, -18, -31, -32),
        'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
                14,  32,  60, -10,  20,  76,  57,  24,
                -2,  43,  32,  60,  72,  63,  43,   2,
                1, -16,  22,  17,  25,  20, -13,  -6,
                -14, -15,  -2,  -5,  -1, -10, -20, -22,
                -30,  -6, -13, -11, -16, -11, -16, -27,
                -36, -18,   0, -19, -15, -15, -21, -38,
                -39, -30, -31, -13, -31, -36, -34, -42),
        'K': (   4,  54,  47, -99, -99,  60,  83, -62,
                -32,  10,  55,  56,  56,  55,  10,   3,
                -62,  12, -57,  44, -67,  28,  37, -31,
                -55,  50,  11,  -4, -19,  13,   0, -49,
                -55, -43, -52, -28, -51, -47,  -8, -50,
                -47, -42, -43, -79, -64, -32, -29, -32,
                -4,   3, -14, -50, -57, -18,  13,   4,
                17,  30,  -3, -14,   6,  -1,  40,  18),
    }
    
    
def scoreSquare(board, square):
    pieceValue = 0
    if(board.piece_type_at(square) == chess.PAWN):
        pieceValue = P + pst['P'][square]
    elif (board.piece_type_at(square) == chess.ROOK):
        pieceValue = R + pst['R'][square]
    elif (board.piece_type_at(square) == chess.BISHOP):
        pieceValue = B + pst['B'][square]
    elif (board.piece_type_at(square) == chess.KNIGHT):
        pieceValue = N + pst['N'][square]
    elif (board.piece_type_at(square) == chess.QUEEN):
        pieceValue = Q + pst['Q'][square]
    elif (board.piece_type_at(square) == chess.KING):
        pieceValue = K + pst['K'][square]

    if board.color_at(square)!= board.turn:
        return -pieceValue
    else:
        return pieceValue

def mateOpportunity(board):
    if board.is_checkmate():
        return 99999
    else:
        return 0

def opening(board):
    if board.fullmove_number < 10:
        return 1/30 * board.legal_moves.count()
    else:
        return 0
    
# def get_all_set_bits(bits):
#     bits_index = []
#     for i, c in enumerate(bin(bits)[:1:-1], 1):
#         if c == '1':
#             bits_index.append(i-1)
#     return bits_index

def evaluate(board):
    score = 0
    for i in range(64):
        score += scoreSquare(board, chess.SQUARES[i])
    score += mateOpportunity(board) + opening(board)
    return score

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
            if polyglot: 
                return random_choice(polyglot)
            else: 
                return bestMove
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
            if polyglot: 
                return random_choice(polyglot)
            else: 
                return bestMove
        else:
            return minEval