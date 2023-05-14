import random

from SB_CommonTypes import Point
from SB_CommonTypes import Direction
from SB_Ships import Ship
from SB_Ships import LinearShip
from SB_Ships import NavyData
from SB_Settings import GameSettings

class ShipError(Exception):
    pass


class ShipPlaceError(ShipError):
    pass

class ShipPlacer:
    def place_ship(self, navy_data: NavyData, ship: Ship, ship_index: int) -> None:
        raise Exception("ShipPlacer.place_ship: Abstract error!")

    def calc_place(self, settings: GameSettings) -> NavyData:
        navy_data = NavyData(settings)
        abs_ship_index = 0

        for curr_ship_index in range(settings.ship_3_count):
            self.place_ship(navy_data, LinearShip(Point(0, 0), Direction.HORIZONTAL, 3), abs_ship_index)
            abs_ship_index += 1

        for curr_ship_index in range(settings.ship_2_count):
            self.place_ship(navy_data, LinearShip(Point(0, 0), Direction.HORIZONTAL, 2), abs_ship_index)
            abs_ship_index += 1

        for curr_ship_index in range(settings.ship_1_count):
            self.place_ship(navy_data, LinearShip(Point(0, 0), Direction.HORIZONTAL, 1), abs_ship_index)
            abs_ship_index += 1

        return navy_data


class ShipPlacerRandom(ShipPlacer):
    def place_ship(self, navy_data: NavyData, ship: Ship, ship_index: int) -> None:
        abs_index = random.randint(0, navy_data.usage_field.available_count - 1)

        if isinstance(ship, LinearShip):
            dir_value = random.randint(0, 1)
            if dir_value == 0:
                # LinearShip(ship).direction = Direction.HORIZONTAL
                ship.direction = Direction.HORIZONTAL
            else:
                # LinearShip(ship).direction = Direction.VERTICAL
                ship.direction = Direction.VERTICAL

        navy_data.add_ship(ship, ship_index, abs_index)
