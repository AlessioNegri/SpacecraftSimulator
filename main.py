import sys

"""
module_name,
package_name,
ClassName,
method_name,
ExceptionName,
function_name,
GLOBAL_CONSTANT_NAME,
global_var_name,
instance_var_name,
function_parameter_name,
local_var_name.
"""

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

from qbstyles import mpl_style

mpl_style(dark=True)

import mplcyberpunk

import matplotlib.pyplot as plt

#plt.style.use("cyberpunk")

#import seaborn as sbn

#sbn.set_style("darkgrid")
#plt.style.use("dark_background")

# ! Sources

from src.mission_parameters import MissionParameters
from src.qml_log import QmlLog

# ! Material

qtQC2.QQuickStyle.setStyle('Material')

# ! APP

app = qtWidgets.QApplication(sys.argv)
#app = qtGui.QGuiApplication(sys.argv)

app.setWindowIcon(qtGui.QIcon(':/img/icon.ico'))
app.setFont('Calibri')

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

missionParameters.set_update_with_canvas(engine)

# ! EXEC

sys.exit(app.exec())