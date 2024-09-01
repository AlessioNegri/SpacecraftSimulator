""" LagrangeCoefficients.py: Implements the algorithms based on the Lagrange coefficients """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"
__book__        = "Orbital Mechanics for Engineering Students"
__chapter__     = "2 - The Two-Body Problem"
__chapter__     = "3 - Orbital Position as a Function of Time"

import os
import sys
import numpy as np

from scipy.optimize import newton

sys.path.append(os.path.dirname(__file__))

from AstronomicalData import AstronomicalData, CelestialBody

class LagrangeCoefficients():
    """Manages all the algorithms based on the Lagrange coefficients"""
    
    # --- ASTRONOMICAL CONSTANTS 
    
    mu = AstronomicalData.gravitational_parameter(CelestialBody.EARTH)
    
    # --- METHODS 

    # ! SECTION 2.11

    # ! ALGORITHM 2.3
    @classmethod
    def calculate_position_velocity_by_angle(cls, r_0 : np.ndarray, v_0 : np.ndarray, dtheta : float) -> list:
        """Evaluates the position and velocity after delta theta from the initial state

        Args:
            r_0 (np.ndarray): Initial position vector
            v_0 (np.ndarray): Initial velocity vector
            dtheta (float): Angle variation

        Returns:
            list: [r_f, v_f]
        """
        
        # >>> 1. Magnitudes
        
        r_0_m = np.linalg.norm(r_0)
        v_0_m = np.linalg.norm(v_0)
        
        # >>> 2. Radial Velocity
        
        v_r0 = np.dot(r_0, v_0) / r_0_m
        
        # >>> 3. Specific Angular momentum
        
        h = r_0_m * np.sqrt(v_0_m**2 - v_r0**2)
        
        # >>> 4. Radius
        
        r = h**2 / cls.mu * 1 / ( 1 + ( h**2 / (cls.mu * r_0_m) - 1 ) * np.cos(dtheta) - h * v_r0 / cls.mu * np.sin(dtheta) )
        
        # >>> 5. Lagrange coefficients
        
        f = 1 - cls.mu * r / h**2 * (1 - np.cos(dtheta))
        
        g = r * r_0_m / h * np.sin(dtheta)
        
        df_dt = cls.mu / h * (1 - np.cos(dtheta)) / np.sin(dtheta) * (cls.mu / h**2 * (1 - np.cos(dtheta)) - 1 / r_0_m - 1 / r)
        
        dg_dt = 1 - cls.mu * r_0_m / h**2 * (1 - np.cos(dtheta))
        
        #return np.concatenate((f * r_0 + g * v_0, dfdt * r_0 + dgdt * v_0), axis=0)
        return [f * r_0 + g * v_0, df_dt * r_0 + dg_dt * v_0]
    
    # ! SECTION 3.7
    
    @classmethod
    def S(cls, z : float) -> float:
        """Stumpff Function S

        Args:
            z (float): Variable

        Returns:
            float: Evaluation
        """
        
        if      z > 0:  return (np.sqrt(z) - np.sin(np.sqrt(z))) / np.sqrt(z)**3
        elif    z < 0:  return (np.sinh(np.sqrt(-z)) - np.sqrt(-z)) / np.sqrt(-z)**3
        else:           return 1/6
    
    @classmethod
    def C(self, z : float) -> float:
        """Stumpff Function C

        Args:
            z (float): Variable

        Returns:
            float: Evaluation
        """
        
        if      z > 0:  return (1 - np.cos(np.sqrt(z))) / z
        elif    z < 0:  return (np.cosh(np.sqrt(-z)) - 1) / (-z)
        else:           return 1/2
    
    # ! ALGORITHM 3.3
    @classmethod
    def calculate_universal_variable(cls, r_0 : float, v_r0 : float, alpha : float, dt : float) -> float:
        """Calculates the universal variable chi

        Args:
            r_0 (float): Initial distance
            v_r0 (float): Initial radial velocity
            alpha (float): Parameter alpha
            dt (float): Delta time

        Returns:
            float: Universal variable chi
        """
        
        # ? Universal Kepler Equation
        
        f = lambda chi, r0, vr0, alpha, dt: r0 * vr0 / np.sqrt(cls.mu) * chi**2 * cls.C(alpha * chi**2) + (1 - alpha * r0) * chi**3 * cls.S(alpha * chi**2) + r0 * chi - np.sqrt(cls.mu) * dt
        
        # ? First Derivative Of Universal Kepler Equation
        
        df = lambda chi, r0, vr0, alpha, dt: r0 * vr0 / np.sqrt(cls.mu) * chi * (1 - alpha * chi**2 * cls.S(alpha * chi**2)) + (1 - alpha * r0) * chi**2 * cls.C(alpha * chi**2) + r0
        
        # ? Result
        
        chi_0 = np.sqrt(cls.mu) * np.abs(alpha) * dt
        
        return newton(f, chi_0, df, args=(r_0, v_r0, alpha, dt))
    
    @classmethod
    def calculate_lagrange_coefficients(cls, r_0 : float, alpha : float, dt : float, chi : float) -> list:
        """Calculates the Lagrange coefficients f and g

        Args:
            r_0 (float): Initial position
            alpha (float): Parameter alpha
            dt (float): Delta time
            chi (float): Universal anomaly

        Returns:
            list: [f, g]
        """
        
        f = 1 - chi**2 / r_0 * cls.C(alpha * chi**2)
        
        g = dt - 1 / np.sqrt(cls.mu) * chi**3 * cls.S(alpha * chi**2)
        
        return [f, g]
    
    # ! ALGORITHM 3.4
    @classmethod
    def calculate_position_velocity_by_time(cls, r_0 : np.ndarray, v_0 : np.ndarray, dt : float) -> list:
        """Evaluates the position and velocity after delta time from the initial state

        Args:
            r_0 (np.ndarray): Initial position vector
            v_0 (np.ndarray): Initial velocity vector
            dt (float): Time variation

        Returns:
            list: [r_f, v_f]
        """
        
        # >>> 1.
        
            # >>> a) Magnitudes
        
        r_0_m = np.linalg.norm(r_0)
        v_0_m = np.linalg.norm(v_0)
        
            # >>> b) Radial Velocity
        
        v_r0 = np.dot(r_0, v_0) / r_0_m
        
            # >>> c) Parameter alpha
        
        alpha = 2 / r_0_m - v_0_m**2 / cls.mu
        
        # >>> 2. Universal variable
        
        chi = cls.calculate_universal_variable(r_0_m, v_r0, alpha, dt)
        
        z = alpha * chi**2
        
        # >>> 3.
        
        f = 1 - chi**2 / r_0_m * cls.C(z)
        
        g = dt - 1 / np.sqrt(cls.mu) * chi**3 * cls.S(z)
        
        # >>> 4.
        
        r = f * r_0 + g * v_0
        
        # >>> 5.
        
        df_dt = np.sqrt(cls.mu) / (np.linalg.norm(r) * r_0_m) * (alpha * chi**3 * cls.S(z) - chi)
        
        dg_dt = 1 - chi**2 / np.linalg.norm(r) * cls.C(z)
        
        # >>> 6.
        
        v = df_dt * r_0 + dg_dt * v_0
        
        return [r, v]
    
if __name__  == '__main__':
    
    print('EXAMPLE 2.13\n')
    print(LagrangeCoefficients.calculate_position_velocity_by_angle(np.array([8182.4, -6865.9, 0]), np.array([0.47572, 8.8116, 0]), np.deg2rad(120)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 3.6\n')
    print(LagrangeCoefficients.calculate_universal_variable(10000, 3.0752, -5.0878e-5, 3600))
    print('-' * 40, '\n')
    
    print('EXAMPLE 3.7\n')
    print(LagrangeCoefficients.calculate_position_velocity_by_time(np.array([7000.0, -12124, 0]), np.array([2.6679, 4.6210, 0]), 3600))
    print('-' * 40, '\n')
    
    print('EXAMPLE 4.2\n')
    print(LagrangeCoefficients.calculate_position_velocity_by_time(np.array([1600, 5310, 3800]), np.array([-7.350, 0.4600, 2.470]), 3200))
    print('-' * 40, '\n')