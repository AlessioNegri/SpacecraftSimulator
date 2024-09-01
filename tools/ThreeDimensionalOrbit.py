""" ThreeDimensionalOrbit.py: Implements the algorithms to represent an orbit in 3D """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"
__book__        = "Orbital Mechanics for Engineering Students"
__chapter__     = "4 - Orbits in Three Dimensions"

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from dataclasses import dataclass
from PIL import Image

sys.path.append(os.path.dirname(__file__))

from Common import wrap_to_2pi
from AstronomicalData import AstronomicalData, CelestialBody
from TwoBodyProblem import TwoBodyProblem
from Time import Time, DirectionType

# --- STRUCT 

@dataclass
class OrbitalElements:
    """Orbital elements parameters"""
    
    h       : float = 0.0   # * Specific Angular Momentum                       [ km^2 / s ]
    e       : float = 0.0   # * Eccentricity                                    [ ]
    i       : float = 0.0   # * Inclination                                     [ rad ]
    Omega   : float = 0.0   # * Right Ascension of the Ascending Node (RAAN)    [ rad ]
    omega   : float = 0.0   # * Argument of the Perigee                         [ rad ]
    theta   : float = 0.0   # * True Anomaly                                    [ rad ]
    a       : float = 0.0   # * Semi-Major Axis                                 [ km ]

# --- CLASS 

