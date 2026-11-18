# Pytago

Link to the GitLab : https://forgens.univ-ubs.fr/gitlab/e2400527/pytago 
Link to the Kanban : https://forgens.univ-ubs.fr/gitlab/e2400527/pytago/-/boards 

## Description

Pytago is a Python-based implementation of the [Pytago](https://en.wikipedia.org/wiki/Pentago) game. The graphical user interface is built with Kivy, while the AI and core game logic are implemented in C for maximum performance.

The board logic has been aggressively optimized, both technically and algorithmically. The game state is represented internally as a 36-bit bitboard, with a unique bit layout that enables ultra-efficient quadrant rotations.

## Installation

Pytago is Python-only for now. To use it, go to the src directory and run `pip install -e .` to compile and install the AI. Then run `python3 main.py` and enjoy!
For Android, run `buildozer android debug` in the root directory. The APK will be in bin/.

## Roadmap

If you have ideas for releases in the future, it is a good idea to list them in the README.

## To read the specifications technic

Open the index.html

## Project members

TyLion, ARM4da, Dragonite, HexIllusionist
