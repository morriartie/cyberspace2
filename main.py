from lib import *
import curses
import assets
from time import sleep



class Renderer:
    def __init__(self, stdscr, player):
        self.stdscr = stdscr
        self.player = player  # Assuming player has x and y attributes
        self.bottom_text = []
        self.max_entities_bottom_box = 4
        self.bottom_box_index = 0

    def reset(self):
        self.bottom_box_index = 0
        
    def move_bottom_box_cursor(self, dx):
        max_entities = self.max_entities_bottom_box
        max_index = len(self.bottom_text) - 1 - max_entities 
        self.bottom_box_index += dx
        self.bottom_box_index = max(0, self.bottom_box_index)
        self.bottom_box_index = min(max_index, self.bottom_box_index) 

    def render_grid(self, grid, cursor=None, distance=9):
        tiles_to_render = []

        # Calculate the range of tiles within the specified distance
        for y in range(max(self.player.y - distance, 0), min(self.player.y + distance + 1, grid.height)):
            for x in range(max(self.player.x - distance, 0), min(self.player.x + distance + 1, grid.width)):
                d = abs(x - self.player.x) + abs(y - self.player.y) 
                if d <= distance:
                    tile = grid.tiles[x][y]
                    screen_x = (x - self.player.x + distance)  # Adjust for character width
                    screen_y = (y - self.player.y + distance)*2
                    tiles_to_render.append((tile, screen_x, screen_y, d))

        tiles_to_render = sorted(tiles_to_render, key=lambda x: x[3])
        for tile, screen_x, screen_y, _ in tiles_to_render:
            symbol = self.get_tile_symbol(tile)
            if cursor and self.is_cursor_on_tile(cursor, tile):
                self.hl_char(screen_x, screen_y, symbol)
            else:
                self.stdscr.addstr(screen_x, screen_y, symbol)
        self.stdscr.addstr('\n')
        self.draw_bottom_menu()

    def is_cursor_on_tile(self, cursor, tile):
        return cursor.x == tile.x and cursor.y == tile.y

    def draw_bottom_menu(self):
        start_index = self.bottom_box_index
        max_entities = self.max_entities_bottom_box
        entities = self.bottom_text#[start_index:]
        #open('debug.txt','w').write('\n'.join([str(v) for v in entities]))
        height, width = self.stdscr.getmaxyx()
        displayed_entities = entities[start_index:start_index + max_entities]
        if (start_index + max_entities) < (len(entities)-1):
            displayed_entities += ['+']
        if start_index > 0:
            displayed_entities = ['+'] + displayed_entities
        start_line = height - len(displayed_entities) - 2 # -2 because of the 2 bars at bottom and top

        # clear the space
        for i in range(start_line, height):
            self.stdscr.move(i, 0)
            self.stdscr.clrtoeol()

        # draw top border
        border_line = '+' + '-' * (width - 2) + '+'
        self.stdscr.addstr(start_line, 0, border_line[:width])

        # draw content
        for i, entity in enumerate(displayed_entities):
            entity_str = "| {:<{}} |".format(str(entity), width - 4)
            self.stdscr.addstr(start_line + i + 1, 0, entity_str[:width])

        # draw bootm border
        #self.stdscr.addstr(height - 3, 0, border_line[:width])
        self.stdscr.refresh()

    def hl_char(self, y, x, char):
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(y, x, char)  # Swap x and y here
        self.stdscr.attroff(curses.color_pair(1))

    def get_tile_symbol(self, tile):
        if tile.entities:
            symbol = tile.entities[0].symbol
            if len(tile.entities) > 1:
                symbol = symbol.upper()
        else:
            symbol = '.'
        return symbol



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

def main(stdscr):
    # Setup
    grid = Grid(10, 10)
    cursor = Cursor(10,10)

    player = Player(w=70, v=0.07, hp=10, defense=3, occupation='detective', name='moriartie')  # Initialize your player
    renderer = Renderer(stdscr, player)

    curses.curs_set(0)
    #stdscr.nodelay(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    # Objects Spawn
    npc1 = assets.spawn_cop()
    npc2 = assets.spawn_citizen()
    weapon1 = assets.spawn_club()
    weapon2 = assets.spawn_rod()
    weapon3 = assets.spawn_flashlight()
    weapon4 = assets.spawn_flashlight()
    weapon5 = assets.spawn_flashlight()
    weapon6 = assets.spawn_flashlight()

    # Objects Placement
    grid.place_entity(player, 6, 6)
    grid.place_entity(npc1, 5, 5)  # placing npc1 at position (5, 5) on the grid
    grid.place_entity(npc2, 4, 4)  # placing npc2 at position (4, 4) on the grid
    grid.place_entity(weapon2, 7, 4)
    grid.place_entity(weapon3, 7, 4)
    grid.place_entity(weapon4, 7, 4)
    grid.place_entity(weapon5, 7, 4)
    grid.place_entity(weapon6, 7, 4)

    # Pre-Run Actions
    npc1.equip_weapon(weapon1)  # npc1 equips the weapon
    npc1.attack(npc2)  # npc1 uses the weapon on npc2
    npc2.inventory.add_item(weapon1)

    # Game Loop
    while True:
        stdscr.clear()
        
        renderer.bottom_text = []
        renderer.bottom_text += [f"cursor: ({cursor.x},{cursor.y})",""]
        entities = grid.tiles[cursor.x][cursor.y].entities
        for i, o in enumerate(entities):
            renderer.bottom_text += [f"{chr(97+i)} - {o}"]
        renderer.render_grid(grid, cursor)

        # Render inspection info
        #inspection_info = '-'*30 + "\n inspection:\n"
        #for i, o in enumerate(grid.tiles[cursor.x][cursor.y].entities):
        #    inspection_info += f" {chr(97+i)} - {o}\n"
        #inspection_info += '-'*30 + "\n"
        #stdscr.addstr(inspection_info)        
        #renderer.draw_bottom_menu(grid.tiles[cursor.x][cursor.y].entities)

        try:
            r = stdscr.getch()
            if r == ord('w'):
                cursor.move(dx=-1)
                renderer.reset()
            elif r == ord('s'):
                cursor.move(dx=1)
                renderer.reset()
            elif r == ord('a'):
                cursor.move(dy=-1)
                renderer.reset()
            elif r == ord('d'):
                cursor.move(dy=1)
                renderer.reset()
            elif r == ord('q'):
                break
            elif r == ord('r'):
                renderer.move_bottom_box_cursor(dx=-1)
            elif r == ord('f'):
                renderer.move_bottom_box_cursor(dx=1)
        except curses.error:
            # No input
            pass

        stdscr.refresh()

curses.wrapper(main)

