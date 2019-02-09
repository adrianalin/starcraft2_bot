import sys
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
import MainWindow

import sc2_bot

if __name__ == '__main__':
    bot = sc2_bot.BotTest()
    app = MainWindow.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()

    bot.pixmap_signal.connect(window.update_picture)
    window.exit_signal.connect(bot.stop_game)

    print('----------------run game loop')
    run_game(maps.get('AbyssalReefLE'), [
        Bot(Race.Protoss, bot),
        Computer(Race.Terran, Difficulty.Hard)
    ], realtime=False)

    sys.exit()

    print('--------------run qt loop')
    sys.exit(app.exec_())
