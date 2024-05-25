import os
import sys
import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml

sys.path.append(os.path.dirname(__file__))

from tools.stdafx import IntEnum, dataclass
from Utility import format

class ManeuverType(IntEnum):
    
    HOHMANN             = 0
    BI_ELLIPTIC_HOHMANN = 1
    PLANE_CHANGE        = 2
    APSE_LINE_ROTATION  = 3
    

#QML_IMPORT_NAME = "extension.maneuver"
#QML_IMPORT_MAJOR_VERSION = 1

#@qtQml.QmlElement
#@dataclass
class Maneuver(qtCore.QObject):
    """Class that manages the generic maneuver and interfaces with QML

    Args:
        qtCore (_type_): _description_
    """
    
    def __init__(self,
                 type : int,
                 option : int,
                 optionValue : float,
                 dv : float = 0.0,
                 dt : float = 0.0,
                 dm : float = 0.0,
                 parent = None):
        """Constructor

        Args:
            type (int): Maneuver type
            option (int): Maneuver option
            optionValue (float): Maneuver option value
            dv (float, optional): Maneuver delta velocity. Defaults to 0.0.
            dt (float, optional): Maneuver delta time. Defaults to 0.0.
            dm (float, optional): Maneuver delta mass. Defaults to 0.0.
            parent (_type_, optional): Parent Qt object. Defaults to None.
        """
        
        super().__init__(parent)
        
        self._type          = type
        self._option        = option
        self._optionValue   = optionValue
        self._dv            = dv
        self._dt            = dt
        self._dm            = dm
    
    # ! LOCAL
    
    def getType(self): return self._type
    
    def getOption(self): return self._option
    
    def getOptionValue(self): return self._optionValue
    
    def getDeltaVelocity(self): return self._dv
    
    def getDeltaTime(self): return self._dt
    
    def getDeltaMass(self): return self._dm
    
    def setDeltaVelocity(self, dv : float): self._dv = dv
    
    def setDeltaTime(self, dt : float): self._dt = dt
    
    def setDeltaMass(self, dm : float): self._dm = dm
    
    # ! QML

    @qtCore.Property(int)
    def type(self): return self._type

    @type.setter
    def type(self, n : int): self._type = n

    @qtCore.Property(int)
    def option(self): return self._option

    @option.setter
    def option(self, n : int): self._option = n
    
    @qtCore.Property(float)
    def optionValue(self): return self._optionValue

    @optionValue.setter
    def optionValue(self, f : float): self._optionValue = f
    
    @qtCore.Property(float)
    def dv(self): return format(self._dv)

    @dv.setter
    def dv(self, f : float): self._dv = f
    
    @qtCore.Property(float)
    def dt(self): return format(self._dt, format='1.0000')

    @dt.setter
    def dt(self, f : float): self._dt = f
    
    @qtCore.Property(float)
    def dm(self): return format(self._dm, format='1.000')

    @dm.setter
    def dm(self, f : float): self._dm = f