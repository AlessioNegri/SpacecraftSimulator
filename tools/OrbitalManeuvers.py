import os
import sys

sys.path.append(os.path.dirname(__file__))

from stdafx import *
from TwoBodyProblem import *
from Time import *
from OrbitDetermination import *
from LagrangeCoefficients import *

class HohmannDirection(IntEnum):
    PER2APO = 0
    APO2PER = 1
    PER2PER = 2
    APO2APO = 3
    
@dataclass
class MANEUVER_RESULT:
    
    dv : float              = 0.0 # ? Delta Velocity [km / s]
    dt : float              = 0.0 # ? Delta Time [s]
    dm : float              = 0.0 # ? Delta Mass [kg]
    oe : ORBITAL_ELEMENTS   = field(default_factory=lambda : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

# ! CHAPTER 6 - Orbital Maneuvers
class OrbitalManeuvers():
    
    mu = AstronomicalData.GravitationalParameter(CelestialBody.EARTH)
    
    g_0 = AstronomicalData.Gravity(CelestialBody.EARTH, km=True)
    
    I_sp = 300.0
    
    def __init__(self) -> None: pass
    
    @classmethod
    def setCelestialBody(cls, celestialBody : CelestialBody) -> None:
        """Sets the current celectial body

        Args:
            celestialBody (CelestialBody): Celestial body
        """
        
        cls.mu = AstronomicalData.GravitationalParameter(celestialBody)
        
        cls.g_0 = AstronomicalData.Gravity(celestialBody, km=True)
        
    @classmethod
    def setSpecificImpulse(cls, I_sp : float) -> None:
        """Sets the spacecraft motor specific impulse

        Args:
            I_sp (float): Specific Impulse
        """
        
        cls.I_sp = I_sp
    
    # ! SECTION 6.2
    
    @classmethod
    def propellantMass(cls, m : float, dv : float) -> float:
        """Ideal rocket equation mass calculation

        Args:
            m (float): Initial mass
            dv (float): Delta velocity

        Returns:
            float: Propellant mass
        """
        
        return m * (1 - np.exp(-dv / (cls.I_sp * cls.g_0)))
    
    # ! SECTION 6.3
    
    @classmethod
    def HohmannTransfer(cls, r_p_1 : float, r_a_1 : float, r_p_2 : float, r_a_2 : float, direction : HohmannDirection = HohmannDirection.PER2APO, m : float = 0.0) -> MANEUVER_RESULT:
        """Hohmann transfer maneuver

        Args:
            r_p_1 (float): Pericenter of orbit 1
            r_a_1 (float): Apocenter of orbit 1
            r_p_2 (float): Pericenter of orbit 2
            r_a_2 (float): Apocenter of orbit 2
            direction (HOHMANN_DIRECTION, optional): Direction of the transfer. Defaults to HOHMANN_DIRECTION.PER2APO.
            m (float, optional): Initial mass of the spacecraft. Defaults to 0.0.

        Returns:
            MANEUVER_RESULT: [dv, dt, dm, orbital elements]
        """
        
        result = MANEUVER_RESULT()
        
        # * 1. Orbit 1
        
        h_1 = np.sqrt(2 * cls.mu) * np.sqrt(r_a_1 * r_p_1 / (r_a_1 + r_p_1))
        
        v_p_1 = h_1 / r_p_1
        
        v_a_1 = h_1 / r_a_1
        
        # * 2. Orbit 2
        
        h_2 = np.sqrt(2 * cls.mu) * np.sqrt(r_a_2 * r_p_2 / (r_a_2 + r_p_2))
        
        v_p_2 = h_2 / r_p_2
        
        v_a_2 = h_2 / r_a_2
        
        # * 3. Transfer Orbit
        
        a_T = e_T = h_T = v_p_T = v_a_T = 0.0
        
        if direction == HohmannDirection.PER2APO:
            
            a_T = 0.5 * (r_p_1 + r_a_2)
            
            e_T = (r_a_2 - r_p_1) / (r_a_2 + r_p_1)
        
            h_T = np.sqrt(2 * cls.mu) * np.sqrt(r_a_2 * r_p_1 / (r_a_2 + r_p_1))
            
            v_p_T = h_T / r_p_1
            
            v_a_T = h_T / r_a_2
            
        elif direction == HohmannDirection.APO2PER:
            
            a_T = 0.5 * (r_p_2 + r_a_1)
            
            e_T = (r_a_1 - r_p_2) / (r_a_1 + r_p_2)
        
            h_T = np.sqrt(2 * cls.mu) * np.sqrt(r_a_1 * r_p_2 / (r_a_1 + r_p_2))
            
            v_p_T = h_T / r_p_2
            
            v_a_T = h_T / r_a_1
            
        elif direction == HohmannDirection.PER2PER:
            
            pass
        
        elif direction == HohmannDirection.APO2APO:
            
            pass
        
        T_T = 2 * np.pi / float(np.sqrt(cls.mu)) * a_T**(3/2)
        
        # * 4.
        
        dv_1 = dv_2 = 0.0
        
        if direction == HohmannDirection.PER2APO:
            
            dv_1 = abs(v_p_T - v_p_1)
            
            dv_2 = abs(v_a_2 - v_a_T)
        
        elif direction == HohmannDirection.APO2PER:
            
            dv_1 = abs(v_a_T - v_a_1)
            
            dv_2 = abs(v_p_2 - v_p_T)
            
        elif direction == HohmannDirection.PER2PER:
            
            pass
        
        elif direction == HohmannDirection.APO2APO:
            
            pass
        
        result.dv = dv_1 + dv_2
        
        # * 5.
        
        result.dt = 0.5 * T_T
        
        # * 6.
        
        dm_1 = cls.propellantMass(m, dv_1)
        
        dm_2 = cls.propellantMass(m - dm_1, dv_2)
        
        result.dm = dm_1 + dm_2
        
        # * 7.
        
        result.oe = ORBITAL_ELEMENTS(h_T, e_T, 0, 0, 0, 0, a_T)
        
        return result
    
    # ! SECTION 6.4
    
    @classmethod
    def BiEllipticHohmannTransfer(cls, r_p_1 : float, r_a_1 : float, r_p_2 : float, r_a_2 : float, r_3 : float, direction : HohmannDirection = HohmannDirection.PER2APO, m : float = 0.0) -> list:
        """Bi-Elliptic Hohmann transfer maneuver

        Args:
            r_p_1 (float): Pericenter of orbit 1
            r_a_1 (float): Apocenter of orbit 1
            r_p_2 (float): Pericenter of orbit 2
            r_a_2 (float): Apocenter of orbit 2
            r_3 (float): Apocenter of orbit 3
            direction (HOHMANN_DIRECTION, optional): Direction of the transfer. Defaults to HOHMANN_DIRECTION.PER2APO.
            m (float, optional): Initial mass of the spacecraft. Defaults to 0.0.

        Returns:
            list: [[dv, dt, dm, orbital elements]_1, [dv, dt, dm, orbital elements]_2]
        """
        
        result = MANEUVER_RESULT()
        
        if direction == HohmannDirection.PER2APO:
            
            hohmann_1 = cls.HohmannTransfer(r_p_1, r_a_1, r_p_1, r_3, HohmannDirection.PER2APO, m)
            
            hohmann_2 = cls.HohmannTransfer(r_p_1, r_3, r_p_2, r_a_2, HohmannDirection.APO2PER, m - hohmann_1.dm)
        
        elif direction == HohmannDirection.APO2PER:
            
            pass
            
        elif direction == HohmannDirection.PER2PER:
            
            pass
        
        elif direction == HohmannDirection.APO2APO:
            
            pass
        
        return [hohmann_1, hohmann_2]
    
    # ! SECTION 6.5
    
    @classmethod
    def PhasingManeuver(cls, r_p_1 : float, r_a_1 : float, theta_B : float, n : float = 1, m : float = 0.0) -> MANEUVER_RESULT:
        """Phasing maneuver

        Args:
            r_p_1 (float): Pericenter of orbit 1
            r_a_1 (float): Apocenter of orbit 
            theta_B (float): True anomaly of target B
            n (float, optional): Number of revolutions on phasing orbit. Defaults to 1.
            m (float, optional): Initial mass of the spacecraft. Defaults to 0.0.

        Returns:
            MANEUVER_RESULT: [dv, dt, dm]
        """
        
        result = MANEUVER_RESULT()
        
        # * 1. Orbit 1 parameters
        
        a_1 = 0.5 * (r_p_1 + r_a_1)
        
        e_1 = (r_a_1 - r_p_1) / (r_a_1 + r_p_1)
        
        h_1 = np.sqrt(2 * cls.mu) * np.sqrt(r_a_1 * r_p_1 / (r_a_1 + r_p_1))
        
        T_1 = 2 * np.pi / float(np.sqrt(cls.mu)) * a_1**(3/2)
        
        v_1 = h_1 / r_p_1
        
        # * 2. Time from A (pericenter - chaser) to B (target)
        
        Time.mu = cls.mu
        
        t_AB = Time.calculateEllipticalOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=T_1, e=e_1, theta=theta_B)
        
        # * 3. Orbit 2
        
        T_2 = T_1 - t_AB / n
        
        a_2 = (float(np.sqrt(cls.mu)) * T_2 / (2 * np.pi))**(2/3)
        
        r_A = r_p_1
        
        r_D = 2 * a_2 - r_A
        
        h_2 = np.sqrt(2 * cls.mu) * np.sqrt(r_A * r_D / (r_A + r_D))
        
        v_A = h_2 / r_A
        
        # * 4.
        
        dv_1 = np.abs(v_A - v_1)
        
        dv_2 = np.abs(v_1 - v_A)
        
        result.dv = dv_1 + dv_2
        
        # * 5.
        
        result.dt = n * T_2
        
        # * 6.
        
        dm_1 = cls.propellantMass(m, dv_1)
        
        dm_2 = cls.propellantMass(m - dm_1, dv_2)
        
        result.dm = dm_1 + dm_2
        
        # * Return
        
        return result

    # ! SECTION 6.6

    @classmethod
    def NonHohmannTransfer(cls, r_p_1 : float, r_a_1 : float, theta_1 : float, r_2 : float, theta_2 : float, m : float = 0.0) -> MANEUVER_RESULT:
        """Non-Hohmann transfer between coaxial elliptical orbits

        Args:
            r_p_1 (float): Pericenter of orbit 1
            r_a_1 (float): Apocenter of orbit 1
            theta_1 (float): True anomaly of orbit 1 for maneuver
            r_2 (float): Target radius
            theta_2 (float): Target true anomaly
            m (float, optional): Initial mass of the spacecraft. Defaults to 0.0.

        Returns:
            MANEUVER_RESULT: [dv, dt, dm]
        """
        
        result = MANEUVER_RESULT()
        
        # * 1. Orbit 1
        
        a_1 = 0.5 * (r_p_1 + r_a_1)
        
        e_1 = (r_a_1 - r_p_1) / (r_a_1 + r_p_1)
        
        h_1 = np.sqrt(2 * cls.mu) * np.sqrt(r_a_1 * r_p_1 / (r_a_1 + r_p_1))
        
        r_1 = h_1**2 / cls.mu * 1 / (1 + e_1 * np.cos(theta_1))
        
        v_t_1 = h_1 / r_1
        
        v_r_1 = cls.mu / h_1 * e_1 * np.sin(theta_1)
        
        v_1 = np.sqrt(v_r_1**2 + v_t_1**2)
        
        gamma_1 = np.arctan(v_r_1 / v_t_1)
        
        # * 2. Orbit 2
        
        e_2 = - (r_2 - r_1) / (r_2 * np.cos(theta_2) - r_1 * np.cos(theta_1))
        
        h_2 = np.sqrt(cls.mu * r_1 * r_2) * np.sqrt((np.cos(theta_2) - np.cos(theta_1)) / (r_2 * np.cos(theta_2) - r_1 * np.cos(theta_1)))
        
        v_t_2 = h_2 / r_1
        
        v_r_2 = cls.mu / h_2 * e_2 * np.sin(theta_1)
        
        v_2 = np.sqrt(v_r_2**2 + v_t_2**2)
        
        gamma_2 = np.arctan(v_r_2 / v_t_2)
        
        r_p_2 = h_2**2 / cls.mu * 1 / (1 + e_2)
        
        r_a_2 = h_2**2 / cls.mu * 1 / (1 - e_2)
        
        a_2 = 0.5 * (r_p_2 + r_a_2)
        
        T_2 = 2 * np.pi / float(np.sqrt(cls.mu)) * a_2**(3/2)
        
        # * 3.
        
        dgamma = gamma_2 - gamma_1
        
        result.dv = np.sqrt(v_1**2 + v_2**2 - 2 * v_1 * v_2 * np.cos(dgamma))
        
        phi = np.arctan((v_r_2 - v_r_1) / (v_t_2 - v_t_1))
        
        # * 4.
        
        Time.mu = cls.mu
        
        t_1 = Time.calculateEllipticalOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=T_2, e=e_2, theta=theta_1)
        
        result.dt = T_2 - t_1
        
        # * 5.
        
        result.dm = cls.propellantMass(m, result.dv)
        
        return result
    
    # ! SECTION 6.7
    
    @classmethod
    def ApseLineRotationFromEta(cls, r_p_1 : float, r_a_1 : float, r_p_2 : float, r_a_2 : float, eta : float, secondIntersectionPoint : bool = False, m : float = 0.0) -> MANEUVER_RESULT:
        """Apse line rotation from angle variation eta

        Args:
            r_p_1 (float): Pericenter of orbit 1
            r_a_1 (float): Apocenter of orbit 1
            r_p_2 (float): Pericenter of orbit 2
            r_a_2 (float): Apocenter of orbit 2
            eta (float): Apse line angle rotation
            secondIntersectionPoint (bool, optional): True for using the second intersection point. Defaults to False.
            m (float, optional): Initial mass of the spacecraft. Defaults to 0.0.

        Returns:
            MANEUVER_RESULT: [dv, dt, dm]
        """
        
        result = MANEUVER_RESULT()
        
        # * 1. Orbit parameters
        
        e_1 = (r_a_1 - r_p_1) / (r_a_1 + r_p_1)
        
        e_2 = (r_a_2 - r_p_2) / (r_a_2 + r_p_2)
        
        h_1 = np.sqrt(2 * cls.mu) * np.sqrt(r_a_1 * r_p_1 / (r_a_1 + r_p_1))
        
        h_2 = np.sqrt(2 * cls.mu) * np.sqrt(r_a_2 * r_p_2 / (r_a_2 + r_p_2))
        
        # * 2. Equation
        
        a = e_1 * h_2**2 - e_2 * h_1**2 * np.cos(eta)
        
        b = - e_2 * h_1**2 * np.sin(eta)
        
        c = h_1**2 - h_2**2
        
        phi = np.arctan(b / a)
        
        theta = phi + np.arccos(c / a * np.cos(phi)) if not secondIntersectionPoint else phi - np.arccos(c / a * np.cos(phi))
        
        # * 3. Orbit 1
        
        r = h_1**2 / cls.mu * 1 / (1 + e_1 * np.cos(theta))
        
        v_t_1 = h_1 / r
        
        v_r_1 = cls.mu / h_1 * e_1 * np.sin(theta)
        
        v_1 = np.sqrt(v_r_1**2 + v_t_1**2)
        
        gamma_1 = np.arctan(v_r_1 / v_t_1)
        
        # * 4. Orbit 2
        
        v_t_2 = h_2 / r
        
        v_r_2 = cls.mu / h_2 * e_2 * np.sin(theta - eta)
        
        v_2 = np.sqrt(v_r_2**2 + v_t_2**2)
        
        gamma_2 = np.arctan(v_r_2 / v_t_2)
        
        # * 5.
        
        dgamma = gamma_2 - gamma_1
        
        result.dv = np.sqrt(v_1**2 + v_2**2 - 2 * v_1 * v_2 * np.cos(dgamma))
        
        if np.abs(v_t_2 - v_t_1) < 1e-6:
            
            phi = np.pi if v_r_2 - v_r_1 > 0 else -np.pi
            
        else:
            
            phi = np.arctan((v_r_2 - v_r_1) / (v_t_2 - v_t_1))
        
        # * 6.
        
        result.dt = 0.0
        
        # * 7.
        
        result.dm = cls.propellantMass(m, result.dv)
        
        # * 8.
        
        result.oe = ORBITAL_ELEMENTS(0, 0, 0, 0, 0, theta, 0)
        
        # * Return
        
        return result
    
    @classmethod
    def ApseLineRotationFromTrueAnomaly(cls, r_p_1 : float, r_a_1 : float, theta_1 : float, dv : float, phi : float, m : float = 0.0) -> list:
        """Apse line rotation from true anomaly

        Args:
            r_p_1 (float): Pericenter of orbit 1
            r_a_1 (float): Apocenter of orbit 1
            theta_1 (float): True anomaly of orbit 1
            dv (float): Delta v
            phi (float): Flight path angle of delta v
            m (float, optional): Initial mass of the spacecraft. Defaults to 0.0.

        Returns:
            list: [r_p_2, r_a_2, eta, dt, dm]
        """
        
        # * 1. Orbit 1
        
        e_1 = (r_a_1 - r_p_1) / (r_a_1 + r_p_1)
        
        h_1 = np.sqrt(2 * cls.mu) * np.sqrt(r_a_1 * r_p_1 / (r_a_1 + r_p_1))
        
        r_1 = h_1**2 / cls.mu * 1 / (1 + e_1 * np.cos(theta_1))
        
        v_t_1 = h_1 / r_1
        
        v_r_1 = cls.mu / h_1 * e_1 * np.sin(theta_1)
        
        # * 2. Delta v
        
        dv_t = dv * np.cos(phi)
        
        dv_r = dv * np.sin(phi)
        
        # * 3. Orbit 2
        
        h_2 = h_1 + r_1 * dv_t
        
        num = (v_t_1 + dv_t) * (v_r_1 + dv_r) * v_t_1**2 * 1 / (cls.mu / r_1)
        
        den = (v_t_1 + dv_t)**2 * e_1 * np.cos(theta_1) + (2 * v_t_1 + dv_t) * dv_t
        
        theta_2 = np.arctan(num / den)
        
        eta = theta_1 - theta_2
        
        e_2 = ((h_1 + r_1 * dv_t)**2 * e_1 * np.cos(theta_1) + (2 * h_1 + r_1 * dv_t) * r_p_1 * dv_t) / (h_1**2 * np.cos(theta_2))
        
        r_p_2 = h_2**2 / cls.mu * 1 / (1 + e_2)
        
        r_a_2 = h_2**2 / cls.mu * 1 / (1 - e_2)
        
        # * 4.
        
        dt = 0.0
        
        # * 5.
        
        dm = cls.propellantMass(m, dv)
        
        return [r_p_2, r_a_2, eta, dt, dm]
    
    # ! SECTION 6.8
    
    @classmethod
    def ChaseManeuver(cls, r_p : float, r_a : float, theta_C : float, theta_T : float, dt : float, m : float = 0.0) -> list:
        """Chase maneuver from Chaser C to Target T

        Args:
            r_p (float): Pericenter of orbit
            r_a (float): Apocenter of orbit
            theta_C (float): True anomaly of Chaser
            theta_T (float): True anomaly of Target
            dt (float): Delta time
            m (float, optional): Initial mass of the spacecraft. Defaults to 0.0.

        Returns:
            list: [dv, dt, dm, orbital elements of transfer orbit, true anomaly of Target on transfer orbit]
        """
        
        result = MANEUVER_RESULT()
        
        # * 1. Parameters
        
        e = (r_a - r_p) / (r_a + r_p)
        
        h = np.sqrt(2 * cls.mu) * np.sqrt(r_a * r_p / (r_a + r_p))
        
        T = 2 * np.pi / cls.mu**2 * (h / np.sqrt(1 - e**2))**3
        
        # * 2. Perifocal Frame state vector
        
        r_C = h**2 / cls.mu * 1 / (1 + e * np.cos(theta_C)) * np.array([np.cos(theta_C), np.sin(theta_C), 0])
        
        v_C = cls.mu / h * np.array([-np.sin(theta_C), (e + np.cos(theta_C)), 0])
        
        # * 3. New Perifocal Frame state vector
        
        Time.mu = cls.mu
        
        t_T = Time.calculateEllipticalOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=T, e=e, theta=theta_T)
        
        t_T_new = t_T + dt
        
        theta_T_new = Time.calculateEllipticalOrbit(DirectionType.TIME_TO_MEAN_ANOMALY, T=T, e=e, t=t_T_new)
        
        r_T = h**2 / cls.mu * 1 / (1 + e * np.cos(theta_T_new)) * np.array([np.cos(theta_T_new), np.sin(theta_T_new), 0])
        
        v_T = cls.mu / h * np.array([-np.sin(theta_T_new), (e + np.cos(theta_T_new)), 0])
        
        # * 4. Lambert
        
        OrbitDetermination.mu = cls.mu
        
        v_t_C, v_t_T, oe, theta_t_2 = OrbitDetermination.solveLambertProblem(r_C, r_T, dt)
        
        # * 5.
        
        dv_1 = linalg.norm(v_t_C - v_C)
        
        dv_2 = linalg.norm(v_T - v_t_T)
        
        result.dv = dv_1 + dv_2
        
        # * 6.
        
        result.dt = dt
        
        # * 7.
        
        dm_1 = cls.propellantMass(m, dv_1)
        
        dm_2 = cls.propellantMass(m - dm_1, dv_2)
        
        result.dm = dm_1 + dm_2
        
        return [result, oe, theta_t_2]
    
    # ! SECTION 6.9
    
    @classmethod
    def PlaneChangeManeuver(cls, r_p_1 : float, r_a_1 : float, theta_1 : float, r_p_2 : float, r_a_2 : float, theta_2 : float, delta : float, m : float = 0.0) -> MANEUVER_RESULT:
        """Plane change maneuver

        Args:
            r_p_1 (float): Pericenter of orbit 1
            r_a_1 (float): Apocenter of orbit 1
            theta_1 (float): True anomaly of orbit 1
            r_p_2 (float): Pericenter of orbit 2
            r_a_2 (float): Apocenter of orbit 2
            theta_2 (float): True anomaly of orbit 2
            delta (float): Dihedral angle
            m (float, optional): Initial mass of the spacecraft. Defaults to 0.0.

        Returns:
            MANEUVER_RESULT: [dv, dt, dm]
        """
        
        result = MANEUVER_RESULT()
        
        # * 1. Orbit 1
        
        e_1 = (r_a_1 - r_p_1) / (r_a_1 + r_p_1)
        
        h_1 = np.sqrt(2 * cls.mu) * np.sqrt(r_a_1 * r_p_1 / (r_a_1 + r_p_1))
        
        r_1 = h_1**2 / cls.mu * 1 / (1 + e_1 * np.cos(theta_1))
        
        v_t_1 = h_1 / r_1
        
        v_r_1 = cls.mu / h_1 * e_1 * np.sin(theta_1)
        
        # * 2. Orbit 2
        
        e_2 = (r_a_2 - r_p_2) / (r_a_2 + r_p_2)
        
        h_2 = np.sqrt(2 * cls.mu) * np.sqrt(r_a_2 * r_p_2 / (r_a_2 + r_p_2))
        
        r_2 = h_2**2 / cls.mu * 1 / (1 + e_2 * np.cos(theta_2))
        
        v_t_2 = h_2 / r_2
        
        v_r_2 = cls.mu / h_2 * e_2 * np.sin(theta_2)
        
        # * 3.
        
        result.dv = np.sqrt((v_r_2 - v_r_1)**2 + v_t_1**2 + v_t_2**2 - 2 * v_t_1 * v_t_2 * np.cos(delta))
        
        # * 4.
        
        result.dt = 0.0
        
        # * 5.
        
        result.dm = cls.propellantMass(m, result.dv)
        
        # * Return
        
        return result
    
    @classmethod
    def PlaneChangeManeuver2(cls, r_p_1 : float, r_a_1 : float, Omega_1 : float, omega_1 : float, i_1 : float, Omega_2 : float, i_2 : float, m : float = 0.0) -> MANEUVER_RESULT:
        """Plane change maneuver with angles

        Args:
            r_p_1 (float): Pericenter of orbit 1
            r_a_1 (float): Apocenter of orbit 1
            Omega_1 (float): Right Ascension of the Ascending Node of orbit 1
            omega_1 (float): Anomaly of the Perigee of orbit 1
            i_1 (float): Inclination of orbit 1
            Omega_2 (float): Right Ascension of the Ascending Node of orbit 2
            i_2 (float): Inclination of orbit 2
            m (float, optional): Initial mass of the spacecraft. Defaults to 0.0.

        Returns:
            MANEUVER_RESULT: [dv, dt, dm, orbital elements]
        """
        
        result = MANEUVER_RESULT()
        
        # * 1. Differences
        
        dOmega = Omega_2 - Omega_1
        
        di = i_2 - i_1
        
        # * 2. Plane Change
        
        if dOmega * di > 0:
            
            delta = np.arccos(np.cos(i_1) * np.cos(i_2) + np.sin(i_1) * np.sin(i_2) * np.cos(dOmega))
            
            cos_u_1 = (-np.cos(i_2) + np.cos(delta) * np.cos(i_1)) / (np.sin(delta) * np.sin(i_1))
            cos_u_2 = (+np.cos(i_1) - np.cos(delta) * np.cos(i_2)) / (np.sin(delta) * np.sin(i_2))
            sin_u_1 = np.sin(dOmega) * np.sin(i_2) / np.sin(delta)
            sin_u_2 = np.sin(dOmega) * np.sin(i_1) / np.sin(delta)
            
            u_1 = np.arctan2(sin_u_1, cos_u_1)
            u_2 = np.arctan2(sin_u_2, cos_u_2)
            
            theta_1 = u_1 - omega_1
            
            omega_2 = theta_1 + u_2
        
        else:
            
            delta = np.arccos(np.cos(i_1) * np.cos(i_2) + np.sin(i_1) * np.sin(i_2) * np.cos(dOmega))
            
            cos_u_1 = (+np.cos(i_2) - np.cos(delta) * np.cos(i_1)) / (np.sin(delta) * np.sin(i_1))
            cos_u_2 = (-np.cos(i_1) + np.cos(delta) * np.cos(i_2)) / (np.sin(delta) * np.sin(i_2))
            sin_u_1 = np.sin(dOmega) * np.sin(i_2) / np.sin(delta)
            sin_u_2 = np.sin(dOmega) * np.sin(i_1) / np.sin(delta)
            
            u_1 = np.arctan2(sin_u_1, cos_u_1)
            u_2 = np.arctan2(sin_u_2, cos_u_2)
            
            theta_1 = 2 * np.pi - u_1 - omega_1
            
            omega_2 = 2 * np.pi - u_2 - theta_1
        
        # * 3.
        
        e_1 = (r_a_1 - r_p_1) / (r_a_1 + r_p_1)
        
        h_1 = np.sqrt(2 * cls.mu) * np.sqrt(r_a_1 * r_p_1 / (r_a_1 + r_p_1))
        
        r_1 = h_1**2 / cls.mu * 1 / (1 + e_1 * np.cos(theta_1))
        
        v_t_1 = h_1 / r_1
        
        result.dv = 2 * v_t_1 * np.sin(delta / 2)
        
        # * 4.
        
        result.dt = 0.0
        
        # * 5.
        
        result.dm = cls.propellantMass(m, result.dv)
        
        # * 6.
        
        result.oe = ORBITAL_ELEMENTS(0, 0, i_2, Omega_2, omega_2, theta_1, 0)
        
        # * Return
        
        return result
    
    # ! SECTION 6.10
    
    @classmethod
    def ConstantTangentialThrustTransferFromTime(cls, r_0 : float, m_0 : float, T : float, I_sp : float, t : float) -> list:
        """Constant tangential thrust transfer from burning time

        Args:
            r_0 (float): Initial radius
            m_0 (float): Initial mass
            T (float): Thrust
            I_sp (float): Specific impulse
            t (float): Time of flight

        Returns:
            list: [final radius, propellant mass]
        """
        
        T = T * 1e-3
        
        # * 1. Target radius
        
        r = cls.mu / (np.sqrt(cls.mu / r_0) + I_sp * cls.g_0 * np.log(1 - T * t / (m_0 * cls.g_0 * I_sp)))**2
        
        # * 2. Propellant mass
        
        m_p = T / (I_sp * cls.g_0) * t
        
        return [r, m_p]
    
    @classmethod
    def ConstantTangentialThrustTransferFromRadius(cls, r_0 : float, m_0 : float, T : float, I_sp : float, r : float) -> list:
        """Constant tangential thrust transfer from final radius

        Args:
            r_0 (float): Initial radius
            m_0 (float): Initial mass
            T (float): Thrust
            I_sp (float): Specific impulse
            r (float): Final radius

        Returns:
            list: [time of flight, propellant mass]
        """
        
        T = T * 1e-3
        
        # * 1. Flight time
        
        t = m_0 * cls.g_0 * I_sp / T * (1 - np.exp(1 / (I_sp * cls.g_0) * (np.sqrt(cls.mu / r) - np.sqrt(cls.mu / r_0))))
        
        # * 2. Propellant mass
        
        m_p = T / (I_sp * cls.g_0) * t
        
        return [t, m_p]
    
    @classmethod
    def NonImpulsiveManeuver(cls, t_0 : float, dt : float, r_0 : np.ndarray, v_0 : np.ndarray, r_f : np.ndarray, m_0 : float, T : float, I_sp : float, semiMajorAxis : bool = False, tol : float = 1e-8) -> list:
        """Non impulsive maneuver

        Args:
            t_0 (float): Initial burning time guess
            dt (float): Time step for burning time calculation
            r_0 (np.ndarray): Initial position vector
            v_0 (np.ndarray): Initial velocity vector
            r_f (np.ndarray): Final position vector
            m_0 (float): Initial mass
            T (float): Thrust
            I_sp (float): Specific impulse
            semiMajorAxis (bool, optional): True for semi-major axis target - False for position vector norm target. Defaults to False.
            tol (float, optional): Tolerance. Defaults to 1e-8.

        Returns:
            list: [burning time, final state vector]
        """
        
        t_burn = t_0 + 10
        
        TwoBodyProblem.mu = cls.mu
        
        ThreeDimensionalOrbit.mu = cls.mu
        
        LagrangeCoefficients()
        
        r = np.zeros(shape=(3))
        v = np.zeros(shape=(3))
        
        prevEpsilon = 0.0
        
        while True:
            
            # * 1. Integrate
            
            result = TwoBodyProblem.integrateRelativeMotionThrust(np.hstack([r_0, v_0, np.array([m_0])]), T, I_sp, 0, t_burn)
            
            Y = result['y']
            
            r = np.array([Y[0,-1], Y[1,-1], Y[2,-1]])
            v = np.array([Y[3,-1], Y[4,-1], Y[5,-1]])
            m = Y[6,-1]
            
            # * 2. Calculate orbital elements
            
            oe = ThreeDimensionalOrbit.calculateOrbitalElements(r, v)
            
            # * 3. Update state vector
            
            if semiMajorAxis:
                
                epsilon = oe.a - linalg.norm(r_f)
                
                y = Y[:,-1]
                
            else:
            
                dtheta = np.pi - oe.theta
            
                L_r_f, L_v_f = LagrangeCoefficients.calculatePositionVelocityByAngle(r, v, dtheta)
            
                epsilon = linalg.norm(L_r_f) - linalg.norm(r_f)
                
                y = np.hstack([L_r_f, L_v_f, np.array([m])])
            
            # * 4. Check error
            
            if np.abs(epsilon) < tol: break
            
            # * 5. Update time interval
            
            if prevEpsilon != 0.0 and prevEpsilon * epsilon < 0:
                
                dt = dt / 2.0
            
            if epsilon < 0:
                
                t_burn += dt
                
            else:
                
                t_burn -= dt
                
            # * 6. Update error
            
            prevEpsilon = epsilon
        
        return [t_burn, y]

