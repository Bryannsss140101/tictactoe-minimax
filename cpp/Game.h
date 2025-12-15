#include <ostream>
#include <vector>

struct Move {
  int row;
  int col;
};

class Game {
private:
  bool turn;
  int board[3][3];

public:
  bool getTurn() const { return turn; }

  void setTurn(bool turn) { this->turn = turn; }

  int getCell(int row, int col) const { return board[row][col]; }

  void setCell(int row, int col, int value) { board[row][col] = value; }

  Game() : turn(true) {
    for (int i = 0; i < 3; i++)
      for (int j = 0; j < 3; j++)
        board[i][j] = 0;
  }

  Game(bool turn, const int (&board)[3][3]) : turn(turn) {
    for (int i = 0; i < 3; i++)
      for (int j = 0; j < 3; j++)
        this->board[i][j] = board[i][j];
  }

  std::vector<Move> getAvailableMoves() const {
    std::vector<Move> moves;

    for (int i = 0; i < 3; i++)
      for (int j = 0; j < 3; j++)
        if (board[i][j] == 0)
          moves.push_back({i, j});

    return moves;
  }

  bool makeMove(Move move) {
    int row = move.row, col = move.col;

    if (row < 0 || row >= 3 || col < 0 || col >= 3)
      return false;

    if (board[row][col] != 0)
      return false;

    board[row][col] = turn ? +1 : -1;

    turn = !turn;

    return true;
  }

  int getWinner() const {
    for (int i = 0; i < 3; i++) {
      int value = board[i][0] + board[i][1] + board[i][2];
      if (value == 3)
        return +1;
      if (value == -3)
        return -1;
    }

    for (int j = 0; j < 3; j++) {
      int value = board[0][j] + board[1][j] + board[2][j];
      if (value == 3)
        return +1;
      if (value == -3)
        return -1;
    }

    int d1 = board[0][0] + board[1][1] + board[2][2];
    if (d1 == 3)
      return +1;
    if (d1 == -3)
      return -1;

    int d2 = board[0][2] + board[1][1] + board[2][0];
    if (d2 == 3)
      return +1;
    if (d2 == -3)
      return -1;

    return 0;
  }

  bool isDraw() const {
    if (getWinner() != 0)
      return false;

    for (int i = 0; i < 3; i++)
      for (int j = 0; j < 3; j++)
        if (board[i][j] == 0)
          return false;

    return true;
  }
};