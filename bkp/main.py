from lib import *
import sys, tty, termios


class _GetchUnix:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class Cursor:
    def __init__(self, lim_x, lim_y, x=5, y=5):
        self.x = x
        self.y = y
        self.lim_x = lim_x
        self.lim_y = lim_y

    def move(self, dx=0, dy=0):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < self.lim_x:
            self.x = new_x
        if 0 <= new_y < self.lim_y:
            self.y = new_y


def clear_screen():
    for i in range(100):
        print()



getch = _GetchUnix()

if __name__ == "__main__":
    # Example usage
    grid = Grid(10, 10)
    npc1 = Human(10, 10, 10, 3, 'cop')  # creating a human
    npc2 = Human(10, 10, 10, 3, 'citizen')  # creating another human

    grid.place_entity(npc1, 5, 5)  # placing npc1 at position (5, 5) on the grid
    grid.place_entity(npc2, 4, 4)  # placing npc2 at position (4, 4) on the grid
    weapon = BluntWeapon("Club", 5, 1, 2)  # creating a weapon

    npc1.equip_weapon(weapon)  # npc1 equips the weapon
    npc1.attack(npc2)  # npc1 uses the weapon on npc2

    weapon2 = BluntWeapon("rod", 4, 1, 1)
    weapon3 = BluntWeapon("flashlight", 3, 1, 1)
    grid.place_entity(weapon2, 7, 4)
    grid.place_entity(weapon3, 7, 4)

    # npc2 attempts to pick up the weapon
    if npc2.inventory.add_item(weapon):
        print("Weapon added to npc2's inventory.")
    else:
        print("Weapon could not be added to npc2's inventory.")

    cursor = Cursor(10,10)
    while 1:
        clear_screen()
        print('-'*30)
        print(" inspection:\n")
        for i, o in enumerate(grid.tiles[cursor.x][cursor.y].entities):
            print(f" {chr(97+i)} - {o}")
        print('-'*30)
        grid.print_scenario(cursor)
        r = getch()
        if r == 'w':
            cursor.move(dy=-1)
        elif r == 's':
            cursor.move(dy=1)
        elif r == 'a':
            cursor.move(dx=-1)
        elif r == 'd':
            cursor.move(dx=1)
        elif r == 'q':
            exit()
