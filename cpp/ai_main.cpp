#include "Tree.h"
#include <iostream>

int main() {
  int turnInt;
  int diffInt;

  if (!(std::cin >> turnInt >> diffInt))
    return 1;

  Game g;
  g.setTurn(turnInt == 1);

  for (int i = 0; i < 3; i++)
    for (int j = 0; j < 3; j++) {
      int v;
      std::cin >> v;
      g.setCell(i, j, v);
    }

  Difficulty diff = (diffInt == 1) ? HARD : MEDIUM;
  Tree ai(diff);

  Move m = ai.getMove(g);
  std::cout << m.row << " " << m.col << "\n";
  return 0;
}
