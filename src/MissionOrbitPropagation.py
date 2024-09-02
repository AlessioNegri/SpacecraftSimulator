""" MissionOrbitPropagation.py: Implements the orbit propagation mission """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np
import mplcyberpunk

from datetime import datetime

from Utility import format
from FigureCanvas import FigureCanvas
from Spacecraft import Spacecraft

from tools.AstronomicalData import CelestialBody
from tools.OrbitalPerturbations import OrbitalPerturbations
from tools.OrbitDetermination import OrbitDetermination

class MissionOrbitPropagation(qtCore.QObject):
    """Manages the orbit propagation mission"""
    
    # --- PROPERTIES 
    
    # ? Angular Momentum [km^2 / s]
    
    @qtCore.Property(float)
    def angular_momentum(self): return format(self._angular_momentum)

    @angular_momentum.setter
    def angular_momentum(self, val : float): self._angular_momentum = val
    
    # ? Eccentricity
    
    @qtCore.Property(float)
    def eccentricity(self): return format(self._eccentricity)

    @eccentricity.setter
    def eccentricity(self, val : float): self._eccentricity = val
    
    # ? Inclination [rad]
    
    @qtCore.Property(float)
    def inclination(self): return format(self._inclination, deg=True)

    @inclination.setter
    def inclination(self, val : float): self._inclination = np.deg2rad(val)
    
    # ? Right Ascension Ascending Node [rad]
    
    @qtCore.Property(float)
    def right_ascension_ascending_node(self): return format(self._right_ascension_ascending_node, deg=True)

    @right_ascension_ascending_node.setter
    def right_ascension_ascending_node(self, val : float): self._right_ascension_ascending_node = np.deg2rad(val)
    
    # ? Periapsis Anomaly [rad]
    
    @qtCore.Property(float)
    def periapsis_anomaly(self): return format(self._periapsis_anomaly, deg=True)

    @periapsis_anomaly.setter
    def periapsis_anomaly(self, val : float): self._periapsis_anomaly = np.deg2rad(val)
    
    # ? True Anomaly [rad]
    
    @qtCore.Property(float)
    def true_anomaly(self): return format(self._true_anomaly, deg=True)

    @true_anomaly.setter
    def true_anomaly(self, val : float): self._true_anomaly = np.deg2rad(val)
    
    # ? Drag Perturbation
    
    @qtCore.Property(bool)
    def drag(self): return self._drag

    @drag.setter
    def drag(self, val : bool): self._drag = val
    
    # ? Gravitational Perturbation
    
    @qtCore.Property(bool)
    def gravitational(self): return self._gravitational

    @gravitational.setter
    def gravitational(self, val : bool): self._gravitational = val
    
    # ? Solar Radiation Pressure Perturbation
    
    @qtCore.Property(bool)
    def solar_radiation_pressure(self): return self._solar_radiation_pressure

    @solar_radiation_pressure.setter
    def solar_radiation_pressure(self, val : bool): self._solar_radiation_pressure = val
    
    # ? Third Body Perturbation
    
    @qtCore.Property(bool)
    def third_body(self): return self._third_body

    @third_body.setter
    def third_body(self, val : bool): self._third_body = val
    
    # ? Third Body Choice
    
    @qtCore.Property(int)
    def third_body_choice(self): return self._third_body_choice

    @third_body_choice.setter
    def third_body_choice(self, val : int): self._third_body_choice = val
    
    # ? Start Date
    
    @qtCore.Property(str)
    def start_date(self): return self._start_date

    @start_date.setter
    def start_date(self, val : str): self._start_date = val
    
    # ? End Date
    
    @qtCore.Property(str)
    def end_date(self): return self._end_date

    @end_date.setter
    def end_date(self, val : str): self._end_date = val
    
    # --- METHODS 
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__MissionOrbitPropagation", self)
        
        self.spacecraft = Spacecraft(engine)
        
        # ? Orbital elements
        
        self._angular_momentum                  : float = 63383.4               # * Angular Momentum                                [ km^2 / s ]
        self._eccentricity                      : float = 0.025422              # * Eccentricity                                    [ ]
        self._inclination                       : float = np.deg2rad(343.427)   # * Inclination                                     [ deg ]
        self._right_ascension_ascending_node    : float = np.deg2rad(45.3812)   # * Right Ascension of the Ascending Node (RAAN)    [ deg ]
        self._periapsis_anomaly                 : float = np.deg2rad(88.3924)   # * Periapsis anomaly                               [ deg ]
        self._true_anomaly                      : float = np.deg2rad(227.493)   # * True anomaly                                    [ deg ]
        
        # ? Orbital perturbations
        
        self._drag                              : bool = False                  # * Use drag perturbation
        self._gravitational                     : bool = False                  # * Use gravitational perturbation
        self._solar_radiation_pressure          : bool = False                  # * Use solar radiation pressure perturbation
        self._third_body                        : bool = False                  # * Use third body perturbation
        self._third_body_choice                 : int = 0                       # * Third body selection
        self._start_date                        : str = '2024-06-01 00:00:00'   # * Start date
        self._end_date                          : str = '2024-06-02 00:00:00'   # * End date
        
        # ? Orbit propagation
        
        self.figure = FigureCanvas(rows=2, cols=3)
        
        # ? Context properties
        
        engine.rootContext().setContextProperty("__OrbitPropagationFigure", self.figure)
    
    def set_update_with_canvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Connects all the QML figures with the backend model

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        win = engine.rootObjects()[0]
        
        self.figure.update_with_canvas(win.findChild(qtCore.QObject, "OrbitPropagationFigure"), win.findChild(qtCore.QObject, "OrbitPropagationFigureParent"))
        
        self.init_figure()
    
    # --- PUBLIC SLOTS 
     
    @qtCore.Slot()
    def simulate(self) -> None:
        """Simulates the orbital perturbations
        """
        
        # ? Simulation
        
        OrbitalPerturbations.set_celestial_body(CelestialBody.EARTH)
        
        y_0 = np.array([self.angular_momentum, self.eccentricity, self.true_anomaly, self.right_ascension_ascending_node, self.inclination, self.periapsis_anomaly])
        
        start_date  = datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')
        end_date    = datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')
        
        JD_0 = OrbitDetermination.julian_day(start_date.year, start_date.month, start_date.day, start_date.hour, start_date.minute, start_date.second)
        JD_f = OrbitDetermination.julian_day(end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second)
        
        B       = self.spacecraft.drag_coefficient * self.spacecraft.reference_surface / self.spacecraft.initial_mass
        B_SRP   = self.spacecraft.radiation_pressure_coefficient * self.spacecraft.absorbing_surface / self.spacecraft.initial_mass
        
        result = OrbitalPerturbations.simulate_gauss_variational_equations(y_0,
                                                                           drag=self.drag,
                                                                           gravitational=self.gravitational,
                                                                           SRP=self.solar_radiation_pressure,
                                                                           B=B,
                                                                           B_SRP=B_SRP,
                                                                           MOON=self.third_body and self.third_body_choice == 0,
                                                                           SUN=self.third_body and self.third_body_choice == 1,
                                                                           JD_0=JD_0 * 86400,
                                                                           JD_f=JD_f * 86400)
        
        a       = result['a']
        e       = result['e']
        h       = result['h']
        i       = result['i']
        Omega   = result['Omega']
        omega   = result['omega']
        t       = result['t']
        
        # ? Plot
        
        self.figure.reset_canvas()
        
        self.figure.axes[0,0].plot(t, a - a[0], color='#FFCC80')
        self.figure.axes[0,0].set_title('Semi-Major Axis Variation [ $km$ ]')
        
        self.figure.axes[0,1].plot(t, e - e[0], color='#90CAF9')
        self.figure.axes[0,1].set_title('Eccentricity Variation')
        
        self.figure.axes[0,2].plot(t, h - h[0], color='#CE93D8')
        self.figure.axes[0,2].set_title('Angular Momentum Variation [ $km^2\;/\;s$ ]')
        
        self.figure.axes[1,0].plot(t, i - i[0], color='#F48FB1')
        self.figure.axes[1,0].set_xlabel('Time [days]')
        self.figure.axes[1,0].set_title('Inclination Variation [ $°$ ]')
        
        self.figure.axes[1,1].plot(t, Omega - Omega[0], color='#E6EE9C')
        self.figure.axes[1,1].set_xlabel('Time [days]')
        self.figure.axes[1,1].set_title('RAAN Variation [ $°$ ]')
        
        self.figure.axes[1,2].plot(t, omega - omega[0], color='#80CBC4')
        self.figure.axes[1,2].set_xlabel('Time [days]')
        self.figure.axes[1,2].set_title('Periapsis Anomaly Variation [ $°$ ]')
        
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
        
        self.figure.axes[0,0].set_title('Semi-Major Axis Variation [ $km$ ]')
        
        self.figure.axes[0,1].set_title('Eccentricity Variation')
        
        self.figure.axes[0,2].set_title('Angular Momentum Variation [ $km^2\;/\;s$ ]')
        
        self.figure.axes[1,0].set_xlabel('Time [days]')
        self.figure.axes[1,0].set_title('Inclination Variation [ $°$ ]')
        
        self.figure.axes[1,1].set_xlabel('Time [days]')
        self.figure.axes[1,1].set_title('RAAN Variation [ $°$ ]')
        
        self.figure.axes[1,2].set_xlabel('Time [days]')
        self.figure.axes[1,2].set_title('Periapsis Anomaly Variation [ $°$ ]')
        
        self.figure.redraw_canvas()