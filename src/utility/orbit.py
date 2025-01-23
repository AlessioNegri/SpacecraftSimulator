""" orbit.py: Generic orbit for QML """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import numpy as np

from enum import IntEnum

from src.common import format

from tools.AstronomicalData import CelestialBody, celestial_body_from_index
from tools.TwoBodyProblem import OrbitalParameters
from tools.ThreeDimensionalOrbit import OrbitalElements

# --- ENUM 

class StateType(IntEnum):
    """List of state selection type"""
    
    CARTESIAN           = 0
    KEPLERIAN           = 1
    MODIFIED_KEPLERIAN  = 2

# --- CLASS 

class Orbit(qtCore.QObject):
    """This class describes the properties and parameters of an Orbit"""
    
    # --- PROPERTIES 
    
    # ? Body
    
    body_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=body_changed)
    def body(self): return self._body

    @body.setter
    def body(self, val : int): self._body = val; self.body_changed.emit()
    
    # ? State
    
    state_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=state_changed)
    def state(self): return self._state

    @state.setter
    def state(self, val : int): self._state = val; self.state_changed.emit()
    
    # ? R_X [km]
    
    r_x_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=r_x_changed)
    def r_x(self): return format(self._r_x)

    @r_x.setter
    def r_x(self, val : float): self._r_x = val; self.r_x_changed.emit()
    
    # ? R_Y [km]
    
    r_y_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=r_y_changed)
    def r_y(self): return format(self._r_y)

    @r_y.setter
    def r_y(self, val : float): self._r_y = val; self.r_y_changed.emit()
    
    # ? R_Z [km]
    
    r_z_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=r_z_changed)
    def r_z(self): return format(self._r_z)

    @r_z.setter
    def r_z(self, val : float): self._r_z = val; self.r_z_changed.emit()
    
    # ? V_X [km / s]
    
    v_x_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=v_x_changed)
    def v_x(self): return format(self._v_x)

    @v_x.setter
    def v_x(self, val : float): self._v_x = val; self.v_x_changed.emit()
    
    # ? V_Y [km / s]
    
    v_y_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=v_y_changed)
    def v_y(self): return format(self._v_y)

    @v_y.setter
    def v_y(self, val : float): self._v_y = val; self.v_y_changed.emit()
    
    # ? V_Z [km / s]
    
    v_z_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=v_z_changed)
    def v_z(self): return format(self._v_z)

    @v_z.setter
    def v_z(self, val : float): self._v_z = val; self.v_z_changed.emit()
    
    # ? Specific Angular Momentum [km^2 / s]
    
    specific_angular_momentum_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=specific_angular_momentum_changed)
    def specific_angular_momentum(self): return format(self._specific_angular_momentum)

    @specific_angular_momentum.setter
    def specific_angular_momentum(self, val : float): self._specific_angular_momentum = val; self.specific_angular_momentum_changed.emit()
    
    # ? Semi Major Axis [km]
    
    semi_major_axis_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=semi_major_axis_changed)
    def semi_major_axis(self): return format(self._semi_major_axis)

    @semi_major_axis.setter
    def semi_major_axis(self, val : float): self._semi_major_axis = val; self.semi_major_axis_changed.emit()
    
    # ? Eccentricity
    
    eccentricity_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=eccentricity_changed)
    def eccentricity(self): return format(self._eccentricity)

    @eccentricity.setter
    def eccentricity(self, val : float): self._eccentricity = val; self.eccentricity_changed.emit()
    
    # ? Inclination [rad]
    
    inclination_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=inclination_changed)
    def inclination(self): return format(self._inclination, deg=True)

    @inclination.setter
    def inclination(self, val : float): self._inclination = np.deg2rad(val); self.inclination_changed.emit()
    
    # ? Right Ascension Ascending Node [rad]
    
    right_ascension_ascending_node_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=right_ascension_ascending_node_changed)
    def right_ascension_ascending_node(self): return format(self._right_ascension_ascending_node, deg=True)

    @right_ascension_ascending_node.setter
    def right_ascension_ascending_node(self, val : float): self._right_ascension_ascending_node = np.deg2rad(val); self.right_ascension_ascending_node_changed.emit()
    
    # ? Periapsis Anomaly [rad]
    
    periapsis_anomaly_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=periapsis_anomaly_changed)
    def periapsis_anomaly(self): return format(self._periapsis_anomaly, deg=True)

    @periapsis_anomaly.setter
    def periapsis_anomaly(self, val : float): self._periapsis_anomaly = np.deg2rad(val); self.periapsis_anomaly_changed.emit()
    
    # ? True Anomaly [rad]
    
    true_anomaly_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=true_anomaly_changed)
    def true_anomaly(self): return format(self._true_anomaly, deg=True)

    @true_anomaly.setter
    def true_anomaly(self, val : float): self._true_anomaly = np.deg2rad(val); self.true_anomaly_changed.emit()
    
    # ? Periapsis Radius [km]
    
    periapsis_radius_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=periapsis_radius_changed)
    def periapsis_radius(self): return format(self._periapsis_radius)

    @periapsis_radius.setter
    def periapsis_radius(self, val : float): self._periapsis_radius = val; self.periapsis_radius_changed.emit()
    
    # ? Apoapsis Radius [km]
    
    apoapsis_radius_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=apoapsis_radius_changed)
    def apoapsis_radius(self): return format(self._apoapsis_radius)

    @apoapsis_radius.setter
    def apoapsis_radius(self, val : float): self._apoapsis_radius = val; self.apoapsis_radius_changed.emit()
    
    # --- METHODS 
    
    def __init__(self) -> None:
        """Constructor
        """
        
        qtCore.QObject.__init__(self)
        
        self._body                              : int = 0                   # * Celestial body                                                  [ ]
        self._state                             : int = StateType.CARTESIAN # * Selected state among CARTESIAN - KEPLERIAN - MODIFIED_KEPLERIAN [ ]
        self._r_x                               : float = 0.0               # * Position vector component x                                     [ km ]
        self._r_y                               : float = 0.0               # * Position vector component y                                     [ km ]
        self._r_z                               : float = 0.0               # * Position vector component z                                     [ km ]
        self._v_x                               : float = 0.0               # * Velocity vector component x                                     [ km / s ]
        self._v_y                               : float = 0.0               # * Velocity vector component y                                     [ km / s ]
        self._v_z                               : float = 0.0               # * Velocity vector component z                                     [ km / s ]
        self._specific_angular_momentum         : float = 0.0               # * Specific angular momentum                                       [ km^2 / s ]
        self._semi_major_axis                   : float = 0.0               # * Semi-major axis                                                 [ km ]
        self._eccentricity                      : float = 0.0               # * Eccentricity                                                    [ ]
        self._inclination                       : float = 0.0               # * Inclination                                                     [ rad ]
        self._right_ascension_ascending_node    : float = 0.0               # * Right Ascension of the Ascending Node (RAAN)                    [ rad ]
        self._periapsis_anomaly                 : float = 0.0               # * Periapsis anomaly                                               [ rad ]
        self._true_anomaly                      : float = 0.0               # * True anomaly                                                    [ rad ]
        self._periapsis_radius                  : float = 0.0               # * Periapsis radius                                                [ km ]
        self._apoapsis_radius                   : float = 0.0               # * Apoapsis radius                                                 [ km ]

    def get_celestial_body(self) -> CelestialBody:
        """Retrieves the celestial body

        Returns:
            CelestialBody: Celestial body
        """
        
        return celestial_body_from_index(self._body)

    def get_cartesian_parameters(self) -> list:
        """Retrieves the Cartesian parameters

        Returns:
            list: [ Position Vector, Velocity Vector ]
        """
        
        return [np.array([self._r_x, self._r_y, self._r_z]), np.array([self._v_x, self._v_y, self._v_z])]
    
    def get_keplerian_parameters(self) -> OrbitalElements:
        """Retrieves the Keplerian parameters

        Returns:
            OrbitalElements: Orbital elements
        """
        
        return OrbitalElements(self._specific_angular_momentum, self._eccentricity, self._inclination, self._right_ascension_ascending_node, self._periapsis_anomaly, self._true_anomaly, self._semi_major_axis)
    
    def update_central_body(self, body : int) -> None:
        """Updates the central body

        Args:
            body (int): Central body
        """
        
        self.body = body
        
    def update_state(self, state : int) -> None:
        """Updates the parameters selection state

        Args:
            state (int): State
        """
        
        self.state = state
    
    def update_cartesian_parameters(self, r : np.ndarray, v : np.ndarray) -> None:
        """Updates the Cartesian parameters

        Args:
            r (np.ndarray): Position vector (3, 1) [km]
            v (np.ndarray): Velocity vector (3, 1) [km / s]
        """
        
        self.r_x = r[0]
        self.r_y = r[1]
        self.r_z = r[2]
        self.v_x = v[0]
        self.v_y = v[1]
        self.v_z = v[2]
    
    def update_keplerian_parameters(self, orbital_elements : OrbitalElements) -> None:
        """Updates the Keplerian parameters

        Args:
            orbital_elements (OrbitalElements): Orbital elements
        """
        
        self._specific_angular_momentum     = orbital_elements.h
        self.semi_major_axis                = orbital_elements.a
        self.eccentricity                   = orbital_elements.e
        self.inclination                    = np.rad2deg(orbital_elements.i)
        self.right_ascension_ascending_node = np.rad2deg(orbital_elements.Omega)
        self.periapsis_anomaly              = np.rad2deg(orbital_elements.omega)
        self.true_anomaly                   = np.rad2deg(orbital_elements.theta)
    
    def update_keplerian_parameters_from_radii(self) -> None:
        """Updates the Keplerian parameters from the periapsis and apoapsis radii
        """
        
        self.semi_major_axis    = (self._periapsis_radius + self._apoapsis_radius) / 2
        self.eccentricity       = (self._apoapsis_radius - self._periapsis_radius) / (self._apoapsis_radius + self._periapsis_radius)
    
    def update_modified_keplerian_parameters(self, orbital_elements : OrbitalElements, orbital_parameters : OrbitalParameters) -> None:
        """Updates the Keplerian parameters

        Args:
            orbital_elements (OrbitalElements): Orbital elements
            orbital_parameters (OrbitalParameters): Orbital parameters
        """
        
        self.specific_angular_momentum      = orbital_elements.h
        self.semi_major_axis                = orbital_elements.a
        self.eccentricity                   = orbital_elements.e
        self.inclination                    = np.rad2deg(orbital_elements.i)
        self.right_ascension_ascending_node = np.rad2deg(orbital_elements.Omega)
        self.periapsis_anomaly              = np.rad2deg(orbital_elements.omega)
        self.true_anomaly                   = np.rad2deg(orbital_elements.theta)
        self.periapsis_radius               = orbital_parameters.r_p
        self.apoapsis_radius                = orbital_parameters.r_a