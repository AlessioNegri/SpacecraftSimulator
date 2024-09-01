""" CircularRestrictedThreeBodyProblem.py: Implements the CR3BP equations """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"
__book__        = "Orbital Mechanics for Engineering Students"
__chapter__     = "2 - The Two-Body Problem"

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from dataclasses import dataclass
from scipy.optimize import newton
from scipy.integrate import solve_ivp

sys.path.append(os.path.dirname(__file__))

from AstronomicalData import AstronomicalData, CelestialBody

# --- STRUCT 

@dataclass
class ParametersCrtbp:
    """Circular Restricted Three Body Problem parameters"""
    
    L_1     : np.ndarray    # * Lagrangian Equilibrium Point 1  [ km ]
    L_2     : np.ndarray    # * Lagrangian Equilibrium Point 2  [ km ]
    L_3     : np.ndarray    # * Lagrangian Equilibrium Point 3  [ km ]
    L_4     : np.ndarray    # * Lagrangian Equilibrium Point 4  [ km ]
    L_5     : np.ndarray    # * Lagrangian Equilibrium Point 5  [ km ]
    Omega   : float = 0.0   # * Inertial Angular Velocity       [ rad / s ]
    pi_1    : float = 0.0   # * Dimensionless Mass Ratio 1      [ ]
    pi_2    : float = 0.0   # * Dimensionless Mass Ratio 2      [ ]
    mu_1    : float = 0.0   # * Gravitational Parameter 1       [ km^3 / s^2 ]
    mu_2    : float = 0.0   # * Gravitational Parameter 2       [ km^3 / s^2 ]
    x_1     : float = 0.0   # * Body Position 1                 [ km ]
    x_2     : float = 0.0   # * Body Position 2                 [ km ]

# --- CLASS 

