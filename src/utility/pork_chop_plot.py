""" pork_chop_plot.py: Thread dedicated to the Pork Chop Plot evaluation """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as core
import numpy as np

from datetime import datetime

from tools.Common import daterange, daterange_length
from tools.AstronomicalData import CelestialBody
from tools.InterplanetaryTrajectories import InterplanetaryTrajectories
from tools.OrbitDetermination import OrbitDetermination

class PorkChopPlot(core.QThread):
    """Evaluates the pork chop plot"""
    
    # --- SIGNALS 
    
    # ? Signal emitted when the status has changed.
    status_changed = core.Signal(float, str)
    
    # ? Signal emitted when the operation has finished.
    finished = core.Signal()
    
    # --- METHODS 
    
    def __init__(self, parent : core.QObject = None) -> None:
        """Constructor

        Args:
            parent (QDialog): QDialog
        """
        
        super().__init__(parent)
        
        self.dv_1   = None # * List of departure delta velocity [ km / s ]
        self.dv_2   = None # * List of arrival delta velocity   [ km / s ]
        self.T_F    = None # * List of time of flight           [ s ]
        self.X      = None # * List of departure date-time      [ ]
        self.Y      = None # * List of arrival date-time        [ ]
        
        self.departure_planet   = CelestialBody.EARTH                                               # * Departure planet
        self.arrival_planet     = CelestialBody.NEPTUNE                                             # * Arrival planet
        self.launch_window      = [datetime(2020, 1, 1, 0, 0, 0), datetime(2021, 1, 1, 0, 0, 0)]    # * Launch window
        self.arrival_window     = [datetime(2031, 1, 1, 0, 0, 0), datetime(2032, 6, 1, 0, 0, 0)]    # * Arrival window
        self.step               = 10                                                                # * Simulation step     [ s ]
        self.stop               = False                                                             # * Stop simuation
    
    def run(self) -> None:
        """QThread run method
        """
        
        self.calculate()
    
    def calculate(self) -> None:
        """Calculates the Pork Chop
        """
        
        # >>> 1. Extract dates
        
        lwBeg, lwEnd = self.launch_window
        
        awBeg, awEnd = self.arrival_window
        
        # >>> 2. Prepare structures
        
        self.dv_1   = np.zeros(shape=(daterange_length(awBeg, awEnd, self.step), daterange_length(lwBeg, lwEnd, self.step)), dtype=float)
        self.dv_2   = np.zeros(shape=(daterange_length(awBeg, awEnd, self.step), daterange_length(lwBeg, lwEnd, self.step)), dtype=float)
        self.T_F    = np.zeros(shape=(daterange_length(awBeg, awEnd, self.step), daterange_length(lwBeg, lwEnd, self.step)), dtype=float)
        self.X      = np.empty(shape=(daterange_length(awBeg, awEnd, self.step), daterange_length(lwBeg, lwEnd, self.step)), dtype='datetime64[s]')
        self.Y      = np.empty(shape=(daterange_length(awBeg, awEnd, self.step), daterange_length(lwBeg, lwEnd, self.step)), dtype='datetime64[s]')

        # >>> 3. Cycle of time windows

        previous_percentage = -1
        
        current_percentage = 0

        self.status_changed.emit(0, 'Start')
        
        for lwIndex, lwDate in enumerate(daterange(lwBeg, lwEnd, self.step)):
            
            current_percentage = lwIndex / float(daterange_length(lwBeg, lwEnd, self.step))
            
            if (int(current_percentage * 100) != previous_percentage):
            
                previous_percentage = int(current_percentage)
            
                self.status_changed.emit(current_percentage, 'Processing...')
            
            for awIndex, awDate in enumerate(daterange(awBeg, awEnd, self.step)):
        
                # >>> a. Extract ephemeris
                
                R_1, V_1 = InterplanetaryTrajectories.ephemeris(self.departure_planet, lwDate)
                R_2, V_2 = InterplanetaryTrajectories.ephemeris(self.arrival_planet, awDate)
                
                dt = (awDate - lwDate).total_seconds()
                
                self.T_F[awIndex, lwIndex] = dt / 3600 / 24
                
                # >>> b. Lambert problem
                
                OrbitDetermination.set_celestial_body(CelestialBody.SUN)
                
                V_D_v, V_A_v, oe, theta_2 = OrbitDetermination.solve_lambert_problem(R_1, R_2, dt)
                
                # >>> c. Hyperbolic excess velocities
                
                self.dv_1[awIndex, lwIndex] = np.linalg.norm(V_D_v - V_1)
                self.dv_2[awIndex, lwIndex] = np.linalg.norm(V_A_v - V_2)
                
                # >>> d. Times
                
                self.X[awIndex, lwIndex] = np.datetime64(lwDate.strftime('%Y-%m-%d'))
                self.Y[awIndex, lwIndex] = np.datetime64(awDate.strftime('%Y-%m-%d'))
                
                # >>> e. Check stop event
                
                if self.stop:
                    
                    self.stop = False
                    
                    self.status_changed.emit(0, 'Stopped')
                    self.finished.emit()
                    
                    return
        
        self.status_changed.emit(1, 'Finished')
        self.finished.emit()