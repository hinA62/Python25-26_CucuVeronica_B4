import math

def minimax(position, depth, alpha, beta, maximizing_player):
    if depth == 0 or position.is_game_over():
        return position.evaluate(), position

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        moves = position.get_all_valid_moves('W')
        
        for move in moves:
            evaluation = minimax(position.simulate_move(move[0], move[1]), depth - 1, alpha, beta, False)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha: break
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        moves = position.get_all_valid_moves('B')
        
        for move in moves:
            evaluation = minimax(position.simulate_move(move[0], move[1]), depth - 1, alpha, beta, True)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha: break
        return min_eval, best_move