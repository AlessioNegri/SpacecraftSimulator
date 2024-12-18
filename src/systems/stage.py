""" stage.py: Stage object for QML """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml

import tools.launch_mechanics as lm

from common import format

class Stage(qtCore.QObject, lm.Stage):
    """This class describes the properties and parameters of a Launcher Stage"""
    
    # --- PROPERTIES 
    
    # ? Structural Mass [kg]
    
    @qtCore.Property(float)
    def structural_mass(self): return format(self.m_s)

    @structural_mass.setter
    def structural_mass(self, val : float): self.m_s = val
    
    # ? Propellant Mass [kg]
    
    @qtCore.Property(float)
    def propellant_mass(self): return format(self.m_p)

    @propellant_mass.setter
    def propellant_mass(self, val : float): self.m_p = val
    
    # ? Diameter [m]
    
    @qtCore.Property(float)
    def diameter(self): return format(self.D)

    @diameter.setter
    def diameter(self, val : float): self.D = val
    
    # ? Gross Mass [kg]
    
    @qtCore.Property(float)
    def gross_mass(self): return format(self.m_g)

    @gross_mass.setter
    def gross_mass(self, val : float): self.m_g = val
    
    # ? Payload Mass [kg]
    
    @qtCore.Property(float)
    def payload_mass(self): return format(self.m_payload)

    @payload_mass.setter
    def payload_mass(self, val : float): self.m_payload = val
    
    # ? Total Mass [kg]
    
    @qtCore.Property(float)
    def total_mass(self): return format(self.m_0)

    @total_mass.setter
    def total_mass(self, val : float): self.m_0 = val
    
    # ? Vacuum Specific Impulse [s]
    
    @qtCore.Property(float)
    def vacuum_specific_impulse(self): return format(self.I_sp_vac)

    @vacuum_specific_impulse.setter
    def vacuum_specific_impulse(self, val : float): self.I_sp_vac = val
    
    # ? Vacuum Thrust [N]
    
    @qtCore.Property(float)
    def vacuum_thrust(self): return format(self.F_vac)

    @vacuum_thrust.setter
    def vacuum_thrust(self, val : float): self.F_vac = val
    
    # ? Propellant Mass Flow Rate [kg/s]
    
    @qtCore.Property(float)
    def propellant_mass_flow_rate(self): return format(self.m_p_dot)

    @propellant_mass_flow_rate.setter
    def propellant_mass_flow_rate(self, val : float): self.m_p_dot = val
    
    # ? Burn Time [s]
    
    @qtCore.Property(float)
    def burn_time(self): return format(self.t_burn)

    @burn_time.setter
    def burn_time(self, val : float): self.t_burn = val
    
    # ? Drag Coefficient []
    
    @qtCore.Property(float)
    def drag_coefficient(self): return format(self.C_D)

    @drag_coefficient.setter
    def drag_coefficient(self, val : float): self.C_D = val
    
    # ? Lift Coefficient []
    
    @qtCore.Property(float)
    def lift_coefficient(self): return format(self.C_L)

    @lift_coefficient.setter
    def lift_coefficient(self, val : float): self.C_L = val
    
    # ? Reference Surface [m^2]
    
    @qtCore.Property(float)
    def reference_surface(self): return format(self.S)

    @reference_surface.setter
    def reference_surface(self, val : float): self.S = val
    
    # --- METHODS 
    
    def __init__(self) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        lm.Stage.__init__(self)