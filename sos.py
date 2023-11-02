
from tictactoe.board import Board
import random


def minimax(self, board: Board, ai_turn: bool, depth: int, alpha: float, beta: float) -> tuple:
    # Fetch all the empty squares (possible moves) on the board.
    available_moves = board.empty_squares

    # If it's the start of the game, make a random move.
    if len(available_moves) == board.size ** 2:
        return 0, random.choice(list(range(board.size ** 2)))

    # Base cases: Check if the game is over or if we've reached the maximum depth.
    if board.is_gameover() or depth >= self.level:
        return self.evaluate_board(board, depth), None

    if ai_turn:
        # Set initial value for maximum evaluation (since AI wants to maximize its score).
        max_eval = float('-inf')
        best_move = None

        # Check all available moves.
        for move in available_moves:
            # Make a move for the AI on the board.
            board.push(move, self.ai)

            # Recursively get the evaluation of this move.
            eval_ = self.minimax(board, False, depth + 1, alpha, beta)[0]

            # Undo the move to backtrack and explore other possibilities.
            board.undo(move)

            # If this move forces the opponent to complete a line, it's a great move.
            if board.winner() == self.foe:
                return board.size ** 2 - depth, move

            # Update maximum evaluation if this move is better than previous ones.
            max_eval = max(max_eval, eval_)

            # Update the best move if current move has the maximum evaluation.
            if max_eval == eval_:
                best_move = move

            # Alpha-beta pruning: Update alpha (best score for maximizing player).
            alpha = max(alpha, max_eval)

            # If the best score for the maximizing player exceeds the worst score for the minimizing player, prune.
            if alpha > beta:
                return max_eval, best_move

        # Return the best move and its evaluation.
        return max_eval, best_move

    else:
        # Set initial value for minimum evaluation (since opponent wants to minimize AI's score).
        min_eval = float('inf')
        best_move = None

        # Check all available moves.
        for move in available_moves:
            # Make a move for the opponent on the board.
            board.push(move, self.foe)

            # Recursively get the evaluation of this move.
            eval_ = self.minimax(board, True, depth + 1, alpha, beta)[0]

            # Undo the move to backtrack and explore other possibilities.
            board.undo(move)

            # If this move forces the AI to complete a line, it's a bad move for the AI.
            if board.winner() == self.ai:
                return -1 * board.size ** 2 - depth, move

            # Update minimum evaluation if this move is worse for the AI than previous ones.
            min_eval = min(min_eval, eval_)

            # Update the best move if current move has the minimum evaluation.
            if min_eval == eval_:
                best_move = move

            # Alpha-beta pruning: Update beta (worst score for maximizing player).
            beta = min(min_eval, beta)

            # If the worst score for the maximizing player is less than the best score for the minimizing player, prune.
            if beta < alpha:
                return min_eval, best_move

        # Return the best move and its evaluation.
        return min_eval, best_move
