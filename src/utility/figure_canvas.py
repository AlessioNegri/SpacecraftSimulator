""" figure_canvas.py: Generic figure canvas for QML """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtGui as qtGui
import PySide6.QtQuick as qtQuick
import numpy as np
import mpl_toolkits.mplot3d.proj3d as proj3d
import mpl_toolkits.mplot3d.axes3d as axes3d
import mplcyberpunk

from matplotlib import dates

from lib.matplotlib_backend_qtquick.backend_qtquick import NavigationToolbar2QtQuick
from lib.matplotlib_backend_qtquick.backend_qtquickagg import FigureCanvasQtQuickAgg

class FigureCanvas(qtCore.QObject):
    """Base class for managing Matplotlib figures in QML"""
    
    # --- CLASS MEMBERS 
    
    default_color = '#93F9D8'   # * Default line plot color
    
    # --- PROPERTIES 
    
    # ? Width
    
    width_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=width_changed)
    def width(self): return self._width

    @width.setter
    def width(self, val : int): self._width = val; self.width_changed.emit()
    
    # ? Height
    
    height_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=height_changed)
    def height(self): return self._height

    @height.setter
    def height(self, val : int): self._height = val; self.height_changed.emit()
    
    # ? Coordinates
    
    coord_changed = qtCore.Signal()
    
    @qtCore.Property(str, notify=coord_changed)
    def coord(self): return self._coord

    @coord.setter
    def coord(self, val : str): self._coord = val; self.coord_changed.emit()
    
    # ? Show Coordinates
    
    show_coord_changed = qtCore.Signal()
    
    @qtCore.Property(bool, notify=show_coord_changed)
    def showCoord(self): return self._show_coord

    @showCoord.setter
    def showCoord(self, val : bool): self._show_coord = val; self.show_coord_changed.emit()

    # --- METHODS 

    def __init__(self, parent : qtCore.QObject = None, dof3 : bool = False, rows : int = 1, cols : int = 1, x_date : bool = False, y_date : bool = False) -> None:
        """Constructor

        Args:
            parent (qtCore.QObject, optional): Parent object. Defaults to None.
            dof3 (bool, optional): True for 3D figures. Defaults to False.
            rows (int, optional): Subplots configuration along row. Defaults to 1.
            cols (int, optional): Subplots configuration along column. Defaults to 1.
            x_date (bool, optional): True for x-axis in date format. Defaults to False.
            y_date (bool, optional): True for y-axis in date format. Defaults to False.
        """
        
        super().__init__(parent)
        
        if rows < 1 or cols < 1: Exception('Figure rows / cols must be greater than 0!')
        
        self.canvas     = None
        self.figure     = None
        self.axes       = None
        self.toolbar    = None
        self.figsize    = (6.0, 4.0)
        self.dof3       = dof3
        self.rows       = rows
        self.cols       = cols
        self.multiplot  = rows != 1 or cols != 1
        self.x_date     = x_date
        self.y_date     = y_date
        
        self.width      = 0
        self.height     = 0
        self.coord      = '(0.00, 0.00)' if not dof3 else ''
        self.showCoord  = True if not dof3 else False

    def update_with_canvas(self, canvas : FigureCanvasQtQuickAgg, qml_object_parent : qtQuick.QQuickItem) -> None:
        """Initializes the canvas for the figure

        Args:
            canvas (FigureCanvasQtQuickAgg): Backend figure canvas
            qml_object_parent (qtQuick.QQuickItem): QML object parent
        """
        
        # ? Set Properties
        
        self.canvas     = canvas
        self.figure     = canvas.figure
        self.toolbar    = NavigationToolbar2QtQuick(canvas=canvas)
        self.figsize    = (qml_object_parent.width() // 100, qml_object_parent.height() // 100) # * width and height in inches
        self.width      = self.figure.get_figwidth() * 100
        self.height     = self.figure.get_figheight() * 100
        
        # ? Set Axes
        
        if self.multiplot:
            
            self.axes = self.figure.subplots(nrows=self.rows, ncols=self.cols)
            
            for r in range(0, self.rows):
                
                for c in range(0, self.cols):
                    
                    self.axes[r][c].grid(True)
                    self.axes[r][c].set_facecolor('#162A35')
            
        else:
            
            self.axes = self.figure.add_subplot(111) if not self.dof3 else self.figure.add_subplot(111, projection='3d')
            
            self.axes.grid(True)
            self.axes.set_facecolor('#162A35')
        
        # ? Set Figure
        
        if self.dof3:
            
            #self.figure.subplots_adjust(left=-0.11, top=0.99)
            self.figure.set_layout_engine('compressed')
            #self.axes.set_aspect('equal', adjustable='box')
            
        else:
            
            #self.figure.subplots_adjust(wspace=0.4, hspace=0.4)
            self.figure.set_layout_engine('tight')
            
        self.figure.set_figwidth(self.figsize[0])
        self.figure.set_figheight(self.figsize[1])
        self.figure.set_facecolor('#162A35')
        self.figure.patch.set_facecolor('#162A35')
        
        # ? Set Canvas
        
        self.canvas.draw_idle()
        
        self.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
    
    def reset_canvas(self) -> None:
        """Resets the figure canvas
        """
        
        if self.multiplot:
            
            for r in range(0, self.rows):
                
                for c in range(0, self.cols):
                    
                    self.axes[r][c].cla()
            
        else:
            
            self.axes.cla()
    
    def redraw_canvas(self, glow_effect : bool = True) -> None:
        """Redraws the figure canvas

        Args:
            glow_effect (bool, optional): Enables the glow effect. Defaults to True.
        """
        
        self.canvas.draw_idle()
        
        if glow_effect and not self.dof3:
            
            mplcyberpunk.add_gradient_fill(self.axes, alpha_gradientglow=0.5)
    
    def format_canvas(self,
                      x_label : str,
                      y_label : str,
                      y_label_pad : int,
                      text : str = "") -> None:
        """Formats the canvas

        Args:
            x_label (str): X label text
            y_label (str): Y label text
            y_label_pad (int): Y label padding
            text (str, optional): Box text content. Defaults to "".
        """
        
        if not self.multiplot:
            
            self.axes.set_xlabel(x_label, fontdict={ 'size': 10 }, loc='right')
            self.axes.set_ylabel(y_label, fontdict={ 'size': 10 }, labelpad=y_label_pad, loc='top', rotation=0)
            
            if text != "":
            
                self.axes.text(x=0.5, y=1.0, s=text, size=12, rotation=0, ha='center', va='center',
                               transform = self.axes.transAxes, bbox=dict(boxstyle='round', ec='#93F9D8', fc='#162A35'))
    
    # --- SLOTS 
    
    @qtCore.Slot(float, float)
    def resize_figure(self, width : float, height : float) -> None:
        """Resizes the figure

        Args:
            width (float): Width in pixels
            height (float): Height in pixels
        """
        
        if self.figure == None: return
        
        self.figsize = (width // 100, height // 100)
        
        if self.figsize[0] > 0: self.figure.set_figwidth(self.figsize[0])
        if self.figsize[1] > 0: self.figure.set_figheight(self.figsize[1])
        
        self.width  = self.figure.get_figwidth() * 100
        self.height = self.figure.get_figheight() * 100
        
        self.canvas.draw_idle()
 
    @qtCore.Slot()
    def on_motion(self, event : qtGui.QMouseEvent):
        """Update the coordinates on the display

        Args:
            event (qtCore.QEvent): Event
        """
        
        if self.multiplot:
            
            for r in range(0, self.rows):
                
                for c in range(0, self.cols):
                    
                    if event.inaxes == self.axes[r][c]:
            
                        self.coord = f'({event.xdata:.2f}, {event.ydata:.2f})'
            
        else:
            
            if event.inaxes == self.axes:
                
                if not self.dof3:
                    
                    if self.x_date and self.y_date:
                        
                        x_date_val = dates.num2date(event.xdata).strftime("%Y-%m-%d %H:%M:%S")
                        y_date_val = dates.num2date(event.ydata).strftime("%Y-%m-%d %H:%M:%S")
                        
                        self.coord = f'({x_date_val}, {y_date_val})'
                    
                    elif self.x_date and not self.y_date:
                        
                        x_date_val = dates.num2date(event.xdata).strftime("%Y-%m-%d %H:%M:%S")
                        
                        self.coord = f'({x_date_val}, {event.ydata:.2f})'
                        
                    elif not self.x_date and self.y_date:
                        
                        y_date_val = dates.num2date(event.ydata).strftime("%Y-%m-%d %H:%M:%S")
                        
                        self.coord = f'({event.xdata:.2f}, {y_date_val})'
                        
                    else:
                    
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