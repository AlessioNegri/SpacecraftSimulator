""" main.py: Main of the application """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import sys

# ! PySide6

import PySide6.QtWidgets as qtWidgets
import PySide6.QtGui as qtGui
import PySide6.QtQml as qtQml
import PySide6.QtCore as qtCore
import PySide6.QtQuickControls2 as qtQC2

# ! Resources

import ui.qml_rc

# ! Matplotlib Integration

from lib.matplotlib_backend_qtquick.backend_qtquickagg import FigureCanvasQtQuickAgg

#from qbstyles import mpl_style

#mpl_style(dark=True)

import matplotlib.pyplot as plt

plt.style.use('dark_background')

# ! Sources

from src.mission_parameters import MissionParameters
from src.qml_log import QmlLog

# ! Material

qtQC2.QQuickStyle.setStyle('Material')

# ! APP

app = qtWidgets.QApplication(sys.argv)

app.setWindowIcon(qtGui.QIcon(':/img/icon.ico'))
app.setFont('Calibri')

# ! Engine

engine = qtQml.QQmlApplicationEngine()

qtQml.qmlRegisterType(FigureCanvasQtQuickAgg, "FigureCanvas", 1, 0, "FigureCanvas")

qmlLog = QmlLog()

missionParameters = MissionParameters(engine)

engine.rootContext().setContextProperty("console", qmlLog)

engine.quit.connect(app.quit)

engine.load(qtCore.QUrl('qrc:/main.qml'))

if not engine.rootObjects(): sys.exit(-1)

# ! EXEC

sys.exit(app.exec())