import random

from SB_CommonTypes import Point
from SB_CommonTypes import SizeBox
from SB_CommonTypes import Direction
from SB_Settings import GameSettings
from SB_Data import Field
from SB_Data import HitField


class Ship:
    def __init__(self, position: Point, loc_points):
        self.__position = position
        # self.__loc_points = loc_points
        self.set_loc_points(loc_points)
        self.__loc_size_box = None
        self.refresh_size_box()

    def set_loc_points(self, loc_points):
        self.__loc_points = loc_points

    def refresh_size_box(self):
        self.__loc_size_box = SizeBox.make_by_points(self.__loc_points)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    def get_loc_point(self, loc_point_index):
        return self.__loc_points[loc_point_index]

    @property
    def loc_point_count(self):
        return len(self.__loc_points)

    @property
    def loc_size_box(self):
        return self.__loc_size_box

    @property
    def width(self):
        return self.__loc_size_box.width

    @property
    def height(self):
        return self.__loc_size_box.height

    def get_point(self, point_index):
        return self.__position + self.get_loc_point(point_index)

    @property
    def point_count(self):
        return len(self.__loc_points)

    def is_contain(self, point):
        for curr_point_index in range(self.point_count):
            if self.get_point(curr_point_index) == point:
                return True
        return False


class LinearShip(Ship):

    def __init__(self, position, direction, size):
        self.__direction = direction
        self.__size = size
        loc_points = self.calc_loc_points(direction, size)

        super().__init__(position, loc_points)

    def calc_loc_points(self, direction, size):
        loc_points = []
        if direction == Direction.HORIZONTAL:
            loc_points = [Point(dx, 0) for dx in range(0, size)]
        elif direction == Direction.VERTICAL:
            loc_points = [Point(0, dy) for dy in range(0, size)]
        else:
            ValueError("LinearShip.calc_loc_points: direction")
        return loc_points

    def __str__(self):
        if self.direction == Direction.HORIZONTAL:
            direction_str = 'HORIZONTAL'
        else:
            direction_str = 'VERTICAL'
        points_str = ""
        for curr_point_index in range(self.point_count):
            curr_point = self.get_point(curr_point_index)
            points_str = points_str + f"({curr_point.x}; {curr_point.y})"
            if not curr_point_index == self.point_count - 1:
                points_str += ', '

        res = f"pos: ({self.position.x}; {self.position.y}), direction = {direction_str}, size = {self.size}, points = [{points_str}]"
        return res

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value
        # self.__loc_points = self.calc_loc_points(self.__direction, self.__size)
        self.set_loc_points(self.calc_loc_points(self.__direction, self.__size))
        self.refresh_size_box()

    @property
    def size(self):
        return self.__size


class NavyData:
    def __init__(self, settings: GameSettings):
        self.__ships = []
        self.__size_x = settings.size_x
        self.__size_y = settings.size_y
        self.__usage_field = Field(self.__size_x, self.__size_y)
        self.__hit_field = HitField(self.__size_x, self.__size_y)
        # self.__usage_matrix = [[0 for curr_x in range(settings.size_x)] for curr_y in range(settings.size_y)]
        # self.__empty_cell_count = settings.size_x * settings.size_y

    def get_ship(self, ship_index):
        return self.__ships[ship_index]

    @property
    def ship_count(self):
        return len(self.__ships)

    @property
    def usage_field(self) -> Field:
        return self.__usage_field

    @property
    def hit_field(self) -> HitField:
        return self.__hit_field

    def get_living_cell_count(self):
        count = 0
        for curr_ship in self.__ships:
            for curr_point_index in range(curr_ship.point_count):
                curr_point = curr_ship.get_point(curr_point_index)
                if not self.__hit_field.get_field_value(curr_point.x, curr_point.y):
                    count += 1

        return count

    def is_all_ships_destroyed(self):
        return not self.get_living_cell_count()

    def is_empty_cell(self, point: Point, is_border=False) -> bool:
        if 0 <= point.x < self.__size_x and 0 <= point.y < self.__size_y:
            value = self.__usage_field.get_field_value(point.x, point.y)
            if is_border:
                return value <= 0
            else:
                return not value
        else:
            return is_border

    def is_ship_can_be_placed(self, ship: Ship, pos: Point) -> bool:
        for curr_loc_point_index in range(ship.loc_point_count):
            curr_loc_point = ship.get_loc_point(curr_loc_point_index)
            curr_point = pos + curr_loc_point
            if not (self.is_empty_cell(curr_point) and
                self.is_empty_cell(Point(curr_point.x - 1, curr_point.y), True) and
                self.is_empty_cell(Point(curr_point.x + 1, curr_point.y), True) and
                self.is_empty_cell(Point(curr_point.x, curr_point.y - 1), True) and
                self.is_empty_cell(Point(curr_point.x, curr_point.y + 1), True)):
                return False

        return True

    # def abs_index_to_point(self, abs_index):
    #     curr_abs_index = 0
    #     for curr_si

    def mark_cell_as_void(self, point):
        if self.__usage_field.is_point_in_field(point):
            if not self.__usage_field.get_field_value(point.x, point.y):
                self.__usage_field.set_field_value(point.x, point.y, -1)
        # if not self.__usage_field[point.y][point.x]:
            # self.__usage_field[point.y][point.x] = -1
            # self.__empty_cell_count -= 1

    def add_ship(self, ship, ship_index, abs_index, stop_index=None):
        # if abs_index == stop_index:
        #     raise Exception("NavyData.add_ship: Cannot place ship!!!")

        stop_index = abs_index
        curr_abs_index = abs_index
        while True:
            # if abs_index >= self.__usage_field.available_count:
            #     abs_index = 0

            pos = self.__usage_field.get_point_by_abs_index(curr_abs_index)
            if self.is_ship_can_be_placed(ship, pos):
                ship.position = pos
                self.__ships.append(ship)
                for curr_point_index in range(ship.point_count):
                    curr_point = ship.get_point(curr_point_index)
                    self.__usage_field.set_field_value(curr_point.x, curr_point.y, 1 + ship_index)

                for curr_point_index in range(ship.point_count):
                    curr_point = ship.get_point(curr_point_index)
                    self.mark_cell_as_void(Point(curr_point.x - 1, curr_point.y))
                    self.mark_cell_as_void(Point(curr_point.x + 1, curr_point.y))
                    self.mark_cell_as_void(Point(curr_point.x, curr_point.y - 1))
                    self.mark_cell_as_void(Point(curr_point.x, curr_point.y + 1))

                break
            else:
                curr_abs_index += 1
                if curr_abs_index >= self.__usage_field.available_count:
                    curr_abs_index = 0
                elif curr_abs_index == stop_index:
                    raise Exception("NavyData.add_ship: Cannot place ship!!!")

                # if stop_index is None:
                #     self.add_ship(ship, ship, abs_index + 1, abs_index)
                # else:
                #     self.add_ship(ship, ship, abs_index + 1, stop_index)