class ThreeDimensionalOrbit():
    """Manages the conversions among different orbit representations"""
    
    # --- ASTRONOMICAL CONSTANTS 
    
    mu      = AstronomicalData.gravitational_parameter(CelestialBody.EARTH)
    J_2     = AstronomicalData.second_zonal_harmonics(CelestialBody.EARTH)
    R_E     = AstronomicalData.equatiorial_radius(CelestialBody.EARTH)
    omega   = AstronomicalData.ground_track_angular_velocity(CelestialBody.EARTH)
    
    # --- METHODS 
    
    @classmethod
    def set_celestial_body(cls, celestialBody : CelestialBody) -> None:
        """Sets the current celectial body

        Args:
            celestialBody (CelestialBody): Celestial body
        """
        
        cls.mu      = AstronomicalData.gravitational_parameter(celestialBody)
        cls.J_2     = AstronomicalData.second_zonal_harmonics(celestialBody)
        cls.R_E     = AstronomicalData.equatiorial_radius(celestialBody)
        cls.omega   = AstronomicalData.ground_track_angular_velocity(celestialBody)
    
    # ! SECTION 4.3
    
    # ! ALGORITHM 4.1
    @classmethod
    def calculate_ra_dec(cls, r : np.ndarray) -> list:
        """Calculates the Right Ascension and Declination

        Args:
            r (np.ndarray): Position vector

        Returns:
            list: [alpha, delta]
        """
        
        # >>> 1. Magnitude
        
        r_m = np.linalg.norm(r)
        
        # >>> 2. Direction cosines
        
        l = r[0] / r_m
        m = r[1] / r_m
        n = r[2] / r_m
        
        # >>> 3. Declination
        
        delta = np.arcsin(n)
        
        # >>> 4. Right Ascension
        
        alpha = np.arccos(l / np.cos(delta)) if m > 0 else (2 * np.pi - np.arccos(l / np.cos(delta)))
        
        return [alpha, delta]
    
    # ! SECTION 4.4
    
    # ! ALGORITHM 4.2
    @classmethod
    def calculate_orbital_elements(cls, r : np.ndarray, v : np.ndarray, deg : bool = False) -> OrbitalElements:
        """Calculates the Orbital Elements from position and velocity vectors in Geocentric Equatorial Frame

        Args:
            r (np.ndarray): Position vector
            v (np.ndarray): Velocity vector
            deg (bool, optional): Enable angles in degrees. Defaults to False.

        Returns:
            ORBITAL_ELEMENTS: Orbital Elements
        """
        
        oe = OrbitalElements()
        
        # >>> 1. Magnitudes
        
        r_m = np.linalg.norm(r)
        
        # >>> 2.
        
        v_m = np.linalg.norm(v)
        
        # >>> 3.
        
        v_r = np.dot(r, v) / r_m
        
        # >>> 4. Angular momentum
        
        h = np.cross(r, v)
        
        # >>> 5. Semi-major axis
        
        oe.h = np.linalg.norm(h)
        
        oe.a = - 0.5 * cls.mu / (0.5 * v_m**2 - cls.mu / r_m)
        
        # >>> 6. Inclination
        
        oe.i = np.arccos(h[2] / oe.h)
        
        # >>> 7. Line of nodes
        
        N = np.array([1, 0, 0])
        
        if (oe.i <= 0.5 * np.pi):
        
            if oe.i > np.deg2rad(1) or (oe.i < np.deg2rad(1) and oe.i > 1e-6):
                
                N = np.cross(np.array([0, 0, 1]), h)
                
            else:
            
                N = np.array([1, 0, 0])
                
        else:
            
            if oe.i < (np.pi - np.deg2rad(1)) or (oe.i > (np.pi - np.deg2rad(1)) and (np.pi - oe.i) > 1e-6):
                
                N = np.cross(np.array([0, 0, 1]), h)
                
            else:
            
                N = np.array([1, 0, 0])
        
        # >>> 8.
        
        N_m = np.linalg.norm(N)
        
        # >>> 9. Right Ascension of the ascending node
        
        oe.Omega = np.arccos(N[0] / N_m) if N[1] >= 0 else (2 * np.pi - np.arccos(N[0] / N_m))
        
        # >>> 10. Eccentricity
        
        e = 1 / cls.mu * (np.cross(v, h) - cls.mu * r / r_m)
        e = 1 / cls.mu * ((v_m**2 - cls.mu / r_m) * r - r_m * v_r * v)
        
        # >>> 11.
        
        oe.e = np.linalg.norm(e)
        
        # >>> 12. Anomaly of the perigee
        
        oe.omega = np.arccos(np.dot(N, e) / (N_m * oe.e)) if e[2] >= 0 else (2 * np.pi - np.arccos(np.dot(N, e) / (N_m * oe.e)))
        
        # >>> 13. True anomaly
        
        oe.theta = np.arccos(np.dot(e, r) / (oe.e * r_m)) if v_r >= 0 else (2 * np.pi - np.arccos(np.dot(e, r) / (oe.e * r_m)))
        
        if deg:
            
            oe.i        = np.rad2deg(oe.i)
            oe.Omega    = np.rad2deg(oe.Omega)
            oe.omega    = np.rad2deg(oe.omega)
            oe.theta    = np.rad2deg(oe.theta)
        
        return oe
    
    # ! SECTION 4.6
    
    @classmethod
    def gef_2_pf(cls, r : np.ndarray, v : np.ndarray) -> list:
        """Geocentric Equatiorial Frame --> Perifocal Frame

        Args:
            r (np.ndarray): Position vector GEF
            v (np.ndarray): Velocity vector GEF

        Returns:
            list: [r_PF, v_PF]
        """
        
        # >>> 1.
        
        oe = cls.calculate_orbital_elements(r, v)
        
        # >>> 2.
        
        R_3_O = np.array(
            [
                [ + np.cos(oe.Omega) , + np.sin(oe.Omega) , 0 ],
                [ - np.sin(oe.Omega) , + np.cos(oe.Omega) , 0 ],
                [ 0                  , 0                  , 1 ]
            ])
        
        R_1_i = np.array(
            [
                [ 1 , 0              , 0              ],
                [ 0 , + np.cos(oe.i) , + np.sin(oe.i) ],
                [ 0 , - np.sin(oe.i) , + np.cos(oe.i) ]
            ])
        
        R_3_o = np.array(
            [
                [ + np.cos(oe.omega) , + np.sin(oe.omega) , 0 ],
                [ - np.sin(oe.omega) , + np.cos(oe.omega) , 0 ],
                [ 0                  , 0                  , 1 ]
            ])
        
        R = np.matmul(R_3_o, np.matmul(R_1_i, R_3_O))
        
        # >>> 3.
        
        return [np.matmul(R, r), np.matmul(R, v)]
    
    # ! ALGORITHM 4.5
    @classmethod
    def pf_2_gef(cls, oe : OrbitalElements) -> list :
        """Perifocal Frame --> Geocentric Equatiorial Frame

        Args:
            oe (ORBITAL_ELEMENTS): Orbital Elements

        Returns:
            list: [r_GEF, v_GEF]
        """
        
        p = (oe.a * (1 - oe.e**2)) if oe.h == 0 else (oe.h**2 / cls.mu)
        
        # >>> 1.
        
        r = p / (1 + oe.e * np.cos(oe.theta)) * np.array([np.cos(oe.theta), np.sin(oe.theta), 0])
        
        # >>> 2.
        
        v = np.sqrt(cls.mu / p) * np.array([-np.sin(oe.theta), oe.e + np.cos(oe.theta), 0])
        
        # >>> 3.
        
        R_3_O = np.array(
            [
                [ + np.cos(oe.Omega) , + np.sin(oe.Omega) , 0 ],
                [ - np.sin(oe.Omega) , + np.cos(oe.Omega) , 0 ],
                [ 0                  , 0                  , 1 ]
            ])
        
        R_1_i = np.array(
            [
                [ 1 , 0              , 0              ],
                [ 0 , + np.cos(oe.i) , + np.sin(oe.i) ],
                [ 0 , - np.sin(oe.i) , + np.cos(oe.i) ]
            ])
        
        R_3_o = np.array(
            [
                [ + np.cos(oe.omega) , + np.sin(oe.omega) , 0 ],
                [ - np.sin(oe.omega) , + np.cos(oe.omega) , 0 ],
                [ 0                  , 0                  , 1 ]
            ])
        
        R = np.matmul(R_3_o, np.matmul(R_1_i, R_3_O))
        
        # >>> 4.
        
        return [np.matmul(R.T, r), np.matmul(R.T, v)]

    # ! SECTION 4.7

    @classmethod
    def calculate_planet_oblateness_effect(cls, oe : OrbitalElements) -> list:
        """Calculates the planet oblateness effect
        
        Args:
            oe (ORBITAL_ELEMENTS): Orbital Elements

        Returns:
            list: [dOmega_dt, domega_dt]
        """
        
        # >>> Right Ascension of the ascending node variation
        
        dOmega_dt = - 3/2 * (np.sqrt(cls.mu) * cls.J_2 * cls.R_E**2) / ((1 - oe.e**2)**2 * oe.a**(7/2)) * np.cos(oe.i)
        
        # >>> Anomaly of the perigee variation
        
        domega_dt = - 3/2 * (np.sqrt(cls.mu) * cls.J_2 * cls.R_E**2) / ((1 - oe.e**2)**2 * oe.a**(7/2)) * (5/2 * np.sin(oe.i)**2 - 2)
        
        return [dOmega_dt, domega_dt]
    
    # ! SECTION 4.8
    
    # ! ALGORITHM 4.6
    @classmethod
    def calculate_ground_track(cls, oe : OrbitalElements, dt : float, show : bool = False, m : float = 1) -> list:
        """Calculates the Ground Track for the given time step

        Args:
            oe (ORBITAL_ELEMENTS): Orbital Elements
            dt (float): Time step
            show (bool, optional): True for plotting the ground track. Defaults to False.
            m (float, optional): Multiple of period. Defaults to 1.
            
        Returns:
            list: [right ascension, declination]
        """
        
        if oe.e >= 1.0: return [[], []]
        
        # >>> 1. Oblateness
        
        dOmega_dt, domega_dt = cls.calculate_planet_oblateness_effect(oe)
        
        # >>> 2. Initial condition
        
        X = cls.pf_2_gef(oe)
        
        parameters = TwoBodyProblem.calculate_orbital_parameters(X[0], X[1])
        
        t_0 = 0.0
        
        dirType = DirectionType.MEAN_ANOMALY_TO_TIME
        
        Time.mu = cls.mu
        
        if      oe.e == 0:      t_0 = Time.calculate_circular_orbit(dirType, T=parameters.T, theta=oe.theta)
        elif    oe.e < 1.0:     t_0 = Time.calculate_elliptical_orbit(dirType, T=parameters.T, e=parameters.e, theta=oe.theta)
        elif    oe.e == 1.0:    t_0 = Time.calculate_parabolic_orbit(dirType, h=parameters.h, theta=oe.theta)
        else:                   t_0 = Time.calculate_hyperbolic_orbit(dirType, h=parameters.h, e=parameters.e, theta=oe.theta)
        
        # >>> 3. Cycle
        
        ra = []
        
        dec = []
        
        dirType = DirectionType.TIME_TO_MEAN_ANOMALY
        
        for t in np.arange(t_0, m * parameters.T + dt, dt):
            
            # >>> a) True anomaly
            
            theta = 0.0
            
            if      oe.e == 0:      theta = Time.calculate_circular_orbit(dirType, T=parameters.T, t=t)
            elif    oe.e < 1.0:     theta = Time.calculate_elliptical_orbit(dirType, T=parameters.T, e=parameters.e, t=t)
            elif    oe.e == 1.0:    theta = Time.calculate_parabolic_orbit(dirType, h=parameters.h, t=t)
            else:                   theta = Time.calculate_hyperbolic_orbit(dirType, h=parameters.h, e=parameters.e, t=t)
            
            # >>> b) New Orbital Elements
            
            oe.Omega = oe.Omega + dOmega_dt * dt
            oe.omega = oe.omega + domega_dt * dt
            oe.theta = theta
            
            # >>> c) New state
            
            X = cls.pf_2_gef(oe)
            
            # >>> d) New position
            
            theta = wrap_to_2pi(cls.omega * (t - t_0))
            
            R_3_t = np.array(
                [
                    [+ np.cos(theta) , + np.sin(theta), 0],
                    [- np.sin(theta) , + np.cos(theta), 0],
                    [0               , 0              , 1]
                ])
            
            # >>> e) Right Ascension and Declination
            
            ra_i, dec_i = cls.calculate_ra_dec(np.matmul(R_3_t, X[0]))
            
            ra.append(np.rad2deg(ra_i))
            dec.append(np.rad2deg(dec_i))
        
        # >>> Plot
        
        if show:
            
            img = np.asarray(Image.open('./tools/texture/Earth.jpg').transpose(Image.FLIP_TOP_BOTTOM))
            
            plt.figure()
            plt.imshow(img, origin='lower', extent=(0, 360, -90, 90))
            plt.grid(True)
            plt.scatter(ra, dec, c='c')
            plt.scatter(ra[0], dec[0], c='m', label='Start')
            plt.scatter(ra[-1], dec[-1], c='r', label='Finish')
            plt.legend()
            plt.xlabel('Right Ascension [deg]')
            plt.ylabel('Declination [deg]')
            plt.xlim([0, 360])
            plt.ylim([-90, 90])
            plt.show()
        
        return [ra, dec]

