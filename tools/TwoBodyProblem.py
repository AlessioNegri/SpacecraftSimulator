""" TwoBodyProblem.py: Solves the 2BP """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"
__book__        = "Orbital Mechanics for Engineering Students"
__chapter__     = "2 - The Two-Body Problem"
__chapter__     = "6 - Orbital Maneuvers"

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mpl_toolkits.mplot3d.art3d as art3d

from dataclasses import dataclass
from scipy.integrate import solve_ivp

sys.path.append(os.path.dirname(__file__))

from AstronomicalData import AstronomicalData, CelestialBody
from Time import Time, DirectionType

# --- STRUCT 

@dataclass
class OrbitalParameters:
    """Parameters of an orbit"""
    
    h           : float = 0.0 # * Specific Angular Momentum     [ km^2 / s ]
    epsilon     : float = 0.0 # * Specific Mechanical Energy    [ km^2 / s^2 ]
    e           : float = 0.0 # * Eccentricity                  [ ]
    T           : float = 0.0 # * Orbital Period                [ s ]
    r_a         : float = 0.0 # * Apoapsis Radius               [ km ]
    r_p         : float = 0.0 # * Periapsis Radius              [ km ]
    a           : float = 0.0 # * Semi-Major Axis               [ km ]
    b           : float = 0.0 # * Semi-Minor Axis               [ km ]
    v_esc       : float = 0.0 # * Escape Velocity               [ km / s ]
    theta_inf   : float = 0.0 # * Infinite True Anomaly         [ rad ]
    beta        : float = 0.0 # * Hyperbola Asymptote Angle     [ rad ]
    delta       : float = 0.0 # * Turn Angle                    [ rad ]
    Delta       : float = 0.0 # * Aiming Radius                 [ km ]
    v_inf       : float = 0.0 # * Hyperbolic Excess Speed       [ km / s ]
    C_3         : float = 0.0 # * Characteristic Energy         [ km^2 / s^2 ]

# --- CLASS 

