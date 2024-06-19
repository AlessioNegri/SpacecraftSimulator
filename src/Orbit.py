import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np

from Utility import format, singleton
from tools.ThreeDimensionalOrbit import ORBITAL_ELEMENTS, ORBITAL_PARAMETERS

@singleton
class Orbit(qtCore.QObject):
    """This class describes the properties and parameters of an Orbit
    """
    
    # ! PROPERTIES
    
    # ? Body
    
    body_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=body_changed)
    def body(self): return self._body

    @body.setter
    def body(self, val : int): self._body = val
    
    # ? State
    
    state_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=state_changed)
    def state(self): return self._state

    @state.setter
    def state(self, val : int): self._state = val
    
    # ? R_X [km]
    
    r_x_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=r_x_changed)
    def r_x(self): return format(self._r_x)

    @r_x.setter
    def r_x(self, val : float): self._r_x = val
    
    # ? R_Y [km]
    
    r_y_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=r_y_changed)
    def r_y(self): return format(self._r_y)

    @r_y.setter
    def r_y(self, val : float): self._r_y = val
    
    # ? R_Z [km]
    
    r_z_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=r_z_changed)
    def r_z(self): return format(self._r_z)

    @r_z.setter
    def r_z(self, val : float): self._r_z = val
    
    # ? V_X [km / s]
    
    v_x_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=v_x_changed)
    def v_x(self): return format(self._v_x)

    @v_x.setter
    def v_x(self, val : float): self._v_x = val
    
    # ? V_Y [km / s]
    
    v_y_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=v_y_changed)
    def v_y(self): return format(self._v_y)

    @v_y.setter
    def v_y(self, val : float): self._v_y = val
    
    # ? V_Z [km / s]
    
    v_z_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=v_z_changed)
    def v_z(self): return format(self._v_z)

    @v_z.setter
    def v_z(self, val : float): self._v_z = val
    
    # ? Semi Major Axis [km]
    
    semi_major_axis_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=semi_major_axis_changed)
    def semi_major_axis(self): return format(self._semi_major_axis)

    @semi_major_axis.setter
    def semi_major_axis(self, val : float): self._semi_major_axis = val
    
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
    
    # ? Periapsis Radius [km]
    
    periapsis_radius_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=periapsis_radius_changed)
    def periapsis_radius(self): return format(self._periapsis_radius)

    @periapsis_radius.setter
    def periapsis_radius(self, val : float): self._periapsis_radius = val
    
    # ? Apoapsis Radius [km]
    
    apoapsis_radius_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=apoapsis_radius_changed)
    def apoapsis_radius(self): return format(self._apoapsis_radius)

    @apoapsis_radius.setter
    def apoapsis_radius(self, val : float): self._apoapsis_radius = val
    
    # ! CONSTRUCTOR
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__Orbit", self)
        
        self._body                              : int = 0
        self._state                             : int = 0
        self._r_x                               : float = 0.0
        self._r_y                               : float = 0.0
        self._r_z                               : float = 0.0
        self._v_x                               : float = 0.0
        self._v_y                               : float = 0.0
        self._v_z                               : float = 0.0
        self._semi_major_axis                   : float = 0.0
        self._eccentricity                      : float = 0.0
        self._inclination                       : float = 0.0
        self._right_ascension_ascending_node    : float = 0.0
        self._periapsis_anomaly                 : float = 0.0
        self._true_anomaly                      : float = 0.0
        self._periapsis_radius                  : float = 0.0
        self._apoapsis_radius                   : float = 0.0
    
    # ! METHODS
    
    def getKeplerianParameters(self) -> ORBITAL_ELEMENTS:
        """Retrieves the Keplerian parameters

        Returns:
            ORBITAL_ELEMENTS: Orbital elements
        """
        
        return ORBITAL_ELEMENTS(0, self._eccentricity, self._inclination, self._right_ascension_ascending_node, self._periapsis_anomaly, self._true_anomaly, self._semi_major_axis)
    
    def updateCentralBody(self, body : int) -> None:
        """Updates the central body

        Args:
            body (int): Central body
        """
        
        self._body = body
        
        self.body_changed.emit()
        
    def updateState(self, state : int) -> None:
        """Updates the parameters selection state

        Args:
            state (int): State
        """
        
        self._state = state
        
        self.state_changed.emit()
    
    def updateCartesianParameters(self, r : np.ndarray, v : np.ndarray) -> None:
        """Updates the Cartesian parameters

        Args:
            r (np.ndarray): Position vector (3, 1) [km]
            v (np.ndarray): Velocity vector (3, 1) [km / s]
        """
        
        self._r_x = r[0]
        self._r_y = r[1]
        self._r_z = r[2]
        self._v_x = v[0]
        self._v_y = v[1]
        self._v_z = v[2]
        
        self.r_x_changed.emit()
        self.r_y_changed.emit()
        self.r_z_changed.emit()
        self.v_x_changed.emit()
        self.v_y_changed.emit()
        self.v_z_changed.emit()
    
    def updateKeplerianParameters(self, orbital_elements : ORBITAL_ELEMENTS) -> None:
        """Updates the Keplerian parameters

        Args:
            orbital_elements (ORBITAL_ELEMENTS): Orbital elements
        """
        
        self._semi_major_axis                   = orbital_elements.a
        self._eccentricity                      = orbital_elements.e
        self._inclination                       = orbital_elements.i
        self._right_ascension_ascending_node    = orbital_elements.Omega
        self._periapsis_anomaly                 = orbital_elements.omega
        self._true_anomaly                      = orbital_elements.theta
        
        self.semi_major_axis_changed.emit()
        self.eccentricity_changed.emit()
        self.inclination_changed.emit()
        self.right_ascension_ascending_node_changed.emit()
        self.periapsis_anomaly_changed.emit()
        self.true_anomaly_changed.emit()
    
    def updateKeplerianParametersFromRadii(self) -> None:
        """Updates the Keplerian parameters from the periapsis and apoapsis radii
        """
        
        self._semi_major_axis   = (self._periapsis_radius + self._apoapsis_radius) / 2
        self._eccentricity      = (self._apoapsis_radius - self._periapsis_radius) / (self._apoapsis_radius + self._periapsis_radius)
        
        self.semi_major_axis_changed.emit()
        self.eccentricity_changed.emit()
    
    def updateModifiedKeplerianParameters(self, orbital_elements : ORBITAL_ELEMENTS, orbital_parameters : ORBITAL_PARAMETERS) -> None:
        """Updates the Keplerian parameters

        Args:
            orbital_elements (ORBITAL_ELEMENTS): Orbital elements
            orbital_parameters (ORBITAL_PARAMETERS): Orbital parameters
        """
        
        self._semi_major_axis                   = orbital_elements.a
        self._eccentricity                      = orbital_elements.e
        self._inclination                       = orbital_elements.i
        self._right_ascension_ascending_node    = orbital_elements.Omega
        self._periapsis_anomaly                 = orbital_elements.omega
        self._true_anomaly                      = orbital_elements.theta
        self._periapsis_radius                  = orbital_parameters.r_p
        self._apoapsis_radius                   = orbital_parameters.r_a
        
        self.semi_major_axis_changed.emit()
        self.eccentricity_changed.emit()
        self.inclination_changed.emit()
        self.right_ascension_ascending_node_changed.emit()
        self.periapsis_anomaly_changed.emit()
        self.true_anomaly_changed.emit()
        self.periapsis_radius_changed.emit()
        self.apoapsis_radius_changed.emit()