""" FigureCanvas.py: Generic figure canvas for QML """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtGui as qtGui
import PySide6.QtQuick as qtQuick
import numpy as np
import mpl_toolkits.mplot3d.proj3d as proj3d
import mpl_toolkits.mplot3d.axes3d as axes3d

from lib.matplotlib_backend_qtquick.backend_qtquick import NavigationToolbar2QtQuick
from lib.matplotlib_backend_qtquick.backend_qtquickagg import FigureCanvasQtQuickAgg

class FigureCanvas(qtCore.QObject):
    """Base class for managing Matplotlib figures in QML"""
    
    # --- PROPERTIES 
    
    # ? Coordinates
    
    coord_changed = qtCore.Signal()
    
    @qtCore.Property(str, notify=coord_changed)
    def coord(self): return self._coord

    @coord.setter
    def coord(self, val : str): self._coord = val; self.coord_changed.emit()

    # --- METHODS 

    def __init__(self, parent : qtCore.QObject = None, dof3 : bool = False, rows : int = 1, cols : int = 1, figure_in_dialog : bool = False) -> None:
        """Constructor

        Args:
            parent (qtCore.QObject, optional): Parent object. Defaults to None.
            dof3 (bool, optional): True for 3D figures. Defaults to False.
            rows (int, optional): Subplots configuration along row. Defaults to 1.
            cols (int, optional): Subplots configuration along column. Defaults to 1.
        """
        
        super().__init__(parent)
        
        if rows < 1 or cols < 1: Exception('Figure rows / cols must be greater than 0!')
        
        self.canvas             = None
        self.figure             = None
        self.axes               = None
        self.toolbar            = None
        self.figsize            = (6.0, 4.0)
        self.dof3               = dof3
        self.rows               = rows
        self.cols               = cols
        self.multiplot          = rows != 1 or cols != 1
        self.figure_in_dialog   = figure_in_dialog
        
        self._coord     = '(0.00, 0.00)' if not dof3 else '(0.00, 0.00, 0.00)'

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
        self.figsize    = (qml_object_parent.width() // 100, (qml_object_parent.height() - 50) // 100) # * width and height in inches
        
        # ? Set Axes
        
        if self.multiplot:
            
            self.axes = self.figure.subplots(nrows=self.rows, ncols=self.cols)
            
            for r in range(0, self.rows):
                
                for c in range(0, self.cols):
                    
                    self.axes[r][c].grid(True)
                    self.axes[r][c].set_facecolor('#424242')# if self.figure_in_dialog else '#1C1B1F')
            
        else:
            
            self.axes = self.figure.add_subplot(111) if not self.dof3 else self.figure.add_subplot(111, projection='3d')
            
            self.axes.grid(True)
            self.axes.set_facecolor('#424242')# if self.figure_in_dialog else '#1C1B1F')
        
        # ? Set Figure
        
        if self.dof3:
            
            self.figure.subplots_adjust(left=-0.11, top=0.99)
            self.figure.set_layout_engine('compressed')
            self.axes.set_aspect('equal', adjustable='box')
            
        else:
            
        
            self.figure.subplots_adjust(wspace=0.4, hspace=0.4)
            self.figure.set_layout_engine('constrained')
            
        self.figure.set_figwidth(self.figsize[0])
        self.figure.set_figheight(self.figsize[1])
        self.figure.patch.set_facecolor('#424242')# if self.figure_in_dialog else '#1C1B1F')
        
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
    
    def redraw_canvas(self) -> None:
        """Redraws the figure canvas
        """
        
        self.canvas.draw_idle()
    
    def line2d_seg_dist(self, p1 : list, p2 : list, p0 : tuple) -> float:
        """Distance(s) from line defined by p1 - p2 to point(s) p0
        
            p0[0] = x(s)
            p0[1] = y(s)

        intersection point p = p1 + u * (p2 - p1)
        
        and intersection point lies within segment if u is between 0 and 1
        
        Args:
            p1 (list): Point 1
            p2 (list): Point 2
            p0 (tuple): Current 2D point

        Returns:
            float: Distance
        """

        x21 = p2[0] - p1[0]
        y21 = p2[1] - p1[1]
        
        x01 = np.asarray(p0[0]) - p1[0]
        y01 = np.asarray(p0[1]) - p1[1]

        u = (x01*x21 + y01*y21) / (x21**2 + y21**2)
        u = np.clip(u, 0, 1)
        d = np.hypot(x01 - u*x21, y01 - u*y21)

        return d
    
    def get_w_lims(self, axis):
        '''Get 3D world limits.'''
        minx, maxx = axis.get_xlim3d()
        miny, maxy = axis.get_ylim3d()
        minz, maxz = axis.get_zlim3d()
        return minx, maxx, miny, maxy, minz, maxz
    
    def unit_cube(self, axis, vals=None):
        minx, maxx, miny, maxy, minz, maxz = vals or self.get_w_lims(axis)
        return [(minx, miny, minz),
                (maxx, miny, minz),
                (maxx, maxy, minz),
                (minx, maxy, minz),
                (minx, miny, maxz),
                (maxx, miny, maxz),
                (maxx, maxy, maxz),
                (minx, maxy, maxz)]
    
    def tunit_cube(self, axis, vals=None, M=None):
        #if M is None:
        #    M = self.M
        xyzs = self.unit_cube(axis, vals)
        tcube = proj3d.proj_points(xyzs, M)
        return tcube
    
    def tunit_edges(self, axis, vals=None, M=None):
        #tc = self.tunit_cube(axis, vals, M)
        
        tc = axis._transformed_cube(axis.get_w_lims())
        #print(tc)
        edges = [(tc[0], tc[1]),
                 (tc[1], tc[2]),
                 (tc[2], tc[3]),
                 (tc[3], tc[0]),

                 (tc[0], tc[4]),
                 (tc[1], tc[5]),
                 (tc[2], tc[6]),
                 (tc[3], tc[7]),

                 (tc[4], tc[5]),
                 (tc[5], tc[6]),
                 (tc[6], tc[7]),
                 (tc[7], tc[4])]
        return edges
    
    def xyz_data(self, event : qtGui.QMouseEvent, ax) -> list:
        """Retrieves the x-y-z coordinates in a 3D plot

        Args:
            event (qtGui.QMouseEvent): Event
            ax (): Figure axis

        Returns:
            list: [x, y, z]
        """
        
        #if ax.M is None: return 0.0, 0.0, 0.0

        xd, yd = event.xdata, event.ydata
        
        p = (xd, yd)
        
        #edges = self.tunit_edges(ax)#ax.tunit_edges()
        
        #print(ax.get_w_lims())
        tc = ax._transformed_cube(ax.get_w_lims())
        
        edges = [(tc[0], tc[1]),
                 (tc[1], tc[2]),
                 (tc[2], tc[3]),
                 (tc[3], tc[0]),

                 (tc[0], tc[4]),
                 (tc[1], tc[5]),
                 (tc[2], tc[6]),
                 (tc[3], tc[7]),

                 (tc[4], tc[5]),
                 (tc[5], tc[6]),
                 (tc[6], tc[7]),
                 (tc[7], tc[4])]
        
        ldists = [(self.line2d_seg_dist(p0, p1, p), i) for i, (p0, p1) in enumerate(edges)]
        
        ldists.sort()

        # ? Nearest edge
        
        edgei = ldists[0][1]

        p0, p1 = edges[edgei]

        # ? Scale the z value to match
        
        x0, y0, z0 = p0
        x1, y1, z1 = p1
        
        d0 = np.hypot(x0 - xd, y0 - yd)
        d1 = np.hypot(x1 - xd, y1 - yd)
        dt = d0 + d1
        
        z = d1 / dt * z0 + d0 / dt * z1

        x, y, z = proj3d.inv_transform(xd, yd, z, ax.M)
        
        return x, y, z
    
    # --- SLOTS 
    
    @qtCore.Slot(float, float)
    def resize_figure(self, width : float, height : float) -> None:
        """Resizes the figure

        Args:
            width (float): Width in pixels
            height (float): Height in pixels
        """
        
        if self.figure == None: return
        
        self.figsize = (width // 100, (height - 50) // 100)
        
        self.figure.set_figwidth(self.figsize[0])
        self.figure.set_figheight(self.figsize[1])
        
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
                
                if self.dof3:
                    #print('>>>', self.xyz_data(event, self.axes))
                    x, y, z = self.xyz_data(event, self.axes)
            
                    self.coord = f'({x[0]:.2f}, {y[0]:.2f}, {z[0]:.2f})'
                
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