from enum import Enum


class Point:
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.__x}, {self.__y})"

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    def create_moved(self, dx, dy):
        return Point(self.x + dx, self.y + dy)


class SizeBox:
    def __init__(self, x_min, y_min, x_max, y_max) -> None:
        self.__x_min = x_min
        self.__y_min = y_min
        self.__x_max = x_max
        self.__y_max = y_max

    @staticmethod
    # def make_by_points(points) -> SizeBox:
    def make_by_points(points):
        if len(points) == 0:
            raise ValueError("SizeBox.make_by_points: len(points)")

        x_min = points[0].x
        x_max = points[0].x
        y_min = points[0].y
        y_max = points[0].y
        for curr_point_index, curr_point in enumerate(points, 1):
            if x_min > curr_point.x:
                x_min = curr_point.x
            if x_max > curr_point.x:
                x_max = curr_point.x
            if y_min > curr_point.y:
                y_min = curr_point.y
            if y_max > curr_point.y:
                y_max = curr_point.y

        return SizeBox(x_min, y_min, x_max, y_max)

    @property
    def width(self):
        return self.__x_max - self.__x_min

    @property
    def height(self):
        return self.__y_max - self.__y_min


class Direction(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class PlayerType(Enum):
    PLAYER_TYPE_HUMAN = 1
    PLAYER_TYPE_COMPUTER = 2


class GameFinishType(Enum):
    GAME_FINISH_TYPE_NONE = 0
    GAME_FINISH_TYPE_WIN = 1


class GameFinish:
    def __init__(self, gft: GameFinishType, player_index):
        self.__gft = gft
        self.__player_index = player_index

    @property
    def type(self):
        return self.__gft

    @property
    def player_index(self):
        return self.__player_index
