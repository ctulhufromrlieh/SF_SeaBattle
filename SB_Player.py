from SB_CommonTypes import Point
from SB_IOController import IOController
from SB_Data import Field
from SB_Settings import GameSettings

import random
import time


class Player:
    def __init__(self, io_controller: IOController, name: str) -> None:
        self.__io_controller = io_controller
        self.__name = name

    def calc_coords(self, enemy_field: Field) -> Point:
        raise Exception("Player.calc_coords: Abstract error!")

    @property
    def io_controller(self):
        return self.__io_controller

    @property
    def name(self):
        return self.__name

    # def get_name(self):
    #     return ""


class PlayerHuman(Player):
    def __init__(self, io_controller: IOController):
        super().__init__(io_controller, "Player")
        # self.__io_controller = io_controller

    def calc_coords(self, enemy_field: Field) -> Point:
        return self.io_controller.ask_coords(f"Enter coordinates (format <X Y>), {self.name}: ", enemy_field)

    # def get_name(self):
    #     return "Player"


class PlayerComputer(Player):
    pass
    # def get_name(self):
    #     return "Computer"


class PlayerComputerRandom(PlayerComputer):
    def calc_coords(self, enemy_field: Field) -> Point:
        # time.sleep(1)
        # time.sleep(0.4)

        abs_index = random.randint(0, enemy_field.available_count - 1)
        point = enemy_field.get_point_by_abs_index(abs_index)
        self.io_controller.show_message(f"Turn of {self.name}: {str(point + Point(1, 1))}")

        return point