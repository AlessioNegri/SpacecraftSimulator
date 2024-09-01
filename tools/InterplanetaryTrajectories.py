""" InterplanetaryTrajectories.py: Implements the interplanetary trajectories equations """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"
__book__        = "Orbital Mechanics for Engineering Students"
__chapter__     = "8 - Interplanetary Trajectories"

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from enum import IntEnum
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from Common import wrap_to360deg, print_progress_bar, daterange, daterange_length
from AstronomicalData import AstronomicalData, CelestialBody
from Time import Time, DirectionType
from ThreeDimensionalOrbit import ThreeDimensionalOrbit
from OrbitalManeuvers import OrbitalManeuvers, ManeuverResult
from OrbitDetermination import OrbitDetermination, OrbitalElements

# --- STRUCT 

class FlybySide(IntEnum):
    """Type of fly-by"""
    
    DARK_SIDE   = 0
    SUNLIT_SIDE = 1

# --- CLASS 

class InterplanetaryTrajectories:
    """Implements methods and functions to simulate interplanetary trajectories"""
    
    # --- METHODS 
    
    # ! SECTION 8.3
    
    @classmethod
    def synodic_period(cls, departurePlanet : CelestialBody, arrivalPlanet : CelestialBody) -> float:
        """Calculates the Synodic Period for an interplanetary transfer

        Args:
            departurePlanet (CelestialBody): Departure planet
            arrivalPlanet (CelestialBody): Arrival planet

        Returns:
            float: Synodic period
        """
        
        # >>> 1. Mean motions
        
        n_1 = 2 * np.pi / AstronomicalData.sidereal_orbital_period(departurePlanet)
        n_2 = 2 * np.pi / AstronomicalData.sidereal_orbital_period(arrivalPlanet)
        
        # >>> 2. Synodic period
        
        T_syn = 2 * np.pi / np.abs(n_2 - n_1)
        
        return T_syn
    
    @classmethod
    def wait_time(cls, departurePlanet : CelestialBody, arrivalPlanet : CelestialBody) -> list:
        """Calculates the wait time for an interplanetary transfer

        Args:
            departurePlanet (CelestialBody): Departure planet
            arrivalPlanet (CelestialBody): Arrival planet

        Returns:
            list: [Wait time, initial phase angle, final phase angle
        """
        
        # >>> 1. Transfer ellipse
        
        mu_sun  = AstronomicalData.gravitational_parameter(CelestialBody.SUN)
        R_1     = AstronomicalData.semi_major_axis(departurePlanet)
        R_2     = AstronomicalData.semi_major_axis(arrivalPlanet)
        n_1     = 2 * np.pi / AstronomicalData.sidereal_orbital_period(departurePlanet)
        n_2     = 2 * np.pi / AstronomicalData.sidereal_orbital_period(arrivalPlanet)
        
        t_12 = np.pi / np.sqrt(mu_sun) * ((R_1 + R_2) / 2)**(3/2)
        
        # >>> 2. Initial phase angle bewteen planets (departure trip)
        
        phi_0 = np.pi - n_2 * t_12
        
        # >>> 3. Final phase angle at planet arrival (departure trip)
        
        phi_f = np.pi - n_1 * t_12
        
        # >>> 4. Initial phase angle bewteen planets (return trip)
        
        phi_0 = - phi_f
        
        # >>> 5. Wait time
        
        t_wait = -1
        
        N = 0
        
        while t_wait < 0:
            
            t_wait = (-2 * phi_f - 2 * np.pi * N) / (n_2 - n_1) if (n_1 > n_2) else (-2 * phi_f + 2 * np.pi * N) / (n_2 - n_1)
            
            N += 1
        
        return [t_wait, phi_0, phi_f]
    
    # ! SECTION 8.6
    
    @classmethod
    def departure(cls, departurePlanet : CelestialBody, arrivalPlanet : CelestialBody, r_p : float, m : float) -> ManeuverResult:
        """Planetary departure hyperbola design

        Args:
            departurePlanet (CelestialBody): Departure planet
            arrivalPlanet (CelestialBody): Arrival planet
            r_p (float): Circular Parking Orbit radius
            m (float): Mass of the spacecraft

        Returns:
            MANEUVER_RESULT: [dv, dt, dm, Orbital Elements]
        """
        
        # >>> 1. Hyperbolic excess speed
        
        mu_sun  = AstronomicalData.gravitational_parameter(CelestialBody.SUN)
        mu_1    = AstronomicalData.gravitational_parameter(departurePlanet)
        R_1     = AstronomicalData.semi_major_axis(departurePlanet)
        R_2     = AstronomicalData.semi_major_axis(arrivalPlanet)
        
        v_inf = np.sqrt(mu_sun / R_1) * (np.sqrt(2 * R_2 / (R_1 + R_2)) - 1)
        
        # >>> 2. Hyperbola trajectory
        
        e = 1 + r_p * v_inf**2 / mu_1
        
        h = r_p * np.sqrt(v_inf**2 + 2 * mu_1 / r_p)
        
        v_p = h / r_p
        
        beta = np.arccos(1 / e)
        
        # >>> 3. Circular parking orbit
        
        v_c = np.sqrt(mu_1 / r_p)
        
        # >>> 4. Maneuver
        
        result = ManeuverResult()
        
        result.dv = np.abs(v_p - v_c)
        
        result.dt = 0.0
        
        result.dm = OrbitalManeuvers.propellant_mass(m, result.dv)
        
        result.oe = OrbitalElements(h, e, 0, 0, 0, 0, 0)
        
        return result
    
    # ! SECTION 8.8
    
    @classmethod
    def rendezvous(cls, departurePlanet : CelestialBody, arrivalPlanet : CelestialBody, r_p_A : float, T : float, m : float) -> ManeuverResult:
        """Planetary arrival hyperbola design

        Args:
            departurePlanet (CelestialBody): Departure planet
            arrivalPlanet (CelestialBody): Arrival planet
            r_p_A (float): Elliptical Capture Orbit pericenter radius
            T (float): Rendezvous Orbit period
            m (float): Mass of the spacecraft

        Returns:
            MANEUVER_RESULT: [dv, dt, dm, Orbital Elements]
        """
        
        # >>> 1. Hyperbolic excess speed
        
        mu_sun  = AstronomicalData.gravitational_parameter(CelestialBody.SUN)
        mu_2    = AstronomicalData.gravitational_parameter(arrivalPlanet)
        R_1     = AstronomicalData.semi_major_axis(departurePlanet)
        R_2     = AstronomicalData.semi_major_axis(arrivalPlanet)
        
        v_inf = np.sqrt(mu_sun / R_2) * (1 - np.sqrt(2 * R_1 / (R_1 + R_2)))
        
        # >>> 2. Rendezvous orbit from period (optimal periapse radius)
        
        a = (T * np.sqrt(mu_2) / (2 * np.pi))**(2/3)
        
        e = 1 - r_p_A / a if r_p_A != 0 else (2 * mu_2) / (a * v_inf**2) - 1
        
        r_p = r_p_A if r_p_A != 0 else 2 * mu_2 / v_inf**2 * (1 - e) / (1 + e)
        
        r_a = 2 * a - r_p if r_p_A != 0 else 2 * mu_2 / v_inf**2
        
        v_c = np.sqrt(mu_2 * (1 + e) / r_p)
        
        # >>> 3. Hyperbola trajectory
        
        e_hyp = 1 + r_p * v_inf**2 / mu_2
        
        h_hyp = r_p * np.sqrt(v_inf**2 + 2 * mu_2 / r_p)
        
        delta = 2 * np.arcsin(1 / e_hyp)
        
        beta = np.arccos(1 / e_hyp)
        
        Delta = h_hyp**2 / mu_2 * 1 / np.sqrt(e_hyp**2 - 1)
        
        v_p = h_hyp / r_p
        
        # >>> 4. Maneuver
        
        result = ManeuverResult()
        
        result.dv = np.abs(v_p - v_c)
        
        result.dt = 0.0
        
        result.dm = OrbitalManeuvers.propellant_mass(m, result.dv)
        
        result.oe = OrbitalElements(h_hyp, e_hyp, 0, 0, 0, 0, 0)
        
        return result
    
    # ! SECTION 8.9
    
    @classmethod
    def flyby(cls, departurePlanet : CelestialBody, arrivalPlanet : CelestialBody, r_p : float, theta_1 : float, m : float, side : FlybySide = FlybySide.DARK_SIDE) -> ManeuverResult:
        """Planetary flyby hyperbola design

        Args:
            departurePlanet (CelestialBody): Departure planet
            arrivalPlanet (CelestialBody): Arrival planet
            r_p (float): Hyperbola periapse radius
            theta_1 (float): True anomaly of the incoming trajectory
            m (float): Mass of the spacecraft
            side (FlybySide, optional): Side w.r.t. Sun. Defaults to FlybySide.DARK_SIDE.

        Returns:
            MANEUVER_RESULT: [dv, dt, dm, Orbital Elements]
        """
        
        # >>> 0. Astronomical Data
        
        mu_sun  = AstronomicalData.gravitational_parameter(CelestialBody.SUN)
        mu_2    = AstronomicalData.gravitational_parameter(arrivalPlanet)
        R_1     = AstronomicalData.semi_major_axis(departurePlanet)
        R_2     = AstronomicalData.semi_major_axis(arrivalPlanet)
        
        # >>> 1. Preflyby ellipse (orbit 1)
        
        e_1 = (R_1 - R_2) / (R_1 + R_2 * np.cos(theta_1))
        
        h_1 = np.sqrt(mu_sun * R_1 * (1 - e_1))
        
        V_t_1 = mu_sun / h_1 * (1 + e_1 * np.cos(theta_1))
        
        V_r_1 = mu_sun / h_1 * e_1 * np.sin(theta_1)
        
        gamma_1 = np.arctan(V_r_1 / V_t_1)
        
        V_1_v_m = np.sqrt(V_r_1**2 + V_t_1**2)
        
        # >>> 2. Flyby hyperbola
        
        V_1_v = np.array([V_t_1, -V_r_1])
        
        V_2 = np.array([np.sqrt(mu_sun / R_2), 0])
        
        v_inf_1 = V_1_v - V_2
        
        v_inf_m = np.linalg.norm(v_inf_1)
        
        e = 1 + r_p * v_inf_m**2 / mu_2
        
        h = r_p * np.sqrt(v_inf_m**2 + 2 * mu_2 / r_p)
        
        delta = 2 * np.arcsin(1 / e)
        
        beta = np.arccos(1 / e)
        
        theta_inf = np.arccos(- 1 / e)
        
        Delta = r_p * np.sqrt((e + 1) / (e - 1))
        
        v_p = h / r_p
        
        phi_1 = np.arctan(v_inf_1[1] / v_inf_1[0])
        
        # >>> 3. Approach
        
        phi_2 = phi_1 + delta if side == FlybySide.DARK_SIDE else phi_1 - delta
        
        v_inf_2 = np.array([v_inf_m * np.cos(phi_2), v_inf_m * np.sin(phi_2)])
        
        V_2_v = V_2 + v_inf_2
        
        V_t_2 = V_2_v[0]
        
        V_r_2 = - V_2_v[1]
        
        # >>> 4. Postflyby ellipse (orbit 2)
            
        h_2 = R_2 * V_t_2
        
        e_cos = h_2**2 / (mu_sun * R_2) - 1
        e_sin = V_r_2 * h_2 / mu_sun
        
        theta_2 = np.arctan2(e_sin, e_cos)
        
        e_2 = e_sin / np.sin(theta_2)
        
        R_p_2 = h_2**2 / mu_sun * 1 / (1 + e_2)
        
        # >>> 5. Maneuver
        
        result = ManeuverResult()
        
        result.dv = 0.0
        
        result.dt = 0.0
        
        result.dm = OrbitalManeuvers.propellant_mass(m, result.dv)
        
        result.oe = OrbitalElements(h_2, e_2, 0, 0, 0, 0, 0)
        
        return result
    
    # ! SECTION 8.10
    
    # ! ALGORITHM 8.1
    @classmethod
    def ephemeris(cls, planet : CelestialBody, date : datetime) -> list:
        """Evaluates the ephemeris for a given planet and date

        Args:
            planet (CelestialBody): Planet
            date (datetime): Date-time

        Returns:
            list: [r_GEF, v_GEF]
        """
        
        # >>> 0. Astronomical data
        
        mu_sun = AstronomicalData.gravitational_parameter(CelestialBody.SUN)
        
        # >>> 1. Julian day number
        
        JD = OrbitDetermination.julian_day(date.year, date.month, date.day, date.hour, date.minute, date.second)
        
        # >>> 2. Number of centuries since J2000
        
        T_0 = (JD - 2_451_545) / 36_525
        
        # >>> 3. Orbital elements
        
        oe, doe_dt = AstronomicalData.planetary_orbital_elements_and_rates(planet)
        
        a = (oe['a'] + doe_dt['a'] * T_0) * AstronomicalData.AU
        
        e = oe['e'] + doe_dt['e'] * T_0
        
        i = wrap_to360deg(oe['i'] + doe_dt['i'] * T_0)
        
        Omega = wrap_to360deg(oe['Omega'] + doe_dt['Omega'] * T_0)
        
        bomega = wrap_to360deg(oe['bomega'] + doe_dt['bomega'] * T_0)
        
        L = wrap_to360deg(oe['L'] + doe_dt['L'] * T_0)
        
        T = 2 * np.pi * np.sqrt(a**3 / mu_sun)
        
        # >>> 4. Angular momentum
        
        h = np.sqrt(mu_sun * a * (1 - e**2))
        
        # >>> 5. Argument of Perihelion and Mean Anomaly
        
        omega = bomega - Omega
        
        M = L - bomega
        
        # >>> 6. True anomaly
        
        t = np.deg2rad(M) * T / (2 * np.pi)
        
        theta = Time.calculate_elliptical_orbit(DirectionType.TIME_TO_MEAN_ANOMALY, T=T, e=e, t=t)
        
        # >>> 7. State vector
        
        ThreeDimensionalOrbit.set_celestial_body(CelestialBody.SUN)
        
        return ThreeDimensionalOrbit.pf_2_gef(OrbitalElements(h, e, np.deg2rad(i), np.deg2rad(Omega), np.deg2rad(omega), theta, a))
    
    # ! SECTION 8.11
    
    # ! ALGORITHM 8.2
    @classmethod
    def optimal_transfer(cls,
                        departurePlanet : CelestialBody,
                        arrivalPlanet : CelestialBody,
                        departureDate : datetime,
                        arrivalDate : datetime,
                        r_p_D : float,
                        r_p_A : float,
                        T : float,
                        m : float,
                        gravityAssist : bool = False,
                        side : FlybySide = FlybySide.DARK_SIDE) -> list:
        """Optimal transfer with Lambert

        Args:
            departurePlanet (CelestialBody): Departure planet
            arrivalPlanet (CelestialBody): Arrival planet
            departureDate (datetime): Departure date
            arrivalDate (datetime): Arrival date
            r_p_D (float): Circular Parking Orbit radius
            r_p_A (float): Elliptical Capture Orbit pericenter radius
            T (float): Rendezvous Orbit period
            m (float): Mass of the spacecraft
            gravityAssist (bool, optional): True for enabling gravity assist. Defaults to False.
            side (FlybySide, optional): Side w.r.t. Sun. Defaults to FlybySide.DARK_SIDE.
        
        Returns:
            list: [maneuver_1, maneuver_2, lambert orbital elements, lambert final true anomaly]
        """
        
        # >>> 1. Intial condition
        
        R_1, V_1 = cls.ephemeris(departurePlanet, departureDate)
        R_2, V_2 = cls.ephemeris(arrivalPlanet, arrivalDate)
        
        dt = (arrivalDate - departureDate).total_seconds()
        
        # >>> 2. Lambert problem
        
        OrbitDetermination.set_celestial_body(CelestialBody.SUN)
        
        V_D_v, V_A_v, oe, theta_2 = OrbitDetermination.solve_lambert_problem(R_1, R_2, dt)
        
        # >>> 3. Hyperbolic excess velocities
        
        v_inf_D = V_D_v - V_1
        v_inf_A = V_A_v - V_2
        
        # print(linalg.norm(v_inf_D), linalg.norm(v_inf_A))
        
        # >>> 4. Departure
        
        mu_D = AstronomicalData.gravitational_parameter(departurePlanet)
        
            # >>> a. Hyperbola trajectory
        
        e = 1 + r_p_D * np.linalg.norm(v_inf_D)**2 / mu_D
        
        h = r_p_D * np.sqrt(np.linalg.norm(v_inf_D)**2 + 2 * mu_D / r_p_D)
        
        beta = np.arccos(1 / e)
        
        v_p = h / r_p_D
        
            # >>> b. Circular parking orbit
        
        v_c = np.sqrt(mu_D / r_p_D)
        
            # >>> c. Maneuver
        
        maneuver_1 = ManeuverResult()
        
        maneuver_1.dv = np.abs(v_p - v_c)
        
        maneuver_1.dt = 0.0
        
        maneuver_1.dm = OrbitalManeuvers.propellant_mass(m, maneuver_1.dv)
        
        maneuver_1.oe = OrbitalElements(h, e, 0, 0, 0, 0, 0)
        
        # >>> 5. Arrival
        
        mu_A = AstronomicalData.gravitational_parameter(arrivalPlanet)
        
        maneuver_2 = ManeuverResult()
        
        if not gravityAssist:
        
            # >>> a. Rendezvous orbit from period
        
            a = (T * np.sqrt(mu_A) / (2 * np.pi))**(2/3)
            
            e = 1 - r_p_A / a if r_p_A != 0 else (2 * mu_A) / (a * np.linalg.norm(v_inf_A)**2) - 1
            
            r_p = r_p_A if r_p_A != 0 else 2 * mu_A / np.linalg.norm(v_inf_A)**2 * (1 - e) / (1 + e)
            
            r_a = 2 * a - r_p if r_p_A != 0 else 2 * mu_A / np.linalg.norm(v_inf_A)**2
            
            v_c = np.sqrt(mu_A * (1 + e) / r_p)
        
            # >>> b. Hyperbola trajectory
        
            e_hyp = 1 + r_p * np.linalg.norm(v_inf_A)**2 / mu_A
            
            h_hyp = r_p * np.sqrt(np.linalg.norm(v_inf_A)**2 + 2 * mu_A / r_p)
            
            delta = 2 * np.arcsin(1 / e_hyp)
            
            beta = np.arccos(1 / e_hyp)
            
            Delta = h_hyp**2 / mu_A * 1 / np.sqrt(e_hyp**2 - 1)
            
            v_p = h_hyp / r_p
        
            # >>> c. Maneuver
            
            maneuver_2.dv = np.abs(v_p - v_c)
            
            maneuver_2.dt = 0.0
            
            maneuver_2.dm = OrbitalManeuvers.propellant_mass(m, maneuver_2.dv) # * - maneuver_1.dm
            
            maneuver_2.oe = OrbitalElements(h_hyp, e_hyp, 0, 0, 0, 0, 0)
        
        else:
            
            # >>> a. Directions
            
            u_S = - R_1 / np. linalg.norm(R_1)
            u_V = V_1 / np.linalg.norm(V_1)
            
            print(v_inf_A)
            print(u_S)
            print(u_V)
            
            return
            
            # >>> a. Hyperbola trajectory
            
            e_hyp = 1 + r_p_A * linalg.norm(v_inf_A)**2 / mu_A
            
            h_hyp = r_p_A * np.sqrt(linalg.norm(v_inf_A)**2 + 2 * mu_A / r_p)
            
            delta = 2 * np.arcsin(1 / e_hyp)
            
            beta = np.arccos(1 / e_hyp)
            
            theta_inf = np.arccos(- 1 / e_hyp)
            
            Delta = h_hyp**2 / mu_A * 1 / np.sqrt(e_hyp**2 - 1)
            
            v_p = h_hyp / r_p
            
            phi_1 = np.arctan(v_inf_1[1] / v_inf_1[0])
            
            # >>> 3. Approach
        
            phi_2 = phi_1 + delta if side == FlybySide.DARK_SIDE else phi_1 - delta
        
            v_inf_2 = np.array([v_inf_m * np.cos(phi_2), v_inf_m * np.sin(phi_2)])
            
            V_2_v = V_2 + v_inf_2
            
            V_t_2 = V_2_v[0]
            
            V_r_2 = - V_2_v[1]
            
            # >>> 4. Postflyby ellipse (orbit 2)
                
            h_2 = R_2 * V_t_2
            
            e_cos = h_2**2 / (mu_sun * R_2) - 1
            e_sin = V_r_2 * h_2 / mu_sun
            
            theta_2 = np.arctan2(e_sin, e_cos)
            
            e_2 = e_sin / np.sin(theta_2)
            
            R_p_2 = h_2**2 / mu_sun * 1 / (1 + e_2)
        
            # >>> c. Maneuver
            
            maneuver_2.dv = np.abs(v_p - v_c)
            
            maneuver_2.dt = 0.0
            
            maneuver_2.dm = OrbitalManeuvers.propellant_mass(m, maneuver_2.dv) # * - maneuver_1.dm
            
            maneuver_2.oe = OrbitalElements(h_2, e_2, 0, 0, 0, 0, 0)
        
        return [maneuver_1, maneuver_2, oe, theta_2]

    # ! EXTRA

    @classmethod
    def pork_chop(cls,
                 departurePlanet : CelestialBody,
                 arrivalPlanet : CelestialBody,
                 launchWindow : list,
                 arrivalWindow : list,
                 step: int = 1,
                 show : bool = False) -> None:
        """Evaluates the pork chop of the transfer

        Args:
            departurePlanet (CelestialBody): Departure planet
            arrivalPlanet (CelestialBody): Arrival planet
            launchWindow (list): Launch window
            arrivalWindow (list): Arrival window
            step (int, optional): Step in days for the cost evaluation. Defaults to 1.
            show (bool, optional):  True for plotting the pork chop. Defaults to False.
        """
        
        # >>> 1. Extract dates
        
        lwBeg, lwEnd = launchWindow
        
        awBeg, awEnd = arrivalWindow
        
        # >>> 2. Cycle of time windows
        
        dv_1    = np.zeros(shape=(daterange_length(awBeg, awEnd, step), daterange_length(lwBeg, lwEnd, step)), dtype=float)
        dv_2    = np.zeros(shape=(daterange_length(awBeg, awEnd, step), daterange_length(lwBeg, lwEnd, step)), dtype=float)
        T_F     = np.zeros(shape=(daterange_length(awBeg, awEnd, step), daterange_length(lwBeg, lwEnd, step)), dtype=float)
        X       = np.empty(shape=(daterange_length(awBeg, awEnd, step), daterange_length(lwBeg, lwEnd, step)), dtype='datetime64[s]')
        Y       = np.empty(shape=(daterange_length(awBeg, awEnd, step), daterange_length(lwBeg, lwEnd, step)), dtype='datetime64[s]')

        print_progress_bar(0, daterange_length(lwBeg, lwEnd, step), prefix = 'Progress:', suffix = 'Start', length = 50)
        
        for lwIndex, lwDate in enumerate(daterange(lwBeg, lwEnd, step)):
            
            print_progress_bar(lwIndex, daterange_length(lwBeg, lwEnd, step), prefix = 'Progress:', suffix = 'Processing...', length = 50)
            
            for awIndex, awDate in enumerate(daterange(awBeg, awEnd, step)):
        
                # >>> a. Extract ephemeris
                
                R_1, V_1 = cls.ephemeris(departurePlanet, lwDate)
                R_2, V_2 = cls.ephemeris(arrivalPlanet, awDate)
                
                dt = (awDate - lwDate).total_seconds()
                
                T_F[awIndex, lwIndex] = dt / 3600 / 24
                
                # >>> b. Lambert problem
                
                OrbitDetermination.set_celestial_body(CelestialBody.SUN)
                
                V_D_v, V_A_v, oe, theta_2 = OrbitDetermination.solve_lambert_problem(R_1, R_2, dt)
                
                # >>> c. Hyperbolic excess velocities
                
                dv_1[awIndex, lwIndex] = np.linalg.norm(V_D_v - V_1)
                dv_2[awIndex, lwIndex] = np.linalg.norm(V_A_v - V_2)
                
                # >>> d. Times
                
                X[awIndex, lwIndex] = np.datetime64(lwDate.strftime('%Y-%m-%d'))
                Y[awIndex, lwIndex] = np.datetime64(awDate.strftime('%Y-%m-%d'))
        
        print_progress_bar(daterange_length(lwBeg, lwEnd, step), daterange_length(lwBeg, lwEnd, step), prefix = 'Progress:', suffix = 'Completed', length = 50)
        
        # >>> 3. Show plot
        
        if show:
            
            dv_cond = dv_1.copy()
            
            dv_cond[dv_cond > 12.5] = 0.0
            
            ax = plt.subplot()
            
            contourVelocity = plt.contourf(X, Y, dv_1 + dv_2, cmap='hot')
            
            contourVelocityConstraint = plt.contour(X, Y, dv_cond, cmap='flag')
            
            contourTimeOfFlight = plt.contour(X, Y, T_F, cmap='summer')
            
            ax.clabel(contourVelocityConstraint, inline=1, fontsize=10)
            ax.clabel(contourTimeOfFlight, inline=1, fontsize=10)
            
            cb1 = plt.colorbar(contourVelocity, label='$\Delta V_{TOT}$ $[km / s]$', shrink=0.5)
            cb2 = plt.colorbar(contourVelocityConstraint, label='$\Delta V_1$ $[km / s]$', orientation='vertical', shrink=0.5)
            
            l, b, w, h = ax.get_position().bounds
            ll, bb, ww, hh = cb1.ax.get_position().bounds
            cb1.ax.set_position([ll, b + 0.1*h, 0.1*ww, h*0.8])
            #cb2.ax.set_position([ll, b + 0.1*h, 0.1*ww, h*0.8])
            
            plt.title('Pork Chop')
            plt.xlabel('Launch Window')
            plt.ylabel('Arrival Window')
            
            plt.show()
        
