from SB_Application import GameApplication
from SB_Settings import PlayerType
from SB_Settings import GameSettings


if __name__ == "__main__":
    # settings = GameSettings(6, 6, 2, [PlayerType.PLAYER_TYPE_HUMAN, PlayerType.PLAYER_TYPE_COMPUTER], 1, 2, 4)
    settings = GameSettings(6, 6, 2, [PlayerType.PLAYER_TYPE_COMPUTER, PlayerType.PLAYER_TYPE_HUMAN], 1, 2, 4)
    # settings = GameSettings(6, 6, 2, [PlayerType.PLAYER_TYPE_COMPUTER, PlayerType.PLAYER_TYPE_COMPUTER], 1, 2, 4)
    app = GameApplication(settings)
    app.run()
