""" Maneuver.py: Generic maneuver for QML """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore

from enum import IntEnum

from common import format

# --- ENUM 

class ManeuverType(IntEnum):
    """List of maneuvers for orbit transfer"""
    
    HOHMANN             = 0
    BI_ELLIPTIC_HOHMANN = 1
    PLANE_CHANGE        = 2
    APSE_LINE_ROTATION  = 3

# --- CLASS 

class Maneuver(qtCore.QObject):
    """Class that manages the generic maneuver and interfaces with QML"""
    
    # --- PROPERTIES 
    
    # ? Type
    
    @qtCore.Property(int)
    def type(self): return self._type

    @type.setter
    def type(self, value : int): self._type = value
    
    # ? Option

    @qtCore.Property(int)
    def option(self): return self._option

    @option.setter
    def option(self, value : int): self._option = value
    
    # ? Option Value
    
    @qtCore.Property(float)
    def option_value(self): return self._option_value

    @option_value.setter
    def option_value(self, value : float): self._option_value = value
    
    # ? Delta Velocity [km/s]
    
    @qtCore.Property(float)
    def delta_velocity(self): return format(self._delta_velocity)

    @delta_velocity.setter
    def delta_velocity(self, value : float): self._delta_velocity = value
    
    # ? Delta Time [s]
    
    @qtCore.Property(float)
    def delta_time(self): return format(self._delta_time, format='1.0000')

    @delta_time.setter
    def delta_time(self, value : float): self._delta_time = value
    
    # ? Delta Mass [kg]
    
    @qtCore.Property(float)
    def delta_mass(self): return format(self._delta_mass, format='1.000')

    @delta_mass.setter
    def delta_mass(self, value : float): self._delta_mass = value
    
    # --- METHODS 
    
    def __init__(self,
                 type : int,
                 option : int,
                 option_value : float,
                 delta_velocity : float = 0.0,
                 delta_time : float = 0.0,
                 delta_mass : float = 0.0,
                 parent = None):
        """Constructor

        Args:
            type (int): Maneuver type
            option (int): Maneuver option
            option_value (float): Maneuver option value
            delta_velocity (float, optional): Maneuver delta velocity [km/s]. Defaults to 0.0.
            delta_time (float, optional): Maneuver delta time [s]. Defaults to 0.0.
            delta_mass (float, optional): Maneuver delta mass [kg]. Defaults to 0.0.
            parent (_type_, optional): Parent Qt object. Defaults to None.
        """
        
        super().__init__(parent)
        
        self._type              = type              # * Type of maneuver
        self._option            = option            # * Option selection for a given maneuver
        self._option_value      = option_value      # * Optional value for the option parameter
        self._delta_velocity    = delta_velocity    # * Delta velocity cost of the maneuver     [ km / s]
        self._delta_time        = delta_time        # * Delta time of the maneuver              [ s ]
        self._delta_mass        = delta_mass        # * Delta mass cost of the maneuver         [ kg ]