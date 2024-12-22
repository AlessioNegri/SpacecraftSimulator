""" MissionOrbitInsertion.py: Implements the orbit insertion mission """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import numpy as np
import mplcyberpunk

from common import format
from src.utility.figure_canvas import FigureCanvas
from systems.stage import Stage

from tools.launch_mechanics import Launcher

class MissionOrbitInsertion(qtCore.QObject):
    """Managers the orbit insertion mission"""
    
    # ? Pitchover Height [m]
    
    @qtCore.Property(float)
    def pitchover_height(self): return format(self._pitchover_height)
    
    @pitchover_height.setter
    def pitchover_height(self, val : float): self._pitchover_height = val
    
    # ? Pitchover Flight Path Angle [deg]
    
    @qtCore.Property(float)
    def pitchover_flight_path_angle(self): return format(self._pitchover_flight_path_angle)
    
    @pitchover_flight_path_angle.setter
    def pitchover_flight_path_angle(self, val : float): self._pitchover_flight_path_angle = val
    
    # ? Circular parking orbit height [km]
    
    @qtCore.Property(float)
    def circular_parking_orbit_height(self): return format(self._circular_parking_orbit_height)
    
    @circular_parking_orbit_height.setter
    def circular_parking_orbit_height(self, val : float):
        
        self._circular_parking_orbit_height = val
        
        self._circular_parking_orbit_velocity = np.sqrt(Launcher.k / (Launcher.R_E + val))
    
    # ? Circular parking orbit velocity [km/s]
    
    @qtCore.Property(float)
    def circular_parking_orbit_velocity(self): return format(self._circular_parking_orbit_velocity)
    
    @circular_parking_orbit_velocity.setter
    def circular_parking_orbit_velocity(self, val : float): self._circular_parking_orbit_velocity = val
    
    # ? Final Integration Time [s]
    
    @qtCore.Property(float)
    def final_integration_time(self): return format(self._final_integration_time)
    
    @final_integration_time.setter
    def final_integration_time(self, val : float): self._final_integration_time = val
    
    # ? Use Stage 1
    
    @qtCore.Property(bool)
    def use_stage_1(self): return self._use_stage_1
    
    @use_stage_1.setter
    def use_stage_1(self, val : bool): self._use_stage_1 = val
    
    # ? Use Stage 2
    
    @qtCore.Property(bool)
    def use_stage_2(self): return self._use_stage_2
    
    @use_stage_2.setter
    def use_stage_2(self, val : bool): self._use_stage_2 = val
    
    # ? Use Stage 3
    
    @qtCore.Property(bool)
    def use_stage_3(self): return self._use_stage_3
    
    @use_stage_3.setter
    def use_stage_3(self, val : bool): self._use_stage_3 = val
    
    # ? Stage 1
    
    @qtCore.Property(Stage)
    def stage_1(self): return self._stage_1
    
    @stage_1.setter
    def stage_1(self, val : Stage): self._stage_1 = val
    
    # ? Stage 2
    
    @qtCore.Property(Stage)
    def stage_2(self): return self._stage_2
    
    @stage_2.setter
    def stage_2(self, val : Stage): self._stage_2 = val
    
    # ? Stage 3
    
    @qtCore.Property(Stage)
    def stage_3(self): return self._stage_3
    
    @stage_3.setter
    def stage_3(self, val : Stage): self._stage_3 = val
    
    # ? Payload Mass [kg]
    
    @qtCore.Property(float)
    def payload_mass(self): return format(self._payload_mass)
    
    @payload_mass.setter
    def payload_mass(self, val : float): self._payload_mass = val
    
    # --- PUBLIC METHODS 
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__MissionOrbitInsertion", self)
        
        # ? Entry Condition
        
        self._pitchover_height                  : float = 130                                           # * Pitchover Height                [ m ]
        self._pitchover_flight_path_angle       : float = 89.85                                         # * Pitchover Flight Path Angle     [ deg ]
        self._circular_parking_orbit_height     : float = 300                                           # * Circular Parking Orbit Height   [ km ]
        self._circular_parking_orbit_velocity   : float = np.sqrt(Launcher.k / (Launcher.R_E + 300))    # * Circular Parking Orbit Velocity [ km / s ]
        self._final_integration_time            : float = 300                                           # * Final Integration Time          [ s ]
        
        # ? Stage 1
        
        self._use_stage_1   = True
        self._stage_1       = Stage()
        
        #self._stage_1.mass(68_000 / 15, 68_000 - 68_000 / 15, 0)
        #self._stage_1.motor(933.913 * 1e3, 390, 0.0)
        #self._stage_1.aerodynamics(5, 0.5, 0.0)
        #self._stage_1.calc()
        
        self._stage_1.mass(13_393, 141_634, 54_035)
        self._stage_1.motor(4_323 * 1e3, 279, 0.0)
        self._stage_1.aerodynamics(3.4, 0.5, 0.0)
        self._stage_1.calc()
        
        # ? Stage 2
        
        self._use_stage_2   = True
        self._stage_2       = Stage()
        
        self._stage_2.mass(4_238, 36_239, 13_558)
        self._stage_2.motor(1_304 * 1e3, 293.5, 0.0)
        self._stage_2.aerodynamics(2.4, 0.5, 0.0)
        self._stage_2.calc()
        
        # ? Stage 3
        
        self._use_stage_3   = True
        self._stage_3       = Stage()
        
        self._stage_3.mass(1_433, 10_567, 1_558)
        self._stage_3.motor(317 * 1e3, 295.9, 0.0)
        self._stage_3.aerodynamics(1.9, 0.5, 0.0)
        self._stage_3.calc()
        
        # ? Payload
        
        self._payload_mass = 1_558  # * Payload Mass [kg]
        
        # ? Figure Canvas
        
        self.figure = FigureCanvas(rows=2, cols=2)
        
        # ? Context properties
        
        engine.rootContext().setContextProperty("__OrbitInsertionFigure", self.figure)
        
        self.connect_stages()
        
    def set_update_with_canvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Connects all the QML figures with the backend model

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        win = engine.rootObjects()[0]
        
        self.figure.update_with_canvas(win.findChild(qtCore.QObject, "OrbitInsertionFigure"), win.findChild(qtCore.QObject, "OrbitInsertionFigureParent"))
        
        self.init_figure()
    
    # --- PUBLIC SLOTS 
    
    @qtCore.Slot()
    def connect_stages(self) -> None:
        """Connects the stages from their parameters
        """
        
        # ? Stage 3
        
        self._stage_3.m_payload = self.payload_mass
        
        self._stage_3.calc()
        
        # ? Stage 2
        
        if self._use_stage_3:
            
            self._stage_2.m_payload = self._stage_3.m_0
            
        else:
        
          self._stage_2.m_payload = self.payload_mass
        
        self._stage_2.calc()
        
        # ? Stage 1
        
        if self._use_stage_2:
            
            self._stage_1.m_payload = self._stage_2.m_0
            
        elif self._use_stage_3:
            
            self._stage_1.m_payload = self._stage_3.m_0
            
        else:
        
          self._stage_1.m_payload = self.payload_mass
        
        self._stage_1.calc()
    
    @qtCore.Slot()
    def simulate(self) -> None:
        """Simulates the orbit insertion mission
        """
        
        # ? Simulation
        
        # * Used only for initialization
        
        result  = dict(y=np.zeros(shape=(7,1)), t=np.zeros(shape=(1)))
        a       = np.zeros(shape=(1))
        t_a     = np.zeros(shape=(1))
        
        # * Integration Parameters
        
        y_0 = np.array([0, np.deg2rad(self.pitchover_flight_path_angle), 0, 0, 0, 0, 0])
        h_t = self.pitchover_height
        t_0 = 0
        t_f = self.final_integration_time
        
        # * Stage 1
        
        if self._use_stage_1:
            
            Launcher.stage = self._stage_1
            
            t_f = min(self.final_integration_time, self._stage_1.t_burn)
            
            if t_f > t_0:
            
                result_1 = Launcher.simulate_launch(y_0, h_t=h_t, t_0=t_0, t_f=t_f)
                
                result['y'] = np.append(result['y'], result_1['y'], axis=1)
                result['t'] = np.append(result['t'], result_1['t'])
                a           = np.append(a, np.array([(result_1['y'][0, i] - result_1['y'][0, i - 1]) / (result_1['t'][i] - result_1['t'][i - 1]) for i in range(1, len(result_1['t']))]))
                t_a         = np.append(t_a, result_1['t'][1:])
                
                y_0 = result_1['y'][:, -1]
                h_t = 0
                t_0 = t_f
                
                y_0[2] -= Launcher.R_E
        
        # * Stage 2
        
        if self._use_stage_2:
        
            Launcher.stage = self._stage_2
            
            t_f = min(self.final_integration_time, self._stage_1.t_burn * self._use_stage_1 + self._stage_2.t_burn)
            
            if t_f > t_0:
                
                result_2 = Launcher.simulate_launch(y_0, h_t=h_t, t_0=t_0, t_f=t_f)
                
                result['y'] = np.append(result['y'], result_2['y'], axis=1)
                result['t'] = np.append(result['t'], result_2['t'])
                a           = np.append(a, np.array([(result_2['y'][0, i] - result_2['y'][0, i - 1]) / (result_2['t'][i] - result_2['t'][i - 1]) for i in range(1, len(result_2['t']))]))
                t_a         = np.append(t_a, result_2['t'][1:])
                
                y_0 = result_2['y'][:, -1]
                h_t = 0
                t_0 = t_f
                
                y_0[2] -= Launcher.R_E
            
        # * Stage 3
        
        if self._use_stage_3:
            
            Launcher.stage = self._stage_3
            
            t_f = min(self.final_integration_time, self._stage_1.t_burn * self._use_stage_1 + self._stage_2.t_burn * self._use_stage_2 + self._stage_3.t_burn)
            
            if t_f > t_0:
                
                result_3 = Launcher.simulate_launch(y_0, h_t=h_t, t_0=t_0, t_f=t_f)
                
                result['y'] = np.append(result['y'], result_3['y'], axis=1)
                result['t'] = np.append(result['t'], result_3['t'])
                a           = np.append(a, np.array([(result_3['y'][0, i] - result_3['y'][0, i - 1]) / (result_3['t'][i] - result_3['t'][i - 1]) for i in range(1, len(result_3['t']))]))
                t_a         = np.append(t_a, result_3['t'][1:])
        
        # * Removes the first element
        
        result['y'] = np.delete(result['y'], 0, axis=1)
        result['t'] = np.delete(result['t'], 0)
        a           = np.delete(a, 0)
        t_a         = np.delete(t_a, 0)
        
        V           = result['y'][0, :]
        gamma       = result['y'][1, :]
        r           = result['y'][2, :]
        x           = result['y'][3, :]
        m           = result['y'][4, :]
        V_D_loss    = result['y'][5, :]
        V_G_loss    = result['y'][6, :]
        t           = result['t']
        
        # ? Plot
        
        self.figure.reset_canvas()
        
        self.figure.axes[0,0].plot(t, V, color='#FFCC80', label='Velocity [$km\;/\;s$] - Time [$s$]')
        self.figure.axes[0,0].legend()
        self.figure.axes[0,0].text(x=0.5,
                                   y=0.95,
                                   s=f'$V_f = {V[-1]:.3f}\;\;km/s$',
                                   size=12,
                                   rotation=0,
                                   ha='center',
                                   va='center',
                                   transform = self.figure.axes[0,0].transAxes,
                                   bbox=dict(boxstyle='round', ec='#FFCC80', fc='#FFCC8080'))
        
        self.figure.axes[0,1].plot(t_a, a / Launcher.g_E, color='#90CAF9', label='Acceleration [$g$] - Time [$s$]')
        self.figure.axes[0,1].legend()
        self.figure.axes[0,1].text(x=0.5,
                                   y=0.95,
                                   s='$a_{max} = ' + f'{(max(a) / Launcher.g_E):.3f}\;\;g$',
                                   size=12,
                                   rotation=0,
                                   ha='center',
                                   va='center',
                                   transform = self.figure.axes[0,1].transAxes,
                                   bbox=dict(boxstyle='round', ec='#90CAF9', fc='#90CAF980'))
        
        self.figure.axes[1,0].plot(t, np.rad2deg(gamma), color='#F48FB1', label='Flight Path Angle [$deg$] - Time [$s$]')
        self.figure.axes[1,0].legend()
        self.figure.axes[1,0].text(x=0.5,
                                   y=0.95,
                                   s=f'$\gamma_f = {np.rad2deg(gamma)[-1]:.3f}\;\;\deg$',
                                   size=12,
                                   rotation=0,
                                   ha='center',
                                   va='center',
                                   transform = self.figure.axes[1,0].transAxes,
                                   bbox=dict(boxstyle='round', ec='#F48FB1', fc='#F48FB180'))
        
        self.figure.axes[1,1].plot(x, r - Launcher.R_E, color='#CE93D8', label='Altitude [$km$] - Downrange Distance [$km$]')
        self.figure.axes[1,1].legend()
        self.figure.axes[1,1].text(x=0.5,
                                   y=0.95,
                                   s=f'$h_f = {(r[-1] - Launcher.R_E):.3f}\;\;km$',
                                   size=12,
                                   rotation=0,
                                   ha='center',
                                   va='center',
                                   transform = self.figure.axes[1,1].transAxes,
                                   bbox=dict(boxstyle='round', ec='#CE93D8', fc='#CE93D880'))
        
        mplcyberpunk.make_lines_glow(self.figure.axes[0,0])
        mplcyberpunk.make_lines_glow(self.figure.axes[0,1])
        mplcyberpunk.make_lines_glow(self.figure.axes[1,0])
        mplcyberpunk.make_lines_glow(self.figure.axes[1,1])
        
        self.figure.redraw_canvas()
    
    @qtCore.Slot()
    def calculate_staging(self) -> None:
        """Calculates all the parameters of the staging
        """
        
        if self._use_stage_1 and self._use_stage_2 and self._use_stage_3:
            
            Launcher.three_stage_vehicle_to_orbit()
        
        elif self._use_stage_1 and self._use_stage_2 and not self._use_stage_3:
            
            Launcher.two_stage_vehicle_to_orbit()
        
        elif self._use_stage_1 and not self._use_stage_2 and not self._use_stage_3:
            
            Launcher.single_stage_vehicle_to_orbit()
    
    # --- PRIVATE METHODS 
    
    def init_figure(self) -> None:
        """Initializes the figure canvas
        """
        
        self.figure.reset_canvas()
            
        self.figure.axes[0,0].plot(0, 0, color='#FFCC80', label='Velocity [$km\;/\;s$] - Time [$s$]')
        self.figure.axes[0,0].legend()
        
        self.figure.axes[0,1].plot(0, 0, color='#90CAF9', label='Acceleration [$g$] - Time [$s$]')
        self.figure.axes[0,1].legend()
        
        self.figure.axes[1,0].plot(0, 0, color='#F48FB1', label='Flight Path Angle [$deg$] - Time [$s$]')
        self.figure.axes[1,0].legend()
        
        self.figure.axes[1,1].plot(0, 0, color='#CE93D8', label='Altitude [$km$] - Downrange Distance [$km$]')
        self.figure.axes[1,1].legend()
        
        self.figure.redraw_canvas()