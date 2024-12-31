""" mission_orbit_transfer.py: Implements the orbit transfer mission """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np
import copy

from PIL import Image

from src.utility.figure_canvas import FigureCanvas
from systems.spacecraft import Spacecraft
from src.utility.orbit import Orbit, StateType
from src.utility.maneuver import Maneuver, ManeuverType

from tools.AstronomicalData import AstronomicalData, CelestialBody, index_from_celestial_body
from tools.TwoBodyProblem import TwoBodyProblem, OrbitalParameters
from tools.ThreeDimensionalOrbit import ThreeDimensionalOrbit, OrbitalElements
from tools.Time import Time, DirectionType
from tools.OrbitalManeuvers import OrbitalManeuvers, HohmannDirection

class MissionOrbitTransfer(qtCore.QObject):
    """Manages the orbit transfer mission"""
    
    # --- PROPERTIES 
    
    # ? Departure Orbit
    
    @qtCore.Property(Orbit)
    def dep_orbit(self): return self._dep_orbit
    
    @dep_orbit.setter
    def dep_orbit(self, val : Orbit): self._dep_orbit = val
    
    # ? Arrival Orbit
    
    @qtCore.Property(Orbit)
    def arr_orbit(self): return self._arr_orbit
    
    @arr_orbit.setter
    def arr_orbit(self, val : Orbit): self._arr_orbit = val
    
    # --- PUBLIC METHODS 
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        self.engine = engine
        
        engine.rootContext().setContextProperty("__MissionOrbitTransfer", self)
        
        self.spacecraft = Spacecraft(engine)
        
        # ? Celestial Body
        
        body = CelestialBody.EARTH  # * Celestial body
        
        ThreeDimensionalOrbit.set_celestial_body(body)
        
        TwoBodyProblem.set_celestial_body(body)
        
        # ? Departure orbit
        
        self.dep_figure_orbit           = FigureCanvas(dof3=True)   # * Orbit figure
        self.dep_figure_ground_track    = FigureCanvas()            # * Ground track figure
        self._dep_orbit                 = Orbit()                   # * Orbit
        
        r = np.array([-8173.55640, -3064.65060, -2840.15350], dtype=float)  # * Position vector     [ km ]
        v = np.array([-3.07330000, 5.94440000, -1.54740000], dtype=float)   # * Velocity vector     [ km / s ]
        
        self._dep_orbit.update_central_body(index_from_celestial_body(CelestialBody.EARTH))
        self._dep_orbit.update_state(StateType.CARTESIAN)
        self._dep_orbit.update_cartesian_parameters(r, v)
        self._dep_orbit.update_keplerian_parameters(ThreeDimensionalOrbit.calculate_orbital_elements(r, v))
        self._dep_orbit.update_modified_keplerian_parameters(ThreeDimensionalOrbit.calculate_orbital_elements(r, v), TwoBodyProblem.calculate_orbital_parameters(r, v))
        
        # ? Arrival orbit
        
        self.arr_figure_orbit           = FigureCanvas(dof3=True)   # * Orbit figure
        self.arr_figure_ground_track    = FigureCanvas()            # * Ground track figure
        self.arr_orbit                  = Orbit()                   # * Orbit
        
        r = np.array([4571.13653, 32940.33361, -14208.95231], dtype=float)  # * Position vector     [ km ]
        v = np.array([-3.06192709, 1.01383552, 0.41402772], dtype=float)    # * Velocity vector     [ km / s ]
        
        self._arr_orbit.update_central_body(index_from_celestial_body(CelestialBody.EARTH))
        self._arr_orbit.update_state(StateType.CARTESIAN)
        self._arr_orbit.update_cartesian_parameters(r, v)
        self._arr_orbit.update_keplerian_parameters(ThreeDimensionalOrbit.calculate_orbital_elements(r, v))
        self._arr_orbit.update_modified_keplerian_parameters(ThreeDimensionalOrbit.calculate_orbital_elements(r, v), TwoBodyProblem.calculate_orbital_parameters(r, v))
        
        # ? Tranfer orbit
        
        self.tra_orbital_parameters     = OrbitalParameters()       # * Orbital parameters
        self.tra_orbital_elements       = OrbitalElements()         # * Orbital elements
        self.tra_figure_orbit           = FigureCanvas(dof3=True)   # * Orbit figure
        self.maneuvers                  = list()                    # * List of orbital maneuvers
        
        # ? Context properties
        
        engine.rootContext().setContextProperty("__DepartureOrbitFigure", self.dep_figure_orbit)
        engine.rootContext().setContextProperty("__DepartureGroundTrackFigure", self.dep_figure_ground_track)
        engine.rootContext().setContextProperty("__ArrivalOrbitFigure", self.arr_figure_orbit)
        engine.rootContext().setContextProperty("__ArrivalGroundTrackFigure", self.arr_figure_ground_track)
        engine.rootContext().setContextProperty("__OrbitTransferFigure", self.tra_figure_orbit)
        
        # ? Simulation Results
        
        self.result_dep = np.array([0])    # * Simulation Result for Departure Orbit
        self.result_arr = np.array([0])    # * Simulation Result for Arrival Orbit
        self.result_tra = np.array([0])    # * Simulation Result for Transfer Orbit
        self.result_fin = np.array([0])    # * Simulation Result for Final Orbit
    
    # --- PUBLIC SLOTS 
    
    @qtCore.Slot()
    def attach_canvas(self) -> None:
        """Connects all the QML figures with the backend model
        """
        
        win = self.engine.rootObjects()[0]
    
        self.dep_figure_orbit.update_with_canvas(win.findChild(qtCore.QObject, "DepartureOrbitFigure"), win.findChild(qtCore.QObject, "DepartureOrbitFigureParent"))
        self.dep_figure_ground_track.update_with_canvas(win.findChild(qtCore.QObject, "DepartureGroundTrackFigure"), win.findChild(qtCore.QObject, "DepartureGroundTrackFigureParent"))
        self.arr_figure_orbit.update_with_canvas(win.findChild(qtCore.QObject, "ArrivalOrbitFigure"), win.findChild(qtCore.QObject, "ArrivalOrbitFigureParent"))
        self.arr_figure_ground_track.update_with_canvas(win.findChild(qtCore.QObject, "ArrivalGroundTrackFigure"), win.findChild(qtCore.QObject, "ArrivalGroundTrackFigureParent"))
        self.tra_figure_orbit.update_with_canvas(win.findChild(qtCore.QObject, "OrbitTransferFigure"), win.findChild(qtCore.QObject, "OrbitTransferFigureParent"))
    
        self.init_transfer_figure()
    
    @qtCore.Slot()
    def detach_canvas(self) -> None:
        """Disconnects all the QML figures from the backend model
        """
        
        self.dep_figure_orbit           = FigureCanvas(dof3=True)
        self.dep_figure_ground_track    = FigureCanvas()
        self.arr_figure_orbit           = FigureCanvas(dof3=True)
        self.arr_figure_ground_track    = FigureCanvas()
        self.tra_figure_orbit           = FigureCanvas(dof3=True)
        
        self.engine.rootContext().setContextProperty("__DepartureOrbitFigure", self.dep_figure_orbit)
        self.engine.rootContext().setContextProperty("__DepartureGroundTrackFigure", self.dep_figure_ground_track)
        self.engine.rootContext().setContextProperty("__ArrivalOrbitFigure", self.arr_figure_orbit)
        self.engine.rootContext().setContextProperty("__ArrivalGroundTrackFigure", self.arr_figure_ground_track)
        self.engine.rootContext().setContextProperty("__OrbitTransferFigure", self.tra_figure_orbit)
    
    @qtCore.Slot()
    def update_celestial_body(self) -> None:
        """Updates the celestial body
        """
        
        ThreeDimensionalOrbit.set_celestial_body(self._dep_orbit.get_celestial_body())
        
        TwoBodyProblem.set_celestial_body(self._dep_orbit.get_celestial_body())
        
        Time.set_celestial_body(self._dep_orbit.get_celestial_body())

        OrbitalManeuvers.set_celestial_body(self._dep_orbit.get_celestial_body())
    
    @qtCore.Slot()
    def update_departure_orbit(self) -> None:
        """Updates the departure orbit parameters
        """
        
        match self._dep_orbit.state:
            
            case StateType.CARTESIAN:
                
                r, v = self._dep_orbit.get_cartesian_parameters()                
                
                self._dep_orbit.update_keplerian_parameters(ThreeDimensionalOrbit.calculate_orbital_elements(r, v))
                self._dep_orbit.update_modified_keplerian_parameters(ThreeDimensionalOrbit.calculate_orbital_elements(r, v), TwoBodyProblem.calculate_orbital_parameters(r, v))
            
            case StateType.KEPLERIAN:
                
                orbital_elements = self._dep_orbit.get_keplerian_parameters()
                
                self._dep_orbit.update_cartesian_parameters(ThreeDimensionalOrbit.pf_2_gef(orbital_elements))
                self._dep_orbit.update_modified_keplerian_parameters(orbital_elements, TwoBodyProblem.calculate_orbital_parameters(ThreeDimensionalOrbit.pf_2_gef(orbital_elements)))
            
            case StateType.MODIFIED_KEPLERIAN:
                
                self.orbit.update_keplerian_parameters_from_radii()
                
                orbital_elements = self._dep_orbit.get_keplerian_parameters()
                
                self._dep_orbit.update_cartesian_parameters(ThreeDimensionalOrbit.pf_2_gef(orbital_elements))
            
            case _:
                
                pass
    
    @qtCore.Slot()
    def update_arrival_orbit(self) -> None:
        """Updates the arrival orbit parameters
        """
        
        match self._arr_orbit.state:
            
            case StateType.CARTESIAN:
                
                r, v = self._arr_orbit.get_cartesian_parameters()                
                
                self._arr_orbit.update_keplerian_parameters(ThreeDimensionalOrbit.calculate_orbital_elements(r, v))
                self._arr_orbit.update_modified_keplerian_parameters(ThreeDimensionalOrbit.calculate_orbital_elements(r, v), TwoBodyProblem.calculate_orbital_parameters(r, v))
            
            case StateType.KEPLERIAN:
                
                orbital_elements = self._arr_orbit.get_keplerian_parameters()
                
                self._arr_orbit.update_cartesian_parameters(ThreeDimensionalOrbit.pf_2_gef(orbital_elements))
                self._arr_orbit.update_modified_keplerian_parameters(orbital_elements, TwoBodyProblem.calculate_orbital_parameters(ThreeDimensionalOrbit.pf_2_gef(orbital_elements)))
            
            case StateType.MODIFIED_KEPLERIAN:
                
                self.orbit.update_keplerian_parameters_from_radii()
                
                orbital_elements = self._arr_orbit.get_keplerian_parameters()
                
                self._arr_orbit.update_cartesian_parameters(ThreeDimensionalOrbit.pf_2_gef(orbital_elements))
            
            case _:
                
                pass
    
    @qtCore.Slot()
    def evaluate_departure_orbit(self):
        """Integrates the equations of the departure orbit
        """
        
        TwoBodyProblem.set_celestial_body(self._dep_orbit.get_celestial_body())
        
        result = TwoBodyProblem.simulate_relative_motion(np.hstack(self._dep_orbit.get_cartesian_parameters()))
        
        self.plot_orbit(self.dep_figure_orbit, self._dep_orbit.get_celestial_body(), result)
    
    @qtCore.Slot()
    def evaluate_arrival_orbit(self):
        """Integrates the equations of the arrival orbit
        """
        
        TwoBodyProblem.set_celestial_body(self._arr_orbit.get_celestial_body())
        
        result = TwoBodyProblem.simulate_relative_motion(np.hstack(self._arr_orbit.get_cartesian_parameters()))
        
        self.plot_orbit(self.arr_figure_orbit, self._arr_orbit.get_celestial_body(), result)
    
    @qtCore.Slot()
    def evaluate_departure_ground_track(self):
        """Calculates the ground track of the departure orbit
        """
        
        ThreeDimensionalOrbit.set_celestial_body(self._dep_orbit.get_celestial_body())
        
        ra, dec = ThreeDimensionalOrbit.calculate_ground_track(copy.copy(self._dep_orbit.get_keplerian_parameters()), 60)
        
        if len(ra) == 0 or len(dec) == 0:
            
            ra_0, dec_0 = ThreeDimensionalOrbit.calculate_ra_dec(self._dep_orbit.get_cartesian_parameters()[0])
            
            ra  = [ra_0]
            dec = [dec_0]
        
        self.plot_ground_track(self.dep_figure_ground_track, self._dep_orbit.get_celestial_body(), ra, dec)
    
    @qtCore.Slot()
    def evaluate_arrival_ground_track(self):
        """Calculates the ground track of the arrival orbit
        """
        
        ThreeDimensionalOrbit.set_celestial_body(self._arr_orbit.get_celestial_body())
        
        ra, dec = ThreeDimensionalOrbit.calculate_ground_track(copy.copy(self._arr_orbit.get_keplerian_parameters()), 60)
        
        if len(ra) == 0 or len(dec) == 0:
            
            ra_0, dec_0 = ThreeDimensionalOrbit.calculate_ra_dec(self._arr_orbit.get_cartesian_parameters()[0])
            
            ra  = [ra_0]
            dec = [dec_0]
        
        self.plot_ground_track(self.arr_figure_ground_track, self._arr_orbit.get_celestial_body(), ra, dec)
    
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
        
        ThreeDimensionalOrbit.set_celestial_body(self._dep_orbit.get_celestial_body())
        
        Time.set_celestial_body(self._dep_orbit.get_celestial_body())
        
        TwoBodyProblem.set_celestial_body(self._dep_orbit.get_celestial_body())
        
        OrbitalManeuvers.set_celestial_body(self._dep_orbit.get_celestial_body())
        OrbitalManeuvers.set_specific_impulse(self.spacecraft._specific_impulse)
        
        # ? Integrate departure/arrival orbits
        
        dep = TwoBodyProblem.simulate_relative_motion(np.hstack(self._dep_orbit.get_cartesian_parameters()))
        arr = TwoBodyProblem.simulate_relative_motion(np.hstack(self._arr_orbit.get_cartesian_parameters()))
        
        self.result_dep = dep['y']
        self.result_arr = arr['y']
        
        # ? Init transfer orbital elements and parameters
        
        self.tra_orbital_elements.h     = self._dep_orbit._specific_angular_momentum
        self.tra_orbital_elements.e     = self._dep_orbit._eccentricity
        self.tra_orbital_elements.i     = self._dep_orbit._inclination
        self.tra_orbital_elements.Omega = self._dep_orbit._right_ascension_ascending_node
        self.tra_orbital_elements.omega = self._dep_orbit._periapsis_anomaly
        self.tra_orbital_elements.theta = self._dep_orbit._true_anomaly
        self.tra_orbital_elements.a     = self._dep_orbit._semi_major_axis
        
        self.tra_orbital_parameters.r_p = self._dep_orbit._periapsis_radius
        self.tra_orbital_parameters.r_a = self._dep_orbit._apoapsis_radius
        
        self.spacecraft.reset()
        
        # ? Integrate transfer orbit segments
        
        tra = dict(y=np.zeros(shape=(6,1))) # * Used only for initialization
        
        for idx, maneuver in enumerate(self.maneuvers):
            
            temp = self.evaluate_maneuver(maneuver, first=idx==0)
            
            tra['y'] = np.append(tra['y'], temp['y'], axis=1)
        
        tra['y'] = np.delete(tra['y'], 0, axis=1) # * Removes the first element
        
        self.result_tra = tra['y']
        
        # ? Final position and orbit
        
        r, v = ThreeDimensionalOrbit.pf_2_gef(self.tra_orbital_elements)
        
        fin = TwoBodyProblem.simulate_relative_motion(np.hstack([r, v]))
        
        self.result_fin = fin['y']
        
        # ? Plot
        
        self.plot_transfer_orbit()
    
    # --- PRIVATE METHODS 
    
    def init_transfer_figure(self) -> None:
        """Initializes the transfer figure canvas
        """
        
        self.tra_figure_orbit.reset_canvas()
        
        # ? Celestial Body
        
        u, v = np.mgrid[0 : 2 * np.pi : 80j, 0 : np.pi : 40j]
        
        R = AstronomicalData.equatiorial_radius(self._dep_orbit.get_celestial_body())
        
        x = R * np.cos(u) * np.sin(v)
        y = R * np.sin(u) * np.sin(v)
        z = R * np.cos(v)
        
        self.tra_figure_orbit.axes.plot_wireframe(x, y, z, color='#FFFFFF', lw=0.1)
        
        # ? Settings
        
        self.tra_figure_orbit.axes.grid(False)
        self.tra_figure_orbit.axes.set_xticks([])
        self.tra_figure_orbit.axes.set_yticks([])
        self.tra_figure_orbit.axes.set_zticks([])
        self.tra_figure_orbit.axes.set_xlim3d([-R/2 * 1.2, R/2 * 1.2])
        self.tra_figure_orbit.axes.set_ylim3d([-R/2 * 1.2, R/2 * 1.2])
        self.tra_figure_orbit.axes.set_zlim3d([-R/2 * 1.2, R/2 * 1.2])
        self.tra_figure_orbit.axes.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.xaxis._axinfo["grid"]['color'] = (1,1,1,0)
        self.tra_figure_orbit.axes.yaxis._axinfo["grid"]['color'] = (1,1,1,0)
        self.tra_figure_orbit.axes.zaxis._axinfo["grid"]['color'] = (1,1,1,0)
        
        self.tra_figure_orbit.redraw_canvas()
        
        # ? Plot
        
        self.plot_transfer_orbit()
    
    def plot_orbit(self, orbitFigure : FigureCanvas, celestialBody : CelestialBody, result : dict) -> None:
        """Plots the orbit

        Args:
            orbitFigure (FigureCanvas): Figure canvas
            celestialBody (CelestialBody): Celestial body
            result (dict): Dictionary of the integration result { 't': time, 'y': state vector  }
        """
        
        orbitFigure.reset_canvas()
        
        # ? Celestial Body
        
        u, v = np.mgrid[0 : 2 * np.pi : 80j, 0 : np.pi : 40j]
        
        x = AstronomicalData.equatiorial_radius(celestialBody) * np.cos(u) * np.sin(v)
        y = AstronomicalData.equatiorial_radius(celestialBody) * np.sin(u) * np.sin(v)
        z = AstronomicalData.equatiorial_radius(celestialBody) * np.cos(v)
        
        orbitFigure.axes.plot_wireframe(x, y, z, color='#FFFFFF', lw=0.1)
        
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
        orbitFigure.axes.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        orbitFigure.axes.xaxis._axinfo["grid"]['color'] = (1,1,1,0)
        orbitFigure.axes.yaxis._axinfo["grid"]['color'] = (1,1,1,0)
        orbitFigure.axes.zaxis._axinfo["grid"]['color'] = (1,1,1,0)
        
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
                
                orbitFigure.axes.plot(temp_ra, temp_dec, c=FigureCanvas.default_color)
                
                temp_ra.clear()
                temp_dec.clear()
            
            else:
                
                temp_ra.append(ra_i)
                temp_dec.append(dec_i)
            
            prev_ra = ra_i
        
        if len(temp_ra) > 0: orbitFigure.axes.plot(temp_ra, temp_dec, c=FigureCanvas.default_color)
        
        orbitFigure.axes.scatter(ra[0], dec[0], c='#E6EE9C', label='Start', s=50)
        orbitFigure.axes.scatter(ra[-1], dec[-1], c='#F48FB1', label='Finish', s=50)
        orbitFigure.axes.set_xlabel('Right Ascension [deg]')
        orbitFigure.axes.set_ylabel('Declination [deg]')
        orbitFigure.axes.legend(facecolor='#1C1B1F', framealpha=0.75)
        orbitFigure.axes.set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180])
        orbitFigure.axes.set_yticks([-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75, 90])
        orbitFigure.axes.set_xticklabels(['-180 W', '-135 W', '-90 W', '-45 W', '0', '45 E', '90 E', '135 E', '180 E'])
        orbitFigure.axes.set_yticklabels(['-90 S', '-75 S', '-60 S', '-45 S', '-30 S', '-15 S', '0', '15 N', '30 N', '45 N', '60 N', '75 N', '90 N'])
        #orbitFigure.axes.set_xlim([0, 360])
        #orbitFigure.axes.set_ylim([-90, 90])
        
        #mplcyberpunk.make_lines_glow(orbitFigure.axes)
        
        orbitFigure.redraw_canvas(glow_effect=False)
    
    def plot_transfer_orbit(self) -> None:
        """Plots the transfer orbit
        """
        
        if self.result_dep.size == 1: return
        
        self.tra_figure_orbit.reset_canvas()
        
        # ? Celestial Body
        
        u, v = np.mgrid[0 : 2 * np.pi : 80j, 0 : np.pi : 40j]
        
        R = AstronomicalData.equatiorial_radius(self._dep_orbit.get_celestial_body())
        
        x = R * np.cos(u) * np.sin(v)
        y = R * np.sin(u) * np.sin(v)
        z = R * np.cos(v)
        
        self.tra_figure_orbit.axes.plot_wireframe(x, y, z, color='#FFFFFF', lw=0.1)
        
        # ? Orbits and positions
        
        self.tra_figure_orbit.axes.scatter(self.result_dep[0,0], self.result_dep[1,0], self.result_dep[2,0], c='#90CAF9', s=50, label='Departure Position')
        self.tra_figure_orbit.axes.scatter(self.result_arr[0,0], self.result_arr[1,0], self.result_arr[2,0], c='#FFAB91', s=50, label='Arrival Position')
        if self.result_tra.size > 0: self.tra_figure_orbit.axes.scatter(self.result_tra[0,-1], self.result_tra[1,-1], self.result_tra[2,-1], c='#A5D6A7', s=50, label='Final Position')
        self.tra_figure_orbit.axes.plot(self.result_dep[0,:], self.result_dep[1,:], self.result_dep[2,:], color='#90CAF9', linestyle='dashed', linewidth='2', label='Departure Orbit')
        self.tra_figure_orbit.axes.plot(self.result_arr[0,:], self.result_arr[1,:], self.result_arr[2,:], color='#FFAB91', linestyle='dashed', linewidth='2', label='Arrival Orbit')
        #self.tra_figure_orbit.axes.plot(self.result_fin[0,:], fself.result_in[1,:], self.result_fin[2,:], color='#CE93D8', linestyle='dashed', linewidth='1', label='Final Orbit')
        self.tra_figure_orbit.axes.plot(self.result_tra[0,:], self.result_tra[1,:], self.result_tra[2,:], color='#A5D6A7', label='Transfer Trajectory')
        
        # ? Settings
        
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        z_min = 0
        z_max = 0
        
        if self.result_tra.size == 0:
            
            x_min = np.min([np.min(self.result_dep[0,:]), np.min(self.result_arr[0,:]), np.min(self.result_fin[0,:]), 0])
            x_max = np.max([np.max(self.result_dep[0,:]), np.max(self.result_arr[0,:]), np.max(self.result_fin[0,:]), 0])
            y_min = np.min([np.min(self.result_dep[1,:]), np.min(self.result_arr[1,:]), np.min(self.result_fin[1,:]), 0])
            y_max = np.max([np.max(self.result_dep[1,:]), np.max(self.result_arr[1,:]), np.max(self.result_fin[1,:]), 0])
            z_min = np.min([np.min(self.result_dep[2,:]), np.min(self.result_arr[2,:]), np.min(self.result_fin[2,:]), 0])
            z_max = np.max([np.max(self.result_dep[2,:]), np.max(self.result_arr[2,:]), np.max(self.result_fin[2,:]), 0])
            
        else:
        
            x_min = np.min([np.min(self.result_dep[0,:]), np.min(self.result_arr[0,:]), np.min(self.result_fin[0,:]), np.min(self.result_tra[0,:])])
            x_max = np.max([np.max(self.result_dep[0,:]), np.max(self.result_arr[0,:]), np.max(self.result_fin[0,:]), np.max(self.result_tra[0,:])])
            y_min = np.min([np.min(self.result_dep[1,:]), np.min(self.result_arr[1,:]), np.min(self.result_fin[1,:]), np.min(self.result_tra[1,:])])
            y_max = np.max([np.max(self.result_dep[1,:]), np.max(self.result_arr[1,:]), np.max(self.result_fin[1,:]), np.max(self.result_tra[1,:])])
            z_min = np.min([np.min(self.result_dep[2,:]), np.min(self.result_arr[2,:]), np.min(self.result_fin[2,:]), np.min(self.result_tra[2,:])])
            z_max = np.max([np.max(self.result_dep[2,:]), np.max(self.result_arr[2,:]), np.max(self.result_fin[2,:]), np.max(self.result_tra[2,:])])
        
        self.tra_figure_orbit.axes.grid(False)
        self.tra_figure_orbit.axes.legend(bbox_to_anchor=(1.5, 0.5), loc='center right')
        self.tra_figure_orbit.axes.set_xticks([])
        self.tra_figure_orbit.axes.set_yticks([])
        self.tra_figure_orbit.axes.set_zticks([])
        self.tra_figure_orbit.axes.set_xlim3d([x_min * 0.7, x_max * 0.7])
        self.tra_figure_orbit.axes.set_ylim3d([y_min * 0.7, y_max * 0.7])
        self.tra_figure_orbit.axes.set_zlim3d([z_min * 0.7, z_max * 0.7])
        self.tra_figure_orbit.axes.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.tra_figure_orbit.axes.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
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
                                                                    self._arr_orbit._periapsis_radius,
                                                                    self._arr_orbit._apoapsis_radius,
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
                
                self.tra_orbital_elements.h     = self._arr_orbit._specific_angular_momentum
                self.tra_orbital_elements.e     = self._arr_orbit._eccentricity
                self.tra_orbital_elements.a     = self._arr_orbit._semi_major_axis
                self.tra_orbital_elements.theta = theta_f
                
                self.tra_orbital_parameters.r_p = self._arr_orbit._periapsis_radius
                self.tra_orbital_parameters.r_a = self._arr_orbit._apoapsis_radius
                
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
                                                                                                     self._arr_orbit._periapsis_radius,
                                                                                                     self._arr_orbit._apoapsis_radius,
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
                
                self.tra_orbital_elements.h     = self._arr_orbit._specific_angular_momentum
                self.tra_orbital_elements.e     = self._arr_orbit._eccentricity
                self.tra_orbital_elements.a     = self._arr_orbit._semi_major_axis
                self.tra_orbital_elements.theta = theta_f_2
                
                self.tra_orbital_parameters.r_p = self._arr_orbit._periapsis_radius
                self.tra_orbital_parameters.r_a = self._arr_orbit._apoapsis_radius
                
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
                                                                           self._arr_orbit._right_ascension_ascending_node,
                                                                           self._arr_orbit._inclination,
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
                                                                               self._arr_orbit._periapsis_anomaly - self.tra_orbital_elements.omega,
                                                                               secondIntersectionPoint=maneuver.option==1,
                                                                               m=self.spacecraft.mass)
                
                # ? Integrate from current point to maneuver point
                
                result = self.integrate_maneuver(self.tra_orbital_elements, self.tra_orbital_elements.theta, maneuver_result.oe.theta)
                    
                dt += result['dt']
                
                # ? Update transfer orbit
                
                self.tra_orbital_elements.omega = self._arr_orbit._periapsis_anomaly
                self.tra_orbital_elements.theta = maneuver_result.oe.theta
                
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