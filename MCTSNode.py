import math

class MCTSNode:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state.clone()  # Clone the game state to avoid mutations
        self.parent = parent
        self.move = move  # The move that led to this node
        self.children = []  # List of child nodes
        self.visits = 0  # Total number of visits
        self.wins = 0  # Number of wins for the current player

    def is_fully_expanded(self):
        """Checks if all possible moves have been expanded."""
        return len(self.children) == len(self.game_state.legal_moves())

    def best_child(self, exploration_weight=1.0):
        """Selects the child node based on the UCT formula."""
        return max(
            self.children,
            key=lambda child: (child.wins / child.visits) + 
                              exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
        )

    def expand(self):
        """Expands the node by adding one child node for an untried move."""
        tried_moves = [child.move for child in self.children]
        legal_moves = self.game_state.legal_moves()
        for move in legal_moves:
            if move not in tried_moves:
                # Create a new game state for the child
                new_game_state = self.game_state.clone()
                new_game_state.make(move)
                child_node = MCTSNode(new_game_state, parent=self, move=move)
                self.children.append(child_node)
                return child_node
        return None  # All moves already expanded

    def backpropagate(self, result):
        """Backpropagates the result of a simulation."""
        self.visits += 1
        if result == self.game_state.player:
            self.wins += 1
        elif result == 0:  # Draw
            self.wins += 0.5
        if self.parent:
            self.parent.backpropagate(result)
