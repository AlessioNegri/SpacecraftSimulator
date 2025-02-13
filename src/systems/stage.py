""" stage.py: Stage object for QML """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore

import tools.launch_mechanics as lm

from src.common import format

class Stage(qtCore.QObject, lm.Stage):
    """This class describes the properties and parameters of a Launcher's Stage"""
    
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
    
    # ? Propellant fraction []
    
    @qtCore.Property(float)
    def propellant_fraction(self): return format(self.k_p)

    @propellant_fraction.setter
    def propellant_fraction(self, val : float): self.k_p = val
    
    # ? Structure fraction []
    
    @qtCore.Property(float)
    def structure_fraction(self): return format(self.k_s)

    @structure_fraction.setter
    def structure_fraction(self, val : float): self.k_s = val
    
    # ? Diameter [m]
    
    @qtCore.Property(float)
    def diameter(self): return format(self.D)

    @diameter.setter
    def diameter(self, val : float): self.D = val
    
    # ? Top Diameter [m]
    
    @qtCore.Property(float)
    def top_diameter(self): return format(self.d)

    @top_diameter.setter
    def top_diameter(self, val : float): self.d = val
    
    # ? Height [m]
    
    @qtCore.Property(float)
    def height(self): return format(self.h)

    @height.setter
    def height(self, val : float): self.h = val
    
    # ? Stage Center Of Gravity Height [m]
    
    @qtCore.Property(float)
    def stage_center_of_gravity_height(self): return format(self.h_CG)

    @stage_center_of_gravity_height.setter
    def stage_center_of_gravity_height(self, val : float): self.h_CG = val
    
    # ? Stage Moment Of Inertia [kg * m^2]
    
    @qtCore.Property(float)
    def stage_moment_of_inertia(self): return format(self.I)

    @stage_moment_of_inertia.setter
    def stage_moment_of_inertia(self, val : float): self.I = val
    
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
    
    # ? Thrust To Weight Ratio []
    
    @qtCore.Property(float)
    def thrust_to_weight_ratio(self): return format(self.F_to_W)

    @thrust_to_weight_ratio.setter
    def thrust_to_weight_ratio(self, val : float): self.F_to_W = val
    
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
        """
        
        qtCore.QObject.__init__(self)
        lm.Stage.__init__(self)