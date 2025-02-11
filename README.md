# Battle Map

This is a small offline game written in Python using Tkinter GUI library. 2 players are required to play with a keyboard. Each round, 2 players original loacation will be arranged in random position on the map. Control p1 with WASD and p2 with IJKL. Take more grid by the countdown to win this game. If p1 and p2 collide together, the game will over immediately.

## Requirements
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following packages :
* Pillow

```bash
pip install -r requirements.txt
```

## Run the game
Run grid_contender.py to start the game program.

```bash
python3 grid_contender.py
```

## Game View

- Main interface view:

  <p align='center'>
    <img width="500" alt="image" src="https://github.com/user-attachments/assets/dafd40e3-7a39-4843-8916-9fce3e45f3de" />
  </p>
- Map editor view:

  <p align='center'>
    <img width="500" alt="image" src="https://github.com/user-attachments/assets/7afa2851-89c8-4a2c-97ac-8fd955001180" />
  </p>
Map can be uploaded from a file, or use the pre-built map editor to design a map. Click the grid on the map to add or remove obstacles. Use your creativity to make interesting maps and play with your friends.

## TODO
- Make it online
- Add ranking system
