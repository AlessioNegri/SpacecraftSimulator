""" MissionAtmosphericEntry.py: Implements the atmospheric entry mission """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np
import mplcyberpunk

from Utility import format
from FigureCanvas import FigureCanvas
from Spacecraft import Spacecraft

from tools.AtmosphericEntry import AtmosphericEntry

class MissionAtmosphericEntry(qtCore.QObject):
    """Manages the atmospheric entry mission"""
    
    # --- PROPERTIES 
    
    # ? Entry Velocity [km / s]
    
    @qtCore.Property(float)
    def entry_velocity(self): return format(self._entry_velocity)
    
    @entry_velocity.setter
    def entry_velocity(self, val : float): self._entry_velocity = val
    
    # ? Entry Flight Path Angle [deg]
    
    @qtCore.Property(float)
    def entry_flight_path_angle(self): return format(self._entry_flight_path_angle)
    
    @entry_flight_path_angle.setter
    def entry_flight_path_angle(self, val : float): self._entry_flight_path_angle = val
    
    # ? Entry Altitude [km]
    
    @qtCore.Property(float)
    def entry_altitude(self): return format(self._entry_altitude)
    
    @entry_altitude.setter
    def entry_altitude(self, val : float): self._entry_altitude = val
    
    # ? Final Integration Time [min]
    
    @qtCore.Property(float)
    def final_integration_time(self): return format(self._final_integration_time)
    
    @final_integration_time.setter
    def final_integration_time(self, val : float): self._final_integration_time = val
    
    # ? Use Parachute
    
    @qtCore.Property(bool)
    def use_parachute(self): return self._use_parachute
    
    @use_parachute.setter
    def use_parachute(self, val : bool): self._use_parachute = val
    
    # ? Impact Velocity [m/s]
    
    impact_velocity_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=impact_velocity_changed)
    def impact_velocity(self): return format(self._impact_velocity)
    
    @impact_velocity.setter
    def impact_velocity(self, val : float): self._impact_velocity = val; self.impact_velocity_changed.emit()
    
    # --- PUBLIC METHODS 
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__MissionAtmosphericEntry", self)
        
        self.spacecraft = Spacecraft(engine)
        
        # ? Entry Condition
        
        self._entry_velocity            : float = 12.6161   # * Entry Velocity          [ km / s ]
        self._entry_flight_path_angle   : float = -9        # * Entry Flight Path Angle [ deg ]
        self._entry_altitude            : float = 120       # * Entry Altitude          [ km ]
        self._final_integration_time    : float = 60        # * Final Integration Time  [ min ]
        self._impact_velocity           : float = 0         # * Impact Velocity         [ m / s ]
        
        self._use_parachute             : bool  = False     # * True for using the parachute
        
        # ? Figure Canvas
        
        self.figure = FigureCanvas(rows=2, cols=3)
        
        # ? Context properties
        
        engine.rootContext().setContextProperty("__AtmosphericEntryFigure", self.figure)
    
    def set_update_with_canvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Connects all the QML figures with the backend model

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        win = engine.rootObjects()[0]
        
        self.figure.update_with_canvas(win.findChild(qtCore.QObject, "AtmosphericEntryFigure"), win.findChild(qtCore.QObject, "AtmosphericEntryFigureParent"))
        
        self.init_figure()
    
    # --- PUBLIC SLOTS 
    
    @qtCore.Slot()
    def simulate(self) -> None:
        """Simulates the atmospheric entry mission
        """
        
        # ? Simulation
        
        AtmosphericEntry.set_capsule_parameters(0, 300, 0, self.spacecraft.capsule_lift_coefficient, self.spacecraft.capsule_drag_coefficient, self.spacecraft.capsule_reference_surface)
        
        AtmosphericEntry.set_parachute_parameters(self.use_parachute, self.spacecraft.parachute_drag_coefficient, self.spacecraft.parachute_reference_surface)
        
        y_0 = np.array([self.entry_velocity, np.deg2rad(self.entry_flight_path_angle), self.entry_altitude, 0, self.spacecraft.capsule_mass])
        
        result = AtmosphericEntry.simulate_atmospheric_entry(y_0, t_f=self.final_integration_time * 60)
        
        V       = result['y'][0, :]
        gamma   = result['y'][1, :]
        r       = result['y'][2, :]
        x       = result['y'][3, :]
        m       = result['y'][4, :]
        t       = result['t']
        
        C       = (1.7415 * 1e-4 * 1 / np.sqrt(self.spacecraft.capsule_nose_radius))
        q_t_c   = np.array([C * np.sqrt(1.225 * np.exp(-(r[i] - AtmosphericEntry.R_E) / AtmosphericEntry.H)) * (V[i] * 1e3)**3 for i in range(0, len(t))])
        a       = np.array([(V[i] - V[i - 1]) / (t[i] - t[i - 1]) for i in range(1, len(t))])
        
        self.impact_velocity = V[-1] * 1e3
        
        # ? Plot
        
        t = t / 60
        
        self.figure.reset_canvas()
        
        #self.figure.figure.suptitle(self.figure_title(V[-1] * 1e3))
        
        self.figure.axes[0,0].plot(t, V, color='#FFCC80', label='Velocity [$km\;/\;s$] - Time [$min$]')
        self.figure.axes[0,0].legend()
        
        self.figure.axes[0,1].plot(t[1:], a / AtmosphericEntry.g_E, color='#90CAF9', label='Acceleration [$g$] - Time [$min$]')
        self.figure.axes[0,1].legend()
        
        self.figure.axes[0,2].plot(x, r - AtmosphericEntry.R_E, color='#CE93D8', label='Altitude [$km$] - Downrange Distance [$km$]')
        self.figure.axes[0,2].legend()
        
        self.figure.axes[1,0].plot(t, gamma * 180 / np.pi, color='#F48FB1', label='Flight Path Angle [$deg$] - Time [$min$]')
        self.figure.axes[1,0].legend()
        
        self.figure.axes[1,1].plot(t, q_t_c * 1e-4, color='#E6EE9C', label='S.P. Convective Heat Flux [$W\;/\;cm^2$] - Time [$min$]')
        self.figure.axes[1,1].legend()
        
        self.figure.axes[1,2].plot(V, r - AtmosphericEntry.R_E, color='#80CBC4', label='Altitude [$km$] - Velocity [$km\;/\;s$]')
        self.figure.axes[1,2].legend()
        
        mplcyberpunk.make_lines_glow(self.figure.axes[0,0])
        mplcyberpunk.make_lines_glow(self.figure.axes[0,1])
        mplcyberpunk.make_lines_glow(self.figure.axes[0,2])
        mplcyberpunk.make_lines_glow(self.figure.axes[1,0])
        mplcyberpunk.make_lines_glow(self.figure.axes[1,1])
        mplcyberpunk.make_lines_glow(self.figure.axes[1,2])
        
        self.figure.redraw_canvas()
    
    # --- PRIVATE METHODS 
        
    def init_figure(self) -> None:
        """Initializes the figure canvas
        """
        
        self.figure.reset_canvas()
        
        #self.figure.figure.suptitle(self.figure_title())
            
        self.figure.axes[0,0].plot(0, 0, color='#FFCC80', label='Velocity [$km\;/\;s$] - Time [$min$]')
        self.figure.axes[0,0].legend()
        
        self.figure.axes[0,1].plot(0, 0, color='#90CAF9', label='Acceleration [$g$] - Time [$min$]')
        self.figure.axes[0,1].legend()
        
        self.figure.axes[0,2].plot(0, 0, color='#CE93D8', label='Altitude [$km$] - Downrange Distance [$km$]')
        self.figure.axes[0,2].legend()
        
        self.figure.axes[1,0].plot(0, 0, color='#F48FB1', label='Flight Path Angle [$deg$] - Time [$min$]')
        self.figure.axes[1,0].legend()
        
        self.figure.axes[1,1].plot(0, 0, color='#E6EE9C', label='S.P. Convective Heat Flux [$W\;/\;cm^2$] - Time [$min$]')
        self.figure.axes[1,1].legend()
        
        self.figure.axes[1,2].plot(0, 0, color='#80CBC4', label='Altitude [$km$] - Velocity [$km\;/\;s$]')
        self.figure.axes[1,2].legend()
        
        self.figure.redraw_canvas()