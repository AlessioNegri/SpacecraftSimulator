import os
import sys

sys.path.append(os.path.dirname(__file__))

#from lib.pyextrema.extrema import extrema

from stdafx import *
from LagrangeCoefficients import *
from ThreeDimensionalOrbit import *
from OrbitDetermination import *

# ! CHAPTER 12 - Orbital Perturbations
class OrbitalPerturbations():
    
    mu = AstronomicalData.GravitationalParameter(CelestialBody.EARTH)
    
    R_E = AstronomicalData.EquatiorialRadius(CelestialBody.EARTH)
    
    omega = AstronomicalData.AngularVelocity(CelestialBody.EARTH)
    
    J_2 = AstronomicalData.SecondZonalHarmonics(CelestialBody.EARTH)
    
    iteration = 0
    
    def __init__(self) -> None: pass
    
    @classmethod
    def setCelestialBody(cls, celestialBody : CelestialBody) -> None:
        """Sets the current celectial body

        Args:
            celestialBody (CelestialBody): Celestial body
        """
        
        cls.mu = AstronomicalData.GravitationalParameter(celestialBody)
        
        cls.R_E = AstronomicalData.EquatiorialRadius(celestialBody)
        
        cls.omega = AstronomicalData.AngularVelocity(celestialBody)
        
        cls.J_2 = AstronomicalData.SecondZonalHarmonics(celestialBody)
        
    
    # ! SECTION 12.4
    
    @classmethod
    def density(cls, z : float) -> float:
        """Calculates the atmospheric density given the altitude above the Earth with the USSA76 model

        Args:
            z (float): Altitude

        Returns:
            float: Density
        """
        
        # * 1. Geometric altitudes [km]
        
        h = np.array([0, 25, 30, 40, 50, 60, 70, 80, 90, 100,
                      110, 120, 130, 140, 150, 180, 200, 250, 300, 350,
                      400, 450, 500, 600, 700, 800, 900, 1000])
        
        # * 2. Corresponding densities [kg / m^3] from USSA76:
        
        rho = np.array([1.225, 4.008e-2, 1.841e-2, 3.996e-3, 1.027e-3,
                        3.097e-4, 8.283e-5, 1.846e-5, 3.416e-6, 5.606e-7,
                        9.708e-8, 2.222e-8, 8.152e-9, 3.831e-9, 2.076e-9,
                        5.194e-10, 2.541e-10, 6.073e-11, 1.916e-11, 7.014e-12,
                        2.803e-12, 1.184e-12, 5.215e-13, 1.137e-13, 3.070e-14,
                        1.136e-14, 5.759e-15, 3.561e-15])
        
        # * 3. Scale heights [km]

        H = np.array([7.310, 6.427, 6.546, 7.360, 8.342,
                      7.583, 6.661, 5.927, 5.533, 5.703,
                      6.782, 9.973, 13.243, 16.322, 21.652,
                      27.974, 34.934, 43.342, 49.755, 54.513,
                      58.019, 60.980, 65.654, 76.377, 100.587,
                      147.203, 208.020])
        
        # * 4. Handle altitudes outside of the range
        
        if      z > 1000:   z = 1000
        elif    z < 0:      z = 0
        
        # * 5. Determine the interpolation interval
        
        idx = 0
        
        for j in range(0, 27):
        
            if z >= h[j] and z < h[j + 1]: idx = j
            
        if z == 1000: idx = 26
        
        # * 6. Exponential interpolation
        
        return rho[idx] * np.exp(-(z - h[idx]) / H[idx])
    
    @classmethod
    def atmosphericDragEquations(cls, t : float, X : np.ndarray, B : float, t_0 : float, t_f : float) -> np.ndarray:
        """Equations of relative motion with atmospheric drag perturbation

        Args:
            t (float): Time
            X (np.ndarray): State [6,1]
            B (float): Ballistic coefficient (C_D * A / m)
            t_0 (float): Initial time
            t_f (float): Final time

        Returns:
            np.ndarray: Derivative of state
        """
        
        # * Parameters
        
        x, y, z, v_x, v_y, v_z = X
        
        r = np.sqrt(x**2 + y**2 + z**2)
        
        # * Atmospheric Drag
        
        v_rel = X[3:] - np.cross(np.array([0, 0, cls.omega]), X[:3])
        
        p = - 0.5 * cls.density(r - cls.R_E) * 1e9 * linalg.norm(v_rel) * B * 1e-6 * v_rel
        
        if int(100 * ((t - t_0) / float(t_f - t_0))) != cls.iteration:
            
            cls.iteration = int(100 * ((t - t_0) / float(t_f - t_0)))
            
            printProgressBar(t - t_0, t_f - t_0, prefix = 'Progress:', suffix = 'Processing...', length = 50)
            
            print(cls.density(r - cls.R_E))
        
        # * Equations
        
        dX_dt = np.zeros(shape=(6))
        
        dX_dt[0] = v_x
        dX_dt[1] = v_y
        dX_dt[2] = v_z
        dX_dt[3] = - (cls.mu / r**3) * x + p[0]
        dX_dt[4] = - (cls.mu / r**3) * y + p[1]
        dX_dt[5] = - (cls.mu / r**3) * z + p[2]
        
        return dX_dt
    
    @classmethod
    def integrateRelativeMotionWithAtmosphericDrag(cls, y_0 : np.ndarray, B : float, t_0 : float = 0.0, t_f : float = 0.0, show : bool = False) -> dict:
        """Integrates the Ordinary Differential Equations for the relative motion with atmospheric drag perturbation (COWELL's method)

        Args:
            y_0 (np.ndarray): Initial state [6,1]
            B (float): Ballistic coefficient (C_D * A / m)
            t_0 (float, optional): Initial time. Defaults to 0.0.
            t_f (float, optional): Final time. Defaults to 0.0.
            show (bool, optional): True for plotting the trajectory. Defaults to False.
            
        Returns:
            dict: { t: time, y: state[n_states, n_points] }
        """
        
        # * 1.
        
        if t_f < t_0: raise CustomException('Invalid integration time')
        
        cls.iteration = 0
        
        integrationResult = solve_ivp(fun=cls.atmosphericDragEquations, t_span=[t_0, t_f], y0=y_0, method='RK45', args=(B, t_0, t_f), rtol=1e-8, atol=1e-8)
        
        if not integrationResult['success']: CustomException(integrationResult['message'])
        
        x = integrationResult['y'][0, :]
        y = integrationResult['y'][1, :]
        z = integrationResult['y'][2, :]
        
        altitude = np.sqrt(x**2 + y**2 + z**2) - cls.R_E
        
        max_altitude, min_altitude, imax, imin = extrema(altitude)
        
        max_altitude = max_altitude[1:]
        min_altitude = min_altitude[:-1]
        imax = imax[1:]
        imin = imin[:-1]
        
        # * 2.
        
        if show:
            
            plt.subplots(figsize=(10, 8)) #fig.subplots_adjust(top=1.1, bottom=-0.1)
            
            ax1 = plt.subplot(121, projection='3d')
            
            # * Max Values
            
            xMax = 1.25 * max(np.absolute(x))
            yMax = 1.25 * max(np.absolute(y))
            zMax = 1.25 * max(np.absolute(z))
            
            # * Plane
            
            p = mpatches.Rectangle((-xMax, -yMax), 2 * xMax, 2 * yMax, fc=(0,0,0,0.1), ec=(0,0,0,1), lw=2)
            
            ax1.add_patch(p)
            
            art3d.pathpatch_2d_to_3d(p, z=0, zdir='z')
            
            # * Axes
            
            ax1.plot([0, xMax], [0, 0], [0, 0], 'k--')
            ax1.plot([0, 0], [0, yMax], [0, 0], 'k--')
            ax1.plot([0, 0], [0, 0], [0, zMax], 'k--')
            
            # * Earth
            
            ax1.scatter(0, 0, 0, s=1000, c='c')
            
            # * Orbit
            
            ax1.plot(x, y, z, label='Orbit')
            
            # * Start
            
            ax1.scatter(x[0], y[0], z[0], s=200, c='g', label='Start')
            
            # * Finish
            
            ax1.scatter(x[-1], y[-1], z[-1], s=200, c='r', label='Finish')
            
            ax1.set_title('Spacecraft Orbit')
            ax1.set_xlabel('$x$ [km]')
            ax1.set_ylabel('$y$ [km]')
            ax1.set_zlabel('$z$ [km]')
            
            # * Pericenter / Apocenter
            
            ax2 = plt.subplot(122)
            
            ax2.scatter(integrationResult['t'][imax] / 86400, max_altitude, label='Apogee')
            ax2.scatter(integrationResult['t'][imin] / 86400, min_altitude, label='Perigee')
            
            plt.grid()
            plt.legend()
            plt.show()
        
        return dict(t=integrationResult['t'], y=integrationResult['y'], dt=np.abs(integrationResult['t'][-1] - integrationResult['t'][0]))
    
    # ! SECTION 12.5
    
    @classmethod
    def gravitationalPerturbationEquations(cls, t : float, X : np.ndarray, r_osc : np.ndarray, v_osc : np.ndarray) -> np.ndarray:
        """Equations of relative motion with gravitational perturbation

        Args:
            t (float): Time
            X (np.ndarray): State [6,1]
            r_osc (np.ndarray): Osculating position vector
            v_osc (np.ndarray): Osculating velocity vector

        Returns:
            np.ndarray: Derivative of state
        """
        
        # * Parameters
        
        dr, dv = X[:3], X[3:]
        
        # * Osculating state
        
        r_ = r_osc + dr
        v_ = v_osc + dv
        
        r = linalg.norm(r_)
        
        x, y, z = r_
        
        # * Gravitational Perturbation
        
        p = 3 / 2 * cls.J_2 * cls.mu * cls.R_E**2 / r**4 * np.array([x / r * (5 * z**2 / r**2 - 1), y / r * (5 * z**2 / r**2 - 1), z / r * (5 * z**2 / r**2 - 3)])
        
        # * Equations
        
        F = lambda q: float((q**2 - 3 * q + 3) / (1 + (1 - q)**(3/2)) * q)
        
        q = (np.dot(dr, (2 * r_ - dr)) / r**2)
        
        #f = 1 - linalg.norm(r_osc)**3 / r **3
        
        dX_dt = np.zeros(shape=(6))
        
        dX_dt[0] = dv[0]
        dX_dt[1] = dv[1]
        dX_dt[2] = dv[2]
        dX_dt[3] = - (cls.mu / linalg.norm(r_osc)**3) * (dr[0] - F(q) * r_[0]) + p[0]
        dX_dt[4] = - (cls.mu / linalg.norm(r_osc)**3) * (dr[1] - F(q) * r_[1]) + p[1]
        dX_dt[5] = - (cls.mu / linalg.norm(r_osc)**3) * (dr[2] - F(q) * r_[2]) + p[2]
        
        return dX_dt
    
    # ! ALGORITHM 12.1
    @classmethod
    def integrateRelativeMotionWithGravitationalPerturbation(cls, y_0 : np.ndarray, t_0 : float = 0.0, t_f : float = 0.0, show : bool = False) -> dict:
        """Integrates the Ordinary Differential Equations for the relative motion with gravitational perturbation (ENCKE's method)

        Args:
            y_0 (np.ndarray): Initial state [6,1]
            t_0 (float, optional): Initial time. Defaults to 0.0.
            t_f (float, optional): Final time. Defaults to 0.0.
            show (bool, optional): True for plotting the trajectory. Defaults to False.
            
        Returns:
            dict: { t: time, y: state[n_states, n_points] }
        """
        
        # * 1.
        
        if t_f < t_0: raise CustomException('Invalid integration time')
        
        t_prev = t_0
        
        dy_0 = np.zeros(shape=(6))
        
        times = np.linspace(t_0, t_f, 1000)
        
        dt = times[1] - times[0]
        
        r_osc, v_osc = LagrangeCoefficients.calculatePositionVelocityByTime(y_0[:3], y_0[3:], dt)
        
        a = []
        e = []
        i = []
        Omega = []
        omega = []
        h = []
        
        for t in times:
            
            #printProgressBar(t - t_0, t_f - t_0, prefix = 'Progress:', suffix = 'Processing...', length = 50)
            
            # * a. Integrate perturbed motion
            
            integrationResult = solve_ivp(fun=cls.gravitationalPerturbationEquations, t_span=[t, t + dt], y0=dy_0, method='RK45', args=(r_osc, v_osc), rtol=1e-8, atol=1e-8)
            
            if not integrationResult['success']: CustomException(integrationResult['message'])
            
            # * b. Evaluates new osculating orbit
            
            r_osc, v_osc = LagrangeCoefficients.calculatePositionVelocityByTime(y_0[:3], y_0[3:], dt)
            
            #print(y_0[:3], r_osc, integrationResult['y'][:3, -1])
        
            r_0 = r_osc + integrationResult['y'][:3, -1]
            v_0 = v_osc + integrationResult['y'][3:, -1]
            y_0 = np.hstack([r_0, v_0])
            
            # * c. Calculates orbital elements
            
            temp = ThreeDimensionalOrbit.calculateOrbitalElements(r_0, v_0, deg=True)
            
            a.append(temp.a)
            e.append(temp.e)
            i.append(temp.i)
            Omega.append(temp.Omega)
            omega.append(temp.omega)
            h.append(temp.h)
            
            # * d. Update previous time
            
            t_prev = t
        
        # * 2.
        
        if show:
            
            plt.figure()
            
            plt.subplot(231)
            plt.plot(times / 3600, a - a[0])
            plt.title('Semi-Major Axis')
            plt.grid()
            
            plt.subplot(232)
            plt.plot(times / 3600, e - e[0])
            plt.title('Eccentricity')
            plt.grid()
            
            plt.subplot(233)
            plt.plot(times / 3600, i - i[0])
            plt.title('Inclination')
            plt.grid()
            
            plt.subplot(234)
            plt.plot(times / 3600, Omega - Omega[0])
            plt.title('Right Ascension of the Ascending Node')
            plt.grid()
            
            plt.subplot(235)
            plt.plot(times / 3600, omega - omega[0])
            plt.title('Anomaly of the Perigee')
            plt.grid()
            
            plt.subplot(236)
            plt.plot(times / 3600, h - h[0])
            plt.title('Angular Momentum')
            plt.grid()
            
            plt.show()
        
        return dict(t=times)
    
    # ! SECTION 12.7
    
    @classmethod
    def GaussVariationalEquations(cls,
                                  t : float,
                                  X : np.ndarray,
                                  drag : bool,
                                  gravitational : bool,
                                  SRP : bool,
                                  MOON : bool,
                                  SUN : bool,
                                  B : float,
                                  B_SRP : float) -> np.ndarray:
        """Equations of relative motion with gravitational perturbation

        Args:
            t (float): Time
            X (np.ndarray): State [6,1]
            drag (bool): True to include drag perturbation
            gravitational (bool): True to include gravitational perturbation
            SRP (bool): True to include Solar Radiation Pressure perturbation
            MOON (bool): True to include Lunar gravity perturbation
            SUN (bool): True to include Solar gravity perturbation
            B (float): Ballistic coefficient (C_D * A / m)
            B_SRP (float): Ballistic coefficient for SRP (C_R * A_S / m)

        Returns:
            np.ndarray: Derivative of state
        """
        
        # * Parameters
        
        h, e, theta, Omega, i, omega = X
        
        r = h**2 / (cls.mu * (1 + e * np.cos(theta)))
        
        # a, e, theta, Omega, i, omega = X
        
        # b = a * np.sqrt(1 - e**2)
        
        # p = b**2 / a
        
        # r = p / (1 + e * np.cos(theta))
        
        # v = np.sqrt(2 * cls.mu / r - cls.mu / a)
        
        # n = np.sqrt(cls.mu / a**3)
        
        # h = n * a * b
        
        p_r = p_s = p_w = 0
        
        # * Drag perturbation
        
        if drag:
            
            r_, v_ = ThreeDimensionalOrbit.PF2GEF(ORBITAL_ELEMENTS(h, e, i, Omega, omega, theta))
            
            v_rel = v_ - np.cross(np.array([0, 0, cls.omega]), r_)
            
            p_r += 0
            p_s += - 0.5 * cls.density(r - cls.R_E) * 1e9 * linalg.norm(v_rel)**2 * B * 1e-6
            p_w += 0
        
        # * Gravitational perturbation
        
        if gravitational:
            
            p_r += - 3 / 2 * cls.J_2 * cls.mu * cls.R_E**2 / (r**4) * (1 - 3 * np.sin(i)**2 * np.sin(omega + theta)**2)
            p_s += - 3 / 2 * cls.J_2 * cls.mu * cls.R_E**2 / (r**4) * np.sin(i)**2 * np.sin(2 * (omega + theta))
            p_w += - 3 / 2 * cls.J_2 * cls.mu * cls.R_E**2 / (r**4) * np.sin(2 * i) * np.sin(omega + theta)
        
        # * Solar Radiation Pressure perturbation
        
        if SRP:
            
            r_, v_ = ThreeDimensionalOrbit.PF2GEF(ORBITAL_ELEMENTS(h, e, i, Omega, omega, theta))
            
            r_sun, lam, eps = cls.SunPosition(OrbitDetermination.JulianDay2Date(t / 86400))
            
            S = AstronomicalData.S_0 * AstronomicalData.R_0**2 / linalg.norm(r_sun)**2
            
            p_SR = cls.Shadow(r_, r_sun) * S / AstronomicalData.c * B_SRP * 1e-3
            
            Q_Xr = np.array(
                [
                    [-np.sin(Omega) * np.cos(i) * np.sin(omega + theta) + np.cos(Omega) * np.cos(omega + theta),
                     +np.cos(Omega) * np.cos(i) * np.sin(omega + theta) + np.sin(Omega) * np.cos(omega + theta),
                     +np.sin(i) * np.sin(omega + theta)],
                    
                    [-np.sin(Omega) * np.cos(i) * np.cos(omega + theta) - np.cos(Omega) * np.sin(omega + theta),
                     +np.cos(Omega) * np.cos(i) * np.cos(omega + theta) - np.sin(Omega) * np.sin(omega + theta),
                     +np.sin(i) * np.cos(omega + theta)],
                    
                    [+np.sin(Omega) * np.sin(i),
                     -np.cos(Omega) * np.sin(i),
                     +np.cos(i)]
                ])
            
            u = np.matmul(Q_Xr, np.array([np.cos(lam), np.sin(lam) * np.cos(eps), np.sin(lam) * np.sin(eps)]))
            
            # sl, cl = np.sin(lam), np.cos(lam)
            # se, ce = np.sin(eps), np.cos(eps)
            # si, ci = np.sin(i), np.cos(i)
            # sO, cO = np.sin(Omega), np.cos(Omega)
            # su, cu = np.sin(omega + theta), np.cos(omega + theta)
            
            # ur = + sl * ce * cO * ci * su + sl * ce * sO * cu - cl * sO * ci * su + cl * cO * cu + sl * se * si * su
            # us = + sl * ce * cO * ci * cu - sl * ce * sO * su - cl * sO * ci * cu - cl * cO * su + sl * se * si * cu
            # uw = - sl * ce * cO * si + cl * sO * si + sl * se * ci
            
            p_r += -p_SR * u[0]
            p_s += -p_SR * u[1]
            p_w += -p_SR * u[2]
        
        # * Moon Gravity perturbation
        
        if MOON:
            
            r_, v_ = ThreeDimensionalOrbit.PF2GEF(ORBITAL_ELEMENTS(h, e, i, Omega, omega, theta))
            
            r_moon = cls.MoonPosition(OrbitDetermination.JulianDay2Date(t / 86400))
            
            r_moon_sc = r_moon - r_
            
            p = AstronomicalData.GravitationalParameter(CelestialBody.MOON) * (r_moon_sc / linalg.norm(r_moon_sc)**3 - r_moon / linalg.norm(r_moon)**3)
            
            r_hat = r_ / linalg.norm(r_)
            w_hat = np.cross(r_, v_) / linalg.norm(np.cross(r_, v_))
            s_hat = np.cross(w_hat, r_) / linalg.norm(np.cross(w_hat, r_))
            
            p_r += np.dot(p, r_hat)
            p_s += np.dot(p, s_hat)
            p_w += np.dot(p, w_hat)
            
        # * Sun Gravity perturbation
        
        if SUN:
            
            r_, v_ = ThreeDimensionalOrbit.PF2GEF(ORBITAL_ELEMENTS(h, e, i, Omega, omega, theta))
            
            r_sun, lam, eps = cls.SunPosition(OrbitDetermination.JulianDay2Date(t / 86400))
            
            r_sun_sc = r_sun - r_
            
            p = AstronomicalData.GravitationalParameter(CelestialBody.SUN) * (r_sun_sc / linalg.norm(r_sun_sc)**3 - r_sun / linalg.norm(r_sun)**3)
            
            r_hat = r_ / linalg.norm(r_)
            w_hat = np.cross(r_, v_) / linalg.norm(np.cross(r_, v_))
            s_hat = np.cross(w_hat, r_) / linalg.norm(np.cross(w_hat, r_))
            
            p_r += np.dot(p, r_hat)
            p_s += np.dot(p, s_hat)
            p_w += np.dot(p, w_hat)
        
        # * Equations
        
        # da_dt       = 2 * a**2 * v / cls.mu * p_s
        # de_dt       = 1 / v * (2 * (e + np.cos(theta)) * p_s - r / a * np.sin(theta) * p_r)
        # dtheta_dt   = h / r**2 - 1 / (e * v) * (2 * np.sin(theta) * p_s + (2 * e + r / a * np.cos(theta) * p_r))
        # dOmega_dt   = r / (h * np.sin(i)) * np.sin(omega + theta) * p_w
        # di_dt       = r / h * np.cos(omega + theta) * p_w
        # domega_dt   = 1 / (e * v) * (2 * np.sin(theta) * p_s + (2 * e + r / a * np.cos(theta) * p_r)) - r * np.sin(omega + theta) / (h * np.tan(i)) * p_w
        
        dh_dt       = r * p_s
        de_dt       = h / cls.mu * np.sin(theta) * p_r + 1 / (cls.mu * h) * ((h**2 + cls.mu * r) * np.cos(theta) + cls.mu * e * r) * p_s
        dtheta_dt   = h / r**2 + 1 / (e * h) * (h**2 / cls.mu * np.cos(theta) * p_r - (r + h**2 / cls.mu) * np.sin(theta) * p_s)
        dOmega_dt   = r / (h * np.sin(i)) * np.sin(omega + theta) * p_w
        di_dt       = r / h * np.cos(omega + theta) * p_w
        domega_dt   = -1 / (e * h) * (h**2 / cls.mu * np.cos(theta) * p_r - (r + h**2 / cls.mu) * np.sin(theta) * p_s) - r * np.sin(omega + theta) / (h * np.tan(i)) * p_w
        
        return np.array([dh_dt, de_dt, dtheta_dt, dOmega_dt, di_dt, domega_dt])
    
    @classmethod
    def integrateGaussVariationalEquations(cls,
                                           y_0 : np.ndarray,
                                           drag : bool = False,
                                           gravitational : bool = False,
                                           SRP : bool = False,
                                           B : float = 0.0,
                                           B_SRP : float = 0.0,
                                           MOON : bool = False,
                                           SUN : bool = False,
                                           t_0 : float = 0.0,
                                           t_f : float = 0.0,
                                           JD_0 : float = 0.0,
                                           JD_f : float = 0.0,
                                           show : bool = False) -> dict:
        """Integrates the Ordinary Differential Equations for the Gauss variational equations

        Args:
            y_0 (np.ndarray): Initial state [6,1] (h, e, theta, Omega, i, omega)
            drag (bool, optional): True to include drag perturbation. Defaults to False.
            gravitational (bool, optional): True to include gravitational perturbation. Defaults to False.
            SRP (bool, optional): True to include Solar Radiation Pressure perturbation. Defaults to False.
            B (float, optional): Ballistic coefficient (C_D * A / m). Defaults to 0.0.
            B_SRP (float, optional): Ballistic coefficient for SRP (C_R * A_S / m). Defaults to 0.0.
            MOON (bool, optional): True to include Lunar gravity perturbation. Defaults to False.
            SUN (bool, optional): True to include Solar gravity perturbation. Defaults to False.
            t_0 (float, optional): Initial time. Defaults to 0.0.
            t_f (float, optional): Final time. Defaults to 0.0.
            JD_0 (float, optional): Initial Julian day. Defaults to 0.0.
            JD_f (float, optional): Final Julian day. Defaults to 0.0.
            show (bool, optional): True for plotting the trajectory. Defaults to False.
            
        Returns:
            dict: { t: time, y: state[n_states, n_points] }
        """
        
        # * 1.
        
        if t_f < t_0 and JD_0 == 0.0 and JD_f == 0.0: raise CustomException('Invalid integration time')
        
        if JD_f < JD_0 and t_0 == 0.0 and t_f == 0.0: raise CustomException('Invalid integration time')
        
        t_span = [t_0, t_f] if JD_0 == 0.0 and JD_f == 0.0 else [JD_0, JD_f]
            
        integrationResult = solve_ivp(fun=cls.GaussVariationalEquations, t_span=t_span, y0=y_0, method='RK45', args=(drag, gravitational, SRP, MOON, SUN, B, B_SRP), rtol=1e-8, atol=1e-8)
            
        if not integrationResult['success']: CustomException(integrationResult['message'])
        
        t       = (integrationResult['t'] - integrationResult['t'][0]) / 86400
        h       = integrationResult['y'][0, :]
        e       = integrationResult['y'][1, :]
        theta   = integrationResult['y'][2, :] * 180 / np.pi
        Omega   = integrationResult['y'][3, :] * 180 / np.pi
        i       = integrationResult['y'][4, :] * 180 / np.pi
        omega   = integrationResult['y'][5, :] * 180 / np.pi
        a       = h**2 / (cls.mu * (1 - e**2))
        
        # * 2.
        
        if show:
            
            plt.figure()
            
            plt.subplot(231)
            plt.plot(t, a - a[0])
            plt.title('Semi-Major Axis')
            plt.grid()
            
            plt.subplot(232)
            plt.plot(t, e - e[0])
            plt.title('Eccentricity')
            plt.grid()
            
            plt.subplot(233)
            plt.plot(t, i - i[0])
            plt.title('Inclination')
            plt.grid()
            
            plt.subplot(234)
            plt.plot(t, Omega - Omega[0])
            plt.title('Right Ascension of the Ascending Node')
            plt.grid()
            
            plt.subplot(235)
            plt.plot(t, omega - omega[0])
            plt.title('Anomaly of the Perigee')
            plt.grid()
            
            plt.subplot(236)
            plt.plot(t, h - h[0])
            plt.title('Angular Momentum')
            plt.grid()
            
            plt.show()
        
        return dict(t=t, a=a, e=e, i=i, Omega=Omega, omega=omega, h=h)
    
    # ! SECTION 12.9
    
    # ! ALGORITHM 12.2
    @classmethod
    def SunPosition(cls, date : datetime) -> list:
        """Calculates the position of the Sun with respect to the Earth based on the Astronomical Almanac

        Args:
            date (datetime): UTC date

        Returns:
            list: [r_sun GEF, lambda, epsilon]
        """
        
        # * 1. Julian day number
        
        JD = OrbitDetermination.JulianDay(date.year, date.month, date.day, date.hour, date.minute, date.second)
        
        # * 2. Number of days since J2000
        
        n = JD - 2_451_545.0
        
        # * 3. Mean anonaly
        
        M = wrapTo360Deg(357.529 + 0.98560023 * n)
        
        # * 4. Mean solar longitude
        
        L = wrapTo360Deg(280.459 + 0.98564736 * n)
        
        # * 5. Longitude
        
        lam = wrapTo360Deg(L + 1.915 * np.sin(np.deg2rad(M)) + 0.0200 * np.sin(2 * np.deg2rad(M)))
        
        # * 6. Obliquity
        
        eps = wrapTo360Deg(23.439 - 3.56e-7 * n)
        
        # * 7. Earth-Sun unit direction vector
        
        u = np.array([np.cos(np.deg2rad(lam)), np.sin(np.deg2rad(lam)) * np.cos(np.deg2rad(eps)), np.sin(np.deg2rad(lam)) * np.sin(np.deg2rad(eps))])
        
        # * 8. Earth-Sun distance
        
        r_S = (1.00014 - 0.01671 * np.cos(np.deg2rad(M)) - 0.000140 * np.cos(2 * np.deg2rad(M))) * AstronomicalData.AU
        
        # * 9. Sun Geocentric position vector
        
        r_S_ = r_S * u
        
        return [r_S_, np.deg2rad(lam), np.deg2rad(eps)]
    
    # ! ALGORITHM 12.3
    @classmethod
    def Shadow(cls, r_sat : np.ndarray, r_sun : np.ndarray) -> int:
        """Evaluates if the satellite is in the Earth shadow

        Args:
            r_sat (np.ndarray): Satellite position vector
            r_sun (np.ndarray): Sun position vector

        Returns:
            int: Shadow function value (0 -> in shadow, 1 -> in light)
        """
        
        # * 1. Magnitudes
        
        _r_sat_ = linalg.norm(r_sat)
        
        _r_sun_ = linalg.norm(r_sun)
        
        # * 2. Angle between position vectors
        
        theta = np.arccos(np.dot(r_sun, r_sat) / (_r_sun_ * _r_sat_))
        
        # * 3. Inner angles
        
        theta_1 = np.arccos(cls.R_E / _r_sun_)
        
        theta_2 = np.arccos(cls.R_E / _r_sat_)
        
        # * 4. Shadow condition
        
        return 0 if theta_1 + theta_2 <= theta else 1
    
    # ! SECTION 12.10
    
    # ! ALGORITHM 12.4
    @classmethod
    def MoonPosition(cls, date : datetime) -> np.ndarray:
        """Calculates the position of the Moon with respect to the Earth based on the Astronomical Almanac

        Args:
            date (datetime): UTC date

        Returns:
            np.ndarray: r_moon GEF
        """
        
        # * 0. Coefficients
        
        b_0 = 218.32
        c_0 = 481_267.881
        
        a = [ 6.29, -1.27, 0.66, 0.21, -0.19, -0.11 ]
        b = [ 135.0, 259.3, 235.7, 269.9, 357.5, 106.5 ]
        c = [ 477_198.87, -413_335.36, 890_534.22, 954_397.74, 35_999.05, 966_404.03 ]
        
        d = [ 5.13, 0.28, -0.28, -0.17 ]
        e = [ 93.3, 220.2, 318.3, 217.6 ]
        f = [ 483_202.03, 960_400.89, 6_003.15, -407_332.21 ]
        
        g_0 = 0.9508
        
        g = [ 0.0518, 0.0095, 0.0078, 0.0028 ]
        h = [ 135.0, 259.3, 253.7, 269.9 ]
        k = [ 477_198.87, -413_335.38, 890_534.22, 954_397.70 ]
        
        # * 1. Julian day number
        
        JD = OrbitDetermination.JulianDay(date.year, date.month, date.day, date.hour, date.minute, date.second)
        
        # * 2. Number of Julian centuries since J2000
        
        T_0 = (JD - 2_451_545.0) / 36_525
        
        # * 3. Obliquity
        
        eps = wrapTo360Deg(23.439 - 0.0130042 * T_0)
        
        # * 4. Lunar ecliptic longitude
        
        lam = wrapTo360Deg(b_0 + c_0 * T_0 + sum([a[i] * np.sin(np.deg2rad(b[i] + c[i] * T_0)) for i in range(0, 6)]))
        
        # * 5. Lunar ecliptic latitude
        
        delta = wrapTo360Deg(sum([d[i] * np.sin(np.deg2rad(e[i] + f[i] * T_0)) for i in range(0, 4)]))
        
        # * 6. Lunar horizontal parallax
        
        HP = wrapTo360Deg(g_0 + sum([g[i] * np.cos(np.deg2rad(h[i] + k[i] * T_0)) for i in range(0, 4)]))
        
        # * 7. Earth-Moon distance
        
        r_m = cls.R_E / np.sin(np.deg2rad(HP))
        
        # * 8. Earth-Moon unit direction vector
        
        u = np.array([np.cos(np.deg2rad(delta)) * np.cos(np.deg2rad(lam)),
                      np.cos(np.deg2rad(eps)) * np.cos(np.deg2rad(delta)) * np.sin(np.deg2rad(lam)) - np.sin(np.deg2rad(eps)) * np.sin(np.deg2rad(delta)),
                      np.sin(np.deg2rad(eps)) * np.cos(np.deg2rad(delta)) * np.sin(np.deg2rad(lam)) + np.cos(np.deg2rad(eps)) * np.sin(np.deg2rad(delta))])
        
        # * 9. Moon Geocentric position vector
        
        r_m_ = r_m * u
        
        return r_m_
    
