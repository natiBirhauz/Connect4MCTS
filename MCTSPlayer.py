import ConnectFour
import MCTSNode
import math
import random

class MCTSPlayer:
    def __init__(self, iterations=1000):
        self.iterations = iterations

    def choose_move(self, game):
        """Uses MCTS to select the best move for the current player."""
        root = MCTSNode(game)

        for _ in range(self.iterations):
            node = root
            # Selection: Traverse the tree until a leaf node is found
            while node.is_fully_expanded() and node.children:
                node = node.best_child()
            # Expansion: Expand the node if not terminal
            if node.game_state.status == node.game_state.ONGOING:
                node = node.expand()
            # Simulation: Rollout from this node
            result = self.simulate(node.game_state)
            # Backpropagation: Update the nodes with the result
            node.backpropagate(result)

        # Select the move that leads to the most visited child
        best_move = max(root.children, key=lambda child: child.visits).move
        return best_move

    def simulate(self, game):
        """Simulates a game by making random moves until a terminal state is reached."""
        simulated_game = game.clone()
        while simulated_game.status == simulated_game.ONGOING:
            move = random.choice(simulated_game.legal_moves())
            simulated_game.make(move)
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

