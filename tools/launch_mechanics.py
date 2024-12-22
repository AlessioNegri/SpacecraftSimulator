""" launch_mechanics.py: Implements the launch mechanics equations """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"
__book__        = "Manned Spacecraft: Design Principles"
__chapter__     = "7 - Launch Mechanics"

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as ode

sys.path.append(os.path.dirname(__file__))

from scipy.optimize import newton

from AstronomicalData import AstronomicalData, CelestialBody

# --- STAGE CLASS 

class Stage:
    """Implements the generic launcher stage"""
    
    def __init__(self):
        """Constructor
        """
        
        self.m_0        = 0.0   # * Total Mass                  [ kg ]
        self.m_g        = 0.0   # * Gross Mass                  [ kg ]
        self.m_s        = 0.0   # * Structure + Engine Mass     [ kg ]
        self.m_p        = 0.0   # * Propellant Mass             [ kg ]
        self.m_payload  = 0.0   # * Payload Mass                [ kg ]
        self.k_p        = 0.0   # * Propellant Fraction         [ ]
        self.k_s        = 0.0   # * Structure Fraction          [ ]
        
        self.F_vac      = 0.0   # * Vacuum Thrust               [ kg * m / s^2 ]
        self.I_sp_vac   = 0.0   # * Vacuum Specific Impulse     [ s ]
        self.F_to_W     = 0.0   # * Thrust To Weight Ratio      [ ]
        self.t_burn     = 0.0   # * Burn Time                   [ s ]
        self.csi        = 0.0   # * Thrust Angle                [ rad ]
        self.m_p_dot    = 0.0   # * Propellant Mass Flow Rate   [ kg /s ]
        
        self.gamma      = 0.0   # * Specific Heats Ratio        [ ]
        self.Gamma      = 0.0   # * Quantity                    [ ]
        self.epsilon    = 0.0   # * Nozzle Expansion Ratio      [ ]
        self.p_c        = 0.0   # * Combustion Chamber Pressure [ atm ]
        
        self.D          = 0.0   # * Diameter                    [ m ]
        self.S          = 0.0   # * Reference Surface           [ m^2 ]
        self.C_D        = 0.0   # * Drag Coefficient            [ ]
        self.C_L        = 0.0   # * Lift Coefficient            [ ]
    
    def mass(self, m_s : float, m_p : float, m_payload : float) -> None:
        """Sets the masses

        Args:
            m_s (float): Structure + engine mass [kg]
            m_p (float): Propellant mass [kg]
            m_payload (float): Payload mass [kg]
        """
        
        self.m_s        = m_s
        self.m_p        = m_p
        self.m_payload  = m_payload
    
    def motor(self, F_vac : float, I_sp_vac : float, csi : float) -> None:
        """Sets the motor parameters

        Args:
            F_vac (float): Vacuum thrust [kg * m / s^2]
            I_sp_vac (float): Vacuum specific impulse [s]
            csi (float): Thrust angle [rad]
        """
        
        self.F_vac      = F_vac
        self.I_sp_vac   = I_sp_vac
        self.csi        = csi
    
    def nozzle(self, gamma : float, epsilon : float, p_c : float) -> None:
        """Sets the nozzle parameters

        Args:
            gamma (float): Specific heats ratio []
            epsilon (float): Nozzle expansion ratio []
            p_c (float): Combustion chamber pressure [atm]
        """
        
        self.gamma      = gamma
        self.epsilon    = epsilon
        self.p_c        = p_c
        
        if self.gamma == 0:
            
            self.Gamma = 0
            
        else:
        
            self.Gamma = 1 / self.gamma * ((self.gamma - 1 ) * 0.5)**(self.gamma / (self.gamma - 1)) *\
                ((self.gamma + 1) / (self.gamma - 1))**((self.gamma + 1) / (2 * (self.gamma - 1)))
    
    def aerodynamics(self, D : float, C_D : float, C_L : float) -> None:
        """Sets the aerodynamics parameters

        Args:
            D (float): Diameter [m]
            C_D (float): Drag coefficient []
            C_L (float): Lift coefficient [atm]
        """
        
        self.D      = D
        self.S      = np.pi * D**2 / 4
        self.C_D    = C_D
        self.C_L    = C_L
    
    def calc(self) -> None:
        """Calculates the dependent parameters
        """
        
        self.m_g        = self.m_s + self.m_p
        self.m_0        = self.m_g + self.m_payload
        self.m_p_dot    = self.F_vac / (self.I_sp_vac * AstronomicalData.gravity(CelestialBody.EARTH))
        self.t_burn     = self.m_p / self.m_p_dot
        
        self.F_to_W     = self.F_vac / (self.m_0 * AstronomicalData.gravity(CelestialBody.EARTH))
        self.k_p        = self.F_to_W / self.I_sp_vac
        self.k_s        = self.m_s / self.m_p
        
        #print(f'm_p_dot = {self.m_p_dot}')
        #print(f't_burn = {self.t_burn}')
    
    def thrust(self, z : float) -> float:
        """Calculates the thrust in function of the altitude

        Args:
            z (float): Altitude [km]

        Returns:
            float: Thrust [kg * m / s^2]
        """
        
        # * I_sp_bar(z) = I_sp(z) / I_sp_vac
        
        I_sp_bar = 1 - self.Gamma * (self.epsilon * np.exp(- z / 7.16) / self.p_c) if self.p_c != 0 else 1
        
        # * F(z) = F_vac * I_sp_bar(z)
        
        F = self.F_vac * I_sp_bar
        
        return F

