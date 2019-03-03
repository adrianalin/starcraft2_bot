import sys
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
import MainWindow

if __name__ == '__main__':

    app = MainWindow.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()

    print('----------------run game loop')
    run_game(maps.get('AbyssalReefLE'), [
        Bot(Race.Protoss, window.getbot),
        Computer(Race.Zerg, Difficulty.CheatVision)
    ], realtime=False)

    sys.exit()

    print('--------------run qt loop')
    sys.exit(app.exec_())
