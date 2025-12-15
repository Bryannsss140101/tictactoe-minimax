#include "Game.h"
#include <algorithm>
#include <limits>
#include <random>
#include <vector>

enum Difficulty { MEDIUM, HARD };

struct Node {
  int value;
  Game state;
  Move action;
  Node *parent;
  std::vector<Node *> children;

  Node(const Game &state, const Move &action = {-1, -1}, Node *parent = nullptr)
      : state(state), action(action), parent(parent), value(0) {}
};

class Tree {
private:
  Node *root = nullptr;
  Difficulty difficulty = MEDIUM;

  Game result(const Game &s, const Move &a) {
    Game newState = s;
    newState.makeMove(a);
    return newState;
  }

  bool isTerminal(const Game &s) { return s.getWinner() != 0 || s.isDraw(); }

  int utility(const Game &state) { return state.getWinner(); }

  void expand(Node *node) {
    if (!node)
      return;

    if (isTerminal(node->state))
      return;

    if (!node->children.empty())
      return;

    for (const auto &a : node->state.getAvailableMoves()) {
      Game newState = result(node->state, a);
      Node *child = new Node(newState, a, node);
      node->children.push_back(child);
    }
  }

  int minimax(Node *node) {
    if (isTerminal(node->state))
      return node->value = utility(node->state);

    expand(node);

    bool maximazing = node->state.getTurn();
    int bestValue = maximazing ? std::numeric_limits<int>::min()
                               : std::numeric_limits<int>::max();

    for (Node *child : node->children) {
      bestValue = maximazing ? std::max(bestValue, minimax(child))
                             : std::min(bestValue, minimax(child));
    }

    return node->value = bestValue;
  }

  void clear(Node *node) {
    if (!node)
      return;

    for (Node *child : node->children)
      clear(child);
    delete node;
  }

  Move getChoice(Node *node, Move best, double error = 0.5) {
    if (!node || node->children.empty())
      return best;

    static std::mt19937 rng(std::random_device{}());
    std::uniform_real_distribution<double> prob(0.0, 1.0);

    if (prob(rng) < error) {
      std::uniform_int_distribution<int> pick(0,
                                              (int)node->children.size() - 1);
      return node->children[pick(rng)]->action;
    }

    return best;
  }

public:
  Tree() = default;

  Tree(Difficulty difficulty) : difficulty(difficulty) {}

  ~Tree() {
    clear(root);
    root = nullptr;
  }

  Move getMove(const Game &s) {
    clear(root);
    root = nullptr;

    root = new Node(s);
    minimax(root);

    bool maximizing = s.getTurn();
    int bestValue = maximizing ? std::numeric_limits<int>::min()
                               : std::numeric_limits<int>::max();

    Move bestMove{-1, -1};

    for (Node *child : root->children) {
      int value = child->value;

      if ((maximizing && value > bestValue) ||
          (!maximizing && value < bestValue)) {
        bestValue = value;
        bestMove = child->action;
      }
    }

    if (difficulty == MEDIUM)
      return getChoice(root, bestMove, 0.75);

    return bestMove;
  }
};