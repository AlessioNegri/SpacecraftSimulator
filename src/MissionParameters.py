import os
import sys
import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml

sys.path.append(os.path.dirname(__file__))

from Utility import format
from FigureCanvas import FigureCanvas
from Maneuver import Maneuver, ManeuverType

from tools.ThreeDimensionalOrbit import *
from tools.OrbitalManeuvers import *

class StateType(IntEnum):
    
    CARTESIAN           = 0
    KEPLERIAN           = 1
    MODIFIED_KEPLERIAN  = 2

class MissionParameters(qtCore.QObject):
    """Class that manages the mission parameters
    """
    
    # ! PROPERTIES
    
    body_changed    = qtCore.Signal()
    state_changed   = qtCore.Signal()
    x_changed       = qtCore.Signal()
    y_changed       = qtCore.Signal()
    z_changed       = qtCore.Signal()
    v_x_changed     = qtCore.Signal()
    v_y_changed     = qtCore.Signal()
    v_z_changed     = qtCore.Signal()
    a_changed       = qtCore.Signal()
    e_changed       = qtCore.Signal()
    i_changed       = qtCore.Signal()
    Omega_changed   = qtCore.Signal()
    omega_changed   = qtCore.Signal()
    theta_changed   = qtCore.Signal()
    r_p_changed     = qtCore.Signal()
    r_a_changed     = qtCore.Signal()
    m_0_changed     = qtCore.Signal()
    I_sp_changed    = qtCore.Signal()
    T_changed       = qtCore.Signal()
    
    def get_body(self):     return self._body
    def get_state(self):    return self._state
    def get_x(self):        return format(self._x)
    def get_y(self):        return format(self._y)
    def get_z(self):        return format(self._z)
    def get_v_x(self):      return format(self._v_x)
    def get_v_y(self):      return format(self._v_y)
    def get_v_z(self):      return format(self._v_z)
    def get_a(self):        return format(self._a)
    def get_e(self):        return format(self._e)
    def get_i(self):        return format(self._i, deg=True)
    def get_Omega(self):    return format(self._Omega, deg=True)
    def get_omega(self):    return format(self._omega, deg=True)
    def get_theta(self):    return format(self._theta, deg=True)
    def get_r_p(self):      return format(self._r_p)
    def get_r_a(self):      return format(self._r_a)
    def get_m_0(self):      return format(self._m_0)
    def get_I_sp(self):     return format(self._I_sp)
    def get_T(self):        return format(self._T)

    def set_body(self, body : int):     self._body = body; self.body_changed.emit()
    def set_state(self, state : int):   self._state = state; self.state_changed.emit()
    def set_x(self, x : float):         self._x = x; self.x_changed.emit()
    def set_y(self, y : float):         self._y = y; self.y_changed.emit()
    def set_z(self, z : float):         self._z = z; self.z_changed.emit()
    def set_v_x(self, v_x : float):     self._v_x = v_x; self.v_x_changed.emit()
    def set_v_y(self, v_y : float):     self._v_y = v_y; self.v_y_changed.emit()
    def set_v_z(self, v_z : float):     self._v_z = v_z; self.v_z_changed.emit()
    def set_a(self, a : float):         self._a = a; self.a_changed.emit()
    def set_e(self, e : float):         self._e = e; self.e_changed.emit()
    def set_i(self, i : float):         self._i = i; self.i_changed.emit()
    def set_Omega(self, Omega : float): self._Omega = Omega; self.Omega_changed.emit()
    def set_omega(self, omega : float): self._omega = omega; self.omega_changed.emit()
    def set_theta(self, theta : float): self._theta = theta; self.theta_changed.emit()
    def set_r_p(self, r_p : float):     self._r_p = r_p; self.r_p_changed.emit()
    def set_r_a(self, r_a : float):     self._r_a = r_a; self.r_a_changed.emit()
    def set_m_0(self, m_0 : float):     self._m_0 = m_0; self.m_0_changed.emit()
    def set_I_sp(self, I_sp : float):   self._I_sp = I_sp; self.I_sp_changed.emit()
    def set_T(self, T : float):         self._T = T; self.T_changed.emit()
    
    body    = qtCore.Property(int, get_body, set_body, notify=body_changed)
    state   = qtCore.Property(int, get_state, set_state, notify=state_changed)
    x       = qtCore.Property(float, get_x, set_x, notify=x_changed)
    y       = qtCore.Property(float, get_y, set_y, notify=y_changed)
    z       = qtCore.Property(float, get_z, set_z, notify=z_changed)
    v_x     = qtCore.Property(float, get_v_x, set_v_x, notify=v_x_changed)
    v_y     = qtCore.Property(float, get_v_y, set_v_y, notify=v_y_changed)
    v_z     = qtCore.Property(float, get_v_z, set_v_z, notify=v_z_changed)
    a       = qtCore.Property(float, get_a, set_a, notify=a_changed)
    e       = qtCore.Property(float, get_e, set_e, notify=e_changed)
    i       = qtCore.Property(float, get_i, set_i, notify=i_changed)
    Omega   = qtCore.Property(float, get_Omega, set_Omega, notify=Omega_changed)
    omega   = qtCore.Property(float, get_omega, set_omega, notify=omega_changed)
    theta   = qtCore.Property(float, get_theta, set_theta, notify=theta_changed)
    r_p     = qtCore.Property(float, get_r_p, set_r_p, notify=r_p_changed)
    r_a     = qtCore.Property(float, get_r_a, set_r_a, notify=r_a_changed)
    m_0     = qtCore.Property(float, get_m_0, set_m_0, notify=m_0_changed)
    I_sp    = qtCore.Property(float, get_I_sp, set_I_sp, notify=I_sp_changed)
    T       = qtCore.Property(float, get_T, set_T, notify=T_changed)
    
    # ! METHODS

    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        # * QML properties
        
        self._body  = 0
        self._state = 0
        self._x     = 0
        self._y     = 0
        self._z     = 0
        self._v_x   = 0
        self._v_y   = 0
        self._v_z   = 0
        self._a     = 0.0
        self._e     = 0.0
        self._i     = 0.0
        self._Omega = 0.0
        self._omega = 0.0
        self._theta = 0.0
        self._r_p   = 0.0
        self._r_a   = 0.0
        self._m_0   = 2000
        self._I_sp  = 300
        self._T     = 10e3
        
        # * Departure parameters
        
        self.body_dep                   = CelestialBody.EARTH
        self.state_dep                  = StateType.CARTESIAN
        self.r_dep                      = np.array([-8173.55640, -3064.65060, -2840.15350], dtype=float)
        self.v_dep                      = np.array([-3.07330000, 5.94440000, -1.54740000], dtype=float)
        self.parameters_dep             = ORBITAL_PARAMETERS()
        self.oe_dep                     = ORBITAL_ELEMENTS()
        self.orbit_figure_dep           = FigureCanvas()
        self.ground_track_figure_dep    = FigureCanvas()
        
        # * Arrival parameters
        
        self.body_arr                   = CelestialBody.EARTH
        self.state_arr                  = StateType.CARTESIAN
        self.r_arr                      = np.array([4571.13653, 32940.33361, -14208.95231], dtype=float)
        self.v_arr                      = np.array([-3.06192709, 1.01383552, 0.41402772], dtype=float)
        self.parameters_arr             = ORBITAL_PARAMETERS()
        self.oe_dep                     = ORBITAL_ELEMENTS()
        self.orbit_figure_arr           = FigureCanvas()
        self.ground_track_figure_arr    = FigureCanvas()
        
        # * Orbit Transfer
        
        self.parameters_tra             = ORBITAL_PARAMETERS()
        self.oe_tra                     = ORBITAL_ELEMENTS()
        self.orbit_transfer_figure      = FigureCanvas()
        
        # * Context properties
        
        engine.rootContext().setContextProperty("__DepartureOrbitFigure", self.orbit_figure_dep)
        engine.rootContext().setContextProperty("__DepartureGroundTrackFigure", self.ground_track_figure_dep)
        engine.rootContext().setContextProperty("__ArrivalOrbitFigure", self.orbit_figure_arr)
        engine.rootContext().setContextProperty("__ArrivalGroundTrackFigure", self.ground_track_figure_arr)
        engine.rootContext().setContextProperty("__OrbitTransferFigure", self.orbit_transfer_figure)
        
        # * Init
        
        self.maneuvers = list()
        
        self.loadDepartureOrbit()
        self.loadArrivalOrbit()
        self.loadSpacecraftProperties()
        self.loadManeuvers()
    
    def setUpdateWithCanvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Connects all the QML figures with the backend model

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        win = engine.rootObjects()[0]
        
        self.orbit_figure_dep.updateWithCanvas(win.findChild(qtCore.QObject, "DepartureOrbitFigure"), win.findChild(qtCore.QObject, "DepartureOrbitFigureParent"), dof3=True, figsize=(8, 6))
        self.ground_track_figure_dep.updateWithCanvas(win.findChild(qtCore.QObject, "DepartureGroundTrackFigure"), win.findChild(qtCore.QObject, "DepartureGroundTrackFigureParent"), figsize=(4, 2))
        self.orbit_figure_arr.updateWithCanvas(win.findChild(qtCore.QObject, "ArrivalOrbitFigure"), win.findChild(qtCore.QObject, "ArrivalOrbitFigureParent"), dof3=True, figsize=(8, 6))
        self.ground_track_figure_arr.updateWithCanvas(win.findChild(qtCore.QObject, "ArrivalGroundTrackFigure"), win.findChild(qtCore.QObject, "ArrivalGroundTrackFigureParent"), figsize=(8, 6))
        self.orbit_transfer_figure.updateWithCanvas(win.findChild(qtCore.QObject, "OrbitTransferFigure"), win.findChild(qtCore.QObject, "OrbitTransferFigureParent"), dof3=True)
        
        self.orbit_transfer_figure.figure.tight_layout()
        self.orbit_transfer_figure.axes.set_aspect('equal', adjustable='box')
    
    # ! SLOTS
    
    # ? Departure Orbit
    
    @qtCore.Slot()
    def loadDepartureOrbit(self) -> None:
        """Loads the departure orbit parameters
        """
        
        self.set_body(indexFromCelestialBody(self.body_dep))
        
        ThreeDimensionalOrbit.setCelestialBody(self.body_dep)
        TwoBodyProblem.setCelestialBody(self.body_dep)
        
        self.set_x(self.r_dep[0])
        self.set_y(self.r_dep[1])
        self.set_z(self.r_dep[2])
        
        self.set_v_x(self.v_dep[0])
        self.set_v_y(self.v_dep[1])
        self.set_v_z(self.v_dep[2])
        
        self.oe_dep = ThreeDimensionalOrbit.calculateOrbitalElements(self.r_dep, self.v_dep)
        
        self.set_a(self.oe_dep.a)
        self.set_e(self.oe_dep.e)
        self.set_i(self.oe_dep.i)
        self.set_Omega(self.oe_dep.Omega)
        self.set_omega(self.oe_dep.omega)
        self.set_theta(self.oe_dep.theta)
        
        self.parameters_dep = TwoBodyProblem.calculateOrbitalParameters(self.r_dep, self.v_dep)
        
        self.set_r_p(self.parameters_dep.r_p)
        self.set_r_a(self.parameters_dep.r_a)
    
    @qtCore.Slot()
    def updateDepartureOrbit(self) -> None:
        """Updates the departure orbit parameters
        """
        
        self.body_dep = celestialBodyFromIndex(self._body)
        
        self.state_dep = self._state
        
        ThreeDimensionalOrbit.setCelestialBody(self.body_dep)
        TwoBodyProblem.setCelestialBody(self.body_dep)
        
        match self.state_dep:
            
            case StateType.CARTESIAN:
                
                self.r_dep = np.array([self._x, self._y, self._z])
                self.v_dep = np.array([self._v_x, self._v_y, self._v_z])
        
                self.oe_dep = ThreeDimensionalOrbit.calculateOrbitalElements(self.r_dep, self.v_dep)
        
                self.set_a(self.oe_dep.a)
                self.set_e(self.oe_dep.e)
                self.set_i(self.oe_dep.i)
                self.set_Omega(self.oe_dep.Omega)
                self.set_omega(self.oe_dep.omega)
                self.set_theta(self.oe_dep.theta)
                
                self.parameters_dep = TwoBodyProblem.calculateOrbitalParameters(self.r_dep, self.v_dep)
                
                self.set_r_p(self.parameters_dep.r_p)
                self.set_r_a(self.parameters_dep.r_a)
            
            case StateType.KEPLERIAN:
                
                self.set_i(np.deg2rad(self._i))
                self.set_Omega(np.deg2rad(self._Omega))
                self.set_omega(np.deg2rad(self._omega))
                self.set_theta(np.deg2rad(self._theta))
                
                self.oe_dep = ORBITAL_ELEMENTS(0, self._e, self._i, self._Omega, self._omega, self._theta, self._a)
                
                self.r_dep, self.v_dep = ThreeDimensionalOrbit.PF2GEF(self.oe_dep)
                
                self.set_x(self.r_dep[0])
                self.set_y(self.r_dep[1])
                self.set_z(self.r_dep[2])
                
                self.set_v_x(self.v_dep[0])
                self.set_v_y(self.v_dep[1])
                self.set_v_z(self.v_dep[2])
                
                self.parameters_dep = TwoBodyProblem.calculateOrbitalParameters(self.r_dep, self.v_dep)
                
                self.set_r_p(self.parameters_dep.r_p)
                self.set_r_a(self.parameters_dep.r_a)
            
            case StateType.MODIFIED_KEPLERIAN:
                
                self.set_i(np.deg2rad(self._i))
                self.set_Omega(np.deg2rad(self._Omega))
                self.set_omega(np.deg2rad(self._omega))
                self.set_theta(np.deg2rad(self._theta))
                
                self.set_a((self._r_p + self._r_a) / 2)
                
                self.set_e((self._r_a - self._r_p) / (self._r_a + self._r_p))
                
                self.oe_dep = ORBITAL_ELEMENTS(0, self._e, self._i, self._Omega, self._omega, self._theta, self._a)
                
                self.r_dep, self.v_dep = ThreeDimensionalOrbit.PF2GEF(self.oe_dep)
                
                self.set_x(self.r_dep[0])
                self.set_y(self.r_dep[1])
                self.set_z(self.r_dep[2])
                
                self.set_v_x(self.v_dep[0])
                self.set_v_y(self.v_dep[1])
                self.set_v_z(self.v_dep[2])
            
            case _:
                
                pass
    
    @qtCore.Slot()
    def evaluateDepartureOrbit(self):
        """Integrates the equations of the departure orbit and the ground track
        """
        
        ThreeDimensionalOrbit.setCelestialBody(self.body_dep)
        TwoBodyProblem.setCelestialBody(self.body_dep)
        
        result = TwoBodyProblem.integrateRelativeMotion(np.hstack([self.r_dep, self.v_dep]))
        
        self.plotOrbit(self.orbit_figure_dep, self.body_dep, result)
        
        ra, dec = ThreeDimensionalOrbit.calculateGroundTrack(self.oe_dep, 60)
        
        if len(ra) == 0 or len(dec) == 0:
            
            ra_0, dec_0 = ThreeDimensionalOrbit.calculateRaDec(self.r_dep)
            
            ra = [ra_0]
            dec = [dec_0]
        
        self.plotGroundTrack(self.ground_track_figure_dep, self.body_dep, ra, dec)
    
    @qtCore.Slot()
    def saveDepartureOrbit(self) -> None:
        """Updates the departure orbit parameters and plot
        """
        
        self.updateDepartureOrbit()
        
        self.evaluateDepartureOrbit()
    
    # ? Arrival Orbit
    
    @qtCore.Slot()
    def loadArrivalOrbit(self) -> None:
        """Loads the arrival orbit parameters
        """
        
        self.set_body(indexFromCelestialBody(self.body_arr))
        
        ThreeDimensionalOrbit.setCelestialBody(self.body_arr)
        TwoBodyProblem.setCelestialBody(self.body_arr)
        
        self.set_x(self.r_arr[0])
        self.set_y(self.r_arr[1])
        self.set_z(self.r_arr[2])
        
        self.set_v_x(self.v_arr[0])
        self.set_v_y(self.v_arr[1])
        self.set_v_z(self.v_arr[2])
        
        self.oe_arr = ThreeDimensionalOrbit.calculateOrbitalElements(self.r_arr, self.v_arr)
        
        self.set_a(self.oe_arr.a)
        self.set_e(self.oe_arr.e)
        self.set_i(self.oe_arr.i)
        self.set_Omega(self.oe_arr.Omega)
        self.set_omega(self.oe_arr.omega)
        self.set_theta(self.oe_arr.theta)
        
        self.parameters_arr = TwoBodyProblem.calculateOrbitalParameters(self.r_arr, self.v_arr)
        
        self.set_r_p(self.parameters_arr.r_p)
        self.set_r_a(self.parameters_arr.r_a)
    
    @qtCore.Slot()
    def updateArrivalOrbit(self) -> None:
        """Updates the arrival orbit parameters
        """
        
        self.body_arr = celestialBodyFromIndex(self._body)
        
        self.state_arr = self._state
        
        ThreeDimensionalOrbit.setCelestialBody(self.body_arr)
        TwoBodyProblem.setCelestialBody(self.body_arr)
        
        match self.state_arr:
            
            case StateType.CARTESIAN:
                
                self.r_arr = np.array([self._x, self._y, self._z])
                self.v_arr = np.array([self._v_x, self._v_y, self._v_z])
        
                self.oe_arr = ThreeDimensionalOrbit.calculateOrbitalElements(self.r_arr, self.v_arr)
        
                self.set_a(self.oe_arr.a)
                self.set_e(self.oe_arr.e)
                self.set_i(self.oe_arr.i)
                self.set_Omega(self.oe_arr.Omega)
                self.set_omega(self.oe_arr.omega)
                self.set_theta(self.oe_arr.theta)
                
                self.parameters_arr = TwoBodyProblem.calculateOrbitalParameters(self.r_arr, self.v_arr)
                
                self.set_r_p(self.parameters_arr.r_p)
                self.set_r_a(self.parameters_arr.r_a)
            
            case StateType.KEPLERIAN:
                
                self.set_i(np.deg2rad(self._i))
                self.set_Omega(np.deg2rad(self._Omega))
                self.set_omega(np.deg2rad(self._omega))
                self.set_theta(np.deg2rad(self._theta))
                
                self.oe_arr = ORBITAL_ELEMENTS(0, self._e, self._i, self._Omega, self._omega, self._theta, self._a)
                
                self.r_arr, self.v_arr = ThreeDimensionalOrbit.PF2GEF(self.oe_arr)
                
                self.set_x(self.r_arr[0])
                self.set_y(self.r_arr[1])
                self.set_z(self.r_arr[2])
                
                self.set_v_x(self.v_arr[0])
                self.set_v_y(self.v_arr[1])
                self.set_v_z(self.v_arr[2])
                
                self.parameters_arr = TwoBodyProblem.calculateOrbitalParameters(self.r_arr, self.v_arr)
                
                self.set_r_p(self.parameters_arr.r_p)
                self.set_r_a(self.parameters_arr.r_a)
            
            case StateType.MODIFIED_KEPLERIAN:
                
                self.set_i(np.deg2rad(self._i))
                self.set_Omega(np.deg2rad(self._Omega))
                self.set_omega(np.deg2rad(self._omega))
                self.set_theta(np.deg2rad(self._theta))
                
                self.set_a((self._r_p + self._r_a) / 2)
                
                self.set_e((self._r_a - self._r_p) / (self._r_a + self._r_p))
                
                self.oe_arr = ORBITAL_ELEMENTS(0, self._e, self._i, self._Omega, self._omega, self._theta, self._a)
                
                self.r_arr, self.v_arr = ThreeDimensionalOrbit.PF2GEF(self.oe_arr)
                
                self.set_x(self.r_arr[0])
                self.set_y(self.r_arr[1])
                self.set_z(self.r_arr[2])
                
                self.set_v_x(self.v_arr[0])
                self.set_v_y(self.v_arr[1])
                self.set_v_z(self.v_arr[2])
            
            case _:
                
                pass
    
    @qtCore.Slot()
    def evaluateArrivalOrbit(self):
        """Integrates the equations of the arrival orbit and the ground track
        """
        
        ThreeDimensionalOrbit.setCelestialBody(self.body_arr)
        TwoBodyProblem.setCelestialBody(self.body_arr)
        
        result = TwoBodyProblem.integrateRelativeMotion(np.hstack([self.r_arr, self.v_arr]))
        
        self.plotOrbit(self.orbit_figure_arr, self.body_arr, result)
        
        ra, dec = ThreeDimensionalOrbit.calculateGroundTrack(self.oe_arr, 60)
        
        if len(ra) == 0 or len(dec) == 0:
            
            ra_0, dec_0 = ThreeDimensionalOrbit.calculateRaDec(self.r_arr)
            
            ra = [ra_0]
            dec = [dec_0]
        
        self.plotGroundTrack(self.ground_track_figure_arr, self.body_arr, ra, dec)
    
    @qtCore.Slot()
    def saveArrivalOrbit(self) -> None:
        """Updates the arrival orbit parameters and plot
        """
        
        self.updateArrivalOrbit()
        
        self.evaluateArrivalOrbit()
    
    # ? Spacecraft Properties
    
    @qtCore.Slot()
    def loadSpacecraftProperties(self) -> None:
        """Loads the spacecraft properties
        """
        
        pass
    
    @qtCore.Slot()
    def saveSpacecraftProperties(self) -> None:
        """Saves the spacecraft properties
        """
        
        pass
    
    # ? Orbit Transfer
    
    @qtCore.Slot(result=int)
    def maneuversCount(self) -> int:
        """Retrieves the number of maneuvers
        """
        
        return len(self.maneuvers)
    
    @qtCore.Slot(int, result=Maneuver)
    def getManeuver(self, index : int) -> Maneuver:
        """Retrieves the maneuver by index

        Args:
            index (int): Index

        Returns:
            Maneuver: Maneuver
        """
        
        return self.maneuvers[index]
    
    @qtCore.Slot()
    def loadManeuvers(self) -> None:
        """Loads the maenuvers
        """
        
        pass
    
    @qtCore.Slot()
    def clearManeuvers(self) -> None:
        """Clears the maenuvers
        """
        
        self.maneuvers.clear()
        
    @qtCore.Slot(int, int, float)
    def addManeuver(self, type : int, option : int, optionValue : float) -> None:
        """Adds a new maenuver

        Args:
            type (int): Maneuver type
            option (int): Maneuver option
            optionValue (float): Maneuver option value
        """
        
        self.maneuvers.append(Maneuver(type, option, optionValue))
    
    @qtCore.Slot()
    def saveManeuvers(self) -> None:
        """Saves the maenuvers
        """
        
        self.plotOrbitTransfer()
    
    # ! PRIVATE
    
    def plotOrbit(self, orbitFigure : FigureCanvas, celestialBody : CelestialBody, result : dict) -> None:
        """Plots the orbit

        Args:
            orbitFigure (FigureCanvas): Figure canvas
            celestialBody (CelestialBody): Celestial body
            result (dict): Dictionary of the integration result { 't': time, 'y': state vector  }
        """
        
        orbitFigure.resetCanvas()
        
        # * Max Values
        
        xMax = 1.25 * max(np.absolute(result['y'][0,:]))
        yMax = 1.25 * max(np.absolute(result['y'][1,:]))
        zMax = 1.25 * max(np.absolute(result['y'][2,:]))
        
        # * Plane
        
        p = mpatches.Rectangle((-xMax, -yMax), 2 * xMax, 2 * yMax, fc=(0,0,0,0.1), ec=(0,0,0,1), lw=2)
        
        orbitFigure.axes.add_patch(p)
        
        art3d.pathpatch_2d_to_3d(p, z=0, zdir='z')
        
        # * Axes
        
        orbitFigure.axes.plot([0, xMax], [0, 0], [0, 0], 'k--')
        orbitFigure.axes.plot([0, 0], [0, yMax], [0, 0], 'k--')
        orbitFigure.axes.plot([0, 0], [0, 0], [0, zMax], 'k--')
        
        # * Celestial Body
        
        #orbitFigure.axes.scatter(0, 0, 0, s=1000, c='c')
        
        u, v = np.mgrid[0 : 2*np.pi : 40j, 0 : np.pi : 20j]
        
        x = AstronomicalData.EquatiorialRadius(celestialBody) * np.cos(u) * np.sin(v)
        y = AstronomicalData.EquatiorialRadius(celestialBody) * np.sin(u) * np.sin(v)
        z = AstronomicalData.EquatiorialRadius(celestialBody) * np.cos(v)
        
        orbitFigure.axes.plot_wireframe(x, y, z, color="r")
        
        # * Orbit
        
        orbitFigure.axes.plot(result['y'][0,:], result['y'][1,:], result['y'][2,:], label='Orbit')
        
        # * Labels
        
        orbitFigure.axes.set_xlabel('$x$ [km]')
        orbitFigure.axes.set_ylabel('$y$ [km]')
        orbitFigure.axes.set_zlabel('$z$ [km]')
        
        orbitFigure.redrawCanvas()
    
    def plotGroundTrack(self, orbitFigure : FigureCanvas, celestialBody : CelestialBody, ra : list, dec : list) -> None:
        """Plots the ground track of the orbit

        Args:
            orbitFigure (FigureCanvas): Figure canvas
            celestialBody (CelestialBody): Celestial body
            ra (list): Right ascension
            dec (list): Declination
        """
        
        orbitFigure.resetCanvas()
        
        texture = AstronomicalData.Texture(celestialBody)
        
        img = np.asarray(Image.open(texture).transpose(Image.FLIP_TOP_BOTTOM))
        
        orbitFigure.axes.imshow(img, origin='lower', extent=(0, 360, -90, 90))
        orbitFigure.axes.scatter(ra, dec, c='c')
        orbitFigure.axes.scatter(ra[0], dec[0], c='y', label='Start')
        orbitFigure.axes.scatter(ra[-1], dec[-1], c='r', label='Finish')
        orbitFigure.axes.set_xlabel('Right Ascension [deg]')
        orbitFigure.axes.set_ylabel('Declination [deg]')
        #orbitFigure.axes.set_xlim([0, 360])
        #orbitFigure.axes.set_ylim([-90, 90])
        
        orbitFigure.redrawCanvas()
    
    def plotOrbitTransfer(self) -> None:
        """Plots the orbit transfer
        """
        
        # * Integrate departure/arrival orbits
        
        TwoBodyProblem.setCelestialBody(self.body_dep)
        
        result_dep = TwoBodyProblem.integrateRelativeMotion(np.hstack([self.r_dep, self.v_dep]))
        result_arr = TwoBodyProblem.integrateRelativeMotion(np.hstack([self.r_arr, self.v_arr]))
        
        # * Integrate maneuvers
        
        OrbitalManeuvers.setCelestialBody(self.body_dep)
        OrbitalManeuvers.setSpecificImpulse(self.I_sp)
        
        result_tra = dict(y=np.zeros(shape=(6,1)))
        
        self.oe_tra.h       = self.oe_dep.h
        self.oe_tra.e       = self.oe_dep.e
        self.oe_tra.i       = self.oe_dep.i
        self.oe_tra.Omega   = self.oe_dep.Omega
        self.oe_tra.omega   = self.oe_dep.omega
        self.oe_tra.theta   = self.oe_dep.theta
        self.oe_tra.a       = self.oe_dep.a
        
        self.parameters_tra.r_p = self.parameters_dep.r_p
        self.parameters_tra.r_a = self.parameters_dep.r_a
        
        for idx, maneuver in enumerate(self.maneuvers):
            
            temp = self.evaluateManeuver(maneuver, first=idx==0)#, last=idx==len(self.maneuvers)-1)
            
            result_tra['y'] = np.append(result_tra['y'], temp['y'], axis=1)
        
        result_tra['y'] = np.delete(result_tra['y'], 0, axis=1)
        
        # * Final orbit
        
        r, v = ThreeDimensionalOrbit.PF2GEF(self.oe_tra)
        
        result_fin = TwoBodyProblem.integrateRelativeMotion(np.hstack([r, v]))
        
        # * Reset canvas
        
        self.orbit_transfer_figure.resetCanvas()
        
        # * Max Values
        
        #xMax = 1.25 * max(max(np.absolute(result_dep['y'][0,:])), max(np.absolute(result_arr['y'][0,:])), max(np.absolute(result_tra['y'][0,:])), max(np.absolute(result_fin['y'][0,:])))
        #yMax = 1.25 * max(max(np.absolute(result_dep['y'][1,:])), max(np.absolute(result_arr['y'][1,:])), max(np.absolute(result_tra['y'][1,:])), max(np.absolute(result_fin['y'][1,:])))
        #zMax = 1.25 * max(max(np.absolute(result_dep['y'][2,:])), max(np.absolute(result_arr['y'][2,:])), max(np.absolute(result_tra['y'][2,:])), max(np.absolute(result_fin['y'][2,:])))
        
        # * Plane
        
        #îp = mpatches.Rectangle((-xMax, -yMax), 2 * xMax, 2 * yMax, fc=(0,0,0,0.1), ec=(0,0,0,1), lw=2)
        
        #self.orbit_transfer_figure.axes.add_patch(p)
        
        #art3d.pathpatch_2d_to_3d(p, z=0, zdir='z')
        
        # * Axes
        
        #self.orbit_transfer_figure.axes.plot([0, xMax], [0, 0], [0, 0], 'k-.')
        #self.orbit_transfer_figure.axes.plot([0, 0], [0, yMax], [0, 0], 'k-.')
        #self.orbit_transfer_figure.axes.plot([0, 0], [0, 0], [0, zMax], 'k-.')
        
        # * Celestial Body
        
        u, v = np.mgrid[0 : 2*np.pi : 40j, 0 : np.pi : 20j]
        
        x = AstronomicalData.EquatiorialRadius(self.body_dep) * np.cos(u) * np.sin(v)
        y = AstronomicalData.EquatiorialRadius(self.body_dep) * np.sin(u) * np.sin(v)
        z = AstronomicalData.EquatiorialRadius(self.body_dep) * np.cos(v)
        
        self.orbit_transfer_figure.axes.plot_wireframe(x, y, z, color='#808080', alpha=0.5)
        
        # * Orbit
        
        self.orbit_transfer_figure.axes.scatter(result_dep['y'][0,0], result_dep['y'][1,0], result_dep['y'][2,0], c='b', label='Departure Position')
        self.orbit_transfer_figure.axes.scatter(result_arr['y'][0,0], result_arr['y'][1,0], result_arr['y'][2,0], c='r', label='Arrival Position')
        self.orbit_transfer_figure.axes.scatter(result_fin['y'][0,0], result_fin['y'][1,0], result_fin['y'][2,0], c='m', label='Final Position')
        self.orbit_transfer_figure.axes.plot(result_dep['y'][0,:], result_dep['y'][1,:], result_dep['y'][2,:], 'b--', lw='2', label='Departure Orbit')
        self.orbit_transfer_figure.axes.plot(result_arr['y'][0,:], result_arr['y'][1,:], result_arr['y'][2,:], 'r--', lw='2', label='Arrival Orbit')
        self.orbit_transfer_figure.axes.plot(result_fin['y'][0,:], result_fin['y'][1,:], result_fin['y'][2,:], 'm--', lw='1', label='Final Orbit')
        self.orbit_transfer_figure.axes.plot(result_tra['y'][0,:], result_tra['y'][1,:], result_tra['y'][2,:], 'g', label='Transfer Trajectory')
        
        # * Labels
        
        self.orbit_transfer_figure.axes.set_xlabel('$x$ [km]')
        self.orbit_transfer_figure.axes.set_ylabel('$y$ [km]')
        self.orbit_transfer_figure.axes.set_zlabel('$z$ [km]')
        self.orbit_transfer_figure.axes.legend(bbox_to_anchor=(-0.5, 0.5), loc='center left')
        
        # * Redraw canvas
        
        self.orbit_transfer_figure.redrawCanvas()
    
    def evaluateManeuver(self, maneuver : Maneuver, first : bool = False) -> dict:
        """Evaluates and integrates the maneuver from the list

        Args:
            maneuver (Maneuver): Maneuver
            first (bool, optional): True for the first maneuver. Defaults to False.

        Returns:
            dict: Integration result
        """
        
        result_first = dict(y=np.zeros(shape=(6,1)))
        
        result = dict(y=np.zeros(shape=(6,1)))
        
        result_man = dict(y=np.zeros(shape=(6,1)))
        
        # * Choose maneuver
        
        match maneuver.getType():
            
            case ManeuverType.HOHMANN:
                
                # * Angles
                
                theta_0 = 0 if maneuver.getOption() == HohmannDirection.PER2APO else np.pi
                theta_f = np.pi if maneuver.getOption() == HohmannDirection.PER2APO else 0
                
                # * Maneuver
                
                maneuverResult = OrbitalManeuvers.HohmannTransfer(self.parameters_tra.r_p, self.parameters_tra.r_a, self.parameters_arr.r_p, self.parameters_arr.r_a, maneuver.getOption(), self.m_0)
                
                maneuverResult.oe.i     = self.oe_tra.i
                maneuverResult.oe.Omega = self.oe_tra.Omega
                maneuverResult.oe.omega = self.oe_tra.omega
                maneuverResult.oe.theta = theta_0
                
                # * Integrate
                
                if first: result_first = self.integrateFirstManeuver(theta_0)
                
                result_man = self.integrateManeuver(maneuverResult.oe, theta_0, theta_f)
                
                # * New  orbital elements
                
                self.oe_tra.h       = self.oe_arr.h
                self.oe_tra.e       = self.oe_arr.e
                self.oe_tra.a       = self.oe_arr.a
                self.oe_tra.theta   = theta_f
                
                self.parameters_tra.r_p = self.parameters_arr.r_p
                self.parameters_tra.r_a = self.parameters_arr.r_a
                
            case ManeuverType.BI_ELLIPTIC_HOHMANN:
                
                # * Angles
                
                theta_0_1 = 0 if maneuver.getOption() == HohmannDirection.PER2APO else np.pi
                theta_f_1 = np.pi if maneuver.getOption() == HohmannDirection.PER2APO else 0
                theta_0_2 = np.pi if maneuver.getOption() == HohmannDirection.PER2APO else 0
                theta_f_2 = 0 if maneuver.getOption() == HohmannDirection.PER2APO else np.pi
                
                # * Maneuver - 1
                
                maneuverResult_1, maneuverResult_2 = OrbitalManeuvers.BiEllipticHohmannTransfer(self.parameters_tra.r_p, self.parameters_tra.r_a, self.parameters_arr.r_p, self.parameters_arr.r_a, maneuver.getOptionValue(), maneuver.getOption(), self.m_0)
                
                maneuverResult_1.oe.i       = self.oe_tra.i
                maneuverResult_1.oe.Omega   = self.oe_tra.Omega
                maneuverResult_1.oe.omega   = self.oe_tra.omega
                maneuverResult_1.oe.theta   = theta_0_1
                
                # * Integrate - 1
                
                if first: result_first = self.integrateFirstManeuver(theta_0_1)
                
                result_man_1 = self.integrateManeuver(maneuverResult_1.oe, theta_0_1, theta_f_1)
                
                # * Maneuver - 2
                
                maneuverResult_2.oe.i       = self.oe_tra.i
                maneuverResult_2.oe.Omega   = self.oe_tra.Omega
                maneuverResult_2.oe.omega   = self.oe_tra.omega
                maneuverResult_2.oe.theta   = theta_0_2
                
                # * Integrate - 2
                
                result_man_2 = self.integrateManeuver(maneuverResult_2.oe, theta_0_2, theta_f_2)
                
                result_man['y'] = np.append(result_man_1['y'], result_man_2['y'], axis=1)
                
                # * New  orbital elements
                
                self.oe_tra.h       = self.oe_arr.h
                self.oe_tra.e       = self.oe_arr.e
                self.oe_tra.a       = self.oe_arr.a
                self.oe_tra.theta   = theta_f_2
                
                self.parameters_tra.r_p = self.parameters_arr.r_p
                self.parameters_tra.r_a = self.parameters_arr.r_a
            
            case ManeuverType.PLANE_CHANGE:
                
                # * Maneuver
                
                maneuverResult = OrbitalManeuvers.PlaneChangeManeuver2(self.parameters_tra.r_p, self.parameters_tra.r_a, self.oe_tra.Omega, self.oe_tra.omega, self.oe_tra.i, self.oe_arr.Omega, self.oe_arr.i, self.m_0)
                
                maneuverResult.oe.h = self.oe_tra.h
                maneuverResult.oe.e = self.oe_tra.e
                maneuverResult.oe.a = self.oe_tra.a
                
                # * Integrate
                
                if first:
                        
                    result_first = self.integrateFirstManeuver(maneuverResult.oe.theta)
                    
                else:
                
                    result_man = self.integrateManeuver(self.oe_tra, self.oe_tra.theta, maneuverResult.oe.theta)
                
                # * New  orbital elements
                
                self.oe_tra.i       = maneuverResult.oe.i
                self.oe_tra.Omega   = maneuverResult.oe.Omega
                self.oe_tra.omega   = maneuverResult.oe.omega
                self.oe_tra.theta   = maneuverResult.oe.theta
            
            case ManeuverType.APSE_LINE_ROTATION:
                
                # * Maneuver
                
                maneuverResult = OrbitalManeuvers.ApseLineRotationFromEta(self.parameters_tra.r_p, self.parameters_tra.r_a, self.parameters_tra.r_p, self.parameters_tra.r_a, self.oe_arr.omega - self.oe_tra.omega, secondIntersectionPoint=maneuver.getOption()==1, m=self.m_0)
                
                # * Integrate
                
                if first:
                    
                    result_first = self.integrateFirstManeuver(maneuverResult.oe.theta)
                    
                else:
                
                    result_man = self.integrateManeuver(self.oe_tra, self.oe_tra.theta, maneuverResult.oe.theta)
                
                # * New  orbital elements
                
                self.oe_tra.omega   = self.oe_arr.omega
                self.oe_tra.theta   = maneuverResult.oe.theta
        
        # * Return
        
        if len(result_first['y'][0,:]) > 1 and len(result_man['y'][0,:]) > 1:
            
            result['y'] = np.append(result_first['y'], result_man['y'], axis=1)
            
        elif len(result_first['y'][0,:]) > 1 and len(result_man['y'][0,:]) == 1:
            
            result['y'] = result_first['y']
            
        elif len(result_first['y'][0,:]) == 1 and len(result_man['y'][0,:]) > 1:
            
            result['y'] = result_man['y']
        
        #if not first: result['y'] = np.delete(result['y'], 0, axis=1)
        
        return result
    
    def integrateFirstManeuver(self, theta_f : float) -> dict:
        """Integrates the trajectory from the departure orbit to the given True Anomaly

        Args:
            theta_f (float): Final True Anomaly

        Returns:
            dict: Integration result
        """
        
        theta_0 = self.oe_dep.theta
        
        t_0 = Time.calculateEllipticalOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=self.parameters_dep.T, e=self.oe_dep.e, theta=theta_0)
        t_f = Time.calculateEllipticalOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=self.parameters_dep.T, e=self.oe_dep.e, theta=theta_f)
        
        if theta_f != 0.0 and t_0 > t_f: t_f += self.parameters_dep.T
        
        return TwoBodyProblem.integrateRelativeMotion(np.hstack([self.r_dep, self.v_dep]), t_0, t_f)
    
    def integrateManeuver(self, oe : ORBITAL_ELEMENTS, theta_0 : float, theta_f : float) -> dict:
        """Integrates the trajectory from the intial True Anomaly to the final True Anomaly of the given Orbital Elements

        Args:
            oe (ORBITAL_ELEMENTS): Orbital Elements
            theta_0 (float): Initial True Anomaly
            theta_f (float): Final True Anomaly

        Returns:
            dict: Integration result
        """
        
        r, v = ThreeDimensionalOrbit.PF2GEF(oe)
           
        parameters = TwoBodyProblem.calculateOrbitalParameters(r, v)
        
        t_0 = Time.calculateEllipticalOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=parameters.T, e=oe.e, theta=theta_0)
        t_f = Time.calculateEllipticalOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=parameters.T, e=oe.e, theta=theta_f)
        
        if theta_f != 0.0 and t_0 > t_f: t_f += parameters.T
        
        return TwoBodyProblem.integrateRelativeMotion(np.hstack([r, v]), t_0, t_f)