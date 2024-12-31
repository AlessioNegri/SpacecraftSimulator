""" MissionOrbitPropagation.py: Implements the orbit propagation mission """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np
import mplcyberpunk

from datetime import datetime

from common import format
from src.utility.figure_canvas import FigureCanvas
from systems.spacecraft import Spacecraft

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
    
    # --- PUBLIC METHODS 
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        self.engine = engine
        
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
        
        # ? Simulation Results
        
        self.result = dict() # * Simulation Result Dictionary
        
        # ? Figure Canvas
        
        self.figure_semi_major_axis     = FigureCanvas()
        self.figure_eccentricity        = FigureCanvas()
        self.figure_angular_momentum    = FigureCanvas()
        self.figure_inclination         = FigureCanvas()
        self.figure_raan                = FigureCanvas()
        self.figure_periapsis_anomaly   = FigureCanvas()
        
        # ? Context properties
        
        engine.rootContext().setContextProperty("__OrbitPropagationFigureSemiMajorAxis", self.figure_semi_major_axis)
        engine.rootContext().setContextProperty("__OrbitPropagationFigureEccentricity", self.figure_eccentricity)
        engine.rootContext().setContextProperty("__OrbitPropagationFigureAngularMomentum", self.figure_angular_momentum)
        engine.rootContext().setContextProperty("__OrbitPropagationFigureInclination", self.figure_inclination)
        engine.rootContext().setContextProperty("__OrbitPropagationFigureRAAN", self.figure_raan)
        engine.rootContext().setContextProperty("__OrbitPropagationFigurePeriapsisAnomaly", self.figure_periapsis_anomaly)
    
    # --- PUBLIC SLOTS 
    
    @qtCore.Slot()
    def attach_canvas(self) -> None:
        """Connects all the QML figures with the backend model
        """
        
        win = self.engine.rootObjects()[0]
        
        self.figure_semi_major_axis.update_with_canvas(win.findChild(qtCore.QObject, "OrbitPropagationFigureSemiMajorAxis"), win.findChild(qtCore.QObject, "OrbitPropagationFigureSemiMajorAxisParent"))
        self.figure_eccentricity.update_with_canvas(win.findChild(qtCore.QObject, "OrbitPropagationFigureEccentricity"), win.findChild(qtCore.QObject, "OrbitPropagationFigureEccentricityParent"))
        self.figure_angular_momentum.update_with_canvas(win.findChild(qtCore.QObject, "OrbitPropagationFigureAngularMomentum"), win.findChild(qtCore.QObject, "OrbitPropagationFigureAngularMomentumParent"))
        self.figure_inclination.update_with_canvas(win.findChild(qtCore.QObject, "OrbitPropagationFigureInclination"), win.findChild(qtCore.QObject, "OrbitPropagationFigureInclinationParent"))
        self.figure_raan.update_with_canvas(win.findChild(qtCore.QObject, "OrbitPropagationFigureRAAN"), win.findChild(qtCore.QObject, "OrbitPropagationFigureRAANParent"))
        self.figure_periapsis_anomaly.update_with_canvas(win.findChild(qtCore.QObject, "OrbitPropagationFigurePeriapsisAnomaly"), win.findChild(qtCore.QObject, "OrbitPropagationFigurePeriapsisAnomalyParent"))
        
        self.init_figure()
    
    @qtCore.Slot()
    def detach_canvas(self) -> None:
        """Disconnects all the QML figures from the backend model
        """
        
        self.figure_semi_major_axis     = FigureCanvas()
        self.figure_eccentricity        = FigureCanvas()
        self.figure_angular_momentum    = FigureCanvas()
        self.figure_inclination         = FigureCanvas()
        self.figure_raan                = FigureCanvas()
        self.figure_periapsis_anomaly   = FigureCanvas()
        
        self.engine.rootContext().setContextProperty("__OrbitPropagationFigureSemiMajorAxis", self.figure_semi_major_axis)
        self.engine.rootContext().setContextProperty("__OrbitPropagationFigureEccentricity", self.figure_eccentricity)
        self.engine.rootContext().setContextProperty("__OrbitPropagationFigureAngularMomentum", self.figure_angular_momentum)
        self.engine.rootContext().setContextProperty("__OrbitPropagationFigureInclination", self.figure_inclination)
        self.engine.rootContext().setContextProperty("__OrbitPropagationFigureRAAN", self.figure_raan)
        self.engine.rootContext().setContextProperty("__OrbitPropagationFigurePeriapsisAnomaly", self.figure_periapsis_anomaly)
    
    @qtCore.Slot()
    def simulate(self) -> None:
        """Simulates the orbital perturbations
        """
        
        # ? Simulation
        
        OrbitalPerturbations.set_celestial_body(CelestialBody.EARTH)
        
        OrbitDetermination.set_celestial_body(CelestialBody.EARTH)
        
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
        
        self.result = result
        
        # ? Plot
        
        self.plot_figures()
    
    # --- PRIVATE METHODS 
    
    def init_figure(self) -> None:
        """Initializes the figure canvas
        """
        
        # ? Semi Major Axis
        
        self.figure_semi_major_axis.reset_canvas()
        self.figure_semi_major_axis.format_canvas('Time [ days ]', 'Semi-Major Axis Variation [ $km$ ]', -200)
        self.figure_semi_major_axis.redraw_canvas()
        
        # ? Eccentricity
        
        self.figure_eccentricity.reset_canvas()
        self.figure_eccentricity.format_canvas('Time [ days ]', 'Eccentricity Variation', -175)
        self.figure_eccentricity.redraw_canvas()
        
        # ? Angular Momentum
        
        self.figure_angular_momentum.reset_canvas()
        self.figure_angular_momentum.format_canvas('Time [ days ]', 'Angular Momentum Variation [ $km^2\;/\;s$ ]', -250)
        self.figure_angular_momentum.redraw_canvas()
        
        # ? Inclination
        
        self.figure_inclination.reset_canvas()
        self.figure_inclination.format_canvas('Time [ days ]', 'Inclination Variation [ $°$ ]', -175)
        self.figure_inclination.redraw_canvas()
        
        # ? RAAN
        
        self.figure_raan.reset_canvas()
        self.figure_raan.format_canvas('Time [ days ]', 'RAAN Variation [ $°$ ]', -150)
        self.figure_raan.redraw_canvas()
        
        # ? Periapsis Anomaly
        
        self.figure_periapsis_anomaly.reset_canvas()
        self.figure_periapsis_anomaly.format_canvas('Time [ days ]', 'Periapsis Anomaly Variation [ $°$ ]', -200)
        self.figure_periapsis_anomaly.redraw_canvas()
        
        # ? Plot
        
        self.plot_figures()
    
    def plot_figures(self) -> None:
        """Plots the figures with the results of the simulation
        """
        
        if len(self.result) == 0: return
        
        a       = self.result['a']
        e       = self.result['e']
        h       = self.result['h']
        i       = self.result['i']
        Omega   = self.result['Omega']
        omega   = self.result['omega']
        t       = self.result['t']
        
        # ? Semi Major Axis
        
        self.figure_semi_major_axis.reset_canvas()
        self.figure_semi_major_axis.format_canvas('Time [ days ]', 'Semi-Major Axis Variation [ $km$ ]', -200)
        self.figure_semi_major_axis.axes.plot(t, a - a[0], color=FigureCanvas.default_color)
        self.figure_semi_major_axis.redraw_canvas()
        
        # ? Eccentricity
        
        self.figure_eccentricity.reset_canvas()
        self.figure_eccentricity.format_canvas('Time [ days ]', 'Eccentricity Variation', -175)
        self.figure_eccentricity.axes.plot(t, e - e[0], color=FigureCanvas.default_color)
        self.figure_eccentricity.redraw_canvas()
        
        # ? Angular Momentum
        
        self.figure_angular_momentum.reset_canvas()
        self.figure_angular_momentum.format_canvas('Time [ days ]', 'Angular Momentum Variation [ $km^2\;/\;s$ ]', -250)
        self.figure_angular_momentum.axes.plot(t, h - h[0], color=FigureCanvas.default_color)
        self.figure_angular_momentum.redraw_canvas()
        
        # ? Inclination
        
        self.figure_inclination.reset_canvas()
        self.figure_inclination.format_canvas('Time [ days ]', 'Inclination Variation [ $°$ ]', -175)
        self.figure_inclination.axes.plot(t, i - i[0], color=FigureCanvas.default_color)
        self.figure_inclination.redraw_canvas()
        
        # ? RAAN
        
        self.figure_raan.reset_canvas()
        self.figure_raan.format_canvas('Time [ days ]', 'RAAN Variation [ $°$ ]', -150)
        self.figure_raan.axes.plot(t, Omega - Omega[0], color=FigureCanvas.default_color)
        self.figure_raan.redraw_canvas()
        
        # ? Periapsis Anomaly
        
        self.figure_periapsis_anomaly.reset_canvas()
        self.figure_periapsis_anomaly.format_canvas('Time [ days ]', 'Periapsis Anomaly Variation [ $°$ ]', -200)
        self.figure_periapsis_anomaly.axes.plot(t, omega - omega[0], color=FigureCanvas.default_color)
        self.figure_periapsis_anomaly.redraw_canvas()