if __name__ == '__main__':
    
    print(np.deg2rad(360 * (1 + 1 / 365.26) / (24 * 3600)))
    print(2 * np.pi / (365.256363004 * 86400))
    
    print('EXAMPLE 4.1\n')
    print(np.rad2deg(ThreeDimensionalOrbit.calculate_ra_dec(np.array([-5368, -1784, 3691]))))
    print('-' * 40, '\n')
    
    print('EXAMPLE 4.3\n')
    print(ThreeDimensionalOrbit.calculate_orbital_elements(np.array([-6045, -3490, 2500]), np.array([-3.457, 6.618, 2.533]), deg=True))
    print('-' * 40, '\n')
    
    print('EXAMPLE 4.7\n')
    print(ThreeDimensionalOrbit.pf_2_gef(OrbitalElements(80000, 1.4, np.deg2rad(30), np.deg2rad(40), np.deg2rad(60), np.deg2rad(30))))
    print(ThreeDimensionalOrbit.gef_2_pf(np.array([-4039.8959232, 4814.56048018, 3628.62470217]), np.array([-10.38598762, -4.77192164, 1.743875])))
    print('-' * 40, '\n')
    
    print('EXAMPLE 4.8\n')
    print(ThreeDimensionalOrbit.calculate_planet_oblateness_effect(OrbitalElements(0, 0.0089312, np.deg2rad(51.43), 0, 0, 0, 6718)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 4.8\n')
    ThreeDimensionalOrbit.calculate_ground_track(OrbitalElements(56554, 0.19760, np.deg2rad(60), np.deg2rad(270), np.deg2rad(45), np.deg2rad(230), 8350), 60, show=True, m=3)
    print('-' * 40, '\n')