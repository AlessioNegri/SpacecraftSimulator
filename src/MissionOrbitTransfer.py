""" MissionOrbitTransfer.py: Implements the orbit transfer mission """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np
import matplotlib.patches as mpatches
import mpl_toolkits.mplot3d.art3d as art3d
import mplcyberpunk
import copy

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

# --- ENUM 

class StateType(IntEnum):
    """List of state selection type"""
    
    CARTESIAN           = 0
    KEPLERIAN           = 1
    MODIFIED_KEPLERIAN  = 2

# --- CLASS 

class MissionOrbitTransfer(qtCore.QObject):
    """Manages the orbit transfer mission"""
    
    # --- PUBLIC METHODS 
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__MissionOrbitTransfer", self)
        
        self.spacecraft = Spacecraft(engine)
        
        self.orbit = Orbit(engine)
        
        # ? Departure orbit
        
        self.dep_body                   = CelestialBody.EARTH                                               # * Celestial body
        self.dep_state                  = StateType.CARTESIAN                                               # * State type
        self.dep_r                      = np.array([-8173.55640, -3064.65060, -2840.15350], dtype=float)    # * Position vector     [ km ]
        self.dep_v                      = np.array([-3.07330000, 5.94440000, -1.54740000], dtype=float)     # * Velocity vector     [ km / s ]
        self.dep_orbital_parameters     = OrbitalParameters()                                               # * Orbital parameters
        self.dep_orbital_elements       = OrbitalElements()                                                 # * Orbital elements
        self.dep_figure_orbit           = FigureCanvas(dof3=True, figure_in_dialog=True)                    # * Orbit figure
        self.dep_figure_ground_track    = FigureCanvas(figure_in_dialog=True)                               # * Ground track figure
        
        # ? Arrival orbit
        
        self.arr_body                   = CelestialBody.EARTH                                               # * Celestial body
        self.arr_state                  = StateType.CARTESIAN                                               # * State type
        self.arr_r                      = np.array([4571.13653, 32940.33361, -14208.95231], dtype=float)    # * Position vector     [ km ]
        self.arr_v                      = np.array([-3.06192709, 1.01383552, 0.41402772], dtype=float)      # * Velocity vector     [ km / s ]
        self.arr_orbital_parameters     = OrbitalParameters()                                               # * Orbital parameters
        self.arr_orbital_elements       = OrbitalElements()                                                 # * Orbital elements
        self.arr_figure_orbit           = FigureCanvas(dof3=True, figure_in_dialog=True)                    # * Orbit figure
        self.arr_figure_ground_track    = FigureCanvas(figure_in_dialog=True)                               # * Ground track figure
        
        # ? Tranfer orbit
        
        self.tra_orbital_parameters     = OrbitalParameters()                                               # * Orbital parameters
        self.tra_orbital_elements       = OrbitalElements()                                                 # * Orbital elements
        self.tra_figure_orbit           = FigureCanvas(dof3=True)                                           # * Orbit figure
        self.maneuvers                  = list()                                                            # * List of orbital maneuvers
        
        # ? Context properties
        
        engine.rootContext().setContextProperty("__DepartureOrbitFigure", self.dep_figure_orbit)
        engine.rootContext().setContextProperty("__DepartureGroundTrackFigure", self.dep_figure_ground_track)
        engine.rootContext().setContextProperty("__ArrivalOrbitFigure", self.arr_figure_orbit)
        engine.rootContext().setContextProperty("__ArrivalGroundTrackFigure", self.arr_figure_ground_track)
        engine.rootContext().setContextProperty("__OrbitTransferFigure", self.tra_figure_orbit)
        
        # ? Init Departure Orbit
        
        ThreeDimensionalOrbit.set_celestial_body(self.dep_body)
        
        TwoBodyProblem.set_celestial_body(self.dep_body)
        
        self.dep_orbital_elements = ThreeDimensionalOrbit.calculate_orbital_elements(self.dep_r, self.dep_v)
        
        self.dep_orbital_parameters = TwoBodyProblem.calculate_orbital_parameters(self.dep_r, self.dep_v)
        
        # ? Init Arrival Orbit
        
        ThreeDimensionalOrbit.set_celestial_body(self.arr_body)
        
        TwoBodyProblem.set_celestial_body(self.arr_body)
        
        self.arr_orbital_elements = ThreeDimensionalOrbit.calculate_orbital_elements(self.arr_r, self.arr_v)
        
        self.arr_orbital_parameters = TwoBodyProblem.calculate_orbital_parameters(self.arr_r, self.arr_v)
    
    def set_update_with_canvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
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
        
        self.init_transfer_figure()
    
    # --- PUBLIC SLOTS 
    
    @qtCore.Slot()
    def fill_departure_orbit(self) -> None:
        """Fills the GUI with the departure orbit parameters
        """
        
        self.orbit.update_central_body(index_from_celestial_body(self.dep_body))
        self.orbit.update_state(self.dep_state)
        self.orbit.update_cartesian_parameters(self.dep_r, self.dep_v)
        self.orbit.update_keplerian_parameters(self.dep_orbital_elements)
        self.orbit.update_modified_keplerian_parameters(self.dep_orbital_elements, self.dep_orbital_parameters)
    
    @qtCore.Slot()
    def fill_arrival_orbit(self) -> None:
        """Fills the GUI with the arrival orbit parameters
        """
        
        self.orbit.update_central_body(index_from_celestial_body(self.arr_body))
        self.orbit.update_state(self.arr_state)
        self.orbit.update_cartesian_parameters(self.arr_r, self.arr_v)
        self.orbit.update_keplerian_parameters(self.arr_orbital_elements)
        self.orbit.update_modified_keplerian_parameters(self.arr_orbital_elements, self.arr_orbital_parameters)
    
    @qtCore.Slot()
    def update_departure_orbit(self) -> None:
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
    def update_arrival_orbit(self) -> None:
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
    def evaluate_departure_orbit(self):
        """Integrates the equations of the departure orbit
        """
        
        TwoBodyProblem.set_celestial_body(self.dep_body)
        
        result = TwoBodyProblem.simulate_relative_motion(np.hstack([self.dep_r, self.dep_v]))
        
        self.plot_orbit(self.dep_figure_orbit, self.dep_body, result)
    
    @qtCore.Slot()
    def evaluate_arrival_orbit(self):
        """Integrates the equations of the arrival orbit
        """
        
        TwoBodyProblem.set_celestial_body(self.arr_body)
        
        result = TwoBodyProblem.simulate_relative_motion(np.hstack([self.arr_r, self.arr_v]))
        
        self.plot_orbit(self.arr_figure_orbit, self.arr_body, result)
    
    @qtCore.Slot()
    def evaluate_departure_ground_track(self):
        """Calculates the ground track of the departure orbit
        """
        
        ThreeDimensionalOrbit.set_celestial_body(self.dep_body)
        
        ra, dec = ThreeDimensionalOrbit.calculate_ground_track(copy.copy(self.dep_orbital_elements), 60)
        
        if len(ra) == 0 or len(dec) == 0:
            
            ra_0, dec_0 = ThreeDimensionalOrbit.calculate_ra_dec(self.dep_r)
            
            ra  = [ra_0]
            dec = [dec_0]
        
        self.plot_ground_track(self.dep_figure_ground_track, self.dep_body, ra, dec)
    
    @qtCore.Slot()
    def evaluate_arrival_ground_track(self):
        """Calculates the ground track of the arrival orbit
        """
        
        ThreeDimensionalOrbit.set_celestial_body(self.arr_body)
        
        ra, dec = ThreeDimensionalOrbit.calculate_ground_track(copy.copy(self.arr_orbital_elements), 60)
        
        if len(ra) == 0 or len(dec) == 0:
            
            ra_0, dec_0 = ThreeDimensionalOrbit.calculate_ra_dec(self.arr_r)
            
            ra  = [ra_0]
            dec = [dec_0]
        
        self.plot_ground_track(self.arr_figure_ground_track, self.arr_body, ra, dec)
    
    @qtCore.Slot(result=int)
    def maneuver_count(self) -> int:
        """Retrieves the number of maneuvers
        """
        
        return len(self.maneuvers)
    
    @qtCore.Slot(int, result=Maneuver)
    def maneuver(self, index : int) -> Maneuver:
        """Retrieves the maneuver by index

        Args:
            index (int): Index

        Returns:
            Maneuver: Maneuver
        """
        
        return self.maneuvers[index]
    
    @qtCore.Slot()
    def clear_maneuvers(self) -> None:
        """Clears the maenuvers
        """
        
        self.maneuvers.clear()
        
    @qtCore.Slot(int, int, float)
    def add_maneuver(self, type : int, option : int, optionValue : float) -> None:
        """Adds a new maenuver

        Args:
            type (int): Maneuver type
            option (int): Maneuver option
            optionValue (float): Maneuver option value
        """
        
        self.maneuvers.append(Maneuver(type, option, optionValue))
    
    @qtCore.Slot()
    def simulate(self) -> None:
        """Simulates the orbit transfer
        """
        
        # ? Setup classes
        
        ThreeDimensionalOrbit.set_celestial_body(self.dep_body)
        
        Time.set_celestial_body(self.dep_body)
        
        TwoBodyProblem.set_celestial_body(self.dep_body)
        
        OrbitalManeuvers.set_celestial_body(self.dep_body)
        
        OrbitalManeuvers.set_specific_impulse(self.spacecraft._specific_impulse)
        
        # ? Integrate departure/arrival orbits
        
        dep = TwoBodyProblem.simulate_relative_motion(np.hstack([self.dep_r, self.dep_v]))
        arr = TwoBodyProblem.simulate_relative_motion(np.hstack([self.arr_r, self.arr_v]))
        
        # ? Init transfer orbital elements and parameters
        
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
        
        # ? Integrate transfer orbit segments
        
        tra = dict(y=np.zeros(shape=(6,1))) # * Used only for initialization
        
        for idx, maneuver in enumerate(self.maneuvers):
            
            temp = self.evaluate_maneuver(maneuver, first=idx==0)
            
            tra['y'] = np.append(tra['y'], temp['y'], axis=1)
        
        tra['y'] = np.delete(tra['y'], 0, axis=1) # * Removes the first element
        
        # ? Final position and orbit
        
        r, v = ThreeDimensionalOrbit.pf_2_gef(self.tra_orbital_elements)
        
        fin = TwoBodyProblem.simulate_relative_motion(np.hstack([r, v]))
        
        # ? Plot
        
        self.plot_transfer_orbit(dep['y'], arr['y'], tra['y'], fin['y'])
    
    # --- PRIVATE METHODS 
    
    def init_transfer_figure(self) -> None:
        """Initializes the transfer figure canvas
        """
        
        self.tra_figure_orbit.reset_canvas()
        
        # ? Celestial Body
        
        u, v = np.mgrid[0 : 2 * np.pi : 80j, 0 : np.pi : 40j]
        
        R = AstronomicalData.equatiorial_radius(self.dep_body)
        
        x = R * np.cos(u) * np.sin(v)
        y = R * np.sin(u) * np.sin(v)
        z = R * np.cos(v)
        
        self.tra_figure_orbit.axes.plot_wireframe(x, y, z, color='#F48FB1', lw=0.1)
        
        # ? Settings
        
        self.tra_figure_orbit.axes.grid(False)
        self.tra_figure_orbit.axes.set_xticks([])
        self.tra_figure_orbit.axes.set_yticks([])
        self.tra_figure_orbit.axes.set_zticks([])
        self.tra_figure_orbit.axes.set_xlim3d([-R/2 * 1.2, R/2 * 1.2])
        self.tra_figure_orbit.axes.set_ylim3d([-R/2 * 1.2, R/2 * 1.2])
        self.tra_figure_orbit.axes.set_zlim3d([-R/2 * 1.2, R/2 * 1.2])
        self.tra_figure_orbit.axes.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.xaxis._axinfo["grid"]['color'] = (1,1,1,0)
        self.tra_figure_orbit.axes.yaxis._axinfo["grid"]['color'] = (1,1,1,0)
        self.tra_figure_orbit.axes.zaxis._axinfo["grid"]['color'] = (1,1,1,0)
        
        self.tra_figure_orbit.redraw_canvas()
    
    def plot_orbit(self, orbitFigure : FigureCanvas, celestialBody : CelestialBody, result : dict) -> None:
        """Plots the orbit

        Args:
            orbitFigure (FigureCanvas): Figure canvas
            celestialBody (CelestialBody): Celestial body
            result (dict): Dictionary of the integration result { 't': time, 'y': state vector  }
        """
        
        orbitFigure.reset_canvas()
        
        # ? Max Values
        
        #xMax = 1.25 * max(result['y'][0,:])
        #yMax = 1.25 * max(result['y'][1,:])
        #zMax = 1.25 * max(result['y'][2,:])
        
        #xMin = 1.25 * min(result['y'][0,:])
        #yMin = 1.25 * min(result['y'][1,:])
        #zMin = 1.25 * min(result['y'][2,:])
        
        # ? Plane
        
        #p = mpatches.Rectangle((xMin, yMin), xMax + np.abs(xMin), yMax + np.abs(yMin), fc=(1,1,1,0.1), ec=(1,1,1,1), lw=2)
        
        #orbitFigure.axes.add_patch(p)
        
        #art3d.pathpatch_2d_to_3d(p, z=0, zdir='z')
        
        # ? Axes
        
        #orbitFigure.axes.plot([0, xMax], [0, 0], [0, 0], 'k--')
        #orbitFigure.axes.plot([0, 0], [0, yMax], [0, 0], 'k--')
        #orbitFigure.axes.plot([0, 0], [0, 0], [0, np.max([zMax, AstronomicalData.equatiorial_radius(celestialBody)])], 'k--')
        
        # ? Celestial Body
        
        #orbitFigure.axes.scatter(0, 0, 0, s=1000, c='c')
        
        u, v = np.mgrid[0 : 2 * np.pi : 80j, 0 : np.pi : 40j]
        
        x = AstronomicalData.equatiorial_radius(celestialBody) * np.cos(u) * np.sin(v)
        y = AstronomicalData.equatiorial_radius(celestialBody) * np.sin(u) * np.sin(v)
        z = AstronomicalData.equatiorial_radius(celestialBody) * np.cos(v)
        
        orbitFigure.axes.plot_wireframe(x, y, z, color='#F48FB1', lw=0.1)
        
        # ? Orbit
        
        orbitFigure.axes.plot(result['y'][0,:], result['y'][1,:], result['y'][2,:], color='#90CAF9', label='Orbit', lw=2)
        
        # ? Settings
        
        x_min = np.min(result['y'][0,:])
        x_max = np.max(result['y'][0,:])
        y_min = np.min(result['y'][1,:])
        y_max = np.max(result['y'][1,:])
        z_min = np.min(result['y'][2,:])
        z_max = np.max(result['y'][2,:])
        
        orbitFigure.axes.grid(False)
        orbitFigure.axes.set_xticks([])
        orbitFigure.axes.set_yticks([])
        orbitFigure.axes.set_zticks([])
        orbitFigure.axes.set_xlim3d([x_min * 1.0, x_max * 1.0])
        orbitFigure.axes.set_ylim3d([y_min * 1.0, y_max * 1.0])
        orbitFigure.axes.set_zlim3d([z_min * 1.0, z_max * 1.0])
        orbitFigure.axes.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.xaxis._axinfo["grid"]['color'] = (1,1,1,0)
        orbitFigure.axes.yaxis._axinfo["grid"]['color'] = (1,1,1,0)
        orbitFigure.axes.zaxis._axinfo["grid"]['color'] = (1,1,1,0)
        #orbitFigure.axes.set_xlabel('$x$ [km]')
        #orbitFigure.axes.set_ylabel('$y$ [km]')
        #orbitFigure.axes.set_zlabel('$z$ [km]')
        
        orbitFigure.redraw_canvas()
    
    def plot_ground_track(self, orbitFigure : FigureCanvas, celestialBody : CelestialBody, ra : list, dec : list) -> None:
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
        
        orbitFigure.axes.imshow(img, origin='lower', extent=(-180, 180, -90, 90), alpha=0.5)
        
        temp_ra = []
        temp_dec = []
        prev_ra = ra[0]
        
        for ra_i, dec_i in zip(ra, dec):
            
            if np.abs(ra_i - prev_ra) > 100:
                
                orbitFigure.axes.plot(temp_ra, temp_dec, c='#90CAF9')
                
                temp_ra.clear()
                temp_dec.clear()
            
            else:
                
                temp_ra.append(ra_i)
                temp_dec.append(dec_i)
            
            prev_ra = ra_i
        
        if len(temp_ra) > 0: orbitFigure.axes.plot(temp_ra, temp_dec, c='#90CAF9')
        
        orbitFigure.axes.scatter(ra[0], dec[0], c='#E6EE9C', label='Start', s=50)
        orbitFigure.axes.scatter(ra[-1], dec[-1], c='#F48FB1', label='Finish', s=50)
        #orbitFigure.axes.set_xlabel('Right Ascension [deg]')
        #orbitFigure.axes.set_ylabel('Declination [deg]')
        orbitFigure.axes.set_xlabel(' ')
        orbitFigure.axes.set_title('Declination [deg] vs Right Ascension [deg]')
        orbitFigure.axes.legend(facecolor='#1C1B1F', framealpha=0.75)
        orbitFigure.axes.set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180])
        orbitFigure.axes.set_yticks([-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75, 90])
        orbitFigure.axes.set_xticklabels(['-180 W', '-135 W', '-90 W', '-45 W', '0', '45 E', '90 E', '135 E', '180 E'])
        orbitFigure.axes.set_yticklabels(['-90 S', '-75 S', '-60 S', '-45 S', '-30 S', '-15 S', '0', '15 N', '30 N', '45 N', '60 N', '75 N', '90 N'])
        #orbitFigure.axes.set_xlim([0, 360])
        #orbitFigure.axes.set_ylim([-90, 90])
        
        mplcyberpunk.make_lines_glow(orbitFigure.axes)
        
        orbitFigure.redraw_canvas()
    
    def plot_transfer_orbit(self, dep : np.ndarray, arr : np.ndarray, tra : np.ndarray, fin : np.ndarray) -> None:
        """Plots the transfer orbit

        Args:
            dep (np.ndarray): Departure orbit
            arr (np.ndarray): Arrival orbit
            tra (np.ndarray): Transfer orbit segments
            fin (np.ndarray): Final orbit
        """
        
        self.tra_figure_orbit.reset_canvas()
        
        # ? Celestial Body
        
        u, v = np.mgrid[0 : 2 * np.pi : 80j, 0 : np.pi : 40j]
        
        R = AstronomicalData.equatiorial_radius(self.dep_body)
        
        x = R * np.cos(u) * np.sin(v)
        y = R * np.sin(u) * np.sin(v)
        z = R * np.cos(v)
        
        self.tra_figure_orbit.axes.plot_wireframe(x, y, z, color='#F48FB1', lw=0.1)
        
        # ? Orbits and positions
        
        self.tra_figure_orbit.axes.scatter(dep[0,0], dep[1,0], dep[2,0], c='#90CAF9', s=50, label='Departure Position')
        self.tra_figure_orbit.axes.scatter(arr[0,0], arr[1,0], arr[2,0], c='#FFAB91', s=50, label='Arrival Position')
        self.tra_figure_orbit.axes.scatter(tra[0,-1], tra[1,-1], tra[2,-1], c='#A5D6A7', s=50, label='Final Position')
        self.tra_figure_orbit.axes.plot(dep[0,:], dep[1,:], dep[2,:], color='#90CAF9', linestyle='dashed', linewidth='2', label='Departure Orbit')
        self.tra_figure_orbit.axes.plot(arr[0,:], arr[1,:], arr[2,:], color='#FFAB91', linestyle='dashed', linewidth='2', label='Arrival Orbit')
        #self.tra_figure_orbit.axes.plot(fin[0,:], fin[1,:], fin[2,:], color='#CE93D8', linestyle='dashed', linewidth='1', label='Final Orbit')
        self.tra_figure_orbit.axes.plot(tra[0,:], tra[1,:], tra[2,:], color='#A5D6A7', label='Transfer Trajectory')
        
        # ? Settings
        
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        z_min = 0
        z_max = 0
        
        if tra.size == 0:
            
            x_min = np.min([np.min(dep[0,:]), np.min(arr[0,:]), np.min(fin[0,:]), 0])
            x_max = np.max([np.max(dep[0,:]), np.max(arr[0,:]), np.max(fin[0,:]), 0])
            y_min = np.min([np.min(dep[1,:]), np.min(arr[1,:]), np.min(fin[1,:]), 0])
            y_max = np.max([np.max(dep[1,:]), np.max(arr[1,:]), np.max(fin[1,:]), 0])
            z_min = np.min([np.min(dep[2,:]), np.min(arr[2,:]), np.min(fin[2,:]), 0])
            z_max = np.max([np.max(dep[2,:]), np.max(arr[2,:]), np.max(fin[2,:]), 0])
            
        else:
        
            x_min = np.min([np.min(dep[0,:]), np.min(arr[0,:]), np.min(fin[0,:]), np.min(tra[0,:])])
            x_max = np.max([np.max(dep[0,:]), np.max(arr[0,:]), np.max(fin[0,:]), np.max(tra[0,:])])
            y_min = np.min([np.min(dep[1,:]), np.min(arr[1,:]), np.min(fin[1,:]), np.min(tra[1,:])])
            y_max = np.max([np.max(dep[1,:]), np.max(arr[1,:]), np.max(fin[1,:]), np.max(tra[1,:])])
            z_min = np.min([np.min(dep[2,:]), np.min(arr[2,:]), np.min(fin[2,:]), np.min(tra[2,:])])
            z_max = np.max([np.max(dep[2,:]), np.max(arr[2,:]), np.max(fin[2,:]), np.max(tra[2,:])])
        
        self.tra_figure_orbit.axes.grid(False)
        self.tra_figure_orbit.axes.legend()
        #self.tra_figure_orbit.axes.legend(bbox_to_anchor=(-0.5, 0.5), loc='center left')
        self.tra_figure_orbit.axes.set_xticks([])
        self.tra_figure_orbit.axes.set_yticks([])
        self.tra_figure_orbit.axes.set_zticks([])
        self.tra_figure_orbit.axes.set_xlim3d([x_min * 0.7, x_max * 0.7])
        self.tra_figure_orbit.axes.set_ylim3d([y_min * 0.7, y_max * 0.7])
        self.tra_figure_orbit.axes.set_zlim3d([z_min * 0.7, z_max * 0.7])
        self.tra_figure_orbit.axes.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.xaxis._axinfo["grid"]['color'] = (1,1,1,0)
        self.tra_figure_orbit.axes.yaxis._axinfo["grid"]['color'] = (1,1,1,0)
        self.tra_figure_orbit.axes.zaxis._axinfo["grid"]['color'] = (1,1,1,0)
        
        self.tra_figure_orbit.redraw_canvas()
    
    def evaluate_maneuver(self, maneuver : Maneuver, first : bool = False) -> dict:
        """Evaluates and integrates the maneuver from the list

        Args:
            maneuver (Maneuver): Maneuver
            first (bool, optional): True for the first maneuver. Defaults to False.

        Returns:
            dict: Integration result
        """
        
        result  = dict(y=np.zeros(shape=(6,1)))
        dt      = 0.0
        
        match maneuver.type:
            
            case ManeuverType.HOHMANN:
                
                # ? Angles
                
                theta_0 = 0 if maneuver.option == HohmannDirection.PER2APO else np.pi
                theta_f = np.pi if maneuver.option == HohmannDirection.PER2APO else 0
                
                # ? Maneuver
                
                maneuver_result = OrbitalManeuvers.hohmann_transfer(self.tra_orbital_parameters.r_p,
                                                                    self.tra_orbital_parameters.r_a,
                                                                    self.arr_orbital_parameters.r_p,
                                                                    self.arr_orbital_parameters.r_a,
                                                                    maneuver.option,
                                                                    self.spacecraft.mass)
                
                maneuver_result.oe.i     = self.tra_orbital_elements.i
                maneuver_result.oe.Omega = self.tra_orbital_elements.Omega
                maneuver_result.oe.omega = self.tra_orbital_elements.omega
                maneuver_result.oe.theta = theta_0
                
                # ? Integrate from current point to maneuver starting point
                
                temp_1 = self.integrate_maneuver(self.tra_orbital_elements, self.tra_orbital_elements.theta, theta_0)
                    
                dt += temp_1['dt']
                
                # ? Integrate from maneuver starting point to ending point
                
                temp_2 = self.integrate_maneuver(maneuver_result.oe, theta_0, theta_f)
                    
                dt += temp_2['dt']
            
                result['y'] = np.append(temp_1['y'], temp_2['y'], axis=1)
                
                # ? Update transfer orbit
                
                self.tra_orbital_elements.h     = self.arr_orbital_elements.h
                self.tra_orbital_elements.e     = self.arr_orbital_elements.e
                self.tra_orbital_elements.a     = self.arr_orbital_elements.a
                self.tra_orbital_elements.theta = theta_f
                
                self.tra_orbital_parameters.r_p = self.arr_orbital_parameters.r_p
                self.tra_orbital_parameters.r_a = self.arr_orbital_parameters.r_a
                
                # ? Budget
                
                maneuver.delta_velocity = maneuver_result.dv
                maneuver.delta_time     = dt / 3600
                maneuver.delta_mass     = maneuver_result.dm
                
                self.spacecraft.update_mass(maneuver_result.dm)
                
            case ManeuverType.BI_ELLIPTIC_HOHMANN:
                
                # ? Angles
                
                theta_0_1 = 0 if maneuver.option == HohmannDirection.PER2APO else np.pi
                theta_f_1 = np.pi if maneuver.option == HohmannDirection.PER2APO else 0
                theta_0_2 = np.pi if maneuver.option == HohmannDirection.PER2APO else 0
                theta_f_2 = 0 if maneuver.option == HohmannDirection.PER2APO else np.pi
                
                # ? Maneuver
                
                maneuver_result_1, maneuver_result_2 = OrbitalManeuvers.bi_elliptic_hohmann_transfer(self.tra_orbital_parameters.r_p,
                                                                                                     self.tra_orbital_parameters.r_a,
                                                                                                     self.arr_orbital_parameters.r_p,
                                                                                                     self.arr_orbital_parameters.r_a,
                                                                                                     maneuver.option_value,
                                                                                                     maneuver.option,
                                                                                                     self.spacecraft.mass)
                
                maneuver_result_1.oe.i       = self.tra_orbital_elements.i
                maneuver_result_1.oe.Omega   = self.tra_orbital_elements.Omega
                maneuver_result_1.oe.omega   = self.tra_orbital_elements.omega
                maneuver_result_1.oe.theta   = theta_0_1
                
                maneuver_result_2.oe.i       = self.tra_orbital_elements.i
                maneuver_result_2.oe.Omega   = self.tra_orbital_elements.Omega
                maneuver_result_2.oe.omega   = self.tra_orbital_elements.omega
                maneuver_result_2.oe.theta   = theta_0_2
                
                # ? Integrate from current point to maneuver starting point (1st arc)
                
                temp_1 = self.integrate_maneuver(self.tra_orbital_elements, self.tra_orbital_elements.theta, theta_0_1)
                    
                dt += temp_1['dt']
                
                # ? Integrate from maneuver starting point (1st arc) to ending point (1st arc)
                
                temp_2 = self.integrate_maneuver(maneuver_result_1.oe, theta_0_1, theta_f_1)
                    
                dt += temp_2['dt']
                
                # ? Integrate from maneuver starting point (2nd arc) to ending point (2nd arc)
                
                temp_3 = self.integrate_maneuver(maneuver_result_2.oe, theta_0_2, theta_f_2)
                
                dt += temp_3['dt']
                
                result['y'] = np.append(temp_1['y'], temp_2['y'], axis=1)
                result['y'] = np.append(result['y'], temp_3['y'], axis=1)
                
                # ? Update transfer orbit
                
                self.tra_orbital_elements.h     = self.arr_orbital_elements.h
                self.tra_orbital_elements.e     = self.arr_orbital_elements.e
                self.tra_orbital_elements.a     = self.arr_orbital_elements.a
                self.tra_orbital_elements.theta = theta_f_2
                
                self.tra_orbital_parameters.r_p = self.arr_orbital_parameters.r_p
                self.tra_orbital_parameters.r_a = self.arr_orbital_parameters.r_a
                
                # ? Budget
                
                maneuver.delta_velocity = maneuver_result_1.dv + maneuver_result_2.dv
                maneuver.delta_time     = dt / 3600
                maneuver.delta_mass     = maneuver_result_1.dm + maneuver_result_2.dm
                
                self.spacecraft.update_mass(maneuver_result_1.dm + maneuver_result_2.dm)
            
            case ManeuverType.PLANE_CHANGE:
                
                # ? Maneuver
                
                maneuver_result = OrbitalManeuvers.plane_change_maneuver_2(self.tra_orbital_parameters.r_p,
                                                                           self.tra_orbital_parameters.r_a,
                                                                           self.tra_orbital_elements.Omega,
                                                                           self.tra_orbital_elements.omega,
                                                                           self.tra_orbital_elements.i,
                                                                           self.arr_orbital_elements.Omega,
                                                                           self.arr_orbital_elements.i,
                                                                           self.spacecraft.mass)
                
                maneuver_result.oe.h = self.tra_orbital_elements.h
                maneuver_result.oe.e = self.tra_orbital_elements.e
                maneuver_result.oe.a = self.tra_orbital_elements.a
                
                # ? Integrate from current point to maneuver point
                
                result = self.integrate_maneuver(self.tra_orbital_elements, self.tra_orbital_elements.theta, maneuver_result.oe.theta)
                    
                dt += result['dt']
                
                # ? Update transfer orbit
                
                self.tra_orbital_elements.i     = maneuver_result.oe.i
                self.tra_orbital_elements.Omega = maneuver_result.oe.Omega
                self.tra_orbital_elements.omega = maneuver_result.oe.omega
                self.tra_orbital_elements.theta = maneuver_result.oe.theta
                
                # ? Budget
                
                maneuver.delta_velocity = maneuver_result.dv
                maneuver.delta_time     = dt / 3600 + maneuver_result.dt / 3600 # * The maneuver time is 0
                maneuver.delta_mass     = maneuver_result.dm
                
                self.spacecraft.update_mass(maneuver_result.dm)
            
            case ManeuverType.APSE_LINE_ROTATION:
                
                # ? Maneuver
                
                maneuver_result = OrbitalManeuvers.apse_line_rotation_from_eta(self.tra_orbital_parameters.r_p,
                                                                               self.tra_orbital_parameters.r_a,
                                                                               self.tra_orbital_parameters.r_p,
                                                                               self.tra_orbital_parameters.r_a,
                                                                               self.arr_orbital_elements.omega - self.tra_orbital_elements.omega,
                                                                               secondIntersectionPoint=maneuver.option==1,
                                                                               m=self.spacecraft.mass)
                
                # ? Integrate from current point to maneuver point
                
                result = self.integrate_maneuver(self.tra_orbital_elements, self.tra_orbital_elements.theta, maneuver_result.oe.theta)
                    
                dt += result['dt']
                
                # ? Update transfer orbit
                
                self.tra_orbital_elements.omega = self.arr_orbital_elements.omega
                self.tra_orbital_elements.theta = maneuver_result.oe.theta
                
                print(self.tra_orbital_elements)
                
                # * Budget
                
                maneuver.delta_velocity = maneuver_result.dv
                maneuver.delta_time     = dt / 3600 + maneuver_result.dt / 3600 # * The maneuver time is 0
                maneuver.delta_mass     = maneuver_result.dm
                
                self.spacecraft.update_mass(maneuver_result.dm)
        
        return result
    
    def integrate_maneuver(self, oe : OrbitalElements, theta_0 : float, theta_f : float) -> dict:
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
    