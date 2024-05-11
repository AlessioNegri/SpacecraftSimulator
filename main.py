import sys

# ! PySide6

import PySide6.QtGui as qtGui
import PySide6.QtQml as qtQml
import PySide6.QtCore as qtCore
import PySide6.QtQuickControls2 as qtQC2

# ! Resources

import ui.qml_rc

# ! Matplotlib Integration

from lib.matplotlib_backend_qtquick.backend_qtquickagg import FigureCanvasQtQuickAgg

# ! Sources

from src.MissionParameters import MissionParameters
from src.QmlLog import QmlLog

# ! Material

qtQC2.QQuickStyle.setStyle('Material')

# ! APP

app = qtGui.QGuiApplication(sys.argv)

app.setWindowIcon(qtGui.QIcon(':/images/img/icon.ico'))

# ! Engine

engine = qtQml.QQmlApplicationEngine()

qtQml.qmlRegisterType(FigureCanvasQtQuickAgg, "FigureCanvas", 1, 0, "FigureCanvas")

qmlLog = QmlLog()

missionParameters = MissionParameters(engine)

engine.rootContext().setContextProperty("console", qmlLog)
engine.rootContext().setContextProperty("__MissionParameters", missionParameters)

engine.quit.connect(app.quit)

engine.load(qtCore.QUrl('qrc:/main.qml'))

if not engine.rootObjects(): sys.exit(-1)

# ! QML-Matplotlib Setup

missionParameters.setUpdateWithCanvas(engine)

# ! EXEC

sys.exit(app.exec())