import os
import sys

sys.path.append(os.path.dirname(__file__))

from ThreeDimensionalOrbit import *
from TwoBodyProblem import *
from LagrangeCoefficients import *
from Time import *

# ! CHAPTER 7 - Relative Motion and Rendezvous
class RelativeMotion:
    
    mu = AstronomicalData.GravitationalParameter(CelestialBody.EARTH)
    
    def __init__(self) -> None: pass
    
    # ! SECTION 7.2
    
    # ! ALGORITHM 7.1
    @classmethod
    def calculateKinematicsLVLH(cls, r_T : np.ndarray, v_T : np.ndarray, r_C : np.ndarray, v_C : np.ndarray) -> list:
        """Calculates the relative position, velocity, and acceleration in the LVLH frame

        Args:
            r_T (np.ndarray): Target position vector
            v_T (np.ndarray): Target velocity vector
            r_C (np.ndarray): Chaser position vector
            v_C (np.ndarray): Chaser velocity vector
            
        Returns:
            list: [r_rel, v_rel, a_rel, Omega]
        """
        
        # * 1. Angular momentum
        
        h_T = np.cross(r_T, v_T)
        
        # * 2. Unit vectors
        
        i = r_T / linalg.norm(r_T)
        k = h_T / linalg.norm(h_T)
        j = np.cross(k, i)
        
        # * 3. Orthogonal trasformation matrix
        
        Q_Xx = np.vstack((i, j, k))
        
        # * 4. Angular velocity
        
        Omega = h_T / linalg.norm(r_T)**2
        
        dOmega_dt = - 2 * np.dot(v_T, r_T) / linalg.norm(r_T)**2 * Omega
        
        # * 5. Absolute accelerations
        
        a_T = - cls.mu / linalg.norm(r_T)**3 * r_T
        a_C = - cls.mu / linalg.norm(r_C)**3 * r_C
        
        # * 6. Relative position
        
        r_rel_X = r_C - r_T
        
        # * 7. Relative velocity
        
        v_rel_X = v_C - v_T - np.cross(Omega, r_rel_X)
        
        # * 8. Relative acceleration
        
        a_rel_X = a_C - a_T - np.cross(dOmega_dt, r_rel_X) - np.cross(Omega, np.cross(Omega, r_rel_X)) - 2 * np.cross(Omega, v_rel_X)
        
        # * 9. LVLH kinematics
        
        r_rel_x = np.matmul(Q_Xx, r_rel_X)
        v_rel_x = np.matmul(Q_Xx, v_rel_X)
        a_rel_x = np.matmul(Q_Xx, a_rel_X)
        
        return [r_rel_x, v_rel_x, a_rel_x, np.matmul(Q_Xx, Omega)]
    
    @classmethod
    def calculateKinematicsGEF(cls, r_T : np.ndarray, v_T : np.ndarray, r_rel_x : np.ndarray, v_rel_x : np.ndarray) -> list:
        """Calculates the absolute position and velocity of the Chaser in the Geocentric Equatorial frame

        Args:
            r_T (np.ndarray): Target position vector
            v_T (np.ndarray): Target velocity vector
            r_rel (np.ndarray): Relative position vector
            v_rel (np.ndarray): Relative velocity vector
            
        Returns:
            list: [r_C, v_C]
        """
        
        # * 1. Angular momentum
        
        h_T = np.cross(r_T, v_T)
        
        # * 2. Unit vectors
        
        i = r_T / linalg.norm(r_T)
        k = h_T / linalg.norm(h_T)
        j = np.cross(k, i)
        
        # * 3. Orthogonal trasformation matrix
        
        Q_Xx = np.vstack((i, j, k))
        
        # * 4. Relative position-velocity in GEF
        
        r_rel_X = np.matmul(linalg.inv(Q_Xx), r_rel_x)
        v_rel_X = np.matmul(linalg.inv(Q_Xx), v_rel_x)
        
        # * 5. Angular velocity
        
        Omega = h_T / linalg.norm(r_T)**2
        
        # * 6. Chaser position
        
        r_C  = r_T + r_rel_X
        
        # * 7. Chaser velocity
        
        v_C = v_T  + v_rel_X + np.cross(Omega, r_rel_X)
        
        return [r_C, v_C]
    
    @classmethod
    def plotKinematicsLVLH(cls, r_T : np.ndarray, v_T : np.ndarray, r_C : np.ndarray, v_C : np.ndarray, m : float = 60, n : float = 1000) -> None:
        """Plots the trajectory of the Target w.r.t. the Chaser in the LVLH frame

        Args:
            r_T (np.ndarray): Target position vector
            v_T (np.ndarray): Target velocity vector
            r_C (np.ndarray): Chaser position vector
            v_C (np.ndarray): Chaser velocity vector
            m (float, optional): Multiple of the Target period. Defaults to 60.
            n (float, optional): Number of points to plot. Defaults to 1000.
        """
        
        # * 1. Target period
        
        TwoBodyProblem.mu = cls.mu
        
        parameters = TwoBodyProblem.calculateOrbitalParameters(r_T, v_T)
        
        T_T = parameters.T
        
        # * 2. Target initial time
        
        ThreeDimensionalOrbit.mu = cls.mu
    
        oe = ThreeDimensionalOrbit.calculateOrbitalElements(r_T, v_T)
        
        Time.mu = cls.mu
        
        t_0 = Time.calculateEllipticalOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=T_T, e=parameters.e, theta=oe.theta)
        
        # * 3. Final time
        
        t_f = t_0 + m * T_T
        
        # * 4. Delta time
        
        dt = (t_f - t_0) / n
        
        # * 5. Cycle
        
        times = np.linspace(t_0, t_f, n)
        
        LagrangeCoefficients.mu = cls.mu
        
        x = []
        y = []
        z = []
        
        for t in times:
            
            # * a. LVLH quantities
        
            r_rel, v_rel, a_rel, Omega = cls.calculateKinematicsLVLH(r_T, v_T, r_C, v_C)
            
            x.append(r_rel[0])
            y.append(r_rel[1])
            z.append(r_rel[2])
            
            # * b. Update Target-Chaser vectors
            
            r_T, v_T = LagrangeCoefficients.calculatePositionVelocityByTime(r_T, v_T, dt)
            
            r_C, v_C = LagrangeCoefficients.calculatePositionVelocityByTime(r_C, v_C, dt)
        
        # * 6. Plot
        
        fig = plt.figure()
        
        fig.subplots_adjust(top=1.1, bottom=-0.1)
        
        ax = plt.axes(projection='3d')
        
        ax.plot(x, y, z)
        
        plt.show()
    
    # ! SECTION 7.3
    
    @classmethod
    def linearizedRelativeMotionEquations(cls, t : float, X : np.ndarray) -> np.ndarray:
        """Linearized equations of relative motion

        Args:
            t (float): Time
            X (np.ndarray): State

        Returns:
            np.ndarray: Derivative of state
        """
        
        dx, dy, dz, dv_x, dv_y, dv_z, x, y, z, v_x, v_y, v_z = X
        
        R = np.sqrt(x**2 + y**2 + z**2)
        
        h = np.linalg.norm(np.cross(np.array([x, y, z]), np.array([v_x, v_y, v_z])))
        
        VR = np.dot(np.array([x, y, z]), np.array([v_x, v_y, v_z]))
        
        dX_dt = np.zeros(shape=(12))
        
        dX_dt[0]  = dv_x
        dX_dt[1]  = dv_y
        dX_dt[2]  = dv_z
        dX_dt[3]  = (2 * cls.mu / R**3 + h**2 / R**4) * dx - 2 * VR * h / R**4 * dy + 2 * h / R**2 * dv_y
        dX_dt[4]  = (h**2 / R**4 - cls.mu / R**3) * dy + 2 * VR * h / R**4 * dx - 2 * h / R**2 * dv_x
        dX_dt[5]  = - cls.mu / R**3 * dz
        dX_dt[6]  = v_x
        dX_dt[7]  = v_y
        dX_dt[8]  = v_z
        dX_dt[9]  = - (cls.mu / R**3) * x
        dX_dt[10] = - (cls.mu / R**3) * y
        dX_dt[11] = - (cls.mu / R**3) * z
        
        return dX_dt
    
    @classmethod
    def integrateLinearizedRelativeMotion(cls, y_0 : np.ndarray, t_0 : float = 0.0, t_f : float = 0.0, show : bool = False) -> None:
        """Integrates the Ordinary Differential Equations for the linearized relative motion in the LVLH frame

        Args:
            y_0 (np.ndarray): Initial state
            t_0 (float, optional): Initial time. Defaults to 0.0.
            t_f (float, optional): Final time. Defaults to 0.0.
            show (bool, optional): True for plotting the trajectory. Defaults to False.
        """
        
        # * 1.
        
        if t_f < t_0: raise CustomException('Invalid integration time')
        
        integrationResult = solve_ivp(fun=cls.linearizedRelativeMotionEquations, t_span=[t_0, t_f], y0=y_0, method='RK45', args=(), rtol=1e-8, atol=1e-8)
        
        if not integrationResult['success']: raise CustomException(integrationResult['message'])
        
        dx = integrationResult['y'][0, :]
        dy = integrationResult['y'][1, :]
        
        # * 2.
        
        if show:
        
            plt.figure(figsize=(10, 8))
            
            plt.plot([0, 1.25 * max(dy)], [0, 0], 'k--')        
            plt.plot(dy, dx, label='Orbit')
            
            plt.scatter(dy[0], dx[0], c='g', label='Start')
            plt.scatter(dy[-1], dx[-1], c='r', label='Finish')
            
            plt.title('Relative Trajectory')
            plt.xlabel('$y$ [km]')
            plt.ylabel('$x$ [km]')
            plt.grid(True)
            plt.legend()
            plt.show()
    
    # ! SECTION 7.4
    
    @classmethod
    def ClohessyWiltshireMatrices(cls, n : float, t : float) -> list:
        """Clohessy-Wiltshire matrices

        Args:
            n (float): Target orbit mean motion
            t (float): Final time

        Returns:
            list: [PHI_rr, PHI_rv, PHI_vr, PHI_vv]
        """
        
        PHI_rr = np.array(
            [
                [ 4 - 3 * np.cos(n * t)       , 0 , 0             ],
                [ 6 * (np.sin(n * t) - n * t) , 1 , 0             ],
                [ 0                           , 0 , np.cos(n * t) ]
            ])
        
        PHI_rv = np.array(
            [
                [ 1 / n * np.sin(n * t)       , 2 / n * (1 - np.cos(n * t))             , 0                     ],
                [ 2 / n * (np.cos(n * t) - 1) , 1 / n * (4 * np.sin(n * t) - 3 * n * t) , 0                     ],
                [ 0                           , 0                                       , 1 / n * np.sin(n * t) ]
            ])
        
        PHI_vr = np.array(
            [
                [ 3 * n * np.sin(n * t)       , 0 , 0                   ],
                [ 6 * n * (np.cos(n * t) - 1) , 0 , 0                   ],
                [ 0                           , 0 , - n * np.sin(n * t) ]
            ])
        
        PHI_vv = np.array(
            [
                [ np.cos(n * t)       , 2 * np.sin(n * t)     , 0             ],
                [ - 2 * np.sin(n * t) , 4 * np.cos(n * t) - 3 , 0             ],
                [ 0                   , 0                     , np.cos(n * t) ]
            ])
        
        return [PHI_rr, PHI_rv, PHI_vr, PHI_vv]
    
    @classmethod
    def ClohessyWiltshireEquations(cls, dr_0 : np.ndarray, dv_0 : np.ndarray, n : float, t : float) -> list:
        """Clohessy-Wiltshire equations

        Args:
            dr_0 (np.ndarray): Initial relative position vector
            dv_0 (np.ndarray): Initial relative velocity vector
            n (float): Target orbit mean motion
            t (float): Final time

        Returns:
            list: [dr, dv]
        """
        
        PHI_rr, PHI_rv, PHI_vr, PHI_vv = cls.ClohessyWiltshireMatrices(n, t)
        
        dr = np.matmul(PHI_rr, dr_0) + np.matmul(PHI_rv, dv_0)
        dv = np.matmul(PHI_vr, dr_0) + np.matmul(PHI_vv, dv_0)
        
        return [dr, dv]
    
    # ! SECTION 7.5
    
    @classmethod
    def twoImpulsiveRendezvousManeuver(cls, r_T : np.ndarray, v_T : np.ndarray, r_C : np.ndarray, v_C : np.ndarray, t_f : float, show : bool = False) -> float:
        """Two-Impulse Rendezvous maneuver

        Args:
            r_T (np.ndarray): Target position vector
            v_T (np.ndarray): Target velocity vector
            r_C (np.ndarray): Chaser position vector
            v_C (np.ndarray): Chaser velocity vector
            t_f (float): Maneuver time
            show (bool, optional): True for plotting the trajectory. Defaults to False.

        Returns:
            float: dv
        """
        
        # * 1.
        
        dr_0, dv_0_minus, a_rel, Omega = cls.calculateKinematicsLVLH(r_T, v_T, r_C, v_C)
        
        # * 2.
        
        PHI_rr, PHI_rv, PHI_vr, PHI_vv = cls.ClohessyWiltshireMatrices(linalg.norm(Omega), t_f)
        
        dv_0_plus = - np.matmul(np.matmul(linalg.inv(PHI_rv), PHI_rr), dr_0)
        
        # * 3.
        
        dr_f, dv_f_minus = cls.ClohessyWiltshireEquations(dr_0, dv_0_plus, linalg.norm(Omega), t_f)
        
        # * 4.
        
        dv_f_plus = np.zeros(shape=(3))
        
        # * 5.
        
        dv_tot = linalg.norm(dv_0_plus - dv_0_minus) + linalg.norm(dv_f_plus - dv_f_minus)
        
        # * 6.
        
        if show:
            
            dx = []
            dy = []
            dz = []
            
            for t in np.linspace(0, t_f, 1000):
                
                dr, dv = cls.ClohessyWiltshireEquations(dr_0, dv_0_plus, linalg.norm(Omega), t)
                
                dx.append(dr[0])
                dy.append(dr[1])
                dz.append(dr[2])
            
            plt.figure(figsize=(10, 8))
            
            ax = plt.axes(projection='3d')
        
            xMax = 1.25 * max(np.absolute(dx))
            yMax = 1.25 * max(np.absolute(dy))
            zMax = 1.25 * max(np.absolute(dz))
            
            p = mpatches.Rectangle((-xMax, -yMax), 2 * xMax, 2 * yMax, fc=(0,0,0,0.1), ec=(0,0,0,1), lw=2)
            
            ax.add_patch(p)
            
            art3d.pathpatch_2d_to_3d(p, z=0, zdir='z')
            
            ax.plot([0, xMax], [0, 0], [0, 0], 'k--')
            ax.plot([0, 0], [0, yMax], [0, 0], 'k--')
            ax.plot([0, 0], [0, 0], [0, zMax], 'k--')
            
            ax.plot(dx, dy, dz, label='Orbit')
            
            ax.scatter(dx[0], dy[0], dz[0], c='g', label='Start')
            ax.scatter(dx[-1], dy[-1], dz[-1], c='r', label='Finish')
            
            ax.set_title('Relative Trajectory')
            ax.set_xlabel('$x$ [km]')
            ax.set_ylabel('$y$ [km]')
            ax.set_zlabel('$z$ [km]')            
            plt.legend()
            plt.show()
        
        return dv_tot

