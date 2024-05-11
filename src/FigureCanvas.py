import os
import sys
import PySide6.QtCore as qtCore
import PySide6.QtGui as qtGui
import PySide6.QtQuick as qtQuick
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(__file__))

from lib.matplotlib_backend_qtquick.backend_qtquick import NavigationToolbar2QtQuick
from lib.matplotlib_backend_qtquick.backend_qtquickagg import FigureCanvasQtQuickAgg

class FigureCanvas(qtCore.QObject):
    """Base class for managing Matplotlib figures in QML
    """
    
    # ! PROPERTIES
    
    coord_changed = qtCore.Signal()
    
    def get_coord(self): return self._coord
    
    def set_coord(self, coord): self._coord = coord; self.coord_changed.emit()
        
    coord = qtCore.Property(str, get_coord, set_coord, notify=coord_changed)

    # ! METHODS

    def __init__(self, parent : qtCore.QObject = None) -> None:
        """Constructor

        Args:
            parent (qtCore.QObject, optional): Parent object. Defaults to None.
        """
        
        super().__init__(parent)
        
        self._coord     = '(0.00, 0.00)'
        
        self.canvas     = None
        self.figure     = None
        self.axes       = None
        self.toolbar    = None
        self.dof3       = False
        self.figsize    = (6.0, 4.0)

    def updateWithCanvas(self, canvas : FigureCanvasQtQuickAgg, parent : qtQuick.QQuickItem, dof3 : bool = False, figsize : tuple = (6.0, 4.0)) -> None:
        """Initializes the canvas for the figure

        Args:
            canvas (FigureCanvasQtQuickAgg): Backend figure canvas
            parent (qtQuick.QQuickItem): Parent qml object
            dof3 (bool, optional): True for 3D figures. Defaults to False.
            figsize (tuple, optional): Width and hegight in inches of the figure. Defaults to (6.0, 4.0).
        """
        
        figsize=(parent.width() // 100, parent.height() // 100)
        
        self.canvas     = canvas
        self.figure     = canvas.figure
        self.axes       = self.figure.add_subplot(111) if not dof3 else self.figure.add_subplot(111, projection='3d')
        self.toolbar    = NavigationToolbar2QtQuick(canvas=canvas)
        self.dof3       = dof3
        self.figsize    = figsize
        
        self.axes.grid(True)
        
        self.figure.set_figwidth(figsize[0])
        self.figure.set_figheight(figsize[1])
        self.figure.subplots_adjust(top=1.00, bottom=0.15, left=0.10, right=0.95)
        
        #if dof3: self.figure.tight_layout()
        
        self.canvas.draw_idle()
        
        self.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
    
    def resetCanvas(self) -> None:
        """Resets the figure canvas
        """
        
        self.axes.cla()
    
    def redrawCanvas(self) -> None:
        """Redraws the figure canvas
        """
        
        self.canvas.draw_idle()
            
    # ! SLOTS
    
    @qtCore.Slot()
    def on_motion(self, event : qtGui.QMouseEvent):
        """Update the coordinates on the display

        Args:
            event (qtCore.QEvent): Event
        """
        
        if event.inaxes == self.axes:
            
            self.coord = f'({event.xdata:.2f}, {event.ydata:.2f})'
 
    @qtCore.Slot()
    def pan(self, *args):
        """Pan button clicked
        """
        
        self.toolbar.pan(*args)

    @qtCore.Slot()
    def zoom(self, *args):
        """Zoom button clicked
        """
        
        self.toolbar.zoom(*args)

    @qtCore.Slot()
    def home(self, *args):
        """Home button clicked"""
        
        self.toolbar.home(*args)

    @qtCore.Slot()
    def back(self, *args):
        """Back button clicked
        """
        
        self.toolbar.back(*args)

    @qtCore.Slot()
    def forward(self, *args):
        """Forward button clicked
        """
        
        self.toolbar.forward(*args)