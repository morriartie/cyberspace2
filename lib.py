# every [Physical Object] should have this
# TAGS: NO_PASS, NO_CLIMB, NO_POCKET

class Entity:
    def __init__(self, w, v, symbol, tags=[], stored_on=None, pocket_volume=0):
        self.symbol = symbol
        self.weight = w
        self.volume = v
        self.tags = tags
        self.x = None
        self.y = None
        if pocket_volume > v:
            print("pocket volume cannot be bigger than the object volume")
        self.inventory = Inventory(pocket_volume)
        self.stored_on = stored_on
        self.tile = None

    def update(self):
        self.x = self.tile.x
        self.y = self.tile.y

    def move(self, dx=0, dy=0):
       max_distance = 1
       prop_dist = abs(dx) + abs(dy)
       
       if prop_dist > max_distance:
            # cant go that far
            return False

       # pegar do tile o objeto do grid
       grid = self.tile.grid
       x = self.tile.x
       y = self.tile.y
       nx = dx + x
       ny = dy + y

       if nx < 0 or ny < 0:
            # target not in grid
            return False

       if nx >= len(grid.tiles) or ny >= len(grid.tiles[0]):
            # target not in grid
            return False

       if grid.tiles[nx][ny].entities:
            # target tile is not empty <-- change here later for multiple objects in same tile
            return False

       if 'UNMOVABLE' in self.tags:
            # object is unmovable
            return False
       
       unmov = [c for c in self.tags if 'UNMOVABLE_' in c]
       if unmov:
           count = int(unmov[0].split('_')[1])
           if count == 0:
               self.tags.remove(unmov[0])
           else:
               self.tags.remove(unmov[0])
               self.tags.append(f'UNMOVABLE_{count-1}')
           # object is unmovable for {count} turns
           return False

       # remover do grid o objeto atual na posicao atual
       grid.tiles[x][y].entities.remove(self) # check if it works
       # colocar o objeto atual na posicao antiga
       grid.tiles[nx][ny].place(self) # check if is the current object thats placed or its superior


# [Value] must be present on every entity capable of fight
class Inventory:
    def __init__(self, total_volume):
        self.total_volume = total_volume
        self.items = []

    def add_item(self, item):
        if 'NO_POCKET' in item.tags:
            return False
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
    def __init__(self, w, v, hp, defense, occupation):
        super().__init__(w, v, '@')
        self.name = 'unknown'
        self.occupation = occupation
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
        if self.name != 'unknown':
            return  f"{self.name} [human] (hp:{self.combat.hp})"
        return f"{self.occupation} [human] (hp:{self.combat.hp})"

class Wall(Entity):
    def __init__(self, w, v, hp, defense, name):
        super().__init__(w, v, '#')
        self.name = name
        self.combat = Combatant(hp, defense)
        

# Player
class Player(Human):
    def __init__(self, w, v, hp, defense, occupation, name='player1'):
        super().__init__(w, v, hp, defense, occupation)
        self.name = name

# [World]
class Tile:
    def __init__(self, y, x, blocked, grid, block_sight=None):
        self.blocked = blocked
        self.block_sight = block_sight if block_sight is not None else blocked
        self.entities = []
        self.grid = grid
        self.y, self.x = y, x

    def place(self, entity):
        if entity.tile and entity in entity.tile.entities:
            entity.tile.entities.remove(entity)
        self.entities.append(entity)
        entity.tile = self
        entity.update()

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile(x,y,False, self) for x in range(width)] for y in range(height)]

    def place_entity(self, entity, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[x][y].place(entity)
            self.tiles[x][y].grid = self