if __name__ == '__main__':
    
    r_T, v_T = ThreeDimensionalOrbit.PF2GEF(ORBITAL_ELEMENTS(52059, 0.025724, np.deg2rad(60), np.deg2rad(40), np.deg2rad(30), np.deg2rad(40)))
    
    r_C, v_C = ThreeDimensionalOrbit.PF2GEF(ORBITAL_ELEMENTS(52362, 0.0072696, np.deg2rad(50), np.deg2rad(40), np.deg2rad(120), np.deg2rad(40)))
    
    print('EXAMPLE 7.1\n')
    print(RelativeMotion.calculateKinematicsLVLH(r_T, v_T, r_C, v_C))
    print('-' * 40)
    
    print('EXAMPLE 7.2\n')
    RelativeMotion.plotKinematicsLVLH(r_T, v_T, r_C, v_C, m=10)
    print('-' * 40)
    
    print('EXAMPLE 7.3\n')
    r, v = ThreeDimensionalOrbit.PF2GEF(ORBITAL_ELEMENTS(0, 0.1, np.deg2rad(0), np.deg2rad(0), np.deg2rad(0), np.deg2rad(0), 6678 / (1 - 0.1)))
    parameters = TwoBodyProblem.calculateOrbitalParameters(r, v)
    RelativeMotion.integrateLinearizedRelativeMotion(np.hstack((np.array([-1, 0, 0]), np.array([0, 2 * 2 * np.pi / parameters.T, 0]), r, v)), t_f=5 * parameters.T, show=True)
    print('-' * 40)
    
    print('EXAMPLE 7.4\n')
    r_T = np.array([1622.39, 5305.10, 3717.44])
    v_T = np.array([-7.29936, 0.492329, 2.48304])
    r_C = np.array([1612.75, 5310.19, 3750.33])
    v_C = np.array([-7.35170, 0.463828, 2.46906])
    print(RelativeMotion.twoImpulsiveRendezvousManeuver(r_T, v_T, r_C, v_C, 8 * 3600, True))
    print('-' * 40)
    
    print('EXAMPLE 7.5\n')
    r_T, v_T = ThreeDimensionalOrbit.PF2GEF(ORBITAL_ELEMENTS(0, 0, np.deg2rad(0), np.deg2rad(0), np.deg2rad(0), np.deg2rad(0), 300 + 6378))
    r_C, v_C = RelativeMotion.calculateKinematicsGEF(r_T, v_T, np.array([0, -2, 0]), np.array([0, 0, 0]))
    print(RelativeMotion.twoImpulsiveRendezvousManeuver(r_T, v_T, r_C, v_C, 1.49 * 3600, True))
    print('-' * 40)