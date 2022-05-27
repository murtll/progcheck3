from random import randint
from math import sqrt
from abc import ABC, abstractmethod, abstractproperty
from myutils import log, UnknownSpeedException, UnknownDistanceException, UnknownReloadException

class Field:
    """Class of field where characters exist"""

    def __init__(self, width, height):
        self.characters = []
        self.width = width
        self.height = height

    def add_character(self, character):
        """Adds given character to field"""

        self.characters.append(character)

    def remove_character(self, character):
        """Removes given character from field"""

        self.characters.remove(character)

class Character(ABC):
    """Abstract class of basic character"""

    @abstractmethod
    def print_position():
        """Prints current character position"""
        pass

    @abstractmethod
    def update():
        """Updates character"""
        pass

    @abstractmethod
    def take_damage(self, damage):
        """Makes character take damage"""
        pass

class Movable(ABC):
    """Abstract class of movable character"""

    @abstractproperty
    def speed():
        """Returns movable speed"""
        pass

    @abstractmethod
    def move(self, x, y):
        """Moves the character to current position plus speed * vector of moving (x, y)"""
        pass


class Fighter(Character, Movable):
    """Basic class of fighter character"""

    def __init__(self, name, speed, health, strength, attack_strength, attack_distance, reload, field, color):
        self.name = name
        self.capacity = 3
        self.field = field
        self.color = color

        field.add_character(self)

        if speed == 'slow':
            self._speed = 100
        elif speed == 'normal':
            self._speed = 150
        elif speed == 'fast':
            self._speed = 200
        else:
            raise UnknownSpeedException()

        if attack_distance == 'low':
            self.attack_distance = 100
        elif attack_distance == 'normal':
            self.attack_distance = 150
        elif attack_distance == 'long':
            self.attack_distance = 200
        else:
            raise UnknownDistanceException()

        if reload == 'slow':
            self.reload = 50
        elif reload == 'normal':
            self.reload = 500
        elif reload == 'fast':
            self.reload = 1000
        else:
            raise UnknownReloadException

        self.health = health * strength
        self.strength = strength
        self.attack_strength = attack_strength * strength
        self.x = randint(0, field.width)
        self.y = randint(0, field.height)

    @property
    def speed(self):
        return self._speed

    def move(self, x, y):
        if self.x + x * self.speed <= self.field.width:
            if self.x + x * self.speed < 0:
                self.x = 0
            else:
                self.x += x * self.speed
        else:
            self.x = self.field.width

        if self.y + y * self.speed <= self.field.height:
            if self.y + y * self.speed < 0:
                self.y = 0
            else:
                self.y += y * self.speed
        else:
            self.y = self.field.height
        self.print_position()

    @log(message='{0} takes {1} damage, {2} HP left')
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.field.remove_character(self)
            self.field = None
            print(self.name, 'dies((9')

    def attack(self):
        """Makes fighter attack closest character if he is closer than attack distance"""
        if self.capacity < 1:
            return
        min_char = None
        _min = float('inf')
        for ch in self.field.characters:
            if ch == self:
                continue
            dist = sqrt((self.x - ch.x) ** 2 + (self.y - ch.y) ** 2)

            if _min > dist and self.attack_distance >= dist:
                _min = dist
                min_char = ch

        if min_char:
            self.capacity -= 1
            print(self.name, 'attacking', min_char.name, 'with', self.attack_strength, 'points')
            min_char.take_damage(self.attack_strength)
        else:
            print(self.name, 'cant perform attack - nobody is in attack radius')

        return min_char

    def update(self):
        if self.capacity == 3:
            return
        elif self.capacity > 3:
            self.capacity = 3
            return
        self.capacity += self.reload / 1000

    def print_position(self):
        print(self.name, 'on position x:', self.x, 'y: ', self.y)


    def __plus__(self, other):
        return Character(self.name, self.speed, self.health + other.health, self.strength + other.strength, self.attack_strength, self.attack_distance, self.reload, self._field)

    def __minus__(self, other):
        return Character(self.name, self.speed, self.health - other.health, self.strength - other.strength, self.attack_strength, self.attack_distance, self.reload, self._field)

"""name, speed, health, strength, attack_strength, attack_distance, reload, field, color"""

class Shelly(Fighter):
    def __init__(self, strength, _field):
        super().__init__('Shelly', 'normal', 3800, strength, 300, 'normal', 'normal', _field, '#d84c84')


class Piper(Fighter):
    def __init__(self, strength, _field):
        super().__init__('Piper', 'normal', 2400, strength, 1520, 'long', 'slow', _field, '#c034bc')


class Bull(Fighter):
    def __init__(self, strength, _field):
        super().__init__('Bull', 'fast', 5000, strength, 400, 'low', 'fast', _field, '#2864cc')
