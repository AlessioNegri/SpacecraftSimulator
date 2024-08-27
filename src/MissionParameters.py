import os
import sys
import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml

sys.path.append(os.path.dirname(__file__))

from Spacecraft import Spacecraft
from MissionOrbitTransfer import MissionOrbitTransfer
from MissionOrbitPropagation import MissionOrbitPropagation
from MissionInterplanetaryTransfer import MissionInterplanetaryTransfer
from MissionAtmosphericEntry import MissionAtmosphericEntry

class MissionParameters(qtCore.QObject):
    """Class that manages the mission parameters
    """
    
    # ! CONSTRUCTOR

    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        self.spacecraft = Spacecraft(engine)
        
        self.mission_orbit_transfer = MissionOrbitTransfer(engine)
        
        self.mission_orbit_transfer.loadDepartureOrbit()
        self.mission_orbit_transfer.loadArrivalOrbit()
        
        self.mission_orbit_propagation = MissionOrbitPropagation(engine)
        
        self.mission_interplanetary_transfer = MissionInterplanetaryTransfer(engine)
        
        self.mission_atmospheric_entry = MissionAtmosphericEntry(engine)
        
    # ! PUBLIC
    
    def setUpdateWithCanvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Connects all the QML figures with the backend model

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        self.mission_orbit_transfer.setUpdateWithCanvas(engine)
        
        self.mission_orbit_propagation.setUpdateWithCanvas(engine)
        
        self.mission_interplanetary_transfer.setUpdateWithCanvas(engine)
        
        self.mission_atmospheric_entry.set_update_with_canvas(engine)