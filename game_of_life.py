import random
from threading import Lock
import copy

class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class GameOfLife(metaclass=SingletonMeta):
    def __init__(self, width=20, height=20):
        self.__width = width
        self.__height = height
        self.__generation = 0
        self.world = self.generate_universe()
        self.__old_world = self.world

    @property
    def generation(self):
        return self.__generation
    @generation.setter
    def generation(self, amount):
        self.__generation = amount

    @property
    def old_world(self):
        if self.generation > 1:
            return copy.deepcopy(self.__old_world)
        else:
            return [[0 for j in range(self.width)] for i in range(self.width)]
        

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def form_new_generation(self):
        universe = self.world
        new_world = [[0 for _ in range(self.__width)] for _ in range(self.__height)]
        self.__old_world = copy.deepcopy(universe)

        for i in range(len(universe)):
            for j in range(len(universe[0])):

                if universe[i][j]:
                    if self.__get_near(universe, [i, j]) not in (2, 3):
                        new_world[i][j] = 0
                        continue
                    new_world[i][j] = 1
                    continue

                if self.__get_near(universe, [i, j]) == 3:
                    new_world[i][j] = 1
                    continue
                new_world[i][j] = 0

        self.generation += 1
        self.world = new_world

    def generate_universe(self):
        self.generation = 0
        return [[random.randint(0, 1) for _ in range(self.__width)] for _ in range(self.__height)]

    @staticmethod
    def __get_near(universe, pos, system=None):
        if system is None:
            system = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

        count = 0
        for i in system:
            if universe[(pos[0] + i[0]) % len(universe)][(pos[1] + i[1]) % len(universe[0])]:
                count += 1
        return count

if __name__ == "__main__":
    class Game(metaclass=SingletonMeta):
        def __init__(self, text='test'):
            self.text = text
    
    g1 = Game()
    g2 = Game()
    print(id(g1) == id(g2))

    g1 = GameOfLife()
    g2 = GameOfLife()
    print(id(g1) == id(g2))

    