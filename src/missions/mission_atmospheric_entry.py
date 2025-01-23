""" mission_atmospheric_entry.py: Implements the atmospheric entry mission """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np

from src.common import format
from src.utility.figure_canvas import FigureCanvas
from src.systems.capsule import Capsule

from tools.AtmosphericEntry import AtmosphericEntry

class MissionAtmosphericEntry(qtCore.QObject):
    """Manages the atmospheric entry mission"""
    
    # --- PROPERTIES 
    
    # ? Entry Velocity [km / s]
    
    @qtCore.Property(float)
    def entry_velocity(self): return format(self._entry_velocity)
    
    @entry_velocity.setter
    def entry_velocity(self, val : float): self._entry_velocity = val
    
    # ? Entry Flight Path Angle [deg]
    
    @qtCore.Property(float)
    def entry_flight_path_angle(self): return format(self._entry_flight_path_angle)
    
    @entry_flight_path_angle.setter
    def entry_flight_path_angle(self, val : float): self._entry_flight_path_angle = val
    
    # ? Entry Altitude [km]
    
    @qtCore.Property(float)
    def entry_altitude(self): return format(self._entry_altitude)
    
    @entry_altitude.setter
    def entry_altitude(self, val : float): self._entry_altitude = val
    
    # ? Final Integration Time [min]
    
    @qtCore.Property(float)
    def final_integration_time(self): return format(self._final_integration_time)
    
    @final_integration_time.setter
    def final_integration_time(self, val : float): self._final_integration_time = val
    
    # ? Use Parachute
    
    @qtCore.Property(bool)
    def use_parachute(self): return self._use_parachute
    
    @use_parachute.setter
    def use_parachute(self, val : bool): self._use_parachute = val
    
    # --- PUBLIC METHODS 
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        self.engine = engine
        
        engine.rootContext().setContextProperty("__MissionAtmosphericEntry", self)
        
        self.capsule = Capsule(engine)
        
        # ? Entry Condition
        
        self._entry_velocity            : float = 12.6161   # * Entry Velocity          [ km / s ]
        self._entry_flight_path_angle   : float = -9        # * Entry Flight Path Angle [ deg ]
        self._entry_altitude            : float = 120       # * Entry Altitude          [ km ]
        self._final_integration_time    : float = 60        # * Final Integration Time  [ min ]
        self._use_parachute             : bool  = False     # * True for using the parachute
        
        # ? Simulation Results
        
        self.result = dict() # * Simulation Result Dictionary
        
        # ? Figure Canvas
        
        self.figure_velocity                = FigureCanvas()
        self.figure_acceleration            = FigureCanvas()
        self.figure_trajectory              = FigureCanvas()
        self.figure_flight_path_angle       = FigureCanvas()
        self.figure_convective_heat_flux    = FigureCanvas()
        self.figure_altitude                = FigureCanvas()
        
        # ? Context properties
        
        engine.rootContext().setContextProperty("__AtmosphericEntryFigureVelocity", self.figure_velocity)
        engine.rootContext().setContextProperty("__AtmosphericEntryFigureAcceleration", self.figure_acceleration)
        engine.rootContext().setContextProperty("__AtmosphericEntryFigureTrajectory", self.figure_trajectory)
        engine.rootContext().setContextProperty("__AtmosphericEntryFigureFlightPathAngle", self.figure_flight_path_angle)
        engine.rootContext().setContextProperty("__AtmosphericEntryFigureConvectiveHeatFlux", self.figure_convective_heat_flux)
        engine.rootContext().setContextProperty("__AtmosphericEntryFigureAltitude", self.figure_altitude)
    
    # --- PUBLIC SLOTS 
    
    @qtCore.Slot()
    def attach_canvas(self) -> None:
        """Connects all the QML figures with the backend model
        """
        
        win = self.engine.rootObjects()[0]
        
        self.figure_velocity.update_with_canvas(win.findChild(qtCore.QObject, "AtmosphericEntryFigureVelocity"), win.findChild(qtCore.QObject, "AtmosphericEntryFigureVelocityParent"))
        self.figure_acceleration.update_with_canvas(win.findChild(qtCore.QObject, "AtmosphericEntryFigureAcceleration"), win.findChild(qtCore.QObject, "AtmosphericEntryFigureAccelerationParent"))
        self.figure_trajectory.update_with_canvas(win.findChild(qtCore.QObject, "AtmosphericEntryFigureTrajectory"), win.findChild(qtCore.QObject, "AtmosphericEntryFigureTrajectoryParent"))
        self.figure_flight_path_angle.update_with_canvas(win.findChild(qtCore.QObject, "AtmosphericEntryFigureFlightPathAngle"), win.findChild(qtCore.QObject, "AtmosphericEntryFigureFlightPathAngleParent"))
        self.figure_convective_heat_flux.update_with_canvas(win.findChild(qtCore.QObject, "AtmosphericEntryFigureConvectiveHeatFlux"), win.findChild(qtCore.QObject, "AtmosphericEntryFigureConvectiveHeatFluxParent"))
        self.figure_altitude.update_with_canvas(win.findChild(qtCore.QObject, "AtmosphericEntryFigureAltitude"), win.findChild(qtCore.QObject, "AtmosphericEntryFigureAltitudeParent"))
        
        self.init_figure()
    
    @qtCore.Slot()
    def detach_canvas(self) -> None:
        """Disconnects all the QML figures from the backend model
        """
        
        self.figure_velocity                = FigureCanvas()
        self.figure_acceleration            = FigureCanvas()
        self.figure_trajectory              = FigureCanvas()
        self.figure_flight_path_angle       = FigureCanvas()
        self.figure_convective_heat_flux    = FigureCanvas()
        self.figure_altitude                = FigureCanvas()
        
        self.engine.rootContext().setContextProperty("__AtmosphericEntryFigureVelocity", self.figure_velocity)
        self.engine.rootContext().setContextProperty("__AtmosphericEntryFigureAcceleration", self.figure_acceleration)
        self.engine.rootContext().setContextProperty("__AtmosphericEntryFigureTrajectory", self.figure_trajectory)
        self.engine.rootContext().setContextProperty("__AtmosphericEntryFigureFlightPathAngle", self.figure_flight_path_angle)
        self.engine.rootContext().setContextProperty("__AtmosphericEntryFigureConvectiveHeatFlux", self.figure_convective_heat_flux)
        self.engine.rootContext().setContextProperty("__AtmosphericEntryFigureAltitude", self.figure_altitude)
    
    @qtCore.Slot()
    def simulate(self) -> None:
        """Simulates the atmospheric entry mission
        """
        
        # ? Simulation
        
        AtmosphericEntry.set_capsule_parameters(0, 300, 0, self.capsule.capsule_lift_coefficient, self.capsule.capsule_drag_coefficient, self.capsule.capsule_reference_surface)
        
        AtmosphericEntry.set_parachute_parameters(self.use_parachute, self.capsule.parachute_drag_coefficient, self.capsule.parachute_reference_surface)
        
        y_0 = np.array([self.entry_velocity, np.deg2rad(self.entry_flight_path_angle), self.entry_altitude, 0, self.capsule.capsule_mass])
        
        result = AtmosphericEntry.simulate_atmospheric_entry(y_0, t_f=self.final_integration_time * 60)
        
        self.result = result
        
        # ? Plot
        
        self.plot_figures()
    
    # --- PRIVATE METHODS 
        
    def init_figure(self) -> None:
        """Initializes the figure canvas
        """
        
        # ? Velocity
        
        self.figure_velocity.reset_canvas()
        self.figure_velocity.format_canvas('Time [ $min$ ]', 'Velocity [ $km\;/\;s$ ]', -110)
        self.figure_velocity.redraw_canvas()
        
        # ? Acceleration
        
        self.figure_acceleration.reset_canvas()
        self.figure_acceleration.format_canvas('Time [ $min$ ]', 'Acceleration [ $g$ ]', -120)
        self.figure_acceleration.redraw_canvas()
        
        # ? Trajectory
        
        self.figure_trajectory.reset_canvas()
        self.figure_trajectory.format_canvas('Downrange Distance [ $km$ ]', 'Altitude [ $km$ ]', -105)
        self.figure_trajectory.redraw_canvas()
        
        # ? Flight Path Angle
        
        self.figure_flight_path_angle.reset_canvas()
        self.figure_flight_path_angle.format_canvas('Time [ $min$ ]', 'Flight Path Angle [ $deg$ ]', -150)
        self.figure_flight_path_angle.redraw_canvas()
        
        # ? Convective Heat Flux
        
        self.figure_convective_heat_flux.reset_canvas()
        self.figure_convective_heat_flux.format_canvas('Time [ $min$ ]', 'S.P. Convective Heat Flux [ $W\;/\;cm^2$ ]', -220)
        self.figure_convective_heat_flux.redraw_canvas()
        
        # ? Altitude
        
        self.figure_altitude.reset_canvas()
        self.figure_altitude.format_canvas('Velocity [ $km\;/\;s$ ]', 'Altitude [ $km$ ]', -105)
        self.figure_altitude.redraw_canvas()
        
        # ? Plot
        
        self.plot_figures()
    
    def plot_figures(self) -> None:
        """Plots the figures with the results of the simulation
        """
        
        if len(self.result) == 0: return
        
        V       = self.result['y'][0, :]
        gamma   = self.result['y'][1, :]
        r       = self.result['y'][2, :]
        x       = self.result['y'][3, :]
        m       = self.result['y'][4, :]
        t       = self.result['t']
        
        C       = (1.7415 * 1e-4 * 1 / np.sqrt(self.capsule.capsule_nose_radius))
        q_t_c   = np.array([C * np.sqrt(1.225 * np.exp(-(r[i] - AtmosphericEntry.R_E) / AtmosphericEntry.H)) * (V[i] * 1e3)**3 for i in range(0, len(t))])
        a       = np.array([(V[i] - V[i - 1]) / (t[i] - t[i - 1]) for i in range(1, len(t))])
        
        t = t / 60
        
        # ? Velocity
        
        self.figure_velocity.reset_canvas()
        self.figure_velocity.format_canvas('Time [ $min$ ]', 'Velocity [ $km\;/\;s$ ]', -110, f'$V_f = {(V[-1] * 1e3):.3f}\;\;m/s$')
        self.figure_velocity.axes.plot(t, V, color=FigureCanvas.default_color)
        self.figure_velocity.redraw_canvas()
        
        # ? Acceleration
        
        self.figure_acceleration.reset_canvas()
        self.figure_acceleration.format_canvas('Time [ $min$ ]', 'Acceleration [ $g$ ]', -120, '$a_{max} = ' + f'{(max(abs(a)) / AtmosphericEntry.g_E):.3f}\;\;g$')
        self.figure_acceleration.axes.plot(t[1:], a / AtmosphericEntry.g_E, color=FigureCanvas.default_color)
        self.figure_acceleration.redraw_canvas()
        
        # ? Trajectory
        
        self.figure_trajectory.reset_canvas()
        self.figure_trajectory.format_canvas('Downrange Distance [ $km$ ]', 'Altitude [ $km$ ]', -105, f'$h_f = {(r[-1] - AtmosphericEntry.R_E):.3f}\;\;km$')
        self.figure_trajectory.axes.plot(x, r - AtmosphericEntry.R_E, color=FigureCanvas.default_color)
        self.figure_trajectory.redraw_canvas()
        
        # ? Flight Path Angle
        
        self.figure_flight_path_angle.reset_canvas()
        self.figure_flight_path_angle.format_canvas('Time [ $min$ ]', 'Flight Path Angle [ $deg$ ]', -150, f'$\gamma_f = {np.rad2deg(gamma)[-1]:.3f}\;\;\deg$')
        self.figure_flight_path_angle.axes.plot(t, gamma * 180 / np.pi, color=FigureCanvas.default_color)
        self.figure_flight_path_angle.redraw_canvas()
        
        # ? Convective Heat Flux
        
        self.figure_convective_heat_flux.reset_canvas()
        self.figure_convective_heat_flux.format_canvas('Time [ $min$ ]', 'S.P. Convective Heat Flux [ $W\;/\;cm^2$ ]', -220, '$\dot{q}_{max}^{conv} = ' + f'{max(q_t_c * 1e-4):.3f}\;\;W\;/\;cm^2$')
        self.figure_convective_heat_flux.axes.plot(t, q_t_c * 1e-4, color=FigureCanvas.default_color)
        self.figure_convective_heat_flux.redraw_canvas()
        
        # ? Altitude
        
        self.figure_altitude.reset_canvas()
        self.figure_altitude.format_canvas('Velocity [ $km\;/\;s$ ]', 'Altitude [ $km$ ]', -105, f'$h_f = {(r[-1] - AtmosphericEntry.R_E):.3f}\;\;km$')
        self.figure_altitude.axes.plot(V, r - AtmosphericEntry.R_E, color=FigureCanvas.default_color)
        self.figure_altitude.redraw_canvas()