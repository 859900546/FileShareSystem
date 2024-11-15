import sys
from PyQt5.QtWidgets import QApplication
from Websocket_filesystem import websocket_client
from ui.main_ui import MainWindow


if __name__ == '__main__':
    # Start the websocket client
    websocket_client.start_ws()

    app = QApplication(sys.argv)

    # Create main window
    window = MainWindow()
    window.Heartbert.delay = 3
    window.init()
    window.show()

    sys.exit(app.exec_())
