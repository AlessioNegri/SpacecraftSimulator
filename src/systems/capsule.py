""" capsule.py: Capsule object for QML """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml

import numpy as np

from src.common import format, singleton
from tools.AtmosphericEntry import AtmosphericEntry

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
    
    # ? Capsule Body Radius [m]
    
    @qtCore.Property(float)
    def capsule_body_radius(self): return format(self._capsule_body_radius)

    @capsule_body_radius.setter
    def capsule_body_radius(self, val : float): self._capsule_body_radius = val
    
    # ? Capsule Shield Angle [rad]
    
    @qtCore.Property(float)
    def capsule_shield_angle(self): return format(self._capsule_shield_angle, deg=True)

    @capsule_shield_angle.setter
    def capsule_shield_angle(self, val : float): self._capsule_shield_angle = np.deg2rad(val)
    
    # ? Capsule Afterbody Angle [rad]
    
    @qtCore.Property(float)
    def capsule_afterbody_angle(self): return format(self._capsule_afterbody_angle, deg=True)

    @capsule_afterbody_angle.setter
    def capsule_afterbody_angle(self, val : float): self._capsule_afterbody_angle = np.deg2rad(val)
    
    # ? Specific Heat Ratio []
    
    @qtCore.Property(float)
    def specific_heat_ratio(self): return format(self._specific_heat_ratio)

    @specific_heat_ratio.setter
    def specific_heat_ratio(self, val : float): self._specific_heat_ratio = val
    
    # ? Capsule Zero-Lift Drag Coefficient []
    
    @qtCore.Property(float)
    def capsule_zero_lift_drag_coefficient(self): return format(self._capsule_zero_lift_drag_coefficient)

    @capsule_zero_lift_drag_coefficient.setter
    def capsule_zero_lift_drag_coefficient(self, val : float): self._capsule_zero_lift_drag_coefficient = val
    
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
    
    # ? Capsule Angle Of Attack [rad]
    
    @qtCore.Property(float)
    def capsule_angle_of_attack(self): return format(self._capsule_angle_of_attack, deg=True)

    @capsule_angle_of_attack.setter
    def capsule_angle_of_attack(self, val : float): self._capsule_angle_of_attack = np.deg2rad(val)
    
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
        
        self._capsule_mass                          : float = 26.27                                                             # * Capsule Mass                        [ kg ]
        self._capsule_nose_radius                   : float = 0.3 / 0.33                                                        # * Capsule Nose Radius                 [ m ]
        self._capsule_body_radius                   : float = 0.3                                                               # * Capsule Base Radius                 [ m ]
        self._capsule_shield_angle                  : float = np.asin(self._capsule_body_radius / self._capsule_nose_radius)    # * Capsule Shield Angle                [ rad ]
        self._capsule_afterbody_angle               : float = np.deg2rad(20)                                                    # * Capsule Afterbody Angle             [ rad ]
        self._specific_heat_ratio                   : float = 1.4                                                               # * Specific Heat Ratio                 [ ]
        self._capsule_zero_lift_drag_coefficient    : float = 0.0                                                               # * Capsule Zero-Lift Drag Coefficient  [ ]
        self._capsule_lift_coefficient              : float = 0.0                                                               # * Capsule Lift Coefficient            [ ]
        self._capsule_drag_coefficient              : float = 1.096                                                             # * Capsule Drag Coefficient            [ ]
        self._capsule_reference_surface             : float = np.pi * 0.3**2                                                    # * Capsule Reference Surface           [ m^2 ]
        self._capsule_angle_of_attack               : float = np.deg2rad(0)                                                     # * Capsule Angle Of Attack             [ rad ]
        self._parachute_drag_coefficient            : float = 1.4                                                               # * Parachute Drag Coefficient          [ ]
        self._parachute_reference_surface           : float = 70                                                                # * Parachute Reference Surface         [ m^2 ]
        
        AtmosphericEntry.set_capsule_aerodynamics(self._capsule_nose_radius, self._capsule_body_radius, self._capsule_shield_angle, self._capsule_afterbody_angle, self._specific_heat_ratio)
        
        self._capsule_zero_lift_drag_coefficient, self._capsule_lift_coefficient, self._capsule_drag_coefficient = AtmosphericEntry.calculate_aerodynamics_coefficients(0)
    
    # --- PUBLIC SLOTS 
    
    @qtCore.Slot()
    def update_coefficients(self) -> None:
        """Updates the aerodynamics coefficients based on the new value of the angle of attack
        """
        
        self._capsule_zero_lift_drag_coefficient, self._capsule_lift_coefficient, self._capsule_drag_coefficient = AtmosphericEntry.calculate_aerodynamics_coefficients(self._capsule_angle_of_attack)