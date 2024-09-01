import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np
import matplotlib.patches as mpatches
import mpl_toolkits.mplot3d.art3d as art3d

from enum import IntEnum
from PIL import Image

from FigureCanvas import FigureCanvas
from Spacecraft import Spacecraft
from Orbit import Orbit
from Maneuver import Maneuver, ManeuverType

from tools.AstronomicalData import AstronomicalData, CelestialBody, index_from_celestial_body, celestial_body_from_index
from tools.TwoBodyProblem import TwoBodyProblem, OrbitalParameters
from tools.ThreeDimensionalOrbit import ThreeDimensionalOrbit, OrbitalElements
from tools.Time import Time, DirectionType
from tools.OrbitalManeuvers import OrbitalManeuvers, HohmannDirection

class StateType(IntEnum):
    
    CARTESIAN           = 0
    KEPLERIAN           = 1
    MODIFIED_KEPLERIAN  = 2

class MissionOrbitTransfer(qtCore.QObject):
    
    # ! CONSTRUCTOR
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__MissionOrbitTransfer", self)
        
        self.spacecraft = Spacecraft(engine)
        
        self.orbit = Orbit(engine)
        
        # * Departure orbit
        
        self.dep_body                   = CelestialBody.EARTH
        self.dep_state                  = StateType.CARTESIAN
        self.dep_r                      = np.array([-8173.55640, -3064.65060, -2840.15350], dtype=float)
        self.dep_v                      = np.array([-3.07330000, 5.94440000, -1.54740000], dtype=float)
        self.dep_orbital_parameters     = OrbitalParameters()
        self.dep_orbital_elements       = OrbitalElements()
        self.dep_figure_orbit           = FigureCanvas(dof3=True)
        self.dep_figure_ground_track    = FigureCanvas()
        
        # * Arrival orbit
        
        self.arr_body                   = CelestialBody.EARTH
        self.arr_state                  = StateType.CARTESIAN
        self.arr_r                      = np.array([4571.13653, 32940.33361, -14208.95231], dtype=float)
        self.arr_v                      = np.array([-3.06192709, 1.01383552, 0.41402772], dtype=float)
        self.arr_orbital_parameters     = OrbitalParameters()
        self.arr_orbital_elements       = OrbitalElements()
        self.arr_figure_orbit           = FigureCanvas(dof3=True)
        self.arr_figure_ground_track    = FigureCanvas()
        
        # * Tranfer orbit
        
        self.tra_orbital_parameters     = OrbitalParameters()
        self.tra_orbital_elements       = OrbitalElements()
        self.tra_figure_orbit           = FigureCanvas(dof3=True)
        self.maneuvers                  = list()
        
        # * Context properties
        
        engine.rootContext().setContextProperty("__DepartureOrbitFigure", self.dep_figure_orbit)
        engine.rootContext().setContextProperty("__DepartureGroundTrackFigure", self.dep_figure_ground_track)
        engine.rootContext().setContextProperty("__ArrivalOrbitFigure", self.arr_figure_orbit)
        engine.rootContext().setContextProperty("__ArrivalGroundTrackFigure", self.arr_figure_ground_track)
        engine.rootContext().setContextProperty("__OrbitTransferFigure", self.tra_figure_orbit)
        
        # * Init
        
        self.loadDepartureOrbit()
    
    # ! PUBLIC
    
    def setUpdateWithCanvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Connects all the QML figures with the backend model

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        win = engine.rootObjects()[0]
        
        self.dep_figure_orbit.update_with_canvas(win.findChild(qtCore.QObject, "DepartureOrbitFigure"), win.findChild(qtCore.QObject, "DepartureOrbitFigureParent"))
        self.dep_figure_ground_track.update_with_canvas(win.findChild(qtCore.QObject, "DepartureGroundTrackFigure"), win.findChild(qtCore.QObject, "DepartureGroundTrackFigureParent"))
        self.arr_figure_orbit.update_with_canvas(win.findChild(qtCore.QObject, "ArrivalOrbitFigure"), win.findChild(qtCore.QObject, "ArrivalOrbitFigureParent"))
        self.arr_figure_ground_track.update_with_canvas(win.findChild(qtCore.QObject, "ArrivalGroundTrackFigure"), win.findChild(qtCore.QObject, "ArrivalGroundTrackFigureParent"))
        self.tra_figure_orbit.update_with_canvas(win.findChild(qtCore.QObject, "OrbitTransferFigure"), win.findChild(qtCore.QObject, "OrbitTransferFigureParent"))
        
        #self.tra_figure_orbit.figure.tight_layout()
        self.tra_figure_orbit.axes.set_aspect('equal', adjustable='box')
    
    # ! SLOTS
    
    # ? Departure Orbit
    
    @qtCore.Slot()
    def loadDepartureOrbit(self) -> None:
        """Loads the departure orbit parameters
        """
        
        ThreeDimensionalOrbit.set_celestial_body(self.dep_body)
        
        TwoBodyProblem.set_celestial_body(self.dep_body)
        
        self.dep_orbital_elements = ThreeDimensionalOrbit.calculate_orbital_elements(self.dep_r, self.dep_v)
        
        self.dep_orbital_parameters = TwoBodyProblem.calculate_orbital_parameters(self.dep_r, self.dep_v)
        
    @qtCore.Slot()
    def fillDepartureOrbit(self) -> None:
        """Fills the GUI with the departure orbit parameters
        """
        
        self.orbit.update_central_body(index_from_celestial_body(self.dep_body))
        self.orbit.update_state(self.dep_state)
        self.orbit.update_cartesian_parameters(self.dep_r, self.dep_v)
        self.orbit.update_keplerian_parameters(self.dep_orbital_elements)
        self.orbit.update_modified_keplerian_parameters(self.dep_orbital_elements, self.dep_orbital_parameters)
    
    @qtCore.Slot()
    def updateDepartureOrbit(self) -> None:
        """Updates the departure orbit parameters
        """
        
        # * Configuration
        
        self.dep_body = celestial_body_from_index(self.orbit._body)
        
        self.dep_state = self.orbit._state
        
        ThreeDimensionalOrbit.set_celestial_body(self.dep_body)
        
        TwoBodyProblem.set_celestial_body(self.dep_body)
        
        # * Evaluation
        
        match self.dep_state:
            
            case StateType.CARTESIAN:
                
                self.dep_r = np.array([self.orbit._r_x, self.orbit._r_y, self.orbit._r_z])
                self.dep_v = np.array([self.orbit._v_x, self.orbit._v_y, self.orbit._v_z])
        
                self.dep_orbital_elements = ThreeDimensionalOrbit.calculate_orbital_elements(self.dep_r, self.dep_v)
                
                self.dep_orbital_parameters = TwoBodyProblem.calculate_orbital_parameters(self.dep_r, self.dep_v)
                
                self.orbit.update_keplerian_parameters(self.dep_orbital_elements)
                self.orbit.update_modified_keplerian_parameters(self.dep_orbital_elements, self.dep_orbital_parameters)
            
            case StateType.KEPLERIAN:
                
                self.dep_orbital_elements = self.orbit.get_keplerian_parameters()
                
                self.dep_r, self.dep_v = ThreeDimensionalOrbit.pf_2_gef(self.dep_orbital_elements)
                
                self.dep_orbital_parameters = TwoBodyProblem.calculate_orbital_parameters(self.dep_r, self.dep_v)
                
                self.orbit.update_cartesian_parameters(self.dep_r, self.dep_v)
                self.orbit.update_modified_keplerian_parameters(self.dep_orbital_elements, self.dep_orbital_parameters)
            
            case StateType.MODIFIED_KEPLERIAN:
                
                self.orbit.update_keplerian_parameters_from_radii()
                
                self.dep_r, self.dep_v = ThreeDimensionalOrbit.pf_2_gef(self.orbit.get_keplerian_parameters())
                
                self.orbit.update_cartesian_parameters(self.dep_r, self.dep_v)
            
            case _:
                
                pass
    
    @qtCore.Slot()
    def evaluateDepartureOrbit(self):
        """Integrates the equations of the departure orbit and the ground track
        """
        
        ThreeDimensionalOrbit.set_celestial_body(self.dep_body)
        TwoBodyProblem.set_celestial_body(self.dep_body)
        
        result = TwoBodyProblem.simulate_relative_motion(np.hstack([self.dep_r, self.dep_v]))
        
        self.plotOrbit(self.dep_figure_orbit, self.dep_body, result)
        
        ra, dec = ThreeDimensionalOrbit.calculate_ground_track(self.dep_orbital_elements, 60)
        
        if len(ra) == 0 or len(dec) == 0:
            
            ra_0, dec_0 = ThreeDimensionalOrbit.calculate_ra_dec(self.dep_r)
            
            ra  = [ra_0]
            dec = [dec_0]
        
        self.plotGroundTrack(self.dep_figure_ground_track, self.dep_body, ra, dec)
    
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
        
        ThreeDimensionalOrbit.set_celestial_body(self.arr_body)
        
        TwoBodyProblem.set_celestial_body(self.arr_body)
        
        self.arr_orbital_elements = ThreeDimensionalOrbit.calculate_orbital_elements(self.arr_r, self.arr_v)
        
        self.arr_orbital_parameters = TwoBodyProblem.calculate_orbital_parameters(self.arr_r, self.arr_v)
    
    @qtCore.Slot()
    def fillArrivalOrbit(self) -> None:
        """Fills the GUI with the arrival orbit parameters
        """
        
        self.orbit.update_central_body(index_from_celestial_body(self.arr_body))
        self.orbit.update_state(self.arr_state)
        self.orbit.update_cartesian_parameters(self.arr_r, self.arr_v)
        self.orbit.update_keplerian_parameters(self.arr_orbital_elements)
        self.orbit.update_modified_keplerian_parameters(self.arr_orbital_elements, self.arr_orbital_parameters)
        
    @qtCore.Slot()
    def updateArrivalOrbit(self) -> None:
        """Updates the arrival orbit parameters
        """
        
        # * Configuration
        
        self.arr_body = celestial_body_from_index(self.orbit._body)
        
        self.arr_state = self.orbit._state
        
        ThreeDimensionalOrbit.set_celestial_body(self.arr_body)
        
        TwoBodyProblem.set_celestial_body(self.arr_body)
        
        # * Evaluation
        
        match self.arr_state:
            
            case StateType.CARTESIAN:
                
                self.arr_r = np.array([self.orbit._r_x, self.orbit._r_y, self.orbit._r_z])
                self.arr_v = np.array([self.orbit._v_x, self.orbit._v_y, self.orbit._v_z])
        
                self.arr_orbital_elements = ThreeDimensionalOrbit.calculate_orbital_elements(self.arr_r, self.arr_v)
                
                self.arr_orbital_parameters = TwoBodyProblem.calculate_orbital_parameters(self.arr_r, self.arr_v)
                
                self.orbit.update_keplerian_parameters(self.arr_orbital_elements)
                self.orbit.update_modified_keplerian_parameters(self.arr_orbital_elements, self.arr_orbital_parameters)
            
            case StateType.KEPLERIAN:
                
                self.arr_orbital_elements = self.orbit.get_keplerian_parameters()
                
                self.arr_r, self.arr_v = ThreeDimensionalOrbit.pf_2_gef(self.arr_orbital_elements)
                
                self.arr_orbital_parameters = TwoBodyProblem.calculate_orbital_parameters(self.arr_r, self.arr_v)
                
                self.orbit.update_cartesian_parameters(self.arr_r, self.arr_v)
                self.orbit.update_modified_keplerian_parameters(self.arr_orbital_elements, self.arr_orbital_parameters)
            
            case StateType.MODIFIED_KEPLERIAN:
                
                self.orbit.update_keplerian_parameters_from_radii()
                
                self.arr_r, self.arr_v = ThreeDimensionalOrbit.pf_2_gef(self.orbit.get_keplerian_parameters())
                
                self.orbit.update_cartesian_parameters(self.arr_r, self.arr_v)
            
            case _:
                
                pass
    
    @qtCore.Slot()
    def evaluateArrivalOrbit(self):
        """Integrates the equations of the arrival orbit and the ground track
        """
        
        ThreeDimensionalOrbit.set_celestial_body(self.arr_body)
        TwoBodyProblem.set_celestial_body(self.arr_body)
        
        result = TwoBodyProblem.simulate_relative_motion(np.hstack([self.arr_r, self.arr_v]))
        
        self.plotOrbit(self.arr_figure_orbit, self.arr_body, result)
        
        ra, dec = ThreeDimensionalOrbit.calculate_ground_track(self.arr_orbital_elements, 60)
        
        if len(ra) == 0 or len(dec) == 0:
            
            ra_0, dec_0 = ThreeDimensionalOrbit.calculate_ra_dec(self.arr_r)
            
            ra  = [ra_0]
            dec = [dec_0]
        
        self.plotGroundTrack(self.arr_figure_ground_track, self.arr_body, ra, dec)
    
    @qtCore.Slot()
    def saveArrivalOrbit(self) -> None:
        """Updates the arrival orbit parameters and plot
        """
        
        self.updateDepartureOrbit()
        
        self.evaluateDepartureOrbit()
    
    # ? Maneuvers
    
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
        
        orbitFigure.reset_canvas()
        
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
        
        x = AstronomicalData.equatiorial_radius(celestialBody) * np.cos(u) * np.sin(v)
        y = AstronomicalData.equatiorial_radius(celestialBody) * np.sin(u) * np.sin(v)
        z = AstronomicalData.equatiorial_radius(celestialBody) * np.cos(v)
        
        orbitFigure.axes.plot_wireframe(x, y, z, color="r")
        
        # * Orbit
        
        orbitFigure.axes.plot(result['y'][0,:], result['y'][1,:], result['y'][2,:], label='Orbit')
        
        # * Labels
        
        orbitFigure.axes.set_xlabel('$x$ [km]')
        orbitFigure.axes.set_ylabel('$y$ [km]')
        orbitFigure.axes.set_zlabel('$z$ [km]')
        
        orbitFigure.redraw_canvas()
    
    def plotGroundTrack(self, orbitFigure : FigureCanvas, celestialBody : CelestialBody, ra : list, dec : list) -> None:
        """Plots the ground track of the orbit

        Args:
            orbitFigure (FigureCanvas): Figure canvas
            celestialBody (CelestialBody): Celestial body
            ra (list): Right ascension
            dec (list): Declination
        """
        
        orbitFigure.reset_canvas()
        
        texture = AstronomicalData.texture(celestialBody)
        
        img = np.asarray(Image.open(texture).transpose(Image.FLIP_TOP_BOTTOM))
        
        orbitFigure.axes.imshow(img, origin='lower', extent=(0, 360, -90, 90))
        orbitFigure.axes.scatter(ra, dec, c='c')
        orbitFigure.axes.scatter(ra[0], dec[0], c='y', label='Start')
        orbitFigure.axes.scatter(ra[-1], dec[-1], c='r', label='Finish')
        orbitFigure.axes.set_xlabel('Right Ascension [deg]')
        orbitFigure.axes.set_ylabel('Declination [deg]')
        #orbitFigure.axes.set_xlim([0, 360])
        #orbitFigure.axes.set_ylim([-90, 90])
        
        orbitFigure.redraw_canvas()
    
    def plotOrbitTransfer(self) -> None:
        """Plots the orbit transfer
        """
        
        ThreeDimensionalOrbit.set_celestial_body(self.dep_body)
        Time.set_celestial_body(self.dep_body)
        
        # * Integrate departure/arrival orbits
        
        TwoBodyProblem.set_celestial_body(self.dep_body)
        
        result_dep = TwoBodyProblem.simulate_relative_motion(np.hstack([self.dep_r, self.dep_v]))
        result_arr = TwoBodyProblem.simulate_relative_motion(np.hstack([self.arr_r, self.arr_v]))
        
        # * Integrate maneuvers
        
        OrbitalManeuvers.set_celestial_body(self.dep_body)
        OrbitalManeuvers.set_specific_impulse(self.spacecraft._specific_impulse)
        
        result_tra = dict(y=np.zeros(shape=(6,1)))
        
        self.tra_orbital_elements.h     = self.dep_orbital_elements.h
        self.tra_orbital_elements.e     = self.dep_orbital_elements.e
        self.tra_orbital_elements.i     = self.dep_orbital_elements.i
        self.tra_orbital_elements.Omega = self.dep_orbital_elements.Omega
        self.tra_orbital_elements.omega = self.dep_orbital_elements.omega
        self.tra_orbital_elements.theta = self.dep_orbital_elements.theta
        self.tra_orbital_elements.a     = self.dep_orbital_elements.a
        
        self.tra_orbital_parameters.r_p = self.dep_orbital_parameters.r_p
        self.tra_orbital_parameters.r_a = self.dep_orbital_parameters.r_a
        
        self.spacecraft.reset()
        
        for idx, maneuver in enumerate(self.maneuvers):
            
            temp = self.evaluateManeuver(maneuver, first=idx==0)#, last=idx==len(self.maneuvers)-1)
            
            result_tra['y'] = np.append(result_tra['y'], temp['y'], axis=1)
        
        result_tra['y'] = np.delete(result_tra['y'], 0, axis=1)
        
        # * Final orbit
        
        r, v = ThreeDimensionalOrbit.pf_2_gef(self.tra_orbital_elements)
        
        result_fin = TwoBodyProblem.simulate_relative_motion(np.hstack([r, v]))
        
        # * Reset canvas
        
        self.tra_figure_orbit.reset_canvas()
        
        # * Celestial Body
        
        u, v = np.mgrid[0 : 2*np.pi : 40j, 0 : np.pi : 20j]
        
        x = AstronomicalData.equatiorial_radius(self.dep_body) * np.cos(u) * np.sin(v)
        y = AstronomicalData.equatiorial_radius(self.dep_body) * np.sin(u) * np.sin(v)
        z = AstronomicalData.equatiorial_radius(self.dep_body) * np.cos(v)
        
        self.tra_figure_orbit.axes.plot_wireframe(x, y, z, color='#808080', alpha=0.5)
        
        # * Orbit
        
        self.tra_figure_orbit.axes.scatter(result_dep['y'][0,0], result_dep['y'][1,0], result_dep['y'][2,0], c='b', label='Departure Position')
        self.tra_figure_orbit.axes.scatter(result_arr['y'][0,0], result_arr['y'][1,0], result_arr['y'][2,0], c='r', label='Arrival Position')
        self.tra_figure_orbit.axes.scatter(result_fin['y'][0,0], result_fin['y'][1,0], result_fin['y'][2,0], c='m', label='Final Position')
        self.tra_figure_orbit.axes.plot(result_dep['y'][0,:], result_dep['y'][1,:], result_dep['y'][2,:], 'b--', lw='2', label='Departure Orbit')
        self.tra_figure_orbit.axes.plot(result_arr['y'][0,:], result_arr['y'][1,:], result_arr['y'][2,:], 'r--', lw='2', label='Arrival Orbit')
        self.tra_figure_orbit.axes.plot(result_fin['y'][0,:], result_fin['y'][1,:], result_fin['y'][2,:], 'm--', lw='1', label='Final Orbit')
        self.tra_figure_orbit.axes.plot(result_tra['y'][0,:], result_tra['y'][1,:], result_tra['y'][2,:], 'g', label='Transfer Trajectory')
        
        # * Labels
        
        self.tra_figure_orbit.axes.set_xlabel('$x$ [km]')
        self.tra_figure_orbit.axes.set_ylabel('$y$ [km]')
        self.tra_figure_orbit.axes.set_zlabel('$z$ [km]')
        self.tra_figure_orbit.axes.legend(bbox_to_anchor=(-0.5, 0.5), loc='center left')
        
        # * Redraw canvas
        
        self.tra_figure_orbit.redraw_canvas()
    
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
        
        dt = 0.0
        
        # * Choose maneuver
        
        match maneuver.type:
            
            case ManeuverType.HOHMANN:
                
                # * Angles
                
                theta_0 = 0 if maneuver.option == HohmannDirection.PER2APO else np.pi
                theta_f = np.pi if maneuver.option == HohmannDirection.PER2APO else 0
                
                # * Maneuver
                
                maneuverResult = OrbitalManeuvers.hohmann_transfer(self.tra_orbital_parameters.r_p, self.tra_orbital_parameters.r_a, self.arr_orbital_parameters.r_p, self.arr_orbital_parameters.r_a, maneuver.option, self.spacecraft._mass)
                
                maneuverResult.oe.i     = self.tra_orbital_elements.i
                maneuverResult.oe.Omega = self.tra_orbital_elements.Omega
                maneuverResult.oe.omega = self.tra_orbital_elements.omega
                maneuverResult.oe.theta = theta_0
                
                # * Integrate
                
                if first:
                    
                    result_first = self.integrateFirstManeuver(theta_0)
                    
                    dt += result_first['dt']
                    
                    result_man = self.integrateManeuver(maneuverResult.oe, theta_0, theta_f)
                    
                    dt += result_first['dt']
                    
                else:
                
                    temp1 = self.integrateManeuver(self.tra_orbital_elements, self.tra_orbital_elements.theta, maneuverResult.oe.theta)
                    
                    dt += temp1['dt']
                    
                    temp2 = self.integrateManeuver(maneuverResult.oe, theta_0, theta_f)
                    
                    dt += temp2['dt']
                
                    result_man['y'] = np.append(temp1['y'], temp2['y'], axis=1)
                
                # * New  orbital elements
                
                self.tra_orbital_elements.h     = self.arr_orbital_elements.h
                self.tra_orbital_elements.e     = self.arr_orbital_elements.e
                self.tra_orbital_elements.a     = self.arr_orbital_elements.a
                self.tra_orbital_elements.theta = theta_f
                
                self.tra_orbital_parameters.r_p = self.tra_orbital_parameters.r_p
                self.tra_orbital_parameters.r_a = self.tra_orbital_parameters.r_a
                
                # * Budget
                
                maneuver.delta_velocity = maneuverResult.dv
                maneuver.delta_time     = dt / 3600 + maneuverResult.dt / 3600
                maneuver.delta_mass     = maneuverResult.dm
                
                self.spacecraft.update_mass(maneuverResult.dm)
                
            case ManeuverType.BI_ELLIPTIC_HOHMANN:
                
                # * Angles
                
                theta_0_1 = 0 if maneuver.option == HohmannDirection.PER2APO else np.pi
                theta_f_1 = np.pi if maneuver.option == HohmannDirection.PER2APO else 0
                theta_0_2 = np.pi if maneuver.option == HohmannDirection.PER2APO else 0
                theta_f_2 = 0 if maneuver.option == HohmannDirection.PER2APO else np.pi
                
                # * Maneuver - 1
                
                maneuverResult_1, maneuverResult_2 = OrbitalManeuvers.bi_elliptic_hohmann_transfer(self.tra_orbital_parameters.r_p, self.tra_orbital_parameters.r_a, self.arr_orbital_parameters.r_p, self.arr_orbital_parameters.r_a, maneuver.option_value, maneuver.option, self.spacecraft._mass)
                
                maneuverResult_1.oe.i       = self.tra_orbital_elements.i
                maneuverResult_1.oe.Omega   = self.tra_orbital_elements.Omega
                maneuverResult_1.oe.omega   = self.tra_orbital_elements.omega
                maneuverResult_1.oe.theta   = theta_0_1
                
                # * Integrate - 1
                
                if first:
                    
                    result_first = self.integrateFirstManeuver(theta_0_1)
                    
                    dt += result_first['dt']
                    
                    result_man_1 = self.integrateManeuver(maneuverResult_1.oe, theta_0_1, theta_f_1)
                    
                    dt += result_man_1['dt']
                    
                else:
                
                    temp1 = self.integrateManeuver(self.tra_orbital_elements, self.tra_orbital_elements.theta, maneuverResult_1.oe.theta)
                    
                    dt += temp1['dt']
                    
                    temp2 = self.integrateManeuver(maneuverResult_1.oe, theta_0_1, theta_f_1)
                    
                    dt += temp2['dt']
                
                    result_man_1['y'] = np.append(temp1['y'], temp2['y'], axis=1)
                
                # * Maneuver - 2
                
                maneuverResult_2.oe.i       = self.tra_orbital_elements.i
                maneuverResult_2.oe.Omega   = self.tra_orbital_elements.Omega
                maneuverResult_2.oe.omega   = self.tra_orbital_elements.omega
                maneuverResult_2.oe.theta   = theta_0_2
                
                # * Integrate - 2
                
                result_man_2 = self.integrateManeuver(maneuverResult_2.oe, theta_0_2, theta_f_2)
                
                dt += result_man_2['dt']
                
                result_man['y'] = np.append(result_man_1['y'], result_man_2['y'], axis=1)
                
                # * New  orbital elements
                
                self.tra_orbital_elements.h     = self.arr_orbital_elements.h
                self.tra_orbital_elements.e     = self.arr_orbital_elements.e
                self.tra_orbital_elements.a     = self.arr_orbital_elements.a
                self.tra_orbital_elements.theta = theta_f_2
                
                self.tra_orbital_parameters.r_p = self.arr_orbital_parameters.r_p
                self.tra_orbital_parameters.r_a = self.arr_orbital_parameters.r_a
                
                # * Budget
                
                maneuver.delta_velocity = maneuverResult_1.dv + maneuverResult_2.dv
                maneuver.delta_time     = dt / 3600 + maneuverResult_1.dt / 3600 + maneuverResult_2.dt / 3600
                maneuver.delta_mass     = maneuverResult_1.dm + maneuverResult_2.dm
                
                self.spacecraft.update_mass(maneuverResult_1.dm + maneuverResult_2.dm)
            
            case ManeuverType.PLANE_CHANGE:
                
                # * Maneuver
                
                maneuverResult = OrbitalManeuvers.plane_change_maneuver_2(self.tra_orbital_parameters.r_p, self.tra_orbital_parameters.r_a, self.tra_orbital_elements.Omega, self.tra_orbital_elements.omega, self.tra_orbital_elements.i, self.arr_orbital_elements.Omega, self.arr_orbital_elements.i, self.spacecraft._mass)
                
                maneuverResult.oe.h = self.tra_orbital_elements.h
                maneuverResult.oe.e = self.tra_orbital_elements.e
                maneuverResult.oe.a = self.tra_orbital_elements.a
                
                # * Integrate
                
                if first:
                        
                    result_first = self.integrateFirstManeuver(maneuverResult.oe.theta)
                    
                    dt += result_first['dt']
                    
                else:
                
                    result_man = self.integrateManeuver(self.tra_orbital_elements, self.tra_orbital_elements.theta, maneuverResult.oe.theta)
                    
                    dt += result_man['dt']
                
                # * New  orbital elements
                
                self.tra_orbital_elements.i     = maneuverResult.oe.i
                self.tra_orbital_elements.Omega = maneuverResult.oe.Omega
                self.tra_orbital_elements.omega = maneuverResult.oe.omega
                self.tra_orbital_elements.theta = maneuverResult.oe.theta
                
                # * Budget
                
                maneuver.delta_velocity = maneuverResult.dv
                maneuver.delta_time     = dt / 3600 + maneuverResult.dt / 3600
                maneuver.delta_mass     = maneuverResult.dm
                
                self.spacecraft.update_mass(maneuverResult.dm)
            
            case ManeuverType.APSE_LINE_ROTATION:
                
                # * Maneuver
                
                maneuverResult = OrbitalManeuvers.apse_line_rotation_from_eta(self.tra_orbital_parameters.r_p, self.tra_orbital_parameters.r_a, self.tra_orbital_parameters.r_p, self.tra_orbital_parameters.r_a, self.arr_orbital_elements.omega - self.tra_orbital_elements.omega, secondIntersectionPoint=maneuver.option==1, m=self.spacecraft._mass)
                
                # * Integrate
                
                if first:
                    
                    result_first = self.integrateFirstManeuver(maneuverResult.oe.theta)
                    
                    dt += result_first['dt']
                    
                else:
                
                    result_man = self.integrateManeuver(self.tra_orbital_elements, self.tra_orbital_elements.theta, maneuverResult.oe.theta)
                    
                    dt += result_man['dt']
                
                # * New  orbital elements
                
                self.tra_orbital_elements.omega = self.arr_orbital_elements.omega
                self.tra_orbital_elements.theta = maneuverResult.oe.theta
                
                # * Budget
                
                maneuver.delta_velocity = maneuverResult.dv
                maneuver.delta_time     = dt / 3600 + maneuverResult.dt / 3600
                maneuver.delta_mass     = maneuverResult.dm
                
                self.spacecraft.update_mass(maneuverResult.dm)
        
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
        
        theta_0 = self.dep_orbital_elements.theta
        
        t_0 = Time.calculate_elliptical_orbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=self.dep_orbital_parameters.T, e=self.dep_orbital_elements.e, theta=theta_0)
        t_f = Time.calculate_elliptical_orbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=self.dep_orbital_parameters.T, e=self.dep_orbital_elements.e, theta=theta_f)
        
        if theta_f != 0.0 and t_0 > t_f: t_f += self.dep_orbital_parameters.T
        
        return TwoBodyProblem.simulate_relative_motion(np.hstack([self.dep_r, self.dep_v]), t_0, t_f)
    
    def integrateManeuver(self, oe : OrbitalElements, theta_0 : float, theta_f : float) -> dict:
        """Integrates the trajectory from the intial True Anomaly to the final True Anomaly of the given Orbital Elements

        Args:
            oe (ORBITAL_ELEMENTS): Orbital Elements
            theta_0 (float): Initial True Anomaly
            theta_f (float): Final True Anomaly

        Returns:
            dict: Integration result
        """
        
        r, v = ThreeDimensionalOrbit.pf_2_gef(oe)
           
        parameters = TwoBodyProblem.calculate_orbital_parameters(r, v)
        
        t_0 = Time.calculate_elliptical_orbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=parameters.T, e=oe.e, theta=theta_0)
        t_f = Time.calculate_elliptical_orbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=parameters.T, e=oe.e, theta=theta_f)
        
        if theta_f != 0.0 and t_0 > t_f: t_f += parameters.T
        
        return TwoBodyProblem.simulate_relative_motion(np.hstack([r, v]), t_0, t_f)
    