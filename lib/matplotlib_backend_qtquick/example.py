import os
import sys

sys.path.append(os.path.dirname(__file__))

from pathlib import Path

import numpy as np

from backend_qtquick import NavigationToolbar2QtQuick
from backend_qtquickagg import FigureCanvasQtQuickAgg
from PySide6 import QtGui, QtQml, QtCore
#from lib.matplotlib_backend_qtquick.qt_compat import QtGui, QtQml, QtCore


class DisplayBridge(QtCore.QObject):
    """ A bridge class to interact with the plot in python
    """
    
    coordinatesChanged = QtCore.Signal(str)

    def __init__(self, parent=None) -> None:
        
        super().__init__(parent)

        # The figure and toolbar
        
        self.figure = None
        self.toolbar = None

        # this is used to display the coordinates of the mouse in the window
        
        self._coordinates = ""

    def updateWithCanvas(self, canvas) -> None:
        """ initialize with the canvas for the figure
        """
        
        self.figure = canvas.figure
        self.toolbar = NavigationToolbar2QtQuick(canvas=canvas)

        # make a small plot
        
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True)

        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(x)

        self.axes.plot(x, y)
        
        canvas.draw_idle()

        # connect for displaying the coordinates
        
        self.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
 
    # define the coordinates property
    # (I have had problems using the @QtCore.Property directy in the past)
    def getCoordinates(self):
        
        return self._coordinates
    
    def setCoordinates(self, coordinates):
        
        self._coordinates = coordinates
        
        self.coordinatesChanged.emit(self._coordinates)
    
    coordinates = QtCore.Property(str, getCoordinates, setCoordinates,
                                  notify=coordinatesChanged)

    # The toolbar commands
    @QtCore.Slot()
    def pan(self, *args):
        """Activate the pan tool."""
        self.toolbar.pan(*args)

    @QtCore.Slot()
    def zoom(self, *args):
        """activate zoom tool."""
        self.toolbar.zoom(*args)

    @QtCore.Slot()
    def home(self, *args):
        self.toolbar.home(*args)

    @QtCore.Slot()
    def back(self, *args):
        self.toolbar.back(*args)

    @QtCore.Slot()
    def forward(self, *args):
        self.toolbar.forward(*args)

    def on_motion(self, event):
        """
        Update the coordinates on the display
        """
        if event.inaxes == self.axes:
            self.coordinates = f"({event.xdata:.2f}, {event.ydata:.2f})"

if __name__ == "__main__":
    
    #QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtGui.QGuiApplication(sys.argv)
    engine = QtQml.QQmlApplicationEngine()

    # instantate the display bridge
    displayBridge = DisplayBridge()

    # Expose the Python object to QML
    context = engine.rootContext()
    context.setContextProperty("displayBridge", displayBridge)

    # matplotlib stuff
    QtQml.qmlRegisterType(FigureCanvasQtQuickAgg, "Backend", 1, 0, "FigureCanvas")

    # Load the QML file
    qmlFile = Path(Path.cwd(), Path(__file__).parent, "example.qml")
    engine.load(QtCore.QUrl.fromLocalFile(str(qmlFile)))

    win = engine.rootObjects()[0]
    displayBridge.updateWithCanvas(win.findChild(QtCore.QObject, "figure"))

    # execute and cleanup
    app.exec()