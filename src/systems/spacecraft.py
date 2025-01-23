""" spacecraft.py: Spacecraft object for QML """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml

from src.common import format, singleton

@singleton
class Spacecraft(qtCore.QObject):
    """This class describes the properties and parameters of a Spacecraft"""
    
    # --- PROPERTIES 
    
    # ? Initial Mass [kg]
    
    @qtCore.Property(float)
    def initial_mass(self): return format(self._initial_mass)

    @initial_mass.setter
    def initial_mass(self, val : float): self._initial_mass = val
    
    # ? Mass [kg]
    
    @qtCore.Property(float)
    def mass(self): return format(self._mass)

    @mass.setter
    def mass(self, val : float): self._mass = val
    
    # ? Specific Impulse [s]
    
    @qtCore.Property(float)
    def specific_impulse(self): return format(self._specific_impulse)

    @specific_impulse.setter
    def specific_impulse(self, val : float): self._specific_impulse = val
    
    # ? Thrust [N]
    
    @qtCore.Property(float)
    def thrust(self): return format(self._thrust)

    @thrust.setter
    def thrust(self, val : float): self._thrust = val
    
    # ? Lift Coefficient []
    
    @qtCore.Property(float)
    def lift_coefficient(self): return format(self._lift_coefficient)

    @lift_coefficient.setter
    def lift_coefficient(self, val : float): self._lift_coefficient = val
    
    # ? Drag Coefficient []
    
    @qtCore.Property(float)
    def drag_coefficient(self): return format(self._drag_coefficient)

    @drag_coefficient.setter
    def drag_coefficient(self, val : float): self._drag_coefficient = val
    
    # ? Reference Surface [m^2]
    
    @qtCore.Property(float)
    def reference_surface(self): return format(self._reference_surface)

    @reference_surface.setter
    def reference_surface(self, val : float): self._reference_surface = val
    
    # ?  Radiation Pressure Coefficient []
    
    @qtCore.Property(float)
    def radiation_pressure_coefficient(self): return format(self._radiation_pressure_coefficient)

    @radiation_pressure_coefficient.setter
    def radiation_pressure_coefficient(self, val : float): self._radiation_pressure_coefficient = val
    
    # ? Absorbing Surface [m^2]
    
    @qtCore.Property(float)
    def absorbing_surface(self): return format(self._absorbing_surface)

    @absorbing_surface.setter
    def absorbing_surface(self, val : float): self._absorbing_surface = val
    
    # --- METHODS 
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__Spacecraft", self)
        
        self._initial_mass                      : float = 2000.0    # * Initial Mass                    [ kg ]
        self._mass                              : float = 2000.0    # * Current Mass                    [ kg ]
        self._specific_impulse                  : float = 300.0     # * Specific Impulse                [ s ]
        self._thrust                            : float = 10e3      # * Thrust                          [ kg * m / s^2 ]
        self._lift_coefficient                  : float = 0.0       # * Lift Coefficient                [ ]
        self._drag_coefficient                  : float = 1.0       # * Drag Coefficient                [ ]
        self._reference_surface                 : float = 1.0       # * Reference Surface               [ m^2 ]
        self._radiation_pressure_coefficient    : float = 2.0       # * Radiation Pressure Coefficient  [ ]
        self._absorbing_surface                 : float = 10        # * Absorbing Surface               [ m^2 ]
    
    def reset(self) -> None:
        """Resets the spacecraft parameters
        """
        
        self._mass = self._initial_mass
    
    def update_mass(self, consumed_mass : float) -> None:
        """Updates the current mass subtracting the consumed one

        Args:
            consumed_mass (float): Consumed mass [kg]
        """
        
        if self._mass >= consumed_mass:
        
            self._mass -= consumed_mass