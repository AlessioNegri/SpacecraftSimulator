import os
import sys

sys.path.append(os.path.dirname(__file__))

from ThreeDimensionalOrbit import *
from LagrangeCoefficients import *

class OrbitDirection(IntEnum):
    PROGRADE    = 0
    RETROGRADE  = 1

# ! CHAPTER 5 - Preliminary Orbit Determination
class OrbitDetermination():
    
    mu = AstronomicalData.GravitationalParameter(CelestialBody.EARTH)
    
    R_E = AstronomicalData.EquatiorialRadius(CelestialBody.EARTH)
    
    f = AstronomicalData.Flattening(CelestialBody.EARTH)
    
    omega = AstronomicalData.GroundTrackAngularVelocity(CelestialBody.EARTH)
    
    def __init__(self) -> None: pass
    
    @classmethod
    def setCelestialBody(cls, celestialBody : CelestialBody) -> None:
        """Sets the current celectial body

        Args:
            celestialBody (CelestialBody): Celestial body
        """
        
        cls.mu = AstronomicalData.GravitationalParameter(celestialBody)
        
        cls.R_E = AstronomicalData.EquatiorialRadius(celestialBody)
        
        cls.f = AstronomicalData.Flattening(celestialBody)
        
        cls.omega = AstronomicalData.GroundTrackAngularVelocity(celestialBody)
    
    # ! SECTION 5.2
    
    # ! ALGORITHM 5.1
    @classmethod
    def predictFromGibbsMethod(cls, r_1 : np.ndarray, r_2 : np.ndarray, r_3 : np.ndarray) -> ORBITAL_ELEMENTS:
        """Gibbs method of orbit determination from tree position vectors

        Args:
            r1 (np.ndarray): Position vector 1
            r2 (np.ndarray): Position vector 2
            r3 (np.ndarray): Position vector 3

        Returns:
            ORBITAL_ELEMENTS: Orbital elements
        """
        
        # * 1. Norm
        
        r_1_m = linalg.norm(r_1)
        r_2_m = linalg.norm(r_2)
        r_3_m = linalg.norm(r_3)
        
        # * 2. Cross products
        
        C_12 = np.cross(r_1, r_2)
        C_23 = np.cross(r_2, r_3)
        C_31 = np.cross(r_3, r_1)
        
        # * 3. Verify
        
        u_r1 = r_1 / r_1_m
        
        if np.dot(u_r1, C_23) > 1e-5: return ORBITAL_ELEMENTS()
        
        # * 4.
        
        N = r_1_m * C_23 + r_2_m * C_31 + r_3_m * C_12
        
        N_m = linalg.norm(N)
        
        D = C_12 + C_23 + C_31
        
        D_m = linalg.norm(D)
        
        S = r_1 * (r_2_m - r_3_m) + r_2 * (r_3_m - r_1_m) + r_3 * (r_1_m - r_2_m)
        
        # * 5.
        
        v_2 = np.sqrt(cls.mu / (N_m * D_m)) * (np.cross(D, r_2) / r_2_m + S)
        
        # * 6.
        
        ThreeDimensionalOrbit.mu = cls.mu
        
        return ThreeDimensionalOrbit.calculateOrbitalElements(r_2, v_2)
    
    # ! SECTION
    
    @classmethod
    def lambertEquation(cls, z : float, r_1 : float, r_2 : float, A : float, dt : float) -> float:
        """Lambert equation

        Args:
            z (float): Variable
            r_1 (float): Position vector 1
            r_2 (float): Position vector 2
            A (float): Parameter A
            dt (float): Delta time

        Returns:
            float: Result
        """
        
        y = r_1 + r_2 + A * (z * LagrangeCoefficients.S(z) - 1) / np.sqrt(LagrangeCoefficients.C(z))
        
        return (y / LagrangeCoefficients.C(z))**(3/2) * LagrangeCoefficients.S(z) + A * np.sqrt(y) - np.sqrt(cls.mu) * dt
    
    @classmethod
    def lambertEquationFirstDerivative(cls, z : float, r_1 : float, r_2 : float, A : float, dt : float) -> float:
        """Lambert equation first derivative

        Args:
            z (float): Variable
            r_1 (float): Position vector 1
            r_2 (float): Position vector 2
            A (float): Parameter A
            dt (float): Delta time

        Returns:
            float: Result
        """
        
        S = LagrangeCoefficients.S(z)
        C = LagrangeCoefficients.C(z)
        
        y0 = r_1 + r_2 + A * (0 * LagrangeCoefficients.S(0) - 1) / np.sqrt(LagrangeCoefficients.C(0))
        
        y = r_1 + r_2 + A * (z * LagrangeCoefficients.S(z) - 1) / np.sqrt(LagrangeCoefficients.C(z))
        
        if z == 0:
            
            return np.sqrt(2) / 40 * y0**(3/2) + A / 8 * (np.sqrt(y0) + A * 1 / np.sqrt(2 * y0))
        
        else:
            
            return (y / C)**(3/2) * ( 1 / (2 * z) * ( C - 3/2 * S / C ) + 3/4 * S**2 / C) + A / 8 * (3 * S / C * np.sqrt(y) + A * np.sqrt(C / y))
    
    # ! ALGORITHM 5.2
    @classmethod
    def solveLambertProblem(cls, r_1 : np.ndarray, r_2 : np.ndarray, dt : float, direction : OrbitDirection = OrbitDirection.PROGRADE, analyze : bool = False) -> list:
        """Lambert's problem

        Args:
            r_1 (np.ndarray): Position vector 1
            r_2 (np.ndarray): Position vector 2
            dt (float): Delta time
            direction (ORBIT_DIRECTION, optional): Type of orbit direction. Defaults to ORBIT_DIRECTION.PROGRADE.
            analyze(bool): True for showing the plot for initial root estimate. Defaults to False.

        Returns:
            list: [v_1, v_2, orbital elements, theta_2]
        """
        
        # * 1. Norm
        
        r_1_m = linalg.norm(r_1)
        r_2_m = linalg.norm(r_2)
        
        # * 2. Delta theta
        
        dtheta = 0.0
        
        temp = np.arccos( (np.dot(r_1, r_2)) / (r_1_m * r_2_m) )
        
        cond = np.cross(r_1, r_2)[2]
        
        if direction == OrbitDirection.PROGRADE:
            
            dtheta = temp if cond >= 0 else (2 * np.pi - temp)
            
        elif direction == OrbitDirection.RETROGRADE:
            
            dtheta = temp if cond < 0 else (2 * np.pi - temp)
            
        # * 3. Parameter A
        
        A = np.sin(dtheta) * np.sqrt( (r_1_m * r_2_m) / (1 - np.cos(dtheta)) )
        
        # * 4. Orbit type
        
        if analyze:
        
            domain = np.linspace(-4, 30, 1000)
            
            values = [cls.lambertEquation(i, r_1_m, r_2_m, A, dt) for i in domain]
            
            plt.figure()
            plt.plot(domain, values)
            plt.grid(True)
            plt.show()
        
        z0 = -4
        
        while cls.lambertEquation(z0, r_1_m, r_2_m, A, dt) < 0: z0 = z0 + 0.1
        
        z = newton(cls.lambertEquation, 1.5, cls.lambertEquationFirstDerivative, args=(r_1_m, r_2_m, A, dt))
        
        # * 5. Parameter y
        
        y = r_1_m + r_2_m + A * (z * LagrangeCoefficients.S(z) - 1) / np.sqrt(LagrangeCoefficients.C(z))
        
        # * 6. Lagrange functions
        
        f = 1 - y / r_1_m
        
        g = A * np.sqrt(y / cls.mu)
        
        dg_dt = 1 - y / r_2_m
        
        # * 7. Velocities
        
        v_1 = 1 / g * (r_2 - f * r_1)
        
        v_2 = 1 / g * (dg_dt * r_2 - r_1)
        
        # * 8. Orbital elements
        
        ThreeDimensionalOrbit.mu = cls.mu
        
        return [v_1, v_2, ThreeDimensionalOrbit.calculateOrbitalElements(r_1, v_1), ThreeDimensionalOrbit.calculateOrbitalElements(r_2, v_2).theta]
    
    # ! SECTION 5.4
    
    @classmethod
    def JulianDay(cls, year : int, month : int, day : int, hours : float, minutes : float, seconds : float) -> float:
        """Julian day

        Args:
            year (int): Year
            month (int): Month
            day (int): Day
            hours (float): Hours
            minutes (float): Minutes
            seconds (float): Seconds

        Returns:
            float: Julian day number
        """
        
        # * 1. Checks
        
        if year < 1901 or year > 2099: raise CustomException('Year must be in range 1901 - 2099')
        
        if month < 1 or month > 12: raise CustomException('Month must be in range 1 - 12')
        
        if day < 1 or day > 31: raise CustomException('Day must be in range 1 - 31')
        
        if hours < 0 or hours > 23: raise CustomException('Hours must be in range 0 - 23')
        
        if minutes < 0 or minutes > 59: raise CustomException('Minutes must be in range 0 - 59')
        
        if seconds < 0 or seconds > 59: raise CustomException('Seconds must be in range 0 - 59')
        
        # * 2. Julian day at 0 h UT
        
        J0 = 367 * year - int( 7/4 * ( year + int( (month + 9) / 12 ) ) ) + int(275/9 * month) + day + 1721013.5
        
        # * 3. Univeral Time
        
        UT = hours + minutes / 60 + seconds / 3600
        
        # * 4. Julian day number
        
        return J0 + UT / 24
    
    # ! ALGORITHM 5.3
    @classmethod
    def LocalSiderealTime(cls, year : int, month : int, day : int, hours : float, minutes : float, seconds : float, longitude : float) -> float:
        """Local sidereal time

        Args:
            year (int): Year
            month (int): Month
            day (int): Day
            hours (float): Hours
            minutes (float): Minutes
            seconds (float): Seconds
            longitude (float): East longitude

        Returns:
            float: Local sidereal time [deg]
        """
        
        # * 0. Checks
        
        if year < 1901 or year > 2099: raise CustomException('Year must be in range 1901 - 2099')
        
        if month < 1 or month > 12: raise CustomException('Month must be in range 1 - 12')
        
        if day < 1 or day > 31: raise CustomException('Day must be in range 1 - 31')
        
        if hours < 0 or hours > 23: raise CustomException('Hours must be in range 0 - 23')
        
        if minutes < 0 or minutes > 59: raise CustomException('Minutes must be in range 0 - 59')
        
        if seconds < 0 or seconds > 59: raise CustomException('Seconds must be in range 0 - 59')
        
        UT = hours + minutes / 60 + seconds / 3600 # ? Univeral Time
        
        J_2000 = 2_451_545
        
        # * 1. Julian day at 0 h UT
        
        J0 = 367 * year - int( 7/4 * ( year + int( (month + 9) / 12 ) ) ) + int(275/9 * month) + day + 1721013.5
        
        # * 2. Time between J0 and J2000
        
        T0 = (J0 - J_2000) / 36_525
        
        # * 3. Greenwich sideral time at 0 h UT [deg]
        
        theta_G0 = 100.4606184 + 36000.77004 * T0 + 0.000387933 * T0**2 - 2.583e-8 * T0**3 # ? [deg]
        
        theta_G0 = wrapTo360Deg(theta_G0)
        
        # * 4. Greenwich sideral time [deg]
        
        theta_G = theta_G0 + 360.98564724 * UT / 24
        
        # * 5. Local sidereal time
        
        theta = theta_G + longitude
        
        theta = wrapTo360Deg(theta)
        
        return theta
    
    # ! SECTION 5.5 - 5.6
    
    @classmethod
    def GEF(cls, theta : float, phi : float, H : float = 0) -> np.ndarray:
        """Geocentric Equatorial Frame position vector

        Args:
            theta (float): Local sidereal time
            phi (float): Latitude
            H (float, optional): Elevation above sea level. Defaults to 0.

        Returns:
            np.ndarray: R
        """
        
        # * 1.
        
        A = ( cls.R_E / np.sqrt(1 - (2 * cls.f - cls.f**2) * np.sin(phi)**2) + H ) * np.cos(phi)
        
        B = ( cls.R_E * (1 - cls.f)**2 / np.sqrt(1 - (2 * cls.f - cls.f**2) * np.sin(phi)**2) + H ) * np.sin(phi)
        
        return np.array([A * np.cos(theta), A * np.sin(theta), B])
    
    @classmethod
    def GEF2TEF(cls, r : np.ndarray, theta : float, phi : float, H : float = 0) -> np.ndarray:
        """Geocentric Equatorial Frame --> Topocentric Equatorial Frame

        Args:
            r (np.ndarray): Geocentric equatiorial position vector of the target
            theta (float): Local sidereal time
            phi (float): Latitude
            H (float, optional): Elevation above sea level. Defaults to 0.

        Returns:
            np.ndarray: rho
        """
        
        # * 1. Geocentric position vector of the site
        
        A = ( cls.R_E / np.sqrt(1 - (2 * cls.f - cls.f**2) * np.sin(phi)**2) + H ) * np.cos(phi)
        
        B = ( cls.R_E * (1 - cls.f)**2 / np.sqrt(1 - (2 * cls.f - cls.f**2) * np.sin(phi)**2) + H ) * np.sin(phi)
        
        R = np.array([A * np.cos(theta), A * np.sin(theta), B])
        
        # * 2. Relative position vector
        
        return r - R
    
    # ! SECTION 5.7
    
    @classmethod
    def GEF2THF(cls, r : np.ndarray, theta : float, phi : float, H : float = 0) -> list:
        """Geocentric Equatorial Frame --> Topocentric Horizone Frame

        Args:
            theta (float): Local sidereal time
            phi (float): latitude
            H (float, optional): Elevation above sea level. Defaults to 0.

        Returns:
            list: [Azimuth A, Elevation a]
        """
        
        # * 1. GEF relative position vector
        
        rho_TEF = cls.GEF2TEF(r, theta, phi, H)
        
        # * 2. THF relative position vector
        
        Q_Xx = np.array(
            [
                [ -np.sin(theta)               , np.cos(theta)                , 0           ],
                [ -np.sin(phi) * np.cos(theta) , -np.sin(phi) * np.sin(theta) , np.cos(phi) ],
                [ np.cos(phi) * np.cos(theta)  , np.cos(phi) * np.sin(theta)  , np.sin(phi) ]
            ])
        
        rho_THF = np.matmul(Q_Xx, rho_TEF)
        
        # * 3. Azimuth and Elevation
        
        rho_h = rho_THF / linalg.norm(rho_THF)
        
        a = np.arcsin(rho_h[2])
        
        A = np.arctan2(rho_h[0] / np.cos(a), rho_h[1] / np.cos(a))
        
        return [A, a]
    
    @classmethod
    def THF2TEF(cls, theta : float, phi : float, A : float, a : float) -> np.ndarray:
        """Topocentric Horizone Frame --> Topocentric Equatorial Frame

        Args:
            theta (float): Local sidereal time
            phi (float): latitude
            A (float): Azimuth
            a (float): elevation

        Returns:
            np.ndarray: rho
        """
        
        # * 1. THF relative position vector
        
        Q_xX = np.array(
            [
                [ -np.sin(theta) , -np.sin(phi) * np.cos(theta) , np.cos(phi) * np.cos(theta) ],
                [ np.cos(theta)  , -np.sin(phi) * np.sin(theta) , np.cos(phi) * np.sin(theta) ],
                [ 0              , np.cos(phi)                  , np.sin(phi)                 ]
            ])
        
        rho_h = np.array([np.cos(a) * np.sin(A), np.cos(a) * np.cos(A), np.sin(a)])
        
        # * 2. GEF relative position vector
        
        return np.matmul(Q_xX, rho_h)
    
    # ! SECTION 5.8
    
    # ! ALGORITHM 5.4
    @classmethod
    def predictFromAngleRange(cls, rho : float, A : float, a : float, drho_dt : float, dA_dt : float, da_dt : float, theta : float, phi : float, H : float = 0) -> list:
        """Predicts the geocentric position and velocity vectors from angle and range measurements

        Args:
            rho (float): Slant range
            A (float): Azimuth
            a (float): Elevation
            drho_dt (float): Range rate
            dA_dt (float): Azimuth rate
            da_dt (float): Elevation rate
            theta (float): Local sidereal time
            phi (float): Latitude
            H (float, optional): Elevation above sea level. Defaults to 0.

        Returns:
            list: [r, v]
        """
        
        # * 1. Geocentric position vector of the site
        
        R = cls.GEF(theta, phi, H)
        
        # * 2. Topocentric declination
        
        delta = np.arcsin(np.cos(phi) * np.cos(A) * np.cos(a) + np.sin(phi) * np.sin(a))
        
        # * 3. Topocentric right ascension
        
        h = 0.0 # ? Hour Angle
        
        if A > 0 and A < np.pi:
            
            h = 2* np.pi - np.arccos((np.cos(phi) * np.sin(a) - np.sin(phi) * np.cos(A) * np.cos(a)) / np.cos(delta))
            
        else:
            
            h = np.arccos((np.cos(phi) * np.sin(a) - np.sin(phi) * np.cos(A) * np.cos(a)) / np.cos(delta))
        
        alpha = theta - h
        
        # * 4. Direction cosine unit vector
        
        rho_h = np.array([np.cos(delta) * np.cos(alpha), np.cos(delta) * np.sin(alpha), np.sin(delta)])
        
        # * 5. Geocentric position vector
        
        r = R + rho * rho_h
        
        # * 6.
        
        dR_dt = np.cross(np.array([0, 0, cls.omega]), R)
        
        # * 7.
        
        ddelta_dt = 1 / np.cos(delta) * ( -dA_dt * np.cos(phi) * np.sin(A) * np.cos(a) + da_dt * ( np.sin(phi) * np.cos(a) - np.cos(phi) * np.cos(A) * np.sin(a) ) )
        
        # * 8.
        
        dalpha_dt = cls.omega + (dA_dt * np.cos(A) * np.cos(a) - da_dt * np.sin(A) * np.sin(a) + ddelta_dt * np.sin(A) * np.cos(a) * np.tan(delta)) / (np.cos(phi) * np.sin(a) - np.sin(phi) * np.cos(A) * np.cos(a))
        
        # * 9.
        
        drho_h_dt = np.array([-dalpha_dt * np.sin(alpha) * np.cos(delta) - ddelta_dt * np.cos(alpha) * np.sin(delta),
                             dalpha_dt * np.cos(alpha) * np.cos(delta) - ddelta_dt * np.sin(alpha) * np.sin(delta),
                             ddelta_dt * np.cos(delta)])
        
        # * 10 Geocentric velocity vector
        
        v = dR_dt + drho_dt * rho_h + rho * drho_h_dt
        
        return [r, v]

    # ! SECTION 5.9 -5.10
    
    # ! ALGORITHM 5.5
    @classmethod
    def predictFromGaussMethod(cls, phi : float, H : float, theta : list, alpha : list, delta : list, t : list, analyze : bool = False) -> list:
        """Predict position and velocity with the Gauss method

        Args:
            phi (float): Latitude
            H (float): Elevation above sea level
            theta (list): List of local sidereal times [3]
            alpha (list): List of right ascensions [3]
            delta (list): List of declinations [3]
            t (list): List of observation times [3]
            analyze(bool): True for showing the plot for initial root estimate. Defaults to False.

        Returns:
            list: Parameters
        """
        
        if len(theta) != 3: raise CustomException('theta must contain three values')
        if len(alpha) != 3: raise CustomException('alpha must contain three values')
        if len(delta) != 3: raise CustomException('delta must contain three values')
        if len(t) != 3: raise CustomException('t must contain three values')
        
        # * 0. Geocentric position vector of the site - THF relative position vector
        
        R_1 = cls.GEF(theta[0], phi, H)
        R_2 = cls.GEF(theta[1], phi, H)
        R_3 = cls.GEF(theta[2], phi, H)
        
        rho_h_1 = np.array([ np.cos(delta[0]) * np.cos(alpha[0]), np.cos(delta[0]) * np.sin(alpha[0]), np.sin(delta[0]) ])
        rho_h_2 = np.array([ np.cos(delta[1]) * np.cos(alpha[1]), np.cos(delta[1]) * np.sin(alpha[1]), np.sin(delta[1]) ])
        rho_h_3 = np.array([ np.cos(delta[2]) * np.cos(alpha[2]), np.cos(delta[2]) * np.sin(alpha[2]), np.sin(delta[2]) ])
        
        # * 1. Time intervals
        
        tau_1   = t[0] - t[1]
        tau_3   = t[2] - t[1]
        tau     = tau_3 - tau_1
        
        # * 2. Crossproducts
        
        p_1 = np.cross(rho_h_2, rho_h_3)
        p_2 = np.cross(rho_h_1, rho_h_3)
        p_3 = np.cross(rho_h_1, rho_h_2)
        
        # * 3.
        
        D_0 = np.dot(rho_h_1, p_1)
        
        # * 4.
        
        D = np.array(
            [
                [ np.dot(R_1, p_1), np.dot(R_1, p_2), np.dot(R_1, p_3) ],
                [ np.dot(R_2, p_1), np.dot(R_2, p_2), np.dot(R_2, p_3) ],
                [ np.dot(R_3, p_1), np.dot(R_3, p_2), np.dot(R_3, p_3) ]
            ]
        )
        
        # * 5. Calculate parameters
        
        A = 1 / D_0 * (-D[0,1] * tau_3 / tau + D[1,1] + D[2,1] * tau_1 / tau)
        
        B = 1 / (6 * D_0) * (D[0,1] * (tau_3**2 - tau**2) * tau_3 / tau + D[2,1] * (tau**2 - tau_1**2) * tau_1 / tau)
        
        # * 6.
        
        E = np.dot(R_2, rho_h_2)
        
        # * 7.
        
        a = - (A**2 + 2 * A * E + linalg.norm(R_2)**2)
        
        b = - 2 * cls.mu * B * (A + E)
        
        c = - cls.mu**2 * B**2
        
        # * 8. Find r_2
        
        def f(x : float, a : float, b : float, c : float) -> float: return x**8 + a * x**6 + b * x**3 + c
        
        def dfdt(x : float, a : float, b : float, c : float) -> float: return 8 * x**7 + 6 * a * x**5 + 3 * b * x**2
        
        if analyze:
            
            values = np.linspace(0, 15000, 1000)
            
            plt.figure()
            plt.plot(values, f(values, a, b, c))
            plt.grid(True)
            plt.show()
        
        r_2_m = newton(f, 10000, dfdt, args=(a, b, c))
        
        # * 9. Slant ranges
        
        rho_1 = 1 / D_0 * ( (6 * (D[2,0] * tau_1 / tau_3 + D[1,0] * tau / tau_3) * r_2_m**3 + cls.mu * D[2,0] * (tau**2 - tau_1**2) * tau_1 / tau_3 ) /
                (6 * r_2_m**3 + cls.mu * (tau**2 - tau_3**2)) - D[0,0] )
        
        rho_2 = A + cls.mu * B / r_2_m**3
        
        rho_3 = 1 / D_0 * ( (6 * (D[0,2] * tau_3 / tau_1 - D[1,2] * tau / tau_1) * r_2_m**3 + cls.mu * D[0,2] * (tau**2 - tau_3**2) * tau_3 / tau_1 ) /
                (6 * r_2_m**3 + cls.mu * (tau**2 - tau_1**2)) - D[2,2] )
        
        # * 10. Geocentric position vector of the target
        
        r_1 = R_1 + rho_1 * rho_h_1
        r_2 = R_2 + rho_2 * rho_h_2
        r_3 = R_3 + rho_3 * rho_h_3
        
        # * 11. Lagrange coefficients
        
        f_1 = 1 - 1/2 * cls.mu / r_2_m**3 * tau_1**2
        f_3 = 1 - 1/2 * cls.mu / r_2_m**3 * tau_3**2
        g_1 = tau_1 - 1/6 * cls.mu / r_2_m**3 * tau_1**3
        g_3 = tau_3 - 1/6 * cls.mu / r_2_m**3 * tau_3**3
        
        # * 12. Position and velocity vectors
        
        v_2 = 1 / (f_1 * g_3 - f_3 * g_1) * (-f_3 * r_1 + f_1 * r_3)
        
        return [r_2, v_2, f_1, f_3, g_1, g_3, R_1, R_2, R_3, D_0, D, rho_h_1, rho_h_2, rho_h_3, rho_1, rho_2, rho_3]
    
    # ! ALGORITHM 5.6
    @classmethod
    def predictFromGaussMethodExtended(cls, phi : float, H : float, theta : list, alpha : list, delta : list, t : list) -> list:
        """Predict position and velocity with the extended Gauss method

        Args:
            phi (float): Latitude
            H (float): Elevation above sea level
            theta (list): List of local sidereal times
            alpha (list): List of right ascensions
            delta (list): List of declinations
            t (list): List of observation times

        Returns:
            list: [Position, Velocity]
        """
        
        r_2, v_2, f_1_prev, f_3_prev, g_1_prev, g_3_prev, R_1, R_2, R_3, D_0, D, rho_h_1, rho_h_2, rho_h_3, rho_1_prev, rho_2_prev, rho_3_prev = cls.predictFromGaussMethod(phi, H, theta, alpha, delta, t)
        
        rho_1 = rho_2 = rho_3 = 0
        
        f_1 = f_3 = g_1 = g_3 = 0
        
        step = 0
        
        while np.abs(rho_1 - rho_1_prev) > 1e-6 and np.abs(rho_2 - rho_2_prev) > 1e-6 and np.abs(rho_3 - rho_3_prev) > 1e-6:
            
            # * Update values
            
            if step != 0:
                
                rho_1_prev = rho_1
                rho_2_prev = rho_2
                rho_3_prev = rho_3
                
                f_1_prev = f_1
                f_3_prev = f_3
                g_1_prev = g_1
                g_3_prev = g_3
            
            # * 1. Norms
            
            r_2_m = linalg.norm(r_2)
            v_2_m = linalg.norm(v_2)
            
            # * 2. Alpha
            
            Alpha = 2 / r_2_m - v_2_m**2 / cls.mu
            
            # * 3. Radial velocity
            
            v_r_2 = np.dot(v_2, r_2) / r_2_m
            
            # * 4. Universal variables
            
            LagrangeCoefficients.mu = cls.mu
            
            chi_1 = LagrangeCoefficients.calculateUniversalVariable(r_2_m, v_r_2, Alpha, t[0] - t[1])
            chi_3 = LagrangeCoefficients.calculateUniversalVariable(r_2_m, v_r_2, Alpha, t[2] - t[1])
            
            # * 5. Lagrange coefficients
            
            f_1, g_1 = LagrangeCoefficients.calculateLagrangeCoefficients(r_2_m, Alpha, t[0] - t[1], chi_1)
            f_3, g_3 = LagrangeCoefficients.calculateLagrangeCoefficients(r_2_m, Alpha, t[2] - t[1], chi_3)
            
            # * 6. Calculate parameters
            
            f_1 = (f_1 + f_1_prev) / 2
            f_3 = (f_3 + f_3_prev) / 2
            g_1 = (g_1 + g_1_prev) / 2
            g_3 = (g_3 + g_3_prev) / 2
            
            c_1 = g_3 / (f_1 * g_3 - f_3 * g_1)
            c_3 = -g_1 / (f_1 * g_3 - f_3 * g_1)
            
            # * 7. Updated slant ranges
            
            rho_1 = 1 / D_0 * (-D[0,0] + D[1,0] / c_1 - D[2,0] * c_3 / c_1)
            rho_2 = 1 / D_0 * (-c_1 * D[0,1] + D[1,1] - c_3 * D[2,1])
            rho_3 = 1 / D_0 * (-D[0,2] * c_1 / c_3 + D[1,2] / c_3 - D[2,2])
            
            # * 8. Geocentric position vector of the target
        
            r_1 = R_1 + rho_1 * rho_h_1
            r_2 = R_2 + rho_2 * rho_h_2
            r_3 = R_3 + rho_3 * rho_h_3
            
            # * 9. Velocity vector
            
            v_2 = 1 / (f_1 * g_3 - f_3 * g_1) * (-f_3 * r_1 + f_1 * r_3)
            
            step += 1
        
        # * 10. Position and velocity vectors
        
        return [r_2, v_2]

