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
    
    # ! SIGNALS
    
    porkChopPlotFinished = qtCore.Signal()
    
    updateProgressBar = qtCore.Signal(float)
    
    # ! PROPERTIES
    
    # ! Pork Chop Plot
    
    # ? Pork Chop Plot - Departure Planet
    
    pcp_planet_dep_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=pcp_planet_dep_changed)
    def pcp_planet_dep(self): return self._pcp_planet_dep

    @pcp_planet_dep.setter
    def pcp_planet_dep(self, val : int): self._pcp_planet_dep = val
    
    # ? Pork Chop Plot - Arrival Planet
    
    pcp_planet_arr_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=pcp_planet_arr_changed)
    def pcp_planet_arr(self): return self._pcp_planet_arr

    @pcp_planet_arr.setter
    def pcp_planet_arr(self, val : int): self._pcp_planet_arr = val
    
    # ? Pork Chop Plot - Launch Window Begin
    
    pcp_launch_window_beg_changed = qtCore.Signal()
    
    @qtCore.Property(str, notify=pcp_launch_window_beg_changed)
    def pcp_launch_window_beg(self): return self._pcp_launch_window_beg

    @pcp_launch_window_beg.setter
    def pcp_launch_window_beg(self, val : str): self._pcp_launch_window_beg = val
    
    # ? Pork Chop Plot - Launch Window End
    
    pcp_launch_window_end_changed = qtCore.Signal()
    
    @qtCore.Property(str, notify=pcp_launch_window_end_changed)
    def pcp_launch_window_end(self): return self._pcp_launch_window_end

    @pcp_launch_window_end.setter
    def pcp_launch_window_end(self, val : str): self._pcp_launch_window_end = val
    
    # ? Pork Chop Plot - Arrival Window Begin
    
    pcp_arrival_window_beg_changed = qtCore.Signal()
    
    @qtCore.Property(str, notify=pcp_arrival_window_beg_changed)
    def pcp_arrival_window_beg(self): return self._pcp_arrival_window_beg

    @pcp_arrival_window_beg.setter
    def pcp_arrival_window_beg(self, val : str): self._pcp_arrival_window_beg = val
    
    # ? Pork Chop Plot - Arrival Window End
    
    pcp_arrival_window_end_changed = qtCore.Signal()
    
    @qtCore.Property(str, notify=pcp_arrival_window_end_changed)
    def pcp_arrival_window_end(self): return self._pcp_arrival_window_end

    @pcp_arrival_window_end.setter
    def pcp_arrival_window_end(self, val : str): self._pcp_arrival_window_end = val
    
    # ? Pork Chop Plot - Step [days]
    
    pcp_step_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=pcp_step_changed)
    def pcp_step(self): return self._pcp_step

    @pcp_step.setter
    def pcp_step(self, val : int): self._pcp_step = val
    
    # ! Interplanetary Leg
    
    # ? Departure Planet
    
    dep_planet_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=dep_planet_changed)
    def dep_planet(self): return self._dep_planet

    @dep_planet.setter
    def dep_planet(self, val : int): self._dep_planet = val
    
    # ? Arrival Planet
    
    arr_planet_changed = qtCore.Signal()
    
    @qtCore.Property(int, notify=arr_planet_changed)
    def arr_planet(self): return self._arr_planet

    @arr_planet.setter
    def arr_planet(self, val : int): self._arr_planet = val
    
    # ? Departure Date
    
    dep_date_changed = qtCore.Signal()
    
    @qtCore.Property(str, notify=dep_date_changed)
    def dep_date(self): return self._dep_date

    @dep_date.setter
    def dep_date(self, val : str): self._dep_date = val
    
    # ? Arrival Date
    
    arr_date_changed = qtCore.Signal()
    
    @qtCore.Property(str, notify=arr_date_changed)
    def arr_date(self): return self._arr_date

    @arr_date.setter
    def arr_date(self, val : str): self._arr_date = val
    
    # ? Departure Periapsis Height [km]
    
    dep_periapsis_height_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=dep_periapsis_height_changed)
    def dep_periapsis_height(self): return format(self._dep_periapsis_height)

    @dep_periapsis_height.setter
    def dep_periapsis_height(self, val : float): self._dep_periapsis_height = val
    
    # ? Arrival Periapsis Height [km]
    
    arr_periapsis_height_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=arr_periapsis_height_changed)
    def arr_periapsis_height(self): return format(self._arr_periapsis_height)

    @arr_periapsis_height.setter
    def arr_periapsis_height(self, val : float): self._arr_periapsis_height = val
    
    # ? Arrival Period [h]
    
    arr_period_changed = qtCore.Signal()
    
    @qtCore.Property(float, notify=arr_period_changed)
    def arr_period(self): return format(self._arr_period)

    @arr_period.setter
    def arr_period(self, val : float): self._arr_period = val
    
    # ! CONSTRUCTOR
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__MissionInterplanetaryTransfer", self)
        
        self.spacecraft = Spacecraft(engine)
        
        # * Pork Chop Plot
        
        self._pcp_planet_dep                = index_from_planet(Planet.EARTH)
        self._pcp_planet_arr                = index_from_planet(Planet.NEPTUNE)
        self._pcp_launch_window_beg         = '2020-01-01'
        self._pcp_launch_window_end         = '2021-01-01'
        self._pcp_arrival_window_beg        = '2031-01-01'
        self._pcp_arrival_window_end        = '2032-06-01'
        self._pcp_step                      = 10
        self.figure_pork_chop_plot          = FigureCanvas()
        self.pork_chop_plot                 = PorkChopPlot()
        
        self.pork_chop_plot.status_changed.connect(self.updateStatus)
        self.pork_chop_plot.finished.connect(self.operationCompleted)
        
        # * Interplanetary Leg
        
        self._dep_planet                    = index_from_planet(Planet.EARTH)
        self._arr_planet                    = index_from_planet(Planet.MARS)
        self._dep_date                      = '1996-11-07 00:00:00'
        self._arr_date                      = '1997-09-12 00:00:00'
        self._dep_periapsis_height          = 180
        self._arr_periapsis_height          = 300
        self._arr_period                    = 48
        self.figure_interplanetary_transfer = FigureCanvas(dof3=True)
        
        # * Context properties
        
        engine.rootContext().setContextProperty("__PorkChopPlotFigure", self.figure_pork_chop_plot)
        engine.rootContext().setContextProperty("__InterplanetaryTransferFigure", self.figure_interplanetary_transfer)
        
    # ! PUBLIC
    
    def setUpdateWithCanvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Connects all the QML figures with the backend model

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        win = engine.rootObjects()[0]
        
        self.figure_pork_chop_plot.update_with_canvas(win.findChild(qtCore.QObject, "PorkChopPlotFigure"), win.findChild(qtCore.QObject, "PorkChopPlotFigureParent"))
        self.figure_interplanetary_transfer.update_with_canvas(win.findChild(qtCore.QObject, "InterplanetaryTransferFigure"), win.findChild(qtCore.QObject, "InterplanetaryTransferFigureParent"))
        
        self.figure_interplanetary_transfer.figure.tight_layout()
        self.figure_interplanetary_transfer.axes.set_aspect('equal', adjustable='box')
    
    # ! SLOTS
    
    # ? Pork Chop Plot
    
    @qtCore.Slot()
    def loadPorkChopPlotParameters(self) -> None:
        """Loads the pork chop plot parameters
        """
        
        pass
    
    @qtCore.Slot()
    def savePorkChopPlotParameters(self) -> None:
        """Saves the pork chop plot parameters
        """
        
        pass
    
    @qtCore.Slot()
    def calculatePorkChopPlot(self) -> None:
        """Calculates the Pork Chop Plot
        """
        
        self.pork_chop_plot.departure_planet = celestial_body_from_planet(planet_from_index(self._pcp_planet_dep))
        
        self.pork_chop_plot.arrival_planet = celestial_body_from_planet(planet_from_index(self._pcp_planet_arr))
        
        self.pork_chop_plot.launch_window = [
            datetime.strptime(self._pcp_launch_window_beg, '%Y-%m-%d'),
            datetime.strptime(self._pcp_launch_window_end, '%Y-%m-%d')
        ]
        
        self.pork_chop_plot.arrival_window = [
            datetime.strptime(self._pcp_arrival_window_beg, '%Y-%m-%d'),
            datetime.strptime(self._pcp_arrival_window_end, '%Y-%m-%d')
        ]
        
        self.pork_chop_plot.step = self._pcp_step
        
        self.pork_chop_plot.start()
    
    @qtCore.Slot()
    def stopCalculatePorkChopPlot(self) -> None:
        """Stops the calculation of the Pork Chop Plot
        """
        
        self.pork_chop_plot.stop = True
    
    @qtCore.Slot()
    def updateStatus(self, progress : float, text : str) -> None:
        """Updates the status bar

        Args:
            progress (float): Progress bar value
            text (str): Status description
        """
        
        self.updateProgressBar.emit(progress)
    
    @qtCore.Slot()
    def operationCompleted(self) -> None:
        """Slot called when the dump manager has finished to load the data
        """
        
        self.plotPorkChop()
    
    # ? Interplanetary Leg
    
    @qtCore.Slot()
    def loadInterplanetaryParameters(self) -> None:
        """Loads the interplanetary parameters
        """
        
        pass
    
    @qtCore.Slot()
    def saveInterplanetaryParameters(self) -> None:
        """Saves the interplanetary parameters
        """
        
        depPlanet = celestial_body_from_planet(planet_from_index(self._dep_planet))
        arrPlanet = celestial_body_from_planet(planet_from_index(self._arr_planet))
        
        depDate = datetime.strptime(self._dep_date, '%Y-%m-%d %H:%M:%S')
        arrDate = datetime.strptime(self._arr_date, '%Y-%m-%d %H:%M:%S')
        
        r_p_D = AstronomicalData.equatiorial_radius(depPlanet) + self._dep_periapsis_height
        r_p_A = AstronomicalData.equatiorial_radius(arrPlanet) + self._arr_periapsis_height
        
        T = self._arr_period * 3600
        
        if self._arr_periapsis_height == 0: r_p_A = 0
        
        maneuver_1, maneuver_2, lambert_oe, theta_2 = InterplanetaryTrajectories.optimal_transfer(depPlanet, arrPlanet, depDate, arrDate, r_p_D, r_p_A, T, self.spacecraft._initial_mass)

        self.plotInterplanetaryTransfer(maneuver_1, maneuver_2, lambert_oe, theta_2)
    
    # ! PRIVATE
    
    # ? Pork Chop Plot
    
    def plotPorkChop(self) -> None:
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
        
        self.porkChopPlotFinished.emit()
    
    # ? Interplanetary Leg
    
    def plotInterplanetaryTransfer(self, maneuver_1 : ManeuverResult, maneuver_2 : ManeuverResult, lambert_oe : OrbitalElements, theta_2 : float) -> None:
        """Plots the interplanetary leg

        Args:
            maneuver_1 (MANEUVER_RESULT): Maneuver to leave the departure planet
            maneuver_2 (MANEUVER_RESULT): Maneuver to rendezvous with the arrival planet
            lambert_oe (ORBITAL_ELEMENTS): Orbital elements of the lambert arc
            theta_2 (float): Second true anomaly of the lambert arc [rad]
        """
        
        self.figure_interplanetary_transfer.reset_canvas()
        
        # * Integrate
        
        ThreeDimensionalOrbit.set_celestial_body(CelestialBody.SUN)
        TwoBodyProblem.set_celestial_body(CelestialBody.SUN)
        Time.set_celestial_body(CelestialBody.SUN)
        
        r, v = ThreeDimensionalOrbit.pf_2_gef(lambert_oe)
        
        parameters = TwoBodyProblem.calculate_orbital_parameters(r, v)
        
        t_0 = Time.calculate_elliptical_orbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=parameters.T, e=parameters.e, theta=lambert_oe.theta)
        t_f = Time.calculate_elliptical_orbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=parameters.T, e=parameters.e, theta=theta_2)
        
        if theta_2 != 0.0 and t_0 > t_f: t_f += parameters.T
        
        result = TwoBodyProblem.simulate_relative_motion(np.hstack([r, v]), t_0, t_f)
        
        # * Planet 1
        
        r_1_x, r_1_y, r_1_z = [], [], []
        r_2_x, r_2_y, r_2_z = [], [], []
        
        start = datetime.strptime(self._dep_date, '%Y-%m-%d %H:%M:%S')
        
        depPlanet = celestial_body_from_planet(planet_from_index(self._dep_planet))
        arrPlanet = celestial_body_from_planet(planet_from_index(self._arr_planet))
        
        for dt in np.linspace(0, np.abs(t_f - t_0), 1000):
            
            r, v = InterplanetaryTrajectories.ephemeris(depPlanet, start + timedelta(0, dt))
            
            r_1_x.append(r[0])
            r_1_y.append(r[1])
            r_1_z.append(r[2])
            
            r, v = InterplanetaryTrajectories.ephemeris(arrPlanet, start + timedelta(0, dt))
            
            r_2_x.append(r[0])
            r_2_y.append(r[1])
            r_2_z.append(r[2])
        
        # * Celestial Bodies
        
        self.figure_interplanetary_transfer.axes.scatter(0, 0, 0, s=1000, c='y')
        
        # * Orbit
        
        self.figure_interplanetary_transfer.axes.plot(r_1_x, r_1_y, r_1_z, 'b--', label='Departure Planet')
        self.figure_interplanetary_transfer.axes.plot(r_2_x, r_2_y, r_2_z, 'r--', label='Arrival Planet')
        self.figure_interplanetary_transfer.axes.plot(result['y'][0,:], result['y'][1,:], result['y'][2,:], 'g', label='Orbit')
        self.figure_interplanetary_transfer.axes.scatter(result['y'][0,0], result['y'][1,0], result['y'][2,0], c='b', label='Departure')
        self.figure_interplanetary_transfer.axes.scatter(result['y'][0,-1], result['y'][1,-1], result['y'][2,-1], c='r', label='Arrival')
        
        # * Labels
        
        self.figure_interplanetary_transfer.axes.set_xlabel('$x$ [km]')
        self.figure_interplanetary_transfer.axes.set_ylabel('$y$ [km]')
        self.figure_interplanetary_transfer.axes.set_zlabel('$z$ [km]')
        self.figure_interplanetary_transfer.axes.legend(bbox_to_anchor=(-0.5, 0.5), loc='center left')
        
        self.figure_interplanetary_transfer.redraw_canvas()