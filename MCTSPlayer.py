from ConnectFour import ConnectFour
from MCTSNode import MCTSNode
import random

class MCTSPlayer:
    def __init__(self, iterations=1000):
        self.iterations = iterations

    def choose_move(self, game):
        """
        Chooses the best move using MCTS. Prioritizes immediate wins or blocking opponent wins.
        """
        # 1. Check for immediate winning moves
        for move in game.legal_moves():
            game_copy = game.clone()
            game_copy.make(move)
            if game_copy.status == game.player:  # Immediate win for the current player
                print(f"Immediate winning move: {move}")
                return move

        # 2. Block opponent's winning moves
        opponent = game.other(game.player)
        for move in game.legal_moves():
            game_copy = game.clone()
            game_copy.make(move)
            if game_copy.status == opponent:  # Opponent has a winning move
                print(f"Blocking opponent's winning move: {move}")
                return move

        # 3. Perform MCTS if no immediate wins or blocks
        root = MCTSNode(game)
        for _ in range(self.iterations):  # Number of MCTS iterations
            node = root
            # Selection: Traverse the tree until we find a node to expand
            while node.is_fully_expanded() and node.children:
                node = node.best_child()
            
            # Expansion: Expand the node
            if node.game_state.status == node.game_state.ONGOING:
                node = node.expand()
            
            # Simulation: Play out the game randomly to evaluate the node
            result = self.simulate(node.game_state)

            # Backpropagation: Update the tree with simulation results
            node.backpropagate(result)

        # Choose the best move based on visits
        best_move = max(root.children, key=lambda child: child.visits).move
        return best_move


    def simulate(self, game_state):
        """
        Simulates a game from the current state to the end.
        Prioritizes immediate winning moves to make simulations smarter.
        """
        simulated_game = game_state.clone()
        current_player = simulated_game.player

        while simulated_game.status == simulated_game.ONGOING:
            legal_moves = simulated_game.legal_moves()
            
            # Prioritize immediate wins for the current player
            for move in legal_moves:
                game_copy = simulated_game.clone()
                game_copy.make(move)
                if game_copy.status == current_player:
                    simulated_game.make(move)
                    break
            else:
                # If no immediate win, play a random move
                simulated_game.make(random.choice(legal_moves))
        
        # Return the result of the simulation
        return simulated_game.status


def main():
    game = ConnectFour()
    mcts_player = MCTSPlayer(iterations=1000)

    print("Welcome to Connect Four with MCTS AI!")
    print("Player 1 is RED (R) and Player 2 is YELLOW (Y).\n")

    while game.status == game.ONGOING:
        print(game)
        print("\nCurrent Player:", "RED" if game.player == game.RED else "YELLOW")
        
        if game.player == game.RED:  # Human Player
            try:
                move = int(input("Enter a column (0-6): "))
                if move not in game.legal_moves():
                    print("Illegal move. Try again.")
                    continue
                game.make(move)
            except ValueError:
                print("Invalid input. Enter a number between 0 and 6.")
        else:  # MCTS AI Player
            print("AI is thinking...")
            move = mcts_player.choose_move(game)
            print(f"AI chose column {move}")
            game.make(move)

    print(game)
    if game.status == game.RED:
        print("\nRED (Player 1) wins!")
    elif game.status == game.YELLOW:
        print("\nYELLOW (Player 2) wins!")
    else:
        print("\nIt's a draw!")
if __name__ == "__main__":
    main()

