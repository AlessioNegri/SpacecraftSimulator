""" mission_parameters.py: Wrapper for all classes """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import os
import sys
import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml

sys.path.append(os.path.dirname(__file__))

from systems.spacecraft import Spacecraft
from systems.capsule import Capsule
from src.missions.mission_orbit_insertion import MissionOrbitInsertion
from src.missions.mission_orbit_transfer import MissionOrbitTransfer
from src.missions.mission_orbit_propagation import MissionOrbitPropagation
from src.missions.mission_interplanetary_transfer import MissionInterplanetaryTransfer
from src.missions.mission_atmospheric_entry import MissionAtmosphericEntry

class MissionParameters(qtCore.QObject):
    """Class that manages the mission parameters"""
    
    # --- CONSTRUCTOR 

    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        self.spacecraft = Spacecraft(engine)
        
        self.capsule = Capsule(engine)
        
        self.mission_orbit_insertion = MissionOrbitInsertion(engine)
        
        self.mission_orbit_transfer = MissionOrbitTransfer(engine)
        
        self.mission_orbit_propagation = MissionOrbitPropagation(engine)
        
        self.mission_interplanetary_transfer = MissionInterplanetaryTransfer(engine)
        
        self.mission_atmospheric_entry = MissionAtmosphericEntry(engine)