class TwoBodyProblem:
    """Implements all the algorithms to solve the Two Body Problem"""
    
    # --- ASTRONOMICAL CONSTANTS 
    
    g_0 = AstronomicalData.gravity(CelestialBody.EARTH, True)
    mu  = AstronomicalData.gravitational_parameter(CelestialBody.EARTH)
    
    # --- METHODS 
    
    @classmethod
    def set_celestial_body(cls, celestialBody : CelestialBody) -> None:
        """Sets the current celectial body

        Args:
            celestialBody (CelestialBody): Celestial body
        """
        
        cls.g_0 = AstronomicalData.gravity(celestialBody, True)
        cls.mu  = AstronomicalData.gravitational_parameter(celestialBody)
        
    # ! SECTION 2.3
    
    @classmethod
    def relative_eom(cls, t : float, X : np.ndarray) -> np.ndarray:
        """Equations of relative motion

        Args:
            t (float): Time
            X (np.ndarray): State [6,1]

        Returns:
            np.ndarray: Derivative of state
        """
        
        x, y, z, v_x, v_y, v_z = X
        
        r = np.sqrt(x**2 + y**2 + z**2)
        
        dX_dt = np.zeros(shape=(6))
        
        dX_dt[0] = v_x
        dX_dt[1] = v_y
        dX_dt[2] = v_z
        dX_dt[3] = - (cls.mu / r**3) * x
        dX_dt[4] = - (cls.mu / r**3) * y
        dX_dt[5] = - (cls.mu / r**3) * z
        
        return dX_dt
    
    # ! ALGORITHM 2.2
    @classmethod
    def simulate_relative_motion(cls, y_0 : np.ndarray, t_0 : float = 0.0, t_f : float = 0.0, show : bool = False) -> dict:
        """Integrates the Ordinary Differential Equations for the relative motion

        Args:
            y_0 (np.ndarray): Initial state [6,1]
            t_0 (float, optional): Initial time. Defaults to 0.0.
            t_f (float, optional): Final time. Defaults to 0.0.
            show (bool, optional): True for plotting the trajectory. Defaults to False.
            
        Returns:
            dict: { t: time, y: state[n_states, n_points] }
        """
        
        # >>> 1.
        
        parameters = cls.calculate_orbital_parameters(y_0[:3], y_0[3:])
        
        if t_f == 0.0 and t_0 >= 0.0:
            
            t_f = parameters.T
        
        if parameters.e >= 1.0:
            
            t_f = Time.calculate_hyperbolic_orbit(DirectionType.MEAN_ANOMALY_TO_TIME, h=parameters.h, e=parameters.e, theta=parameters.theta_inf * 0.999)
        
        if t_f < t_0: raise Exception('Invalid integration time')
        
        integrationResult = solve_ivp(fun=cls.relative_eom, t_span=[t_0, t_f], y0=y_0, method='RK45', args=(), rtol=1e-8, atol=1e-8)
        
        if not integrationResult['success']: Exception(integrationResult['message'])
        
        x = integrationResult['y'][0, :]
        y = integrationResult['y'][1, :]
        z = integrationResult['y'][2, :]
        
        # >>> 2.
        
        if show:
            
            plt.figure(figsize=(10, 8)) #fig.subplots_adjust(top=1.1, bottom=-0.1)
            
            ax = plt.axes(projection='3d')
            
            # ? Max Values
            
            xMax = 1.25 * max(np.absolute(x))
            yMax = 1.25 * max(np.absolute(y))
            zMax = 1.25 * max(np.absolute(z))
            
            # ? Plane
            
            p = mpatches.Rectangle((-xMax, -yMax), 2 * xMax, 2 * yMax, fc=(0,0,0,0.1), ec=(0,0,0,1), lw=2)
            
            ax.add_patch(p)
            
            art3d.pathpatch_2d_to_3d(p, z=0, zdir='z')
            
            # ? Axes
            
            ax.plot([0, xMax], [0, 0], [0, 0], 'k--')
            ax.plot([0, 0], [0, yMax], [0, 0], 'k--')
            ax.plot([0, 0], [0, 0], [0, zMax], 'k--')
            
            # ? Earth
            
            ax.scatter(0, 0, 0, s=1000, c='c')
            
            # ? Orbit
            
            ax.plot(x, y, z, label='Orbit')
            
            # ? Start
            
            ax.scatter(x[0], y[0], z[0], s=200, c='g', label='Start')
            
            # ? Finish
            
            ax.scatter(x[-1], y[-1], z[-1], s=200, c='r', label='Finish')
            
            ax.set_title('Spacecraft Orbit')
            ax.set_xlabel('$x$ [km]')
            ax.set_ylabel('$y$ [km]')
            ax.set_zlabel('$z$ [km]')
            
            plt.legend()
            plt.show()
        
        return dict(t=integrationResult['t'], y=integrationResult['y'], dt=np.abs(integrationResult['t'][-1] - integrationResult['t'][0]))
    
    # ! SECTION 2.4 - 2.9
    
    @classmethod
    def calculate_orbital_parameters(cls, r : np.ndarray, v : np.ndarray, show : bool = False) -> OrbitalParameters:
        """Calculates the orbital parameters

        Args:
            r (np.ndarray): Position vector
            v (np.ndarray): Velocity vector
            show (bool, optional): Shows the console print. Defaults to False.
        
        Returns:
            ORBITAL_PARAMETERS: Orbital parameters
        """
        
        parameters = OrbitalParameters()
        
        # >>> Angular Momentum
        
        h = np.cross(r, v)
        
        parameters.h = np.linalg.norm(h)
        
        # >>> Energy
        
        parameters.epsilon = np.linalg.norm(v)**2 / 2 - cls.mu / np.linalg.norm(r)
        
        # >>> Eccentricity
        
        parameters.e = np.sqrt((2 * np.linalg.norm(h)**2 * parameters.epsilon) / (cls.mu **2) + 1)
        
        # >>> Select Orbit Type
        
        if parameters.e == 0: # ? CIRCULAR
            
            parameters.r_p  = np.linalg.norm(r)                                                # * Pericenter radius
            parameters.r_a  = np.linalg.norm(r)                                                # * Apocenter radius
            parameters.a    = np.linalg.norm(r)                                                # * Semi-major axis
            parameters.b    = np.linalg.norm(r)                                                # * Semi-latus rectum
            parameters.T    = (2 * np.pi) /  np.sqrt(cls.mu) * np.linalg.norm(r) ** (3 / 2)    # * Period
            
            if show:
                
                print('*' * 10, 'CIRCULAR ORBIT', '*' * 10)
                print(f'h   = {parameters.h:10.2f} \t [km^2 / s]')
                print(f'e   = {parameters.e:10.5f} \t []')
                print(f'r_p = {parameters.r_p:10.2f} \t [km]')
                print(f'r_a = {parameters.r_a:10.2f} \t [km]')
                print(f'a   = {parameters.a:10.2f} \t [km]')
                print(f'b   = {parameters.b:10.2f} \t [km]')
                print(f'T   = {parameters.T / 3600:10.5f} \t [h]')
                print('*' * 40)
        
        elif parameters.e > 0 and parameters.e < 1: # ? ELLIPTICAL
            
            parameters.r_p  = parameters.h ** 2 / cls.mu * 1 / (1 + parameters.e)       # * Pericenter radius
            parameters.r_a  = parameters.h ** 2 / cls.mu * 1 / (1 - parameters.e)       # * Apocenter radius
            parameters.a    = (parameters.r_p + parameters.r_a) / 2                     # * Semi-major axis
            parameters.b    = parameters.a * np.sqrt(1 - parameters.e ** 2)             # * Semi-latus rectum
            parameters.T    = (2 * np.pi) /  np.sqrt(cls.mu) * parameters.a ** (3 / 2)  # * Period
            
            if show:
                
                print('*' * 10, 'ELLIPTICAL ORBIT', '*' * 10)
                print(f'h   = {parameters.h:10.2f} \t [km^2 / s]')
                print(f'e   = {parameters.e:10.5f} \t []')
                print(f'r_p = {parameters.r_p:10.2f} \t [km]')
                print(f'r_a = {parameters.r_a:10.2f} \t [km]')
                print(f'a   = {parameters.a:10.2f} \t [km]')
                print(f'b   = {parameters.b:10.2f} \t [km]')
                print(f'T   = {parameters.T / 3600:10.5f} \t [h]')
                print('*' * 40)
        
        elif parameters.e == 1: # ? PARABOLIC
            
            parameters.r_p      = parameters.h ** 2 / cls.mu * 1 / (1 + 1)  # * Pericenter radius
            parameters.r_a      = np.inf                                    # * Apocenter radius
            parameters.a        = np.inf                                    # * Semi-major axis
            parameters.b        = 0                                         # * Semi-latus rectum
            parameters.T        = np.inf                                    # * Period
            parameters.v_esc    = np.sqrt(2 * cls.mu  / parameters.r_p)     # * Escape velocity
            
            
            if show:
                
                print('*' * 10, 'PARABOLIC ORBIT', '*' * 10)
                print(f'h     = {parameters.h:10.2f} \t [km^2 / s]')
                print(f'e     = {parameters.e:10.5f} \t []')
                print(f'r_p   = {parameters.r_p:10.2f} \t [km]')
                print(f'r_a   = {parameters.r_a:10.2f} \t [km]')
                print(f'a     = {parameters.a:10.2f} \t [km]')
                print(f'b     = {parameters.b:10.2f} \t [km]')
                print(f'T     = {parameters.T / 3600:10.5f} \t [h]')
                print(f'v_esc = {parameters.v_esc:10.2f} \t [km / s]')
                print('*' * 40)
        
        else: # ? HYPERBOLIC
            
            parameters.r_p          = parameters.h ** 2 / cls.mu * 1 / (1 + parameters.e)   # * Pericenter radius
            parameters.r_a          = parameters.h ** 2 / cls.mu * 1 / (1 - parameters.e)   # * Apocenter radius
            parameters.a            = (np.abs(parameters.r_a) - parameters.r_p) / 2         # * Semi-major axis
            parameters.b            = parameters.a * np.sqrt(parameters.e ** 2 - 1)         # * Semi-latus rectum
            parameters.T            = np.inf                                                # * Period
            parameters.v_esc        = np.sqrt(2 * cls.mu  / parameters.r_p)                 # * Escape velocity
            parameters.theta_inf    = np.arccos(-1 / parameters.e)                          # * True anomaly at inf
            parameters.beta         = np.arccos(1 / parameters.e)                           # * Hyperbola asymptote angle
            parameters.delta        = 2 * np.arcsin(1 / parameters.e)                       # * Turn angle
            parameters.Delta        = parameters.a * np.sqrt(parameters.e ** 2 - 1)         # * Aiming radius
            parameters.v_inf        = np.sqrt(cls.mu / parameters.a)                        # * Hyperbolic excess speed
            parameters.C_3          = parameters.v_inf ** 2                                 # * Characteristic energy
            
            if show:
                
                print('*' * 10, 'HYPERBOLIC ORBIT', '*' * 10)
                print(f'h         = {parameters.h:10.2f} \t [km^2 / s]')
                print(f'e         = {parameters.e:10.5f} \t []')
                print(f'r_p       = {parameters.r_p:10.2f} \t [km]')
                print(f'r_a       = {parameters.r_a:10.2f} \t [km]')
                print(f'a         = {parameters.a:10.2f} \t [km]')
                print(f'b         = {parameters.b:10.2f} \t [km]')
                print(f'T         = {parameters.T / 3600:10.5f} \t [h]')
                print(f'v_esc     = {parameters.v_esc:10.2f} \t [km / s]')
                print(f'theta_inf = {np.rad2deg(parameters.theta_inf):10.2f} \t [deg]')
                print(f'beta      = {np.rad2deg(parameters.beta):10.2f} \t [deg]')
                print(f'delta     = {np.rad2deg(parameters.delta):10.2f} \t [deg]')
                print(f'Delta     = {parameters.Delta:10.2f} \t [km]')
                print(f'v_inf     = {parameters.v_inf:10.2f} \t [km / s]')
                print(f'C_3       = {parameters.C_3:10.2f} \t [km / s]')
                print('*' * 40)
        
        return parameters
    
    # ! SECTION 6.10
    
    @classmethod
    def thrust_relative_eom(cls, t : float, X : np.ndarray, T : float, I_sp : float) -> np.ndarray:
        """Equations of relative motion with thrust

        Args:
            t (float): Time
            X (np.ndarray): State [7,1]
            T (float): Thrust
            I_sp (float): Specific impulse

        Returns:
            np.ndarray: Derivative of state
        """
        
        x, y, z, v_x, v_y, v_z, m = X
        
        r = np.sqrt(x**2 + y**2 + z**2)
        
        v = np.sqrt(v_x**2 + v_y**2 + v_z**2)
        
        dX_dt = np.zeros(shape=(7))
        
        dX_dt[0] = v_x
        dX_dt[1] = v_y
        dX_dt[2] = v_z
        dX_dt[3] = - (cls.mu / r**3) * x + (T / m) * (v_x / v)
        dX_dt[4] = - (cls.mu / r**3) * y + (T / m) * (v_y / v)
        dX_dt[5] = - (cls.mu / r**3) * z + (T / m) * (v_z / v)
        dX_dt[6] = - T / (I_sp * cls.g_0)
        
        return dX_dt
    
    @classmethod
    def simulate_relative_motion_with_thrust(cls, y_0 : np.ndarray, T : float, I_sp : float, t_0 : float = 0.0, t_f : float = 0.0):
        """Integrates the Ordinary Differential Equations for the relative motion with Thrust

        Args:
            y_0 (np.ndarray): Initial state [7,1]
            T (float): Thrust
            I_sp (float): Specific impulse
            t_0 (float, optional): Initial time. Defaults to 0.0.
            t_f (float, optional): Final time. Defaults to 0.0.
            
        Returns:
            dict: { t: time, y: state[n_states, n_points] }
        """
        
        T = T * 1e-3 # * [kg * km / s^2]
        
        if t_f < t_0: raise Exception('Invalid integration time')
        
        cls.calculate_orbital_parameters(y_0[:3], y_0[3:6])
        
        if t_f == 0.0: t_f = cls.parameters.T
        
        integrationResult = solve_ivp(fun=cls.thrust_relative_eom, t_span=[t_0, t_f], y0=y_0, method='RK45', args=(T, I_sp), rtol=1e-8, atol=1e-8)
        
        if not integrationResult['success']: Exception(integrationResult['message'])
        
        return dict(t=integrationResult['t'], y=integrationResult['y'])
    
