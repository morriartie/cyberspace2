from lib import *


# weights in kg
# volumes in m3
# damage in MPa (a 9mm gun is approx 235 MPa)
# a punch is approx 0.004, but we can call it 1


# objects
def spawn_club():
    return BluntWeapon(name="club", w=5, v=1, damage=3, _range=1)

def spawn_rod():
    return BluntWeapon("rod", 4, 1, 2)

def spawn_flashlight():
    return BluntWeapon("flashlight", 3, 1, 1)

# beings
def spawn_citizen():
    return Human(w=70, v=0.07, hp=10, defense=3, occupation='citizen')

def spawn_cop():
    return Human(75, 0.07, 10, 6, 'cop')

# structures 
def spawn_concrete_wall():
    return Wall(w=3600, v=1.5, hp=999, defense=60, name='concrete wall')

def spawn_wood_wall():
    return Wall(750, 1.5, 208, 30, 'wood wall')