if __name__ == '__main__':
    
    print('EXAMPLE 12.1\n')
    #OrbitalPerturbations.integrateRelativeMotionWithAtmosphericDrag(np.array([5873.40, -658.522, 3007.49, -2.89641, 4.09401, 6.14446]), 2.2 * (np.pi * 1**2 / 4) / 100, t_f=110 * 86400, show=True)
    print('-' * 40, '\n')
    
    print('EXAMPLE 12.2\n')
    #OrbitalPerturbations.integrateRelativeMotionWithGravitationalPerturbation(np.array([-2384.46, 5729.01, 3050.46, -7.36138, -2.98997, 1.64354]), t_f=48 * 3600, show=True)
    print('-' * 40, '\n')
    
    print('EXAMPLE 12.6\n')
    #OrbitalPerturbations.integrateGaussVariationalEquations(np.array([55839, 0.17136, np.deg2rad(40), np.deg2rad(45), np.deg2rad(28), np.deg2rad(30)]), drag=False, gravitational=True, B=2.2 * (np.pi * 1**2 / 4) / 100, t_f=48 * 3600, show=True)
    print('-' * 40, '\n')
    
    print('EXAMPLE 12.7\n')
    print(OrbitalPerturbations.SunPosition(datetime(2013, 7, 25, 8, 0, 0)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 12.8\n')
    print(OrbitalPerturbations.Shadow(np.array([2817.899, -14110.473, -7502.672]), np.array([-11_747_041, 139_486_985, 60_472_278])))
    print('-' * 40, '\n')
    
    print('EXAMPLE 12.9\n')
    JD_0 = 2_438_400.5
    
    _date = OrbitDetermination.JulianDay2Date(JD_0)
    
    print(JD_0, OrbitDetermination.JulianDay(_date.year, _date.month, _date.day, _date.hour, _date.minute, _date.second))
    
    _date_f = datetime(_date.year + 3, _date.month, _date.day, _date.hour, _date.minute, _date.second)
    
    JD_f = OrbitDetermination.JulianDay(_date_f.year, _date_f.month, _date_f.day, _date_f.hour, _date_f.minute, _date_f.second)
    
    print(_date, _date_f, JD_0, JD_f)
    
    #OrbitalPerturbations.integrateGaussVariationalEquations(np.array([63383.4, 0.025422, np.deg2rad(343.427), np.deg2rad(45.3812), np.deg2rad(88.3924), np.deg2rad(227.493)]), SRP=True, B_SRP=2 * 2, JD_0=JD_0*86400, JD_f=JD_f*86400, show=True)
    print('-' * 40, '\n')
    
    print('EXAMPLE 12.10\n')
    print(OrbitalPerturbations.MoonPosition(datetime(2013, 7, 25, 8, 0, 0)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 12.11\n')
    JD_0 = 2_454_283.0
    
    _date = OrbitDetermination.JulianDay2Date(JD_0)
    
    print(JD_0, OrbitDetermination.JulianDay(_date.year, _date.month, _date.day, _date.hour, _date.minute, _date.second))
    
    _date_f = _date + timedelta(days=60)
    
    JD_f = OrbitDetermination.JulianDay(_date_f.year, _date_f.month, _date_f.day, _date_f.hour, _date_f.minute, _date_f.second)
    
    print(_date, _date_f, JD_0, JD_f)
    
    oe_LEO = np.array([51591.1, 0.01, np.deg2rad(0), np.deg2rad(0), np.deg2rad(28.5), np.deg2rad(0)])
    oe_HEO = np.array([68084.1, 0.741, np.deg2rad(0), np.deg2rad(0), np.deg2rad(63.4), np.deg2rad(270)])
    oe_GEO = np.array([129640, 0.0001, np.deg2rad(0), np.deg2rad(0), np.deg2rad(1), np.deg2rad(0)])
    
    #OrbitalPerturbations.integrateGaussVariationalEquations(oe_LEO, MOON=True, JD_0=JD_0*86400, JD_f=JD_f*86400, show=True)
    print('-' * 40, '\n')
    
    print('EXAMPLE 12.12\n')
    _date_f = _date + timedelta(days=720)
    
    JD_f = OrbitDetermination.JulianDay(_date_f.year, _date_f.month, _date_f.day, _date_f.hour, _date_f.minute, _date_f.second)
    
    OrbitalPerturbations.integrateGaussVariationalEquations(oe_LEO, SUN=True, JD_0=JD_0*86400, JD_f=JD_f*86400, show=True)
    print('-' * 40, '\n')