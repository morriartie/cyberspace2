# every [Physical Object] should have this
class Entity:
    def __init__(self, w, v, symbol, tags=[], stored_on=None, pocket_volume=1):
        self.symbol = symbol
        self.weight = w
        self.volume = v
        self.tags = tags
        if pocket_volume > v:
            print("pocket volume cannot be bigger than the object volume")
        self.inventory = Inventory(pocket_volume)
        self.stored_on = stored_on
        self.tile = None

# [Value] must be present on every entity capable of fight
class Inventory:
    def __init__(self, total_volume):
        self.total_volume = total_volume
        self.items = []

    def add_item(self, item):
        new_volume = sum([item.volume for item in self.items]) + item.volume
        if item.stored_on:
            print("item already stored by something else")
            return False
        if new_volume > self.total_volume:
            print("this storage can't hold this item")
            return False
        item.stored_on = self
        self.items.append(item)
        return True

    def remove_item(self, item):
        item.stored_on = None
        self.items.remove(item)


class Combatant:
    def __init__(self, hp, defense):
        self.hp = hp
        self.defense = defense

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.die()

    def die(self):
        print("This entity has died.")


# [Objects]
class BluntWeapon(Entity):
    def __init__(self, name, w, v, damage, _range=1):
        super().__init__(w, v, symbol='p')
        self.name = name
        self.damage = damage
        self.range = _range

    def __str__(self):
        return f"{self.name} [Blunt Weapon]"


class Human(Entity):
    def __init__(self, w, v, hp, defense, name):
        super().__init__(w, v, '@')
        self.name = name
        self.combat = Combatant(hp, defense)
        self.weapon = None

    def equip_weapon(self, weapon):
        self.weapon = weapon

    def attack(self, target):
        if self.weapon:
            damage = self.weapon.damage
        else:
            damage = 0  # Or some base damage
        target.combat.take_damage(damage)

    def __str__(self):
        return f"{self.name} [human] (hp:{self.combat.hp})"


# [World]
class Tile:
    def __init__(self, x, y, blocked, block_sight=None):
        self.blocked = blocked
        self.block_sight = block_sight if block_sight is not None else blocked
        self.entities = []
        self.x, self.y = x, y

    def place(self, entity):
        if entity.tile:
            entity.tile.entities.remove(entity)
        self.entities.append(entity)
        entity.tile = self

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile(x,y,False) for x in range(width)] for y in range(height)]

    def place_entity(self, entity, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[x][y].place(entity)

    def print_scenario(self, cursor=None):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[x][y]
                if tile.entities:
                    symbol = tile.entities[0].symbol
                    if len(tile.entities) > 1:
                        symbol = symbol.upper()
                else:
                    symbol = '.'
                if cursor and cursor.x == x and cursor.y == y:
                    print(hl_char(symbol), end=' ')
                else:
                    print(symbol, end=' ')
            print()  # New line after each row

def hl_char(char, background_color_code="43"):
    return f"\033[{background_color_code}m{char}\033[0m"

