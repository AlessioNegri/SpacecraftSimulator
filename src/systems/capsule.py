""" capsule.py: Capsule object for QML """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml

from utility import format, singleton

@singleton
class Capsule(qtCore.QObject):
    """This class describes the properties and parameters of a Capsule"""
    
    # --- PROPERTIES 
    
    # ? Capsule Mass [kg]
    
    @qtCore.Property(float)
    def capsule_mass(self): return format(self._capsule_mass)

    @capsule_mass.setter
    def capsule_mass(self, val : float): self._capsule_mass = val
    
    # ? Capsule Nose Radius [m]
    
    @qtCore.Property(float)
    def capsule_nose_radius(self): return format(self._capsule_nose_radius)

    @capsule_nose_radius.setter
    def capsule_nose_radius(self, val : float): self._capsule_nose_radius = val
    
    # ? Capsule Lift Coefficient []
    
    @qtCore.Property(float)
    def capsule_lift_coefficient(self): return format(self._capsule_lift_coefficient)

    @capsule_lift_coefficient.setter
    def capsule_lift_coefficient(self, val : float): self._capsule_lift_coefficient = val
    
    # ? Capsule Drag Coefficient []
    
    @qtCore.Property(float)
    def capsule_drag_coefficient(self): return format(self._capsule_drag_coefficient)

    @capsule_drag_coefficient.setter
    def capsule_drag_coefficient(self, val : float): self._capsule_drag_coefficient = val
    
    # ? Capsule Reference Surface [m^2]
    
    @qtCore.Property(float)
    def capsule_reference_surface(self): return format(self._capsule_reference_surface)

    @capsule_reference_surface.setter
    def capsule_reference_surface(self, val : float): self._capsule_reference_surface = val
    
    # ? Parachute Drag Coefficient []
    
    @qtCore.Property(float)
    def parachute_drag_coefficient(self): return format(self._parachute_drag_coefficient)

    @parachute_drag_coefficient.setter
    def parachute_drag_coefficient(self, val : float): self._parachute_drag_coefficient = val
    
    # ? Parachute Reference Surface [m^2]
    
    @qtCore.Property(float)
    def parachute_reference_surface(self): return format(self._parachute_reference_surface)

    @parachute_reference_surface.setter
    def parachute_reference_surface(self, val : float): self._parachute_reference_surface = val
    
    # --- METHODS 
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__Capsule", self)
        
        self._capsule_mass                  : float = 26.27 # * Capsule Mass                [ kg ]
        self._capsule_nose_radius           : float = 0.3   # * Capsule Nose Radius         [ m ]
        self._capsule_lift_coefficient      : float = 0.0   # * Capsule Lift Coefficient    [ ]
        self._capsule_drag_coefficient      : float = 1.096 # * Capsule Drag Coefficient    [ ]
        self._capsule_reference_surface     : float = 0.341 # * Capsule Reference Surface   [ m^2 ]
        self._parachute_drag_coefficient    : float = 1.4   # * Parachute Drag Coefficient  [ ]
        self._parachute_reference_surface   : float = 70    # * Parachute Reference Surface [ m^2 ]