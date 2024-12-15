""" AtmosphericEntry.py: Implements the atmospheric entry equations """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"
__book__        = "Manned Spacecraft: Design Principles"
__chapter__     = "6 - Atmospheric Entry Mechanics"

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as ode

sys.path.append(os.path.dirname(__file__))

from AstronomicalData import AstronomicalData, CelestialBody

class AtmosphericEntry:
    """Implements the atmospheric entry equations"""
    
    # --- MEMBERS 
    
    g_E     = AstronomicalData.gravity(CelestialBody.EARTH, km=True)        # * Sea Level Gravity           [ km / s^2 ]
    R_E     = AstronomicalData.equatiorial_radius(CelestialBody.EARTH)      # * Planet Equatiorial Radius   [ km ]
    k       = AstronomicalData.gravitational_parameter(CelestialBody.EARTH) # * Gravitational Parameter     [ km^3 / s^2 ]
    m       = 0.0                                                           # * Initial Mass                [ kg ]
    F       = 0.0                                                           # * Thrust                      [ kg * m / s^2 ]
    I_sp    = 300.0                                                         # * Specific Impulse            [ s ]
    csi     = 0.0                                                           # * Thrust Angle                [ rad ]
    C_L     = 0.0                                                           # * Lift Coefficient            [ ]
    C_D     = 1.0                                                           # * Drag Coefficient            [ ]
    S       = 1.0                                                           # * Reference Surface           [ m^2 ]
    H       = 6.9                                                           # * Constant Scale Height       [ km ]
    R_N     = 0.3                                                           # * Nose Radius                 [ m ]
    C_D_P   = 1.4                                                           # * Parachute Drag Coefficient  [ ]
    S_P     = 70.0                                                          # * Parachute Reference Surface [ ]
    
    use_parachute = False                                                   # * Check for parachute usage
    
    # --- INTERNAL MEMBERS 
    
    _parachute_deployed     = False                                         # * Check when the parachute is deployed
    _parachute_deployed_t_0 = 0.0                                           # * Intitial Parachute Deploy               [ s ]
    _parachute_opening_time = 0.0                                           # * Parachute Deploy Time                   [ s ]
    
    # --- METHODS 
    
    @classmethod
    def set_capsule_parameters(cls, F : float, I_sp : float, csi : float, C_L : float, C_D : float, S : float) -> None:
        """Sets the parameters for the atmospheric entry

        Args:
            F (float): Thrust [ kg * m / s^2 ]
            I_sp (float): Specific Impulse [ s ]
            csi (float): Thrust angle [ rad ]
            C_L (float): Lift coefficient [ ]
            C_D (float): Drag coefficient [ ]
            S (float): Surface area [ m^2 ]
        """
        
        cls.F       = F
        cls.I_sp    = I_sp
        cls.csi     = csi
        cls.C_L     = C_L
        cls.C_D     = C_D
        cls.S       = S
        
    @classmethod
    def set_parachute_parameters(cls, use_parachute : bool, C_D_P : float, S_P : float) -> None:
        """Sets the parameters for the parachute

        Args:
            use_parachute (bool): True for using the parachute
            C_D_P (float): Parachute Drag Coefficient [ ]
            S_P (float): Parachute Reference Surface [ m^2 ]
        """
        
        cls.use_parachute   = use_parachute
        cls.C_D_P           = C_D_P
        cls.S_P             = S_P
    
    # ! SECTION 6.1
    
    @classmethod
    def entry_eom(cls, t : float, X : np.ndarray) -> np.ndarray:
        """Atmospheric entry equations of motion\n
        
        (1) dV/dt     = ( F cos(csi) ) / m - D / m - ( k sin(gamma) ) / r^2\n
        (2) dgamma/dt = ( F sin(csi) ) / (m V) + L / (m V) - ( k cos(gamma) ) / ( V r^2 ) + ( V cos(gamma) ) / r\n
        (3) dr/dt     = V sin(gamma)\n
        (4) dx/dt     = ( V cos(gamma) ) / r\n
        (5) dm/dt     = - F / ( g_E I_sp )

        Args:
            t (float): Time
            X (np.ndarray): State [5,1] -> (V, gamma, r, x, m)

        Returns:
            np.ndarray: Derivative of state
        """
        
        # >>> Parameters
        
        V, gamma, r, x, m = X
        
        rho = 1.5 * np.exp(-(r - cls.R_E) / cls.H) # * [kg / m^3]
        
        L = 0.5 * rho * (V * 1e3)**2 * cls.C_L * cls.S * 1e-3 # * [kg * km / s^2]
        
        D = 0.5 * rho * (V * 1e3)**2 * cls.C_D * cls.S * 1e-3 # * [kg * km / s^2]
        
        D_P = 0.5 * rho * (V * 1e3)**2 * cls.C_D_P * cls.S_P * 1e-3 # * [kg * km / s^2]
        
        if cls.use_parachute:
            
            if not cls._parachute_deployed:
                
                D_P = 0
            
                if (r - cls.R_E) <= 5:
                    
                    cls._parachute_deployed     = True
                    cls._parachute_deployed_t_0 = t
                    cls._parachute_opening_time = 3
            
            else:
                
                dt = t - cls._parachute_deployed_t_0
                
                D_P = D_P * dt / cls._parachute_opening_time if dt <= cls._parachute_opening_time else D_P
                
                if dt < 0: D_P = 0
                
        else:
            
            D_P = 0
        
        # >>> Equations
        
        dX_dt = np.zeros(shape=(5))
        
        dX_dt[0] = (cls.F * 1e-3 * np.cos(cls.csi)) / m - (D + D_P) / m  - cls.k / r**2 * np.sin(gamma)
        dX_dt[1] = (cls.F * 1e-3 * np.sin(cls.csi)) / (m * V) + L / (m * V) - cls.k / (r**2 * V) * np.cos(gamma) + V / r * np.cos(gamma)
        dX_dt[2] = V * np.sin(gamma)
        dX_dt[3] = cls.R_E * V / r * np.cos(gamma)
        dX_dt[4] = - cls.F * 1e-3 / (cls.g_E * cls.I_sp)
        
        return dX_dt
    
    # ! SECTION 6.4 - 6.5
    
    @classmethod
    def simulate_atmospheric_entry(cls, y_0 : np.ndarray, t_0 : float = 0.0, t_f : float = 0.0, show : bool = False) -> dict:
        
        """Integrates the Ordinary Differential Equations for the Atmospheric Entry

        Args:
            y_0 (np.ndarray): Initial state [5,1] -> (V, gamma, z, x, m)
            t_0 (float, optional): Initial time. Defaults to 0.0.
            t_f (float, optional): Final time. Defaults to 0.0.
            show (bool, optional): True for plotting the parameters. Defaults to False.
            
        Returns:
            dict: { t: time, y: state, dt: t - t_0 }
        """
        
        if t_f < t_0: raise Exception('Invalid integration time: t_0 > t_f!')
            
        # >>> 1. Integrate ODE 
    
        def terminal_condition(t : float, X : np.ndarray) -> bool: return X[2] - cls.R_E
        
        terminal_condition.terminal = True
        
        y_0[2] += cls.R_E
        
        cls._parachute_deployed     = False
        cls._parachute_deployed_t_0 = 0
        cls._parachute_opening_time = 0
        
        integrationResult = ode.solve_ivp(fun=cls.entry_eom, t_span=[t_0, t_f], y0=y_0, method='RK45', rtol=1e-8, atol=1e-8, events=terminal_condition)
        
        if not integrationResult['success']: raise Exception(integrationResult['message'])
        
        # >>> 2. Result 
        
        V       = integrationResult['y'][0, :]
        gamma   = integrationResult['y'][1, :]
        r       = integrationResult['y'][2, :]
        x       = integrationResult['y'][3, :]
        m       = integrationResult['y'][4, :]
        t       = integrationResult['t']
        
        C       = (1.7415 * 1e-4 * 1 / np.sqrt(cls.R_N))
        q_t_c   = np.array([C * np.sqrt(1.225 * np.exp(-(r[i] - cls.R_E) / cls.H)) * (V[i] * 1e3)**3 for i in range(0, len(t))])
        a       = np.array([(V[i] - V[i - 1]) / (t[i] - t[i - 1]) for i in range(1, len(t))])
        
        # >>> 3. Plot 
        
        if show:
            
            fig, axes = plt.subplots(2, 3, constrained_layout=True)
            
            fig.suptitle(f"ATMOSPHERIC ENTRY: $V_e = {y_0[0]}\;\;km/s$   $\gamma_e = {np.rad2deg(y_0[1])}\;\;°$   $z_e = {y_0[2] - cls.R_E}\;\;km$   $R_N = {cls.R_N}\;\;m$   $V_f = {V[-1] * 1e3}\;\;m/s$")
            
            axes[0,0].set_xlabel("Time [$s$]")
            axes[0,0].set_ylabel("$V$ [$km / s$]")
            axes[0,0].grid()
            axes[0,0].plot(t / 60, V)
            
            axes[0,1].set_xlabel("Time [$s$]")
            axes[0,1].set_ylabel("$\gamma$ [°]")
            axes[0,1].grid()
            axes[0,1].plot(t / 60, gamma * 180 / np.pi)
            
            axes[0,2].set_xlabel("Downrange distance $x$ [$km$]")
            axes[0,2].set_ylabel("$z$ [$km$]")
            axes[0,2].grid()
            axes[0,2].plot(x, r - cls.R_E)
            
            axes[1,0].set_xlabel("$V$ [$km / s$]")
            axes[1,0].set_ylabel("$z$ [$km$]")
            axes[1,0].grid()
            axes[1,0].plot(V, r - cls.R_E)
            
            axes[1,1].set_xlabel("Time [$s$]")
            axes[1,1].set_ylabel("$q_{t,c}$ [$W / cm^2$]")
            axes[1,1].grid()
            axes[1,1].plot(t / 60, q_t_c * 1e-4)
            
            axes[1,2].set_xlabel("Time [$s$]")
            axes[1,2].set_ylabel("$dV/dt\;\;(g_E)$")
            axes[1,2].grid()
            axes[1,2].plot(t[1:] / 60, a / cls.g_E)
        
        return dict(t=t, y=integrationResult['y'], dt=np.abs(t[-1] - t[0]))

if __name__ == '__main__':
    
    print('EXAMPLE 6.1\n')
    AtmosphericEntry.set_capsule_parameters(0, 300, 0, 0, 1.096, 0.341)
    AtmosphericEntry.simulate_atmospheric_entry(np.array([12.6161, np.deg2rad(-9), 120, 0, 26.27]), t_f=3000, show=True)
    print('-' * 40, '\n')
    
    plt.show()