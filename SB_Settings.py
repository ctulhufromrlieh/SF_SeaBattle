from SB_CommonTypes import PlayerType

class GameSettings:
    def __init__(self, size_x=6, size_y=6, player_count=2, player_types=None,
                 ship_3_count=1, ship_2_count=2, ship_1_count=4) -> None:
        if player_types is not None:
            if not len(player_types) == player_count:
                raise ValueError("GameSettings.__init__: player_types")

        self.__size_x = size_x
        self.__size_y = size_y
        self.__player_count = player_count
        self.__player_types = []
        if player_types is None:
            self.__player_types = [PlayerType.PLAYER_TYPE_HUMAN, PlayerType.PLAYER_TYPE_COMPUTER]
        else:
            self.__player_types = player_types.copy()
        self.__ship_3_count = ship_3_count
        self.__ship_2_count = ship_2_count
        self.__ship_1_count = ship_1_count

    @property
    def size_x(self):
        return self.__size_x

    @property
    def size_y(self):
        return self.__size_y

    def get_player_type(self, player_index) -> PlayerType:
        return self.__player_types[player_index]

    @property
    def player_count(self):
        return self.__player_count

    @property
    def ship_3_count(self):
        return self.__ship_3_count

    @property
    def ship_2_count(self):
        return self.__ship_2_count

    @property
    def ship_1_count(self):
        return self.__ship_1_count

    @property
    def player_human_index(self):
        for curr_player_index, curr_player_type in enumerate(self.__player_types):
            if curr_player_type == PlayerType.PLAYER_TYPE_HUMAN:
                return curr_player_index

        return -1

    @property
    def player_computer_count(self):
        count = 0
        for curr_player_index, curr_player_type in enumerate(self.__player_types):
            if curr_player_type == PlayerType.PLAYER_TYPE_COMPUTER:
                count += 1

        return count

    @property
    def is_only_computers(self):
        return self.player_human_index == -1
