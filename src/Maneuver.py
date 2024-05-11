import os
import sys
import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml

sys.path.append(os.path.dirname(__file__))

from tools.stdafx import IntEnum, dataclass

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
    
    def __init__(self, type : int, option : int, optionValue : float, parent = None):
        """Constructor

        Args:
            type (int): Maneuver type
            option (int): Maneuver option
            optionValue (float): Maneuver option value
            parent (_type_, optional): Parent Qt object. Defaults to None.
        """
        
        super().__init__(parent)
        
        self._type          = type
        self._option        = option
        self._optionValue   = optionValue
    
    # ! LOCAL
    
    def getType(self): return self._type
    
    def getOption(self): return self._option
    
    def getOptionValue(self): return self._optionValue
    
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
    def optionValue(self, f : int): self._optionValue = f