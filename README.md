# Game of Life - Pygame
Visualization of Conway's Game of Life, using pygame

## Table of contents
* [General info](#general-info)
* [Packages and implementation](#packages-and-implementation)
* [Setup and usage](#setup-and-usage)
* [Todo](#todo)

## General info
This repository implements Conway's Game of Life cellular automaton using pygame.
The automaton consists of a grid containing square cells, where each one has two possible states: live or dead. What determines the next state of the cell is a set of rules that is a function of the neighbouring cells, as follows:
1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

With the combination of the mentioned rules, different patterns can emerge, illustrated by the video bellow.

https://user-images.githubusercontent.com/30839327/191647960-2fb16397-8a39-4e6d-b9c6-169fd6dc985f.mp4

## Packages and implementation
* numba
* pygame
* numpy

The rendering part of this visualization was done using the pygame framework. To calculate the four rules of the automaton, the numba JIT compiler was used.
This compiler works by passing it as a decorator to the update_state function, which calculate all the four rules of the game to determine the next state of the cells. The first time it's called, the function is compiled, and all the subsequent calls run directly from the compiled code, which increases the performance significantly.


## Setup and usage
To setup and run this visualization, install the packages located in requirements.txt by running the following command:
```
pip install -r requirements.txt
```
For running a visualization, run the main.py file and pass a command-line argument relative to a initial pattern, as follows:
```
python main.py plus
```
The following initial patterns can be set to run the visualization:
* x
* plus
* random
* 5

In order to start or pause the automaton, press the **SPACE** key


## Todo
* Implement different initial patterns
* Create the option to change the pattern while inside the game
* Feature to draw the blocks with the mouse
* Create some kind of logic related to sound and the cells colors
* Develop different types of automatons
