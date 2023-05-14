from SB_Settings import GameSettings
from SB_ShipPlacer import ShipPlacerRandom
from SB_CommonTypes import PlayerType
from SB_IOController import IOControllerConsole

import math
import time

if __name__ == "__main__":
    settings = GameSettings(6, 6, 2, [PlayerType.PLAYER_TYPE_HUMAN, PlayerType.PLAYER_TYPE_COMPUTER], 1, 2, 4)

    placer = ShipPlacerRandom()
    io_controller = IOControllerConsole()

    navy_data = placer.calc_place(settings)

    print("Ship places:")
    io_controller.show_navy_data_usage_field(navy_data)

    print("Ships:")
    for curr_ship_index in range(navy_data.ship_count):
        print(f"Ship #{curr_ship_index}:")
        print(navy_data.get_ship(curr_ship_index))


    # app.run()