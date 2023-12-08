from lib import *


# weights in kg
# volumes in m3
# damage in MPa (a 9mm gun is approx 235 MPa)
# a punch is approx 0.004, but we can call it 1


# objects
def spawn_club():
    b = BluntWeapon(name="club", w=5, v=1, damage=3, _range=1)
    return b

def spawn_rod():
    b = BluntWeapon("rod", 4, 1, 2)
    return b

def spawn_flashlight():
    b = BluntWeapon("flashlight", 3, 1, 1)
    return b

# beings
def spawn_citizen():
    h = Human(w=70, v=0.07, hp=10, defense=3, occupation='citizen')
    h.tags = ['UNPASSABLE']
    return h

def spawn_cop():
    c = Human(75, 0.07, 10, 6, 'cop')
    c.tags = ['UNPASSABLE']
    return c

# structures 
def spawn_concrete_wall():
    w = Wall(w=3600, v=1.5, hp=999, defense=60, name='concrete wall')
    w.tags = ['UNPASSABLE']
    return w

def spawn_wood_wall():
    w = Wall(750, 1.5, 208, 30, 'wood wall')
    w.tags = ['UNPASSABLE']
    return w