if __name__ == '__main__':
    
    print('EXAMPLE 8.1\n')
    print(InterplanetaryTrajectories.synodic_period(CelestialBody.EARTH, CelestialBody.MARS) / 86400)
    print('-' * 40, '\n')
    
    print('EXAMPLE 8.2\n')
    print(InterplanetaryTrajectories.wait_time(CelestialBody.EARTH, CelestialBody.MARS))
    print('-' * 40, '\n')
    
    print('EXAMPLE 8.3\n')
    print(AstronomicalData.sphere_of_influence(CelestialBody.EARTH) / 6378)
    print(AstronomicalData.sphere_of_influence(CelestialBody.MOON))
    print('-' * 40, '\n')
    
    print('EXAMPLE 8.4\n')
    print(InterplanetaryTrajectories.departure(CelestialBody.EARTH, CelestialBody.MARS, 6378 + 300, 2000))
    print('-' * 40, '\n')
    
    print('EXAMPLE 8.5\n')
    print(InterplanetaryTrajectories.rendezvous(CelestialBody.EARTH, CelestialBody.MARS, 0, 7 * 3600, 2000))
    print('-' * 40, '\n')
    
    print('EXAMPLE 8.6\n')
    print(InterplanetaryTrajectories.flyby(CelestialBody.EARTH, CelestialBody.VENUS, 300 + AstronomicalData.equatiorial_radius(CelestialBody.VENUS), np.deg2rad(-30), 2000))
    print(InterplanetaryTrajectories.flyby(CelestialBody.EARTH, CelestialBody.VENUS, 300 + AstronomicalData.equatiorial_radius(CelestialBody.VENUS), np.deg2rad(-30), 2000, FlybySide.SUNLIT_SIDE))
    print('-' * 40, '\n')
    
    print('EXAMPLE 8.7\n')
    print(InterplanetaryTrajectories.ephemeris(CelestialBody.EARTH, datetime(2003, 8, 27, 12, 0, 0)))
    print(InterplanetaryTrajectories.ephemeris(CelestialBody.MARS, datetime(2003, 8, 27, 12, 0, 0)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 8.8 - 8.9 - 8.10\n')
    print(InterplanetaryTrajectories.optimal_transfer(CelestialBody.EARTH, CelestialBody.MARS, datetime(1996, 11, 7, 0, 0, 0), datetime(1997, 9, 12, 0, 0, 0), 6378 + 180, 3380 + 300, 48 * 3600, 2000))
    print('-' * 40, '\n')
    print(InterplanetaryTrajectories.optimal_transfer(CelestialBody.EARTH, CelestialBody.MARS, datetime(1996, 11, 7, 0, 0, 0), datetime(1997, 9, 12, 0, 0, 0), 6378 + 180, 3380 + 300, 48 * 3600, 2000, gravityAssist=True))
    print('-' * 40, '\n')
    
    print('Progetto')
    print(InterplanetaryTrajectories.optimal_transfer(CelestialBody.EARTH, CelestialBody.NEPTUNE, datetime(2020, 5, 8, 0, 0, 0), datetime(2039, 2, 15, 0, 0, 0), 6378 + 180, AstronomicalData.equatiorial_radius(CelestialBody.NEPTUNE) + 300, 48 * 3600, 2000))
    print(InterplanetaryTrajectories.departure(CelestialBody.EARTH, CelestialBody.NEPTUNE, 6378 + 180, 2000))
    print(InterplanetaryTrajectories.rendezvous(CelestialBody.EARTH, CelestialBody.NEPTUNE, AstronomicalData.equatiorial_radius(CelestialBody.NEPTUNE) + 300, 48 * 3600, 2000))
    print('-' * 40, '\n')
    
    print('Pork Chop Plot')
    InterplanetaryTrajectories.pork_chop(CelestialBody.EARTH,
                                        CelestialBody.NEPTUNE,
                                        [datetime(2020, 1, 1, 0, 0, 0), datetime(2021, 1, 1, 0, 0, 0)],
                                        [datetime(2031, 1, 1, 0, 0, 0), datetime(2050, 6, 1, 0, 0, 0)],
                                        step=3,
                                        show=True)
    print('-' * 40, '\n')