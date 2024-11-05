""" MissionInterplanetaryTransfer.py: Implements the Interplanetary transfer mission """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np

from datetime import datetime, timedelta

from Utility import format
from FigureCanvas import FigureCanvas
from Spacecraft import Spacecraft
from PorkChopPlot import PorkChopPlot

from tools.AstronomicalData import AstronomicalData, CelestialBody, Planet, index_from_planet, planet_from_index, celestial_body_from_planet
from tools.TwoBodyProblem import TwoBodyProblem
from tools.ThreeDimensionalOrbit import ThreeDimensionalOrbit, DirectionType, OrbitalElements
from tools.Time import Time
from tools.InterplanetaryTrajectories import InterplanetaryTrajectories, ManeuverResult

class MissionInterplanetaryTransfer(qtCore.QObject):
    """Manages the interplanetary transfer mission"""
    
    # --- SIGNALS 
    
    signal_pork_chop_plot_finished = qtCore.Signal()
    
    signal_update_progress_bar = qtCore.Signal(float)
    
    # --- PROPERTIES 
    
    # ? Launch Window Begin
    
    @qtCore.Property(str)
    def launch_window_beg(self): return self._launch_window_beg

    @launch_window_beg.setter
    def launch_window_beg(self, val : str): self._launch_window_beg = val
    
    # ? Launch Window End
    
    @qtCore.Property(str)
    def launch_window_end(self): return self._launch_window_end

    @launch_window_end.setter
    def launch_window_end(self, val : str): self._launch_window_end = val
    
    # ? Arrival Window Begin
    
    @qtCore.Property(str)
    def arrival_window_beg(self): return self._arrival_window_beg

    @arrival_window_beg.setter
    def arrival_window_beg(self, val : str): self._arrival_window_beg = val
    
    # ? Arrival Window End
    
    @qtCore.Property(str)
    def arrival_window_end(self): return self._arrival_window_end

    @arrival_window_end.setter
    def arrival_window_end(self, val : str): self._arrival_window_end = val
    
    # ? Window Step [days]
    
    pcp_step_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=pcp_step_changed)
    def window_step(self): return self._window_step

    @window_step.setter
    def window_step(self, val : int): self._window_step = val
    
    # ? Departure Planet
    
    @qtCore.Property(int)
    def dep_planet(self): return self._dep_planet

    @dep_planet.setter
    def dep_planet(self, val : int): self._dep_planet = val
    
    # ? Arrival Planet
    
    @qtCore.Property(int)
    def arr_planet(self): return self._arr_planet

    @arr_planet.setter
    def arr_planet(self, val : int): self._arr_planet = val
    
    # ? Departure Date
    
    @qtCore.Property(str)
    def dep_date(self): return self._dep_date

    @dep_date.setter
    def dep_date(self, val : str): self._dep_date = val
    
    # ? Arrival Date
    
    @qtCore.Property(str)
    def arr_date(self): return self._arr_date

    @arr_date.setter
    def arr_date(self, val : str): self._arr_date = val
    
    # ? Departure Periapsis Height [km]
    
    @qtCore.Property(float)
    def dep_periapsis_height(self): return format(self._dep_periapsis_height)

    @dep_periapsis_height.setter
    def dep_periapsis_height(self, val : float): self._dep_periapsis_height = val
    
    # ? Arrival Periapsis Height [km]
    
    @qtCore.Property(float)
    def arr_periapsis_height(self): return format(self._arr_periapsis_height)

    @arr_periapsis_height.setter
    def arr_periapsis_height(self, val : float): self._arr_periapsis_height = val
    
    # ? Arrival Period [h]
    
    @qtCore.Property(float)
    def arr_period(self): return format(self._arr_period)

    @arr_period.setter
    def arr_period(self, val : float): self._arr_period = val
    
    # --- PUBLIC METHODS 
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__MissionInterplanetaryTransfer", self)
        
        self.spacecraft = Spacecraft(engine)
        
        # * Pork Chop Plot
        
        self._launch_window_beg             = '2020-01-01'                      # * Launch window begin
        self._launch_window_end             = '2021-01-01'                      # * Launch window end
        self._arrival_window_beg            = '2031-01-01'                      # * Arrival window begin
        self._arrival_window_end            = '2032-06-01'                      # * Arrival window end
        self._window_step                   = 10                                # * Windows step
        self.figure_pork_chop_plot          = FigureCanvas()                    # * Pork chop plot figure
        self.pork_chop_plot                 = PorkChopPlot()                    # * Pork chop plot thread
        
        self.pork_chop_plot.status_changed.connect(self.update_progress_bar)
        self.pork_chop_plot.finished.connect(self.generation_completed)
        
        # * Interplanetary Leg
        
        self._dep_planet                    = index_from_planet(Planet.EARTH)   # * Departure planet
        self._arr_planet                    = index_from_planet(Planet.MARS)    # * Arrival planet
        self._dep_date                      = '1996-11-07 00:00:00'             # * Departure date
        self._arr_date                      = '1997-09-12 00:00:00'             # * Arrival date
        self._dep_periapsis_height          = 180                               # * Departure parking orbit height             [ km ]
        self._arr_periapsis_height          = 300                               # * Arrival rendezvous orbit periapsis height  [ km ]
        self._arr_period                    = 48                                # * Arrival rendezvous orbit period            [ h ]
        self.figure_interplanetary_transfer = FigureCanvas(dof3=True)           # * Interplanetary transfer figure
        
        # * Context properties
        
        engine.rootContext().setContextProperty("__PorkChopPlotFigure", self.figure_pork_chop_plot)
        engine.rootContext().setContextProperty("__InterplanetaryTransferFigure", self.figure_interplanetary_transfer)
    
    def set_update_with_canvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Connects all the QML figures with the backend model

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        win = engine.rootObjects()[0]
        
        self.figure_pork_chop_plot.update_with_canvas(win.findChild(qtCore.QObject, "PorkChopPlotFigure"), win.findChild(qtCore.QObject, "PorkChopPlotFigureParent"))
        self.figure_interplanetary_transfer.update_with_canvas(win.findChild(qtCore.QObject, "InterplanetaryTransferFigure"), win.findChild(qtCore.QObject, "InterplanetaryTransferFigureParent"))
        
        self.init_transfer_figure()
    
    # --- PUBLIC SLOTS 
    
    @qtCore.Slot()
    def generate_pork_chop_plot(self) -> None:
        """Generates the Pork Chop Plot
        """
        
        self.pork_chop_plot.departure_planet = celestial_body_from_planet(planet_from_index(self._dep_planet))
        
        self.pork_chop_plot.arrival_planet = celestial_body_from_planet(planet_from_index(self._arr_planet))
        
        self.pork_chop_plot.launch_window = [
            datetime.strptime(self._launch_window_beg, '%Y-%m-%d'),
            datetime.strptime(self._launch_window_end, '%Y-%m-%d')
        ]
        
        self.pork_chop_plot.arrival_window = [
            datetime.strptime(self._arrival_window_beg, '%Y-%m-%d'),
            datetime.strptime(self._arrival_window_end, '%Y-%m-%d')
        ]
        
        self.pork_chop_plot.step = self._window_step
        
        self.pork_chop_plot.start()
    
    @qtCore.Slot()
    def stop_generate_pork_chop_plot(self) -> None:
        """Stops the generation of the Pork Chop Plot
        """
        
        self.pork_chop_plot.stop = True
    
    @qtCore.Slot()
    def update_progress_bar(self, progress : float, text : str) -> None:
        """Updates the progress bar and text

        Args:
            progress (float): Progress bar value
            text (str): Status description
        """
        
        self.signal_update_progress_bar.emit(progress)
    
    @qtCore.Slot()
    def generation_completed(self) -> None:
        """Slot called when the pork chop plot has been generated
        """
        
        self.plot_pork_chop()
    
    @qtCore.Slot()
    def simulate(self) -> None:
        """Simulates the interplanetary transfer
        """
        
        # ? Prepare parameters
        
        depPlanet = celestial_body_from_planet(planet_from_index(self._dep_planet))
        arrPlanet = celestial_body_from_planet(planet_from_index(self._arr_planet))
        
        depDate = datetime.strptime(self._dep_date, '%Y-%m-%d %H:%M:%S')
        arrDate = datetime.strptime(self._arr_date, '%Y-%m-%d %H:%M:%S')
        
        r_p_D = AstronomicalData.equatiorial_radius(depPlanet) + self._dep_periapsis_height
        r_p_A = AstronomicalData.equatiorial_radius(arrPlanet) + self._arr_periapsis_height
        
        T = self._arr_period * 3600
        
        if self._arr_periapsis_height == 0: r_p_A = 0
        
        # ? Optimal transfer calculation
        
        maneuver_1, maneuver_2, lambert_oe, theta_2 = InterplanetaryTrajectories.optimal_transfer(depPlanet,
                                                                                                  arrPlanet,
                                                                                                  depDate,
                                                                                                  arrDate,
                                                                                                  r_p_D,
                                                                                                  r_p_A,
                                                                                                  T,
                                                                                                  self.spacecraft.initial_mass)

        # ? Integration
        
        ThreeDimensionalOrbit.set_celestial_body(CelestialBody.SUN)
        TwoBodyProblem.set_celestial_body(CelestialBody.SUN)
        Time.set_celestial_body(CelestialBody.SUN)
        
        result = self.integrate_maneuver(lambert_oe, lambert_oe.theta, theta_2)
        
        # ? Plot

        self.plot_interplanetary_transfer(result)
    
    # --- PRIVATE METHODS 
    
    def init_transfer_figure(self) -> None:
        """Initializes the transfer figure canvas
        """
        
        self.figure_interplanetary_transfer.reset_canvas()
        
        ThreeDimensionalOrbit.set_celestial_body(CelestialBody.SUN)
        TwoBodyProblem.set_celestial_body(CelestialBody.SUN)
        Time.set_celestial_body(CelestialBody.SUN)
        
        # ? Planets orbit
        
        depDate = datetime.strptime(self._dep_date, '%Y-%m-%d %H:%M:%S')
        
        r_mercury, v_mercury    = InterplanetaryTrajectories.ephemeris(CelestialBody.MERCURY, datetime.strptime(self._dep_date, '%Y-%m-%d %H:%M:%S'))
        r_venus, v_venus        = InterplanetaryTrajectories.ephemeris(CelestialBody.VENUS, datetime.strptime(self._dep_date, '%Y-%m-%d %H:%M:%S'))
        r_earth, v_earth        = InterplanetaryTrajectories.ephemeris(CelestialBody.EARTH, datetime.strptime(self._dep_date, '%Y-%m-%d %H:%M:%S'))
        r_mars, v_mars          = InterplanetaryTrajectories.ephemeris(CelestialBody.MARS, datetime.strptime(self._dep_date, '%Y-%m-%d %H:%M:%S'))
        
        mercury = TwoBodyProblem.simulate_relative_motion(np.hstack([r_mercury, v_mercury]))
        venus   = TwoBodyProblem.simulate_relative_motion(np.hstack([r_venus, v_venus]))
        earth   = TwoBodyProblem.simulate_relative_motion(np.hstack([r_earth, v_earth]))
        mars    = TwoBodyProblem.simulate_relative_motion(np.hstack([r_mars, v_mars]))
        
        self.figure_interplanetary_transfer.axes.plot(mercury['y'][0,:], mercury['y'][1,:], mercury['y'][2,:], color='#9E9E9E', linestyle='dashed', linewidth='2', label='Mercury')
        self.figure_interplanetary_transfer.axes.plot(venus['y'][0,:], venus['y'][1,:], venus['y'][2,:], color='#4CAF50', linestyle='dashed', linewidth='2', label='Venus')
        self.figure_interplanetary_transfer.axes.plot(earth['y'][0,:], earth['y'][1,:], earth['y'][2,:], color='#2196F3', linestyle='dashed', linewidth='2', label='Earth')
        self.figure_interplanetary_transfer.axes.plot(mars['y'][0,:], mars['y'][1,:], mars['y'][2,:], color='#F44336', linestyle='dashed', linewidth='2', label='Mars')
        self.figure_interplanetary_transfer.axes.scatter(0, 0, 0, c='#FFC107', s=500)
        
        # ? Settings
        
        self.figure_interplanetary_transfer.axes.grid(False)
        self.figure_interplanetary_transfer.axes.legend()
        self.figure_interplanetary_transfer.axes.set_xticks([])
        self.figure_interplanetary_transfer.axes.set_yticks([])
        self.figure_interplanetary_transfer.axes.set_zticks([])
        self.figure_interplanetary_transfer.axes.set_xlim3d([np.min(mars['y'][0,:]) * 0.8, np.max(mars['y'][0,:]) * 0.8])
        self.figure_interplanetary_transfer.axes.set_ylim3d([np.min(mars['y'][1,:]) * 0.8, np.max(mars['y'][1,:]) * 0.8])
        self.figure_interplanetary_transfer.axes.set_zlim3d([np.min(mars['y'][2,:]) * 0.8, np.max(mars['y'][2,:]) * 0.8])
        self.figure_interplanetary_transfer.axes.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.xaxis._axinfo["grid"]['color'] = (1,1,1,0)
        self.figure_interplanetary_transfer.axes.yaxis._axinfo["grid"]['color'] = (1,1,1,0)
        self.figure_interplanetary_transfer.axes.zaxis._axinfo["grid"]['color'] = (1,1,1,0)
        
        self.figure_interplanetary_transfer.redraw_canvas()
    
    def plot_pork_chop(self) -> None:
        """Plots the Pork Chop Plot
        """
        
        self.figure_pork_chop_plot.reset_canvas()
        
        # if (len(self.figure_pork_chop_plot.figure.axes) > 1):
            
        #     return
            
        #     self.figure_pork_chop_plot.figure.delaxes(self.figure_pork_chop_plot.figure.axes[2])
        #     self.figure_pork_chop_plot.figure.delaxes(self.figure_pork_chop_plot.figure.axes[1])
        
        dv_1    = self.pork_chop_plot.dv_1
        dv_2    = self.pork_chop_plot.dv_2
        T_F     = self.pork_chop_plot.T_F
        X       = self.pork_chop_plot.X
        Y       = self.pork_chop_plot.Y
        
        dv_cond = dv_1.copy()
            
        dv_cond[dv_cond > 12.5] = 0.0
        
        contourVelocity = self.figure_pork_chop_plot.axes.contourf(X, Y, dv_1 + dv_2, cmap='hot')
        
        contourVelocityConstraint = self.figure_pork_chop_plot.axes.contour(X, Y, dv_cond, cmap='flag')
        
        contourTimeOfFlight = self.figure_pork_chop_plot.axes.contour(X, Y, T_F, cmap='summer')
        
        self.figure_pork_chop_plot.axes.clabel(contourVelocityConstraint, inline=1, fontsize=10)
        self.figure_pork_chop_plot.axes.clabel(contourTimeOfFlight, inline=1, fontsize=10)
        
        # self.figure_pork_chop_plot.figure.colorbar(contourVelocity, label='$\Delta V_{TOT}$ $[km / s]$', shrink=0.5)
        # self.figure_pork_chop_plot.figure.colorbar(contourVelocityConstraint, label='$\Delta V_1$ $[km / s]$', orientation='vertical', shrink=0.5)
        
        self.figure_pork_chop_plot.axes.set_title('Pork Chop')
        self.figure_pork_chop_plot.axes.set_xlabel('Launch Window')
        self.figure_pork_chop_plot.axes.set_ylabel('Arrival Window')
        
        self.figure_pork_chop_plot.redraw_canvas()
        
        self.signal_pork_chop_plot_finished.emit()
    
    def plot_interplanetary_transfer(self, transfer_trajectory : np.ndarray) -> None:
        """Plots the interplanetary leg

        Args:
            transfer_trajectory (np.ndarray): Transfer trajectory
        """
        
        self.figure_interplanetary_transfer.reset_canvas()
        
        # ? Planets position from ephemeris
        
        r_1_x, r_1_y, r_1_z = [], [], []
        r_2_x, r_2_y, r_2_z = [], [], []
        
        start = datetime.strptime(self._dep_date, '%Y-%m-%d %H:%M:%S')
        
        depPlanet = celestial_body_from_planet(planet_from_index(self._dep_planet))
        arrPlanet = celestial_body_from_planet(planet_from_index(self._arr_planet))
        
        for dt in np.linspace(0, np.abs(transfer_trajectory['dt']), 1000):
            
            r, _ = InterplanetaryTrajectories.ephemeris(depPlanet, start + timedelta(0, dt))
            
            r_1_x.append(r[0])
            r_1_y.append(r[1])
            r_1_z.append(r[2])
            
            r, _ = InterplanetaryTrajectories.ephemeris(arrPlanet, start + timedelta(0, dt))
            
            r_2_x.append(r[0])
            r_2_y.append(r[1])
            r_2_z.append(r[2])
        
        # ? Orbits and positions
        
        self.figure_interplanetary_transfer.axes.plot(r_1_x, r_1_y, r_1_z, color='#90CAF9', linestyle='dashed', linewidth='2', label='Departure Planet')
        self.figure_interplanetary_transfer.axes.plot(r_2_x, r_2_y, r_2_z, color='#FFAB91', linestyle='dashed', linewidth='2', label='Arrival Planet')
        self.figure_interplanetary_transfer.axes.plot(transfer_trajectory['y'][0,:], transfer_trajectory['y'][1,:], transfer_trajectory['y'][2,:], color='#A5D6A7', label='Orbit')
        self.figure_interplanetary_transfer.axes.scatter(0, 0, 0, c='#FFC107', s=500)
        self.figure_interplanetary_transfer.axes.scatter(r_1_x[0], r_1_y[0], r_1_z[0], marker='s', c='#90CAF9', s=50, label='Departure Planet Start')
        self.figure_interplanetary_transfer.axes.scatter(r_1_x[-1], r_1_y[-1], r_1_z[-1], c='#90CAF9', s=50, label='Departure Planet End')
        self.figure_interplanetary_transfer.axes.scatter(r_2_x[0], r_2_y[0], r_2_z[0], marker='s', c='#FFAB91', s=50, label='Arrival Planet Start')
        self.figure_interplanetary_transfer.axes.scatter(r_2_x[-1], r_2_y[-1], r_2_z[-1], c='#FFAB91', s=50, label='Arrival Planet End')
        
        # ? Settings
        
        x_min = np.min([np.min(r_1_x), np.min(r_2_x), np.min(transfer_trajectory['y'][0,:])])
        x_max = np.max([np.max(r_1_x), np.max(r_2_x), np.max(transfer_trajectory['y'][0,:])])
        y_min = np.min([np.min(r_1_y), np.min(r_2_y), np.min(transfer_trajectory['y'][1,:])])
        y_max = np.max([np.max(r_1_y), np.max(r_2_y), np.max(transfer_trajectory['y'][1,:])])
        z_min = np.min([np.min(r_1_z), np.min(r_2_z), np.min(transfer_trajectory['y'][2,:])])
        z_max = np.max([np.max(r_1_z), np.max(r_2_z), np.max(transfer_trajectory['y'][2,:])])
        
        self.figure_interplanetary_transfer.axes.grid(False)
        self.figure_interplanetary_transfer.axes.legend()
        #self.figure_interplanetary_transfer.axes.legend(bbox_to_anchor=(-0.5, 0.5), loc='center left')
        self.figure_interplanetary_transfer.axes.set_xticks([])
        self.figure_interplanetary_transfer.axes.set_yticks([])
        self.figure_interplanetary_transfer.axes.set_zticks([])
        self.figure_interplanetary_transfer.axes.set_xlim3d([x_min * 0.8, x_max * 0.8])
        self.figure_interplanetary_transfer.axes.set_ylim3d([y_min * 0.8, y_max * 0.8])
        self.figure_interplanetary_transfer.axes.set_zlim3d([z_min * 0.8, z_max * 0.8])
        self.figure_interplanetary_transfer.axes.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.figure_interplanetary_transfer.axes.xaxis._axinfo["grid"]['color'] = (1,1,1,0)
        self.figure_interplanetary_transfer.axes.yaxis._axinfo["grid"]['color'] = (1,1,1,0)
        self.figure_interplanetary_transfer.axes.zaxis._axinfo["grid"]['color'] = (1,1,1,0)
        
        self.figure_interplanetary_transfer.redraw_canvas()
    
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