if __name__ == '__main__':
    
    print('EXAMPLE 6.1\n')
    print(OrbitalManeuvers.HohmannTransfer(480 + 6378, 800 + 6378, 16000 + 6378, 16000 + 6378, HohmannDirection.PER2APO, 2000))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.2\n')
    parameters = TwoBodyProblem.calculateOrbitalParameters(np.array([-(5000 + 6378), 0, 0]), np.array([0, -10, 0]))
    print(OrbitalManeuvers.HohmannTransfer(parameters.r_p, parameters.r_a, 500 + 6378, 500 + 6378, HohmannDirection.PER2APO, 2000))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.3\n')
    print(OrbitalManeuvers.HohmannTransfer(7000, 7000, 105000, 105000, HohmannDirection.PER2APO, 2000))
    print(OrbitalManeuvers.BiEllipticHohmannTransfer(7000, 7000, 105000, 105000, 210000, HohmannDirection.PER2APO, 2000))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.4\n')
    print(OrbitalManeuvers.PhasingManeuver(6800, 13600, np.deg2rad(90)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.5\n')
    print(OrbitalManeuvers.PhasingManeuver(42164, 42164, np.deg2rad(-12), 3))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.6\n')
    print(OrbitalManeuvers.NonHohmannTransfer(10000, 20000, np.deg2rad(150), 6378, np.deg2rad(0)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.7\n')
    print(OrbitalManeuvers.ApseLineRotationFromEta(8000, 16000, 7000, 21000, np.deg2rad(25)))
    print(OrbitalManeuvers.ApseLineRotationFromEta(8000, 16000, 8000, 16000, np.deg2rad(25)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.8\n')
    print(OrbitalManeuvers.ApseLineRotationFromTrueAnomaly(7000, 17000, np.deg2rad(0), 2, np.deg2rad(60)))
    print(OrbitalManeuvers.ApseLineRotationFromTrueAnomaly(8000, 16000, np.deg2rad(12.5), 0.8820638380136657, np.deg2rad(-90)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.9\n')
    print(OrbitalManeuvers.ChaseManeuver(8100, 18900, np.deg2rad(45), np.deg2rad(150), 3600))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.11\n')
    print(OrbitalManeuvers.PlaneChangeManeuver(6678, 42164, np.deg2rad(180), 42164, 42164, np.deg2rad(0), np.deg2rad(28)))
    print(OrbitalManeuvers.PlaneChangeManeuver(6678, 6678, np.deg2rad(180), 6678, 42164, np.deg2rad(0), np.deg2rad(28)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.13\n')
    print(OrbitalManeuvers.PlaneChangeManeuver(500 + 6378, 10000 + 6378, np.deg2rad(120), 500 + 6378, 10000 + 6378, np.deg2rad(120), np.deg2rad(15)))
    print(OrbitalManeuvers.PlaneChangeManeuver(500 + 6378, 10000 + 6378, np.deg2rad(300), 500 + 6378, 10000 + 6378, np.deg2rad(300), np.deg2rad(15)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.15\n')
    t_burn, y = OrbitalManeuvers.NonImpulsiveManeuver(0, 10, np.array([480 + 6378, 0, 0]), np.array([0, 7.7102, 0]), np.array([-(16000 + 6378), 0, 0]), 2000, 10e3, 300)
    print(t_burn)
    print(y)
    print(OrbitalManeuvers.NonImpulsiveManeuver(0, 10, y[:3], y[3:6], np.array([-(16000 + 6378), 0, 0]), y[-1], 10e3, 300, True))
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.16\n')
    t, m_p = OrbitalManeuvers.ConstantTangentialThrustTransferFromRadius(6678, 1000, 0.0025e3, 10000, 42164)
    print(t, m_p)
    print('-' * 40, '\n')
    
    print('EXAMPLE 6.17\n')
    #print(OrbitalManeuvers.NonImpulsiveManeuver(t, 1000, np.array([6678, 0, 0]), np.array([0, 7.72584, 0]), np.array([42164, 0, 0]), 1000, 0.0025e3, 10000, True, tol=1e-6))
    print('-' * 40, '\n')
    
    print('Progetto\n')
    r_0 = np.array([-8173.55640, -3064.65060, -2840.15350])
    v_0 = np.array([-3.07330000, 5.94440000, -1.54740000])
    oe_0 = ThreeDimensionalOrbit.calculateOrbitalElements(r_0, v_0)
    p_0 = TwoBodyProblem.calculateOrbitalParameters(r_0, v_0)
    print(oe_0)
    
    oe_f = ORBITAL_ELEMENTS(0, 0.1218, 0.4440, 2.5486, 3.1052, 2.0233, 34754)
    r_f, v_f = ThreeDimensionalOrbit.PF2GEF(oe_f)
    print(r_f, v_f)
    p_f = TwoBodyProblem.calculateOrbitalParameters(r_f, v_f)
    
    print(OrbitalManeuvers.PlaneChangeManeuver(p_0.r_p, p_0.r_a, np.deg2rad(154.85), p_0.r_p, p_0.r_a, np.deg2rad(154.85), oe_f.i - oe_0.i))
    res = OrbitalManeuvers.PlaneChangeManeuver2(p_0.r_p, p_0.r_a, oe_0.Omega, oe_0.omega, oe_0.i, oe_f.Omega, oe_f.i)
    print(res)
    print(OrbitalManeuvers.ApseLineRotationFromEta(p_0.r_p, p_0.r_a, p_0.r_p, p_0.r_a, oe_f.omega - res.oe.omega))
    print(OrbitalManeuvers.HohmannTransfer(p_0.r_p, p_0.r_a, p_f.r_p, p_f.r_a, HohmannDirection.APO2PER))
    print(OrbitalManeuvers.BiEllipticHohmannTransfer(p_0.r_p, p_0.r_a, p_f.r_p, p_f.r_a, 4 * p_f.r_a, HohmannDirection.PER2APO))