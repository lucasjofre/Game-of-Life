# Game of Life - Pygame
Visualization of Conway's Game of Life, using pygame

## Table of contents
* [General info](#general-info)
* [Packages and implementation](#packages-and-implementation)
* [Setup and usage](#setup-and-usage)

## General info
This repository implements Conway's Game of Life cellular automaton using pygame.
The automaton consists of a grid containing square cells, where each one has two possible states: live or dead. What determines the next state of the cell is a set of rules that are a function of the neighbouring cells, as follows:
1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

With the combination of the mentioned rules, different patterns can emerge, illustrated by the video bellow.

https://user-images.githubusercontent.com/30839327/191647960-2fb16397-8a39-4e6d-b9c6-169fd6dc985f.mp4

## Packages and implementation



## Setup and usage












