from SB_CommonTypes import Point


class Field:
    def __init__(self, size_x, size_y):
        self.__size_x = size_x
        self.__size_y = size_y
        self.__available_count = self.__size_x * self.__size_y
        self.__field = [[0 for curr_x in range(self.size_x)] for curr_y in range(self.size_y)]

    @property
    def size_x(self):
        return self.__size_x

    @property
    def size_y(self):
        return self.__size_y

    @property
    def available_count(self):
        return self.__available_count

    def is_point_in_field_by_coords(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def is_point_in_field(self, point):
        return self.is_point_in_field_by_coords(point.x, point.y)

    def is_point_used_by_coords(self, x, y):
        if not self.is_point_in_field_by_coords(x, y):
            raise ValueError("Field.is_point_used_by_coords: (x, y) is out of field")

        return self.__field[y][x]

    def is_point_used(self, point):
        return self.is_point_used_by_coords(point.x, point.y)

    def get_point_by_abs_index(self, abs_index):
        if abs_index < 0 or abs_index >= self.__available_count:
            raise ValueError("Field.get_point_by_abs_index: abs_index is out of range")

        curr_abs_index = 0
        for curr_y in range(self.size_y):
            for curr_x in range(self.size_x):
                if not self.is_point_used_by_coords(curr_x, curr_y):
                    if curr_abs_index == abs_index:
                        return Point(curr_x, curr_y)
                    else:
                        curr_abs_index += 1

    def get_field_value(self, x, y) -> int:
        return self.__field[y][x]

    # @field_values.setter
    def set_field_value(self, x, y, value: int):
        if self.is_point_used_by_coords(x, y):
            raise ValueError("Field.field_values*setter: point is already used")

        is_not_empty = self.__field[y][x]
        self.__field[y][x] = value
        if is_not_empty and not value:
            self.__available_count += 1
        elif not is_not_empty and value:
            self.__available_count -= 1


class HitField(Field):
    def hit_by_point(self, point: Point):
        self.set_field_value(point.x, point.y, 1)

    def hit_by_abs_index(self, abs_index):
        point = self.get_point_by_abs_index(abs_index)
        self.hit_by_point(point)