class CircularRestrictedThreeBodyProblem():
    """Simulates the Circular Restricted Three Body Problem"""
    
    # --- ASTRONOMICAL CONSTANTS 
    
    m_1     = AstronomicalData.mass(CelestialBody.EARTH)
    m_2     = AstronomicalData.mass(CelestialBody.MOON)
    r_12    = AstronomicalData.semi_major_axis(CelestialBody.MOON)
    R_E_1   = AstronomicalData.equatiorial_radius(CelestialBody.EARTH)
    
    # --- METHODS 
        
    # ! SECTION 2.12
    
    @classmethod
    def calculate_orbital_parameters(cls, show : bool = False) -> ParametersCrtbp:
        """Calculates the orbital parameters

        Args:
            show (bool, optional): Shows the console print. Defaults to False.
        
        Returns:
            PARAMETERS_R3BP: Orbital parameters
        """
        
        # >>> 1.
        
        parameters = ParametersCrtbp(np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3))
        
        # ? Gravitational parameter global
        
        mu = AstronomicalData.G * (cls.m_1 + cls.m_2)
        
        # ? Inertial angular velocity
        
        parameters.Omega = np.sqrt(mu / cls.r_12**3)
        
        # ? Dimensionless mass ratio
        
        parameters.pi_1 = cls.m_1 / (cls.m_1 + cls.m_2)
        
        parameters.pi_2 = cls.m_2 / (cls.m_1 + cls.m_2)
        
        # ? Gravitational parameter
        
        parameters.mu_1 = mu * parameters.pi_1
        
        parameters.mu_2 = mu * parameters.pi_2
        
        # ? Body position
        
        parameters.x_1 = - parameters.pi_2 * cls.r_12
        
        parameters.x_2 = + parameters.pi_1 * cls.r_12
        
        # ? Lagrange points
        
        f  = lambda csi, pi_2: (1 - pi_2) / np.abs(csi + pi_2)**3 * (csi + pi_2) + pi_2 / np.abs(csi + pi_2 - 1)**3 * (csi + pi_2 - 1) - csi
        
        csi_1 = newton(f, 0.8369, args=(parameters.pi_2, ))
        csi_2 = newton(f, 1.156, args=(parameters.pi_2, ))
        csi_3 = newton(f, -1.005, args=(parameters.pi_2, ))
        
        parameters.L_1 = np.array([csi_1 * cls.r_12, 0, 0])
        parameters.L_2 = np.array([csi_2 * cls.r_12, 0, 0])
        parameters.L_3 = np.array([csi_3 * cls.r_12, 0, 0])
        parameters.L_4 = np.array([0.5 * cls.r_12 - parameters.pi_2 * cls.r_12, + np.sqrt(3) / 2 * cls.r_12, 0])
        parameters.L_5 = np.array([0.5 * cls.r_12 - parameters.pi_2 * cls.r_12, - np.sqrt(3) / 2 * cls.r_12, 0])
        
        # >>> 2.
        
        if show:
            
            print('*' * 10, 'RESTRICTED 3 BODY PROBLEM', '*' * 10)
            print(f'Omega = {parameters.Omega * 1e6:10.5f} \t x 10^-6 [rad / s]')
            print(f'pi_1  = {parameters.pi_1:10.5f} \t []')
            print(f'pi_2  = {parameters.pi_2:10.5f} \t []')
            print(f'mu_1  = {parameters.mu_1:10.2f} \t [km^3 / s^2]')
            print(f'mu_2  = {parameters.mu_2:10.2f} \t [km^3 / s^2]')
            print(f'x_1   = {parameters.x_1:10.2f} \t [km]')
            print(f'x_2   = {parameters.x_2:10.5f} \t [km]')
            print(f'L_1   = {parameters.L_1[0]:10.2f} \t {parameters.L_1[1]:10.2f} \t {parameters.L_1[2]:10.2f} \t [km]')
            print(f'L_2   = {parameters.L_2[0]:10.2f} \t {parameters.L_2[1]:10.2f} \t {parameters.L_2[2]:10.2f} \t [km]')
            print(f'L_3   = {parameters.L_3[0]:10.2f} \t {parameters.L_3[1]:10.2f} \t {parameters.L_3[2]:10.2f} \t [km]')
            print(f'L_4   = {parameters.L_4[0]:10.2f} \t {parameters.L_4[1]:10.2f} \t {parameters.L_4[2]:10.2f} \t [km]')
            print(f'L_5   = {parameters.L_5[0]:10.2f} \t {parameters.L_5[1]:10.2f} \t {parameters.L_5[2]:10.2f} \t [km]')
            print('-' * 40)
        
        return parameters
    
    @classmethod
    def crtbp_eom(cls, t : float, X : np.ndarray, parameters : ParametersCrtbp) -> np.ndarray:
        """Equations of the Circular Restricted Three Body Problem dynamics

        Args:
            t (float): Time
            X (np.ndarray): State [6,1]
            parameters (PARAMETERS_CRTBP): CRTBP parameters

        Returns:
            np.ndarray: Derivative of state
        """
        
        x, y, z, v_x, v_y, v_z = X
        
        Omega   = parameters.Omega
        mu_1    = parameters.mu_1
        mu_2    = parameters.mu_2
        x_1     = parameters.x_1
        x_2     = parameters.x_2
        
        r_1 = np.sqrt((x - parameters.x_1)**2 + y**2 + z**2)
        r_2 = np.sqrt((x - parameters.x_2)**2 + y**2 + z**2)
        
        dX_dt = np.zeros(shape=(6))
        
        dX_dt[0] = v_x
        dX_dt[1] = v_y
        dX_dt[2] = v_z
        dX_dt[3] = + 2 * Omega * v_y + Omega**2 * x - mu_1 / r_1**3 * (x - x_1) - mu_2 / r_2**3 * (x - x_2)
        dX_dt[4] = - 2 * Omega * v_x + Omega**2 * y - mu_1 / r_1**3 * y - mu_2 / r_2**3 * y
        dX_dt[5] = - mu_1 / r_1**3 * z - mu_2 / r_2**3 * z
        
        return dX_dt
    
    @classmethod
    def simulate_crtbp(cls, y_0 : np.ndarray, t_0 : float = 0.0, t_f : float = 0.0, show : bool = False) -> dict:
        """Integrates the Ordinary Differential Equations for the Circular Restricted Three Body Problem

        Args:
            y_0 (np.ndarray): Initial state [6,1]
            t_0 (float, optional): Initial time. Defaults to 0.0.
            t_f (float, optional): Final time. Defaults to 0.0.
            show (bool, optional): True for plotting the trajectory. Defaults to False.
            
        Returns:
            dict: { t: time, y: state[n_states, n_points] }
        """
        
        # >>> 1.
        
        if t_f < t_0: raise Exception('Invalid integration time')
        
        parameters = cls.calculate_orbital_parameters()
        
        integrationResult = solve_ivp(fun=cls.crtbp_eom, t_span=[t_0, t_f], y0=y_0, method='RK45', args=(parameters, ), rtol=1e-8, atol=1e-8)
        
        if not integrationResult['success']: Exception(integrationResult['message'])
        
        x = integrationResult['y'][0, :]
        y = integrationResult['y'][1, :]
        z = integrationResult['y'][2, :]
        
        # >>> 2.
        
        if show:
            
            plt.figure(figsize=(10, 8))
            
            ax = plt.axes(projection='3d')
            
            # * Body 1
            
            ax.scatter(parameters.x_1, 0, 0, c='c')
            
            angles = np.linspace(0 * np.pi, 2 * np.pi, 100)
            
            ax.plot(cls.R_E_1 * np.cos(angles), cls.R_E_1 * np.sin(angles), color = 'green')
            
            # * Body 2
            
            ax.scatter(parameters.x_2, 0, 0, c='m')
            
            # * Lagrangian Equilibrium Points
            
            ax.scatter(parameters.L_1[0], parameters.L_1[1], parameters.L_1[2], c='k', marker='^', label='$L_1$')
            ax.scatter(parameters.L_2[0], parameters.L_2[1], parameters.L_2[2], c='k', marker='^', label='$L_2$')
            ax.scatter(parameters.L_3[0], parameters.L_3[1], parameters.L_3[2], c='k', marker='^', label='$L_3$')
            ax.scatter(parameters.L_4[0], parameters.L_4[1], parameters.L_4[2], c='k', marker='s', label='$L_4$')
            ax.scatter(parameters.L_5[0], parameters.L_5[1], parameters.L_5[2], c='k', marker='s', label='$L_5$')
            
            # * Orbit
            
            ax.plot(x, y, z, c='b', label='Orbit')
            
            # * Start
            
            ax.scatter(x[0], y[0], z[0], c='g', label='Start')
            
            # * Finish
            
            ax.scatter(x[-1], y[-1], z[-1], c='r', label='Finish')
            
            ax.set_title('Spacecraft Orbit')
            ax.set_xlabel('$x$ [km]')
            ax.set_ylabel('$y$ [km]')
            ax.set_zlabel('$z$ [km]')
            
            plt.legend()
            plt.show()
        
        return dict(t=integrationResult['t'], y=integrationResult['y'])

if __name__  == '__main__':
    
    print('EXAMPLE 2.16\n')
    print(CircularRestrictedThreeBodyProblem.calculate_orbital_parameters())
    print('-' * 40, '\n')
    
    print('EXAMPLE 2.18\n')
    x = 187529.34 + 200#-(6378 + 200) * np.cos(np.deg2rad(60))
    y = 332900.17 + 200#-(6378 + 200) * np.sin(np.deg2rad(60))
    
    vx = -0.01#10.9148 * np.cos(np.deg2rad(0))
    vy = 0.01#10.9148 * np.sin(np.deg2rad(0))
    vz = 0.01
    
    y0 = np.array([x, y, 0, vx, vy, vz])
    
    CircularRestrictedThreeBodyProblem.simulate_crtbp(y0, 0, 100 * 24 * 3600, show=True)
    print('-' * 40, '\n')