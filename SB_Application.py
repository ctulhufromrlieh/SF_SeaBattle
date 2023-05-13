from SB_Settings import PlayerType
from SB_Settings import GameSettings

from SB_Player import Player
from SB_Player import PlayerHuman
from SB_Player import PlayerComputerRandom

from SB_Ships import NavyData
from SB_Ships import ShipPlacer
from SB_Ships import ShipPlacerRandom

from SB_Data import Field
from SB_Data import HitField
from SB_CommonTypes import GameFinishType
from SB_CommonTypes import GameFinish

from SB_IOController import IOController
from SB_IOController import IOControllerConsole


class GameApplication:
    def __init__(self, settings: GameSettings) -> None:
        self.__settings = settings
        self.__players = []
        self.__navy_datas = []
        # self.__enemy_fields = []
        # self.__enemy_fields = []
        self.__io_controller = None

    @staticmethod
    def create_io_controller() -> IOController:
        return IOControllerConsole()

    @staticmethod
    def get_computer_name(settings: GameSettings, player_index: int) -> str:
        if settings.player_computer_count > 1:
            computer_player_index = -1
            if settings.player_human_index != -1 and settings.player_human_index < player_index:
                computer_player_index = player_index - 1
            elif settings.player_human_index == -1 or settings.player_human_index > player_index:
                computer_player_index = player_index
            else:
                raise Exception("GameApplication.get_computer_name: player_index")
            return f"Computer #{computer_player_index + 1}"
        else:
            return "Computer"

    def create_player_by_player_type(self, io_controller: IOController, player_index: int, player_type: PlayerType) -> Player:
        if player_type == PlayerType.PLAYER_TYPE_COMPUTER:
            return PlayerComputerRandom(io_controller, self.get_computer_name(self.__settings, player_index))
        elif player_type == PlayerType.PLAYER_TYPE_HUMAN:
            return PlayerHuman(io_controller)
        else:
            raise ValueError("GameApplication.create_player_by_player_type: player_type out of PlayerType enum")

    @staticmethod
    def create_ship_placer() -> ShipPlacer:
        return ShipPlacerRandom()

    def create_navy_data_by_player_index(self, ship_placer: ShipPlacer) -> NavyData:
        return ship_placer.calc_place(self.__settings)

    def initialize(self):
        # self.__enemy_fields = [HitField(self.__settings.size_x, self.__settings.size_y),
        #                        HitField(self.__settings.size_x, self.__settings.size_y)]

        ship_placer = self.create_ship_placer()
        self.__io_controller = self.create_io_controller()

        for curr_player_index in range(self.__settings.player_count):
            curr_player_type = self.__settings.get_player_type(curr_player_index)
            self.__players.append(self.create_player_by_player_type(self.__io_controller, curr_player_index, curr_player_type))
            self.__navy_datas.append(self.create_navy_data_by_player_index(ship_placer))

    # def is_game_finished(self):
    #     return self.calc_gf().type == GameFinishType.GAME_FINISH_TYPE_WIN

    def calc_gf(self) -> GameFinish:
        player_winner = -1
        player_looser = -1
        for curr_player_index in range(len(self.__navy_datas)):
            if self.__navy_datas[curr_player_index].is_all_ships_destroyed():
                player_looser = curr_player_index
                break

        if player_looser == -1:
            player_winner = -1
        elif player_looser == 0:
            player_winner = 1
        elif player_looser == 1:
            player_winner = 0
        else:
            # these conditions only for two players but may be in the future...
            raise Exception("GameApplication.calc_gf: player_looser value (may be playercount > 2)")

        if player_winner == -1:
            return GameFinish(GameFinishType.GAME_FINISH_TYPE_NONE, -1)
        else:
            return GameFinish(GameFinishType.GAME_FINISH_TYPE_WIN, player_winner)

    def get_enemy_index(self, player_index: int) -> HitField:
        if player_index == 0:
            return 1
        elif player_index == 1:
            return 0
        else:
            # these conditions only for two players but may be in the future...
            raise Exception("GameApplication.get_enemy_index: player_looser value (may be playercount > 2)")

    def get_enemy_field(self, player_index: int) -> HitField:
        if player_index == 0:
            return self.__navy_datas[1].hit_field
        elif player_index == 1:
            return self.__navy_datas[0].hit_field
        else:
            # these conditions only for two players but may be in the future...
            raise Exception("GameApplication.get_enemy_field: player_looser value (may be playercount > 2)")

    def run(self):
        self.initialize()

        self.__io_controller.show_message("=" * 20)
        self.__io_controller.show_message("Wellcome to Sea Battle game!")
        self.__io_controller.show_message("=" * 20)
        self.__io_controller.show_message("")

        player_names = [curr_player.name for curr_player in self.__players]
        self.__io_controller.show_message("Initial state:")
        self.__io_controller.show_fields(self.__navy_datas, player_names, -1, self.__settings.player_human_index)

        player_index = 0
        round_index = 0
        while True:
            self.__io_controller.show_message("=" * 20)
            self.__io_controller.show_message(f"  Round #{round_index + 1}.")
            self.__io_controller.show_message(f"  Turn of <{self.__players[player_index].name}>:")

            enemy_index = self.get_enemy_index(player_index)
            enemy_field: HitField = self.__navy_datas[enemy_index].hit_field

            self.__io_controller.show_message("Current state:")
            self.__io_controller.show_fields(self.__navy_datas, player_names,
                                             player_index, self.__settings.player_human_index)

            target_point = self.__players[player_index].calc_coords(enemy_field)
            enemy_field.hit_by_point(target_point)

            gf = self.calc_gf()
            if gf.type == GameFinishType.GAME_FINISH_TYPE_WIN:
                self.__io_controller.show_message("")
                self.__io_controller.show_message("Final state:")
                self.__io_controller.show_fields(self.__navy_datas, player_names, player_index,
                                                 self.__settings.player_human_index)

                self.__io_controller.show_message(f"{self.__players[gf.player_index].name} win!")
                break

            player_index += 1
            if player_index >= self.__settings.player_count:
                player_index = 0
                round_index += 1
    