if __name__ == '__main__':
    
    print('EXAMPLE 5.1\n')
    print(OrbitDetermination.predictFromGibbsMethod(np.array([-294.32, 4265.1, 5986.7]), np.array([-1365.5, 3637.6, 6346.8]), np.array([-2940.3, 2473.7, 6555.8])))
    print('-' * 40, '\n')
    
    print('EXAMPLE 5.2\n')
    print(OrbitDetermination.solveLambertProblem(np.array([5000, 10000, 2100]), np.array([-14600, 2500, 7000]), 3600))
    print('-' * 40, '\n')
    
    print('EXAMPLE 5.4\n')
    print(OrbitDetermination.JulianDay(2004, 5, 12, 14, 45, 30))
    print('-' * 40, '\n')
    
    print('EXAMPLE 5.5\n')
    print(OrbitDetermination.JulianDay(2004, 5, 12, 14, 45, 30) - OrbitDetermination.JulianDay(1957, 10, 4, 19, 26, 24))
    print('-' * 40, '\n')
    
    print('EXAMPLE 5.6\n')
    print(OrbitDetermination.LocalSiderealTime(2004, 3, 3, 4, 30, 0, 139.80))
    print('-' * 40, '\n')
    
    print('EXAMPLE 5.7\n')
    print(np.rad2deg(ThreeDimensionalOrbit.calculateRaDec(OrbitDetermination.GEF2TEF(np.array([-5368, -1784, 3691]), np.deg2rad(186.7), np.deg2rad(20)))))
    print('-' * 40, '\n')
    
    print('EXAMPLE 5.8\n')
    print(OrbitDetermination.THF2TEF(np.deg2rad(215.1), np.deg2rad(38), np.deg2rad(214.3), np.deg2rad(43)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 5.9\n')
    print(np.rad2deg(OrbitDetermination.GEF2THF(np.array([-2032.4, 4591.2, -4544.8]), np.deg2rad(110), np.deg2rad(-40))))
    print('-' * 40, '\n')
    
    print('EXAMPLE 5.10\n')
    r, v = OrbitDetermination.predictFromAngleRange(2551, np.deg2rad(90), np.deg2rad(30), 0, 1.973e-3, 9.864e-4, np.deg2rad(300), np.deg2rad(60))
    print(ThreeDimensionalOrbit.calculateOrbitalElements(r, v, True))
    print('-' * 40, '\n')
    
    print('EXAMPLE 5.11\n')
    print(OrbitDetermination.predictFromGaussMethod(np.deg2rad(40), 1, np.deg2rad([44.506, 45.000, 45.499]), np.deg2rad([43.537, 54.420, 64.318]), np.deg2rad([-8.7833, -12.074, -15.105]), [0, 118.10, 237.58], analyze=True))
    print('-' * 40, '\n')
    
    print('EXAMPLE 5.12\n')
    r, v = OrbitDetermination.predictFromGaussMethodExtended(np.deg2rad(40), 1, np.deg2rad([44.506, 45.000, 45.499]), np.deg2rad([43.537, 54.420, 64.318]), np.deg2rad([-8.7833, -12.074, -15.105]), [0, 118.10, 237.58])
    print(ThreeDimensionalOrbit.calculateOrbitalElements(r, v, True))
    print('-' * 40, '\n')