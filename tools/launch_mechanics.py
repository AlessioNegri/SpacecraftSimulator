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
        
        self.F_vac      = 0.0   # * Vacuum Thrust               [ kg * m / s^2 ]
        self.I_sp_vac   = 0.0   # * Vacuum Specific Impulse     [ s ]
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
    
    Launcher.plot_launch(res['y'], res['t'])
    
    print('-' * 40, '\n')
    
    plt.show()