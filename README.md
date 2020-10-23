# Search

## This repository contains four different search algorithms from both informed and uninformed search situations

### For uninformed search situation there is Depth First Search and Breath First Search in this repository
#### Depth First Search finds the path from the start to the goal by choosing one path and continuously exploring it until it gets to the goal or it eventually hits a dead end at which stage it will back off and use another path. This search method may not always find the shortest path to the goal but it will always  find a path to the goal provided there is one and the maze is finite.
#### Breath First Search finds the path from the start to the goal by exploring shallow moves. It always chooses the move option that is closest to the start position until it reaches its goal. This method will always find the shortest path but may have to explore many moves if the goal is far from the starting position.

### For informed search situation there is Greedy Best First Search and A* Search in this repository
#### Greedy Best First Search uses the technique of always exploring moves that are closer to the goal. Provided there is a solution and the maze is finite, then this search method will always find a solution but it may not always be the best solution to the search problem
#### A* Search also uses the technique of always exploring moves that are closer to the goal while considering the number of moves it took to get to the current state. This algorithm will rather explore a move that took shorter time to reach although that move may not be the closest move to the goal. In this search method, if there is a solution and a finite maze then the optimal solution will be found by the algorithm
