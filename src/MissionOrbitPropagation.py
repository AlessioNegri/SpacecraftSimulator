import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np

from Utility import format
from FigureCanvas import FigureCanvas
from Orbit import Orbit

from tools.stdafx import datetime
from tools.AstronomicalData import CelestialBody
from tools.OrbitalPerturbations import OrbitalPerturbations
from tools.OrbitDetermination import OrbitDetermination

class MissionOrbitPropagation(qtCore.QObject):
    
    # ! PROPERTIES
    
    # ? Angular Momentum [km^2 / s]
    
    angular_momentum_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=angular_momentum_changed)
    def angular_momentum(self): return format(self._angular_momentum)

    @angular_momentum.setter
    def angular_momentum(self, val : float): self._angular_momentum = val
    
    # ? Eccentricity
    
    eccentricity_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=eccentricity_changed)
    def eccentricity(self): return format(self._eccentricity)

    @eccentricity.setter
    def eccentricity(self, val : float): self._eccentricity = val
    
    # ? Inclination [rad]
    
    inclination_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=inclination_changed)
    def inclination(self): return format(self._inclination, deg=True)

    @inclination.setter
    def inclination(self, val : float): self._inclination = np.deg2rad(val)
    
    # ? Right Ascension Ascending Node [rad]
    
    right_ascension_ascending_node_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=right_ascension_ascending_node_changed)
    def right_ascension_ascending_node(self): return format(self._right_ascension_ascending_node, deg=True)

    @right_ascension_ascending_node.setter
    def right_ascension_ascending_node(self, val : float): self._right_ascension_ascending_node = np.deg2rad(val)
    
    # ? Periapsis Anomaly [rad]
    
    periapsis_anomaly_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=periapsis_anomaly_changed)
    def periapsis_anomaly(self): return format(self._periapsis_anomaly, deg=True)

    @periapsis_anomaly.setter
    def periapsis_anomaly(self, val : float): self._periapsis_anomaly = np.deg2rad(val)
    
    # ? True Anomaly [rad]
    
    true_anomaly_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=true_anomaly_changed)
    def true_anomaly(self): return format(self._true_anomaly, deg=True)

    @true_anomaly.setter
    def true_anomaly(self, val : float): self._true_anomaly = np.deg2rad(val)
    
    # ? Drag Perturbation
    
    drag_changed = qtCore.Signal()
    
    @qtCore.Property(bool, notify=drag_changed)
    def drag(self): return self._drag

    @drag.setter
    def drag(self, val : bool): self._drag = val
    
    # ? Drag Ballistic Coefficient [m^2 / kg]
    
    drag_ballistic_coefficient_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=drag_ballistic_coefficient_changed)
    def drag_ballistic_coefficient(self): return format(self._drag_ballistic_coefficient)

    @drag_ballistic_coefficient.setter
    def drag_ballistic_coefficient(self, val : float): self._drag_ballistic_coefficient = val
    
    # ? Gravitational Perturbation
    
    gravitational_changed = qtCore.Signal()
    
    @qtCore.Property(bool, notify=gravitational_changed)
    def gravitational(self): return self._gravitational

    @gravitational.setter
    def gravitational(self, val : bool): self._gravitational = val
    
    # ? Solar Radiation Pressure Perturbation
    
    srp_changed = qtCore.Signal()
    
    @qtCore.Property(bool, notify=srp_changed)
    def srp(self): return self._srp

    @srp.setter
    def srp(self, val : bool): self._srp = val
    
    # ? Solar Radiation Pressure Ballistic Coefficient [m^2 / kg]
    
    srp_ballistic_coefficient_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=srp_ballistic_coefficient_changed)
    def srp_ballistic_coefficient(self): return format(self._srp_ballistic_coefficient)

    @srp_ballistic_coefficient.setter
    def srp_ballistic_coefficient(self, val : float): self._srp_ballistic_coefficient = val
    
    # ? Third Body Perturbation
    
    third_body_changed = qtCore.Signal()
    
    @qtCore.Property(bool, notify=third_body_changed)
    def third_body(self): return self._third_body

    @third_body.setter
    def third_body(self, val : bool): self._third_body = val
    
    # ? Third Body Choice
    
    third_body_choice_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=third_body_choice_changed)
    def third_body_choice(self): return self._third_body_choice

    @third_body_choice.setter
    def third_body_choice(self, val : int): self._third_body_choice = val
    
    # ? Start Date
    
    start_date_changed = qtCore.Signal()
    
    @qtCore.Property(str, notify=start_date_changed)
    def start_date(self): return self._start_date

    @start_date.setter
    def start_date(self, val : str): self._start_date = val
    
    # ? End Date
    
    end_date_changed = qtCore.Signal()
    
    @qtCore.Property(str, notify=end_date_changed)
    def end_date(self): return self._end_date

    @end_date.setter
    def end_date(self, val : str): self._end_date = val
    
    # ! CONSTRUCTOR
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__MissionOrbitPropagation", self)
        
        # * Orbital elements
        
        self._angular_momentum                  : float = 63383.4
        self._eccentricity                      : float = 0.025422
        self._inclination                       : float = np.deg2rad(343.427)
        self._right_ascension_ascending_node    : float = np.deg2rad(45.3812)
        self._periapsis_anomaly                 : float = np.deg2rad(88.3924)
        self._true_anomaly                      : float = np.deg2rad(227.493)
        
        # * Orbital Perturbations
        
        self._drag                              : bool = False
        self._drag_ballistic_coefficient        : float = 2.2 * (np.pi * 1**2 / 4) / 100
        self._gravitational                     : bool = False
        self._srp                               : bool = False
        self._srp_ballistic_coefficient         : float = 2 * 2
        self._third_body                        : bool = False
        self._third_body_choice                 : int = 0
        self._start_date                        : str = '2024-06-01 00:00:00'
        self._end_date                          : str = '2024-06-02 00:00:00'
        
        # * Orbit propagation
        
        self.figure_orbit_propagation = FigureCanvas()
        
        # * Context properties
        
        engine.rootContext().setContextProperty("__OrbitPropagationFigure", self.figure_orbit_propagation)
    
    # ! PUBLIC
    
    def setUpdateWithCanvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Connects all the QML figures with the backend model

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        win = engine.rootObjects()[0]
        
        self.figure_orbit_propagation.updateWithCanvas(win.findChild(qtCore.QObject, "OrbitPropagationFigure"), win.findChild(qtCore.QObject, "OrbitPropagationFigureParent"), rows=2, cols=3)
    
     # ! SLOTS
     
    @qtCore.Slot()
    def loadOrbitalPerturbationsParameters(self) -> None:
        """Loads the orbital perturbations parameters
        """
        
        pass
    
    @qtCore.Slot()
    def saveOrbitalPerturbationsParameters(self) -> None:
        """Saves the orbital perturbations parameters
        """
        
        OrbitalPerturbations.setCelestialBody(CelestialBody.EARTH)
        
        y_0 = np.array([self._angular_momentum, self._eccentricity, self._true_anomaly, self._right_ascension_ascending_node, self._inclination, self._periapsis_anomaly])
        
        start_date = datetime.strptime(self._start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(self._end_date, '%Y-%m-%d %H:%M:%S')
        
        JD_0 = OrbitDetermination.JulianDay(start_date.year, start_date.month, start_date.day, start_date.hour, start_date.minute, start_date.second)
        JD_f = OrbitDetermination.JulianDay(end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second)
        
        y = OrbitalPerturbations.integrateGaussVariationalEquations(y_0,
                                                                    drag=self._drag,
                                                                    gravitational=self._gravitational,
                                                                    SRP=self._srp,
                                                                    B=self._drag_ballistic_coefficient,
                                                                    B_SRP=self._srp_ballistic_coefficient,
                                                                    MOON=self._third_body and self._third_body_choice == 0,
                                                                    SUN=self._third_body and self._third_body_choice == 1,
                                                                    JD_0=JD_0 * 86400,
                                                                    JD_f=JD_f * 86400)
        
        self.plotOrbitalPerturbations(y)
    
    # ! PRIVATE
    
    def plotOrbitalPerturbations(self, y : np.ndarray) -> None:
        """Plots the orbital perturbations

        Args:
            y (np.ndarray): Integration vector [t, a, e, i, Omega, omega, h]
        """
        
        self.figure_orbit_propagation.resetCanvas()
        
        self.figure_orbit_propagation.figure.suptitle('Orbital Perturbations', fontsize=16)
        
        self.figure_orbit_propagation.axes[0][0].plot(y['t'], y['a'] - y['a'][0])
        self.figure_orbit_propagation.axes[0][0].set_title('$a - a_0$ [$km$]')
        self.figure_orbit_propagation.axes[0][0].grid(True)
        
        self.figure_orbit_propagation.axes[0][1].plot(y['t'], y['e'] - y['e'][0])
        self.figure_orbit_propagation.axes[0][1].set_title('$e - e_0$')
        self.figure_orbit_propagation.axes[0][1].grid(True)
        
        self.figure_orbit_propagation.axes[0][2].plot(y['t'], y['h'] - y['h'][0])
        self.figure_orbit_propagation.axes[0][2].set_title('$h - h_0$ [$km^2 / s$]')
        self.figure_orbit_propagation.axes[0][2].grid(True)
        
        self.figure_orbit_propagation.axes[1][0].plot(y['t'], y['i'] - y['i'][0])
        self.figure_orbit_propagation.axes[1][0].set_title('$i - i_0$ [deg]')
        self.figure_orbit_propagation.axes[1][0].set_xlabel('Time [days]')
        self.figure_orbit_propagation.axes[1][0].grid(True)
        
        self.figure_orbit_propagation.axes[1][1].plot(y['t'], y['Omega'] - y['Omega'][0])
        self.figure_orbit_propagation.axes[1][1].set_title('$\Omega - \Omega_0$ [deg]')
        self.figure_orbit_propagation.axes[1][1].set_xlabel('Time [days]')
        self.figure_orbit_propagation.axes[1][1].grid(True)
        
        self.figure_orbit_propagation.axes[1][2].plot(y['t'], y['omega'] - y['omega'][0])
        self.figure_orbit_propagation.axes[1][2].set_title('$\omega - \omega_0$ [deg]')
        self.figure_orbit_propagation.axes[1][2].set_xlabel('Time [days]')
        self.figure_orbit_propagation.axes[1][2].grid(True)

        self.figure_orbit_propagation.redrawCanvas()