if __name__  == '__main__':
    
    print('EXAMPLE 2.3\n')
    TwoBodyProblem.simulate_relative_motion(np.array([8000, 0, 6000, 0, 7, 0]), show=True)
    print('-' * 40, '\n')
    
    # r, v = ThreeDimensionalOrbit.PF2GEF(ORBITAL_ELEMENTS(0, 0.33333, 0, 0, 0, 0, 12000))
    # res1 = TwoBodyProblem.integrateRelativeMotion(np.hstack([r, v]))
    # r, v = ThreeDimensionalOrbit.PF2GEF(ORBITAL_ELEMENTS(0, 0.33333, 0, 0, np.deg2rad(25), 0, 12000))
    # res2 = TwoBodyProblem.integrateRelativeMotion(np.hstack([r, v]))
    
    # plt.figure(figsize=(10, 8))
            
    # ax = plt.axes(projection='3d')
    
    # ax.scatter(0, 0, 0, s=1000, c='c')
    # ax.plot(res1['y'][0,:], res1['y'][1,:], res1['y'][2,:], label='Orbit')
    # ax.plot(res2['y'][0,:], res2['y'][1,:], res2['y'][2,:], label='Orbit')
    # plt.show()
    
    print('EXAMPLE 6.15\n')
    result = TwoBodyProblem.simulate_relative_motion_with_thrust(np.array([6858, 0, 0, 0, 7.7102, 0, 2000]), 10e3, 300, 0, 261.112700)
    print('r = ', result['y'][:3, -1])
    print('v = ', result['y'][3:6, -1])
    print('m = ', result['y'][6, -1])
    print('-' * 40, '\n')