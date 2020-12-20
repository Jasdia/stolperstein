from tkinter import *

frame = Tk()


def create_grid(field, players):
    for idx, row in enumerate(field):
        for idy, cell in enumerate(row):
            color = "white"
            if cell == 1:
                color = "orange"
            elif cell == 2:
                color = "green"
            elif cell == 3:
                color = "blue"
            elif cell == 4:
                color = "purple"
            elif cell == 5:
                color = "yellow"
            elif cell == 6:
                color = "grey"

            Label(width="1", height="1", bg=color, relief="solid").grid(row=idy, column=idx)

    for player in players.values():
        Label(width="1", height="1", bg="red", relief="solid").grid(row=player.x, column=player.y)

    frame.mainloop()
