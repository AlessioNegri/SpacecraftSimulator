import PySide6.QtCore as core

from tools.stdafx import *
from tools.InterplanetaryTrajectories import *

class PorkChopPlot(core.QThread):
    
    statusChanged = core.Signal(float, str)
    
    finished = core.Signal()
    
    def __init__(self, parent : core.QObject = None) -> None:
        """Constructor

        Args:
            parent (QDialog): QDialog
        """
        
        super().__init__(parent)
        
        self.dv_1 = None
        self.dv_2 = None
        self.T_F = None
        self.X = None
        self.Y = None
        
        self.departurePlanet = CelestialBody.EARTH
        self.arrivalPlanet = CelestialBody.NEPTUNE
        self.launchWindow = [datetime(2020, 1, 1, 0, 0, 0), datetime(2021, 1, 1, 0, 0, 0)]
        self.arrivalWindow = [datetime(2031, 1, 1, 0, 0, 0), datetime(2032, 6, 1, 0, 0, 0)]
        self.step = 10
        self.stop = False
    
    def run(self) -> None:
        """QThreas run method
        """
        
        self.calculate()
    
    def calculate(self) -> None:
        """Calculates the Pork Chop
        """
        
        # * 1. Extract dates
        
        lwBeg, lwEnd = self.launchWindow
        
        awBeg, awEnd = self.arrivalWindow
        
        # * 2. Cycle of time windows
        
        self.dv_1   = np.zeros(shape=(daterangeLength(awBeg, awEnd, self.step), daterangeLength(lwBeg, lwEnd, self.step)), dtype=float)
        self.dv_2   = np.zeros(shape=(daterangeLength(awBeg, awEnd, self.step), daterangeLength(lwBeg, lwEnd, self.step)), dtype=float)
        self.T_F    = np.zeros(shape=(daterangeLength(awBeg, awEnd, self.step), daterangeLength(lwBeg, lwEnd, self.step)), dtype=float)
        self.X      = np.empty(shape=(daterangeLength(awBeg, awEnd, self.step), daterangeLength(lwBeg, lwEnd, self.step)), dtype='datetime64[s]')
        self.Y      = np.empty(shape=(daterangeLength(awBeg, awEnd, self.step), daterangeLength(lwBeg, lwEnd, self.step)), dtype='datetime64[s]')

        self.statusChanged.emit(0, 'Start')
        
        for lwIndex, lwDate in enumerate(daterange(lwBeg, lwEnd, self.step)):
            
            self.statusChanged.emit(lwIndex / float(daterangeLength(lwBeg, lwEnd, self.step)), 'Processing...')
            #printProgressBar(lwIndex, daterangeLength(lwBeg, lwEnd, self.step), prefix = 'Progress:', suffix = 'Processing...', length = 50)
            
            for awIndex, awDate in enumerate(daterange(awBeg, awEnd, self.step)):
        
                # * a. Extract ephemeris
                
                R_1, V_1 = InterplanetaryTrajectories.Ephemeris(self.departurePlanet, lwDate)
                R_2, V_2 = InterplanetaryTrajectories.Ephemeris(self.arrivalPlanet, awDate)
                
                dt = (awDate - lwDate).total_seconds()
                
                self.T_F[awIndex, lwIndex] = dt / 3600 / 24
                
                # * b. Lambert problem
                
                OrbitDetermination.setCelestialBody(CelestialBody.SUN)
                
                V_D_v, V_A_v, oe, theta_2 = OrbitDetermination.solveLambertProblem(R_1, R_2, dt)
                
                # * c. Hyperbolic excess velocities
                
                self.dv_1[awIndex, lwIndex] = linalg.norm(V_D_v - V_1)
                self.dv_2[awIndex, lwIndex] = linalg.norm(V_A_v - V_2)
                
                # * d. Times
                
                self.X[awIndex, lwIndex] = np.datetime64(lwDate.strftime('%Y-%m-%d'))
                self.Y[awIndex, lwIndex] = np.datetime64(awDate.strftime('%Y-%m-%d'))
                
                # * e. Check stop event
                
                if self.stop:
                    
                    self.stop = False
                    
                    self.statusChanged.emit(0, 'Stopped')
                    self.finished.emit()
                    
                    return
        
        self.statusChanged.emit(1, 'Finished')
        self.finished.emit()