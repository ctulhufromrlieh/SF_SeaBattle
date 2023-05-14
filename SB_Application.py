import collections

from SB_Settings import GameSettings


from SB_IOController import IOController
from SB_IOController import IOControllerConsole

from SB_GameLogic import GameLogicSeaBattle


class GameApplication:
    def __init__(self, settings: GameSettings) -> None:
        self.__settings = settings
        self.__io_controller = self.create_io_controller()
        self.__game_logic = self.create_game_logic()

    def create_game_logic(self):
        return GameLogicSeaBattle(self.__io_controller, self.__settings)

    @staticmethod
    def create_io_controller() -> IOController:
        return IOControllerConsole()

    def run(self):
        if not self.__game_logic.initialize():
            self.__io_controller.show_message("Game cannot initialize. Exiting...")
            exit(0)

        player_index = 0
        round_index = 0
        while True:
            self.__game_logic.make_turn(player_index, round_index)
            if self.__game_logic.is_end_of_game():
                break

            player_index, round_index = self.__game_logic.switch_player_and_round(player_index, round_index)
    