# --- LAUNCH CLASS 

class Launcher:
    """Implements the launch mechanics equations"""
    
    # --- MEMBERS 
    
    g_E     = AstronomicalData.gravity(CelestialBody.EARTH, km=True)        # * Sea Level Gravity           [ km / s^2 ]
    R_E     = AstronomicalData.equatiorial_radius(CelestialBody.EARTH)      # * Planet Equatiorial Radius   [ km ]
    k       = AstronomicalData.gravitational_parameter(CelestialBody.EARTH) # * Gravitational Parameter     [ km^3 / s^2 ]
    stage   = Stage()                                                       # * Stage
    H       = 7.5                                                           # * Constant Scale Height       [ km ] 7.16
    
    # --- METHODS 
    
    # ! SECTION 7.1
    
    @classmethod
    def launch_eom(cls, t : float, X : np.ndarray, t_0 : float, stage : Stage, h_t : float) -> np.ndarray:
        """Launch mechanics equations of motion\n
        
        (1) dV/dt     = ( F cos(csi) ) / m - D / m - ( k sin(gamma) ) / r^2\n
        (2) dgamma/dt = ( F sin(csi) ) / (m V) + L / (m V) - ( k cos(gamma) ) / ( V r^2 ) + ( V cos(gamma) ) / r\n
        (3) dr/dt     = V sin(gamma)\n
        (4) dx/dt     = R_E ( V cos(gamma) ) / r\n
        (5) dm/dt     = - F / ( g_E I_sp )
        
        Args:
            t (float): Time [s]
            X (np.ndarray): State [5, 1] -> (V, gamma, r, x, m)
            t_0 (float): Initial integration time [s]
            stage (Stage): Launcher stage
            h_t (float): Height at which pitchover begins [m]

        Returns:
            np.ndarray: Derivative of state
        """
        
        # >>> Parameters
        
        V, gamma, r, x, m, V_D_loss, V_G_loss = X
        
        z = r - cls.R_E
        
        # >>> Stage
        
        F       = stage.thrust(z) * 1e-3    # * [kg * km / s^2]
        csi     = stage.csi                 # * [rad]
        m_p_dot = stage.m_p_dot             # * [kg / s]
        t_burn  = stage.t_burn              # * [s]
        S       = stage.S                   # * [m^2]
        C_D     = stage.C_D                 # * []
        C_L     = stage.C_L                 # * []
        
        # >>> Aerodynamics
        
        rho = 1.225 * np.exp(- z / cls.H) # * [kg / m^3]
        
        L = 0.5 * rho * (V * 1e3)**2 * C_L * S * 1e-3 # * [kg * km / s^2]
        
        D = 0.5 * rho * (V * 1e3)**2 * C_D * S * 1e-3 # * [kg * km / s^2]
        
        # >>> Burning Time
        
        if t - t_0 > t_burn:
            
            m_p_dot = 0
            F = 0
        
        # >>> Equations
        
        dX_dt = np.zeros(shape=(7))
        
        if z < 0:
            
            dX_dt[0] = 0
            dX_dt[1] = 0
            dX_dt[2] = 0
            dX_dt[3] = 0
            dX_dt[4] = 0
            dX_dt[5] = 0
            dX_dt[6] = 0
        
        elif z <= h_t * 1e-3 and gamma > 0:
            
            dX_dt[0] = (F * np.cos(csi)) / m - D / m  - cls.k / r**2
            dX_dt[1] = (F * np.sin(csi)) / (m * V) + L / (m * V) if V != 0 else 0
            dX_dt[2] = V
            dX_dt[3] = 0
            dX_dt[4] = - m_p_dot
            dX_dt[5] = - D / m
            dX_dt[6] = - cls.k / r**2
        
        else:
        
            dX_dt[0] = (F * np.cos(csi)) / m - D / m  - cls.k / r**2 * np.sin(gamma)
            dX_dt[1] = (F * np.sin(csi)) / (m * V) + L / (m * V) - cls.k / (r**2 * V) * np.cos(gamma) + V / r * np.cos(gamma)
            dX_dt[2] = V * np.sin(gamma)
            dX_dt[3] = cls.R_E * V / r * np.cos(gamma)
            dX_dt[4] = - m_p_dot
            dX_dt[5] = - D / m
            dX_dt[6] = - cls.k / r**2 * np.sin(gamma)
        
        return dX_dt
    
    # ! SECTION 7.2 - 7.4
    
    @classmethod
    def simulate_launch(cls, y_0 : np.ndarray, h_t : float = 0.0, t_0 : float = 0.0, t_f : float = 0.0) -> dict:
        """Integrates the Ordinary Differential Equations for the Launch Mechanics

        Args:
            y_0 (np.ndarray): Initial state [5,1] -> (V, gamma, z, x, m)
            h_t (float, optional): Height at which pitchover begins [m]. Defaults to 0.0.
            t_0 (float, optional): Initial time. Defaults to 0.0.
            t_f (float, optional): Final time. Defaults to 0.0.
            
        Returns:
            dict: { t: time, y: state, dt: t - t_0 }
        """
            
        # >>> 1. Integrate ODE 
        
        y_0[2] += cls.R_E
        y_0[4] = cls.stage.m_0
        
        if t_f < t_0: raise Exception('Invalid integration time: t_0 > t_f!')
        
        def terminal_condition(t : float, X : np.ndarray, t_0 : float, stage : Stage, h_t : float) -> bool: return not (X[2] - cls.R_E <= 0 and X[1] < 0)
        
        terminal_condition.terminal = True
        
        integrationResult = ode.solve_ivp(fun=cls.launch_eom, t_span=[t_0, t_f], y0=y_0, method='RK45', rtol=1e-8, atol=1e-8, args=(t_0, cls.stage, h_t), events=terminal_condition)
        
        if not integrationResult['success']: raise Exception(integrationResult['message'])
        
        # >>> 2. Result 
        
        t = integrationResult['t']
        
        return dict(t=t, y=integrationResult['y'], dt=np.abs(t[-1] - t[0]))
        
    @classmethod
    def plot_launch(cls, y : np.ndarray, t : np.ndarray) -> None:
        """Plots the launch trajectory and parameters

        Args:
            y (np.ndarray): Integrated state vector
            t (np.ndarray): Integration time
        """
        
        V           = y[0, :]
        gamma       = y[1, :]
        r           = y[2, :]
        x           = y[3, :]
        m           = y[4, :]
        V_D_loss    = y[5, :]
        V_G_loss    = y[6, :]
        a           = np.array([(V[i] - V[i - 1]) / (t[i] - t[i - 1]) for i in range(1, len(t))])
        
        fig, axes = plt.subplots(2, 2, constrained_layout=True)
        
        fig.suptitle(f"LAUNCH: $V_0 = {V[0] * 1e3:.3f}\;\;m/s$   " +
                     f"$\gamma_0 = {gamma[0]:.3f}\;\;rad$   " +
                     f"$V_f = {V[-1]:.3f}\;\;km/s$   " +
                     f"$\gamma_f = {np.rad2deg(gamma[-1]):.3f}\;\;deg$   " +
                     f"$h_f = {(r[-1] - cls.R_E):.3f}\;\;km$   " +
                     f"$x_f = {x[-1]:.3f}\;\;km$   " +
                     "$V_D^{loss} = " + f"{-V_D_loss[-1]:.3f}\;\;km/s$   " +
                     "$V_G^{loss} = " + f"{-V_G_loss[-1]:.3f}\;\;km/s$")
        
        axes[0,0].set_xlabel("Time [$s$]")
        axes[0,0].set_ylabel("$V$ [$km / s$]")
        axes[0,0].grid()
        axes[0,0].plot(t, V)
        
        axes[0,1].set_xlabel("Time [$s$]")
        axes[0,1].set_ylabel("$\gamma$ [°]")
        axes[0,1].grid()
        axes[0,1].plot(t, np.rad2deg(gamma))
        
        axes[1,0].set_xlabel("Downrange distance $x$ [$km$]")
        axes[1,0].set_ylabel("$z$ [$km$]")
        axes[1,0].grid()
        axes[1,0].plot(x, r - cls.R_E)
        
        axes[1,1].set_xlabel("Time [$s$]")
        axes[1,1].set_ylabel("$dV/dt\;\;(g_E)$")
        axes[1,1].grid()
        axes[1,1].plot(t[1:], a / cls.g_E)
    
    #! SECTION 7.5
    
    @classmethod
    def single_stage_vehicle_to_orbit(cls,
                                      stage : Stage,
                                      V_bo : float,
                                      m_payload : float,
                                      F_W_1 : float,
                                      I_sp_1 : float,
                                      gamma_avg_1 : float = 30,
                                      k_s_1 : float = 0.062) -> Stage:
        """Evaluate the stage parameters for a single stage vehicle to orbit

        Args:
            stage (Stage): Stage
            V_bo (float): Final burnout velocity for orbit insertion [km/s]
            m_payload (float): Payload mass [kg]
            F_W_1 (float): Thrust to weight ratio
            I_sp_1 (float): Specific impulse [s]
            gamma_avg_1 (float, optional): Average value of flight path angle. Defaults to 30.
            k_s_1 (float, optional): Structural fraction. Defaults to 0.062.

        Returns:
            Stage: Updated stage parameters
        """
        
        
        # >>> Propellant fraction
        
        k_p_1 = F_W_1 / I_sp_1
        
        # >>> Burnout time
        
        f = lambda t: V_bo + cls.g_E * I_sp_1 * np.log(1 - k_p_1 * t) + cls.g_E * t * np.sin(np.deg2rad(gamma_avg_1))
        
        f_dot = lambda t: - cls.g_E * I_sp_1 * k_p_1 * 1 / (1 - k_p_1 * t) + cls.g_E * np.sin(np.deg2rad(gamma_avg_1))
        
        t_bo_1 = newton(f, 1 / k_p_1 - 1, f_dot)
        
        # >>> Stack mass
        
        dt_1 = t_bo_1 - 0
        
        m_0_I = m_payload / (1 - (1 + k_s_1) * k_p_1 * dt_1)
        
        # >>> Thrust
        
        F_1 = F_W_1 * m_0_I * cls.g_E * 1e3
        
        # >>> Propellant mass
        
        m_p_1 = k_p_1 * dt_1 * m_0_I
        
        # >>> Structural mass
        
        m_s_1 = k_s_1 * m_p_1
        
        # >>> Update stage
        
        stage.mass(m_s_1, m_p_1, m_payload)
        stage.motor(F_1, I_sp_1, stage.csi)
        stage.calc()
        
        return stage
    
    @classmethod
    def two_stage_vehicle_to_orbit(cls,
                                   stage_1 : Stage,
                                   stage_2 : Stage,
                                   V_bo : float,
                                   m_payload : float,
                                   t_bo_1 : float,
                                   F_W : list,
                                   I_sp : list,
                                   gamma_avg : list = [30, 30],
                                   k_s : list = [0.062, 0.12]) -> list:
        """Evaluate the stages parameters for a two-stage vehicle to orbit

        Args:
            stage_1 (Stage): Stage 1
            stage_2 (Stage): Stage 2
            V_bo (float): Final burnout velocity for orbit insertion [km/s]
            m_payload (float): Payload mass [kg]
            t_bo_1 (float): Burnout time for the first stage [s]
            F_W (list): List of two thrust to weight ratios
            I_sp (list): List of two specific impulses [s]
            gamma_avg (list, optional): List of two average values of flight path angle. Defaults to [30, 30].
            k_s (list, optional): List of two structural fractions. Defaults to [0.062, 0.12].

        Returns:
            list: List of updated stages parameters
        """
        
        # ! Check
        
        if len(F_W) != 2 or len(I_sp) != 2 or len(gamma_avg) != 2 or len(k_s) != 2: return stage_1, stage_2
        
        F_W_1, F_W_2 = F_W
        
        I_sp_1, I_sp_2 = I_sp
        
        gamma_avg_1, gamma_avg_2 = gamma_avg
        
        k_s_1, k_s_2 = k_s
        
        # >>> Propellant fraction
        
        k_p_1 = F_W_1 / I_sp_1
        
        k_p_2 = F_W_2 / I_sp_2
        
        # >>> Burnout velocity
        
        V_bo_1 = - cls.g_E * I_sp_1 * np.log(1 - k_p_1 * t_bo_1) - cls.g_E * t_bo_1 * np.sin(np.deg2rad(gamma_avg_1))
        
        # >>> Burnout time
        
        f = lambda t: V_bo + cls.g_E * I_sp_2 * np.log(1 - k_p_2 * (t - t_bo_1)) + cls.g_E * (t - t_bo_1) * np.sin(np.deg2rad(gamma_avg_2)) - V_bo_1
        
        f_dot = lambda t: - cls.g_E * I_sp_2 * k_p_2 * 1 / (1 - k_p_2 * (t - t_bo_1)) + cls.g_E * np.sin(np.deg2rad(gamma_avg_2))
        
        t_bo_2 = newton(f, 1 / k_p_2 + t_bo_1 - 1, f_dot)
        
        # >>> Stack mass
        
        dt_1 = t_bo_1 - 0
        
        dt_2 = t_bo_2 - t_bo_1
        
        m_0_I = m_payload / ( (1 - (1 + k_s_1) * k_p_1 * dt_1) * (1 - (1 + k_s_2) * k_p_2 * dt_2) )
        
        m_0_II = m_payload / (1 - (1 + k_s_2) * k_p_2 * dt_2)
        
        # >>> Thrust
        
        F_1 = F_W_1 * m_0_I * cls.g_E * 1e3
        
        F_2 = F_W_2 * m_0_II * cls.g_E * 1e3
        
        # >>> Propellant mass
        
        m_p_1 = k_p_1 * dt_1 * m_0_I
        
        m_p_2 = k_p_2 * dt_2 * m_0_II
        
        # >>> Structural mass
        
        m_s_1 = k_s_1 * m_p_1
        
        m_s_2 = k_s_2 * m_p_2
        
        # >>> Update stage
        
        stage_1.mass(m_s_1, m_p_1, m_0_II)
        stage_1.motor(F_1, I_sp_1, stage_1.csi)
        stage_1.calc()
        
        stage_2.mass(m_s_2, m_p_2, m_payload)
        stage_2.motor(F_2, I_sp_2, stage_2.csi)
        stage_2.calc()
        
        return stage_1, stage_2
    
    @classmethod
    def three_stage_vehicle_to_orbit(cls,
                                     stage_1 : Stage,
                                     stage_2 : Stage,
                                     stage_3 : Stage,
                                     V_bo : float,
                                     m_payload : float,
                                     t_bo_1 : float,
                                     t_bo_2 : float,
                                     F_W : list,
                                     I_sp : list,
                                     gamma_avg : list = [30, 30, 30],
                                     k_s : list = [0.062, 0.12, 0.12]) -> list:
        """Evaluate the stages parameters for a three-stage vehicle to orbit

        Args:
            stage_1 (Stage): Stage 1
            stage_2 (Stage): Stage 2
            stage_3 (Stage): Stage 3
            V_bo (float): Final burnout velocity for orbit insertion [km/s]
            m_payload (float): Payload mass [kg]
            t_bo_1 (float): Burnout time for the first stage [s]
            t_bo_2 (float): Burnout time for the second stage [s]
            F_W (list): List of three thrust to weight ratios
            I_sp (list): List of three specific impulses [s]
            gamma_avg (list, optional): List of three average values of flight path angle. Defaults to [30, 30, 30].
            k_s (list, optional): List of three structural fractions. Defaults to [0.062, 0.12, 0.12].

        Returns:
            list: List of updated stages parameters
        """
        
        # ! Check
        
        if len(F_W) != 3 or len(I_sp) != 3 or len(gamma_avg) != 3 or len(k_s) != 3: return stage_1, stage_2, stage_3
        
        F_W_1, F_W_2, F_W_3 = F_W
        
        I_sp_1, I_sp_2, I_sp_3 = I_sp
        
        gamma_avg_1, gamma_avg_2, gamma_avg_3 = gamma_avg
        
        k_s_1, k_s_2, k_s_3 = k_s
        
        # >>> Propellant fraction
        
        k_p_1 = F_W_1 / I_sp_1
        
        k_p_2 = F_W_2 / I_sp_2
        
        k_p_3 = F_W_3 / I_sp_3
        
        # >>> Burnout velocity
        
        V_bo_1 = - cls.g_E * I_sp_1 * np.log(1 - k_p_1 * t_bo_1) - cls.g_E * t_bo_1 * np.sin(np.deg2rad(gamma_avg_1))
        
        V_bo_2 = - cls.g_E * I_sp_2 * np.log(1 - k_p_2 * (t_bo_2 - t_bo_1)) - cls.g_E * (t_bo_2 - t_bo_1) * np.sin(np.deg2rad(gamma_avg_2)) + V_bo_1
        
        # >>> Burnout time
        
        f = lambda t: V_bo + cls.g_E * I_sp_3 * np.log(1 - k_p_3 * (t - t_bo_2)) + cls.g_E * (t - t_bo_2) * np.sin(np.deg2rad(gamma_avg_3)) - V_bo_2
        
        f_dot = lambda t: - cls.g_E * I_sp_3 * k_p_3 * 1 / (1 - k_p_3 * (t - t_bo_2)) + cls.g_E * np.sin(np.deg2rad(gamma_avg_3))
        
        t_bo_3 = newton(f, 1 / k_p_3 + t_bo_2 - 1, f_dot)
        
        # >>> Stack mass
        
        dt_1 = t_bo_1 - 0
        
        dt_2 = t_bo_2 - t_bo_1
        
        dt_3 = t_bo_3 - t_bo_2
        
        m_0_I = m_payload / ( (1 - (1 + k_s_1) * k_p_1 * dt_1) * (1 - (1 + k_s_2) * k_p_2 * dt_2) * (1 - (1 + k_s_3) * k_p_3 * dt_3) )
        
        m_0_II = m_payload / ( (1 - (1 + k_s_2) * k_p_2 * dt_2) * (1 - (1 + k_s_3) * k_p_3 * dt_3) )
        
        m_0_III = m_payload / (1 - (1 + k_s_3) * k_p_3 * dt_3)
        
        # >>> Thrust
        
        F_1 = F_W_1 * m_0_I * cls.g_E * 1e3
        
        F_2 = F_W_2 * m_0_II * cls.g_E * 1e3
        
        F_3 = F_W_3 * m_0_III * cls.g_E * 1e3
        
        # >>> Propellant mass
        
        m_p_1 = k_p_1 * dt_1 * m_0_I
        
        m_p_2 = k_p_2 * dt_2 * m_0_II
        
        m_p_3 = k_p_3 * dt_3 * m_0_III
        
        # >>> Structural mass
        
        m_s_1 = k_s_1 * m_p_1
        
        m_s_2 = k_s_2 * m_p_2
        
        m_s_3 = k_s_3 * m_p_3
        
        # >>> Update stage
        
        stage_1.mass(m_s_1, m_p_1, m_0_II)
        stage_1.motor(F_1, I_sp_1, stage_1.csi)
        stage_1.calc()
        
        stage_2.mass(m_s_2, m_p_2, m_0_III)
        stage_2.motor(F_2, I_sp_2, stage_2.csi)
        stage_2.calc()
        
        stage_3.mass(m_s_3, m_p_3, m_payload)
        stage_3.motor(F_3, I_sp_3, stage_3.csi)
        stage_3.calc()
        
        return stage_1, stage_2, stage_3

if __name__ == '__main__':
    
    print('EXAMPLE 7.1\n')
    
    # * VEGA C - P120C 
    
    stage_1 = Stage()
    
    #stage_1.mass(13_393, 141_634, 54_035)
    #stage_1.motor(4_323 * 1e3, 279, 0.0)
    #stage_1.nozzle(1.3, 16, 88.8231)
    #stage_1.aerodynamics(3.4, 1.2, 0.0)
    #stage_1.calc()
    
    stage_1.mass(68_000 / 15, 68_000 - 68_000 / 15, 0)
    stage_1.motor(933.913 * 1e3, 390, 0.0)
    stage_1.aerodynamics(5, 0.5, 0.0)
    stage_1.calc()
    
    Launcher.stage = stage_1
    
    #res = Launcher.simulate_launch(np.array([34.9e-3, np.pi / 2 - 0.001, 0, 0, 0]))

    res = Launcher.simulate_launch(np.array([0, np.deg2rad(89.85), 0, 0, 0, 0, 0]), h_t=130, t_f=stage_1.t_burn)
    
    #Launcher.plot_launch(res['y'], res['t'])
    
    print('-' * 40, '\n')
    
    print('EXAMPLE 7.2\n')
    
    stage_1 = Stage()
    
    stage_1 = Launcher.single_stage_vehicle_to_orbit(stage_1, 7.909, 10_680, 1.3, 450)
    
    print(stage_1.m_0, stage_1.m_p, stage_1.m_s, stage_1.m_payload, stage_1.t_burn, stage_1.F_vac)
    
    print('-' * 40, '\n')
    
    print('EXAMPLE 7.3\n')
    
    stage_2 = Stage()
    
    stage_1, stage_2 = Launcher.two_stage_vehicle_to_orbit(stage_1, stage_2, 7.909, 10_680, 200, [1.3, 1.3], [450, 450])
    
    print(stage_1.m_0, stage_1.m_p, stage_1.m_s, stage_1.m_payload, stage_1.t_burn, stage_1.F_vac)
    print(stage_2.m_0, stage_2.m_p, stage_2.m_s, stage_2.m_payload, stage_2.t_burn, stage_2.F_vac)
    
    print('-' * 40, '\n')
    
    print('EXAMPLE 7.4\n')
    
    stage_3 = Stage()
    
    stage_1, stage_2, stage_3 = Launcher.three_stage_vehicle_to_orbit(stage_1, stage_2, stage_3, 7.909, 10_680, 200, 345, [1.3, 1.3, 1.3], [450, 450, 450])
    
    print(stage_1.m_0, stage_1.m_p, stage_1.m_s, stage_1.m_payload, stage_1.t_burn, stage_1.F_vac)
    print(stage_2.m_0, stage_2.m_p, stage_2.m_s, stage_2.m_payload, stage_2.t_burn, stage_2.F_vac)
    print(stage_3.m_0, stage_3.m_p, stage_3.m_s, stage_3.m_payload, stage_3.t_burn, stage_3.F_vac)
    
    print('-' * 40, '\n')
    
    #plt.show()