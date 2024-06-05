import os
import sys

sys.path.append(os.path.dirname(__file__))

from stdafx import *

# ! CHAPTER 9 - Rigid Body Dynamics
# ! CHAPTER 4 - Orbits in Three Dimensions
class RigidBodyDynamics:
    
    def __init__(self) -> None: pass
    
    @classmethod
    def setCelestialBody(cls, celestialBody : CelestialBody) -> None:
        """Sets the current celectial body

        Args:
            celestialBody (CelestialBody): Celestial body
        """
        
        pass
    
    # ! SECTION 9.6
    
    @classmethod
    def EulerEquationsEulerAngles(cls, t : float, X : np.ndarray, J : np.ndarray, u : np.ndarray) -> np.ndarray:
        """Eulers's Equations of rigid body dynamics with Euler Angles Kinematics

        Args:
            t (float): Time
            X (np.ndarray): State [6,1]
            J (np.ndarray): Inertia Tensor (principal)
            u (np.ndarray): Control torque

        Returns:
            np.ndarray: Derivative of state
        """
        
        u = np.zeros(shape=(3))
        
        omega_x, omega_y, omega_z, phi, theta, psi = X
        
        dX_dt = np.zeros(shape=(6))
        
        # * Dynamics
        
        dX_dt[0] = (J[2,2] - J[1,1]) / J[0,0] * omega_y * omega_z + u[0] / J[0,0]
        dX_dt[1] = (J[2,2] - J[0,0]) / J[1,1] * omega_z * omega_x + u[1] / J[1,1]
        dX_dt[2] = (J[0,0] - J[1,1]) / J[2,2] * omega_x * omega_y + u[2] / J[2,2]
        
        # * Kinematics
        
        dX_dt[3] = 1 / np.sin(theta) * (omega_x * np.sin(psi) + omega_y * np.cos(psi))
        dX_dt[4] = omega_x * np.cos(psi) - omega_y * np.sin(psi)
        dX_dt[5] = -1 / np.tan(theta) * (omega_x * np.sin(psi) + omega_y * np.cos(psi)) + omega_z
        
        return dX_dt
    
    @classmethod
    def EulerEquationsYawPitchRollAngles(cls, t : float, X : np.ndarray, J : np.ndarray, u : np.ndarray) -> np.ndarray:
        """Eulers's Equations of rigid body dynamics with YawPitchRoll Angles Kinematics

        Args:
            t (float): Time
            X (np.ndarray): State [6,1]
            J (np.ndarray): Inertia Tensor (principal)
            u (np.ndarray): Control torque

        Returns:
            np.ndarray: Derivative of state
        """
        
        u = np.zeros(shape=(3))
        
        omega_x, omega_y, omega_z, phi, theta, psi = X
        
        dX_dt = np.zeros(shape=(6))
        
        # * Dynamics
        
        dX_dt[0] = (J[2,2] - J[1,1]) / J[0,0] * omega_y * omega_z + u[0] / J[0,0]
        dX_dt[1] = (J[2,2] - J[0,0]) / J[1,1] * omega_z * omega_x + u[1] / J[1,1]
        dX_dt[2] = (J[0,0] - J[1,1]) / J[2,2] * omega_x * omega_y + u[2] / J[2,2]
        
        # * Kinematics
        
        dX_dt[3] = 1 / np.cos(theta) * (omega_x * np.sin(psi) + omega_z * np.cos(psi))
        dX_dt[4] = omega_y * np.cos(psi) - omega_z * np.sin(psi)
        dX_dt[5] = omega_x + omega_y * np.tan(theta) * np.sin(psi) + omega_z * np.tan(theta) * np.cos(psi)
        
        return dX_dt
    
    @classmethod
    def EulerEquationsQuaternions(cls, t : float, X : np.ndarray, J : np.ndarray, u : np.ndarray) -> np.ndarray:
        """Eulers's Equations of rigid body dynamics with Quaternions Kinematics

        Args:
            t (float): Time
            X (np.ndarray): State [6,1]
            J (np.ndarray): Inertia Tensor (principal)
            u (np.ndarray): Control torque

        Returns:
            np.ndarray: Derivative of state
        """
        
        omega_x, omega_y, omega_z, q = X
        
        Omega = np.array([[0, omega_z, -omega_y, omega_x],
                          [-omega_z, 0, omega_x, omega_y],
                          [omega_y, -omega_x, 0, omega_z],
                          [-omega_x, -omega_y, -omega_z, 0]])
        
        dX_dt = np.zeros(shape=(7))
        
        # * Dynamics
        
        dX_dt[0] = (J[2,2] - J[1,1]) / J[0,0] * omega_y * omega_z + u[0] / J[0,0]
        dX_dt[1] = (J[2,2] - J[0,0]) / J[1,1] * omega_z * omega_x + u[1] / J[1,1]
        dX_dt[2] = (J[0,0] - J[1,1]) / J[2,2] * omega_x * omega_y + u[2] / J[2,2]
        
        # * Kinematics
        
        dX_dt[3] = 0.5 * np.dot(Omega[0,:], q)
        dX_dt[4] = 0.5 * np.dot(Omega[1,:], q)
        dX_dt[5] = 0.5 * np.dot(Omega[2,:], q)
        dX_dt[6] = 0.5 * np.dot(Omega[3,:], q)
        
        return dX_dt
    
    @classmethod
    def integrateAttitudeDynamics(cls, y_0 : np.ndarray, t_0 : float = 0.0, t_f : float = 0.0, show : bool = False) -> dict:
        """Integrates the Ordinary Differential Equations for the attitude dynamics

        Args:
            y_0 (np.ndarray): Initial state [6,1]
            t_0 (float, optional): Initial time. Defaults to 0.0.
            t_f (float, optional): Final time. Defaults to 0.0.
            show (bool, optional): True for plotting the kinematics. Defaults to False.
            
        Returns:
            dict: { t: time, y: state[n_states, n_points] }
        """
        
        # * 1.
        
        if t_f < t_0: raise CustomException('Invalid integration time')
        
        J = np.array([[12e-4, 0, 0], [0, 12e-4, 0], [0, 0, 4.5e-4]])
        
        u = np.array([0, 0, 0])
        
        integrationResult = solve_ivp(fun=cls.EulerEquationsEulerAngles, t_span=[t_0, t_f], y0=y_0, method='RK45', args=(J, u), rtol=1e-8, atol=1e-8)
        
        if not integrationResult['success']: CustomException(integrationResult['message'])
        
        vfunc = np.vectorize(wrapTo2Pi)
        
        t       = integrationResult['t']
        omega_x = integrationResult['y'][0, :]
        omega_y = integrationResult['y'][1, :]
        omega_z = integrationResult['y'][2, :]
        phi     = np.rad2deg(vfunc(integrationResult['y'][3, :]))
        theta   = np.rad2deg(vfunc(integrationResult['y'][4, :]))
        psi     = np.rad2deg(vfunc(integrationResult['y'][5, :]))
        
        # * 2.
        
        if show:
            
            plt.figure(figsize=(10, 8))
            
            plt.plot(t, phi, label='$\phi$')
            plt.plot(t, theta, label='$\\theta$')
            plt.plot(t, psi, label='$\psi$')
            
            plt.title('Attitude Dynamics')
            plt.xlabel('$t$ [s]')
            plt.ylabel('Euler Angle [deg]')
            
            plt.grid()
            plt.legend()
            plt.show()
        
        return dict(t=integrationResult['t'], y=integrationResult['y'], dt=np.abs(integrationResult['t'][-1] - integrationResult['t'][0]))
    
    # ! SECTION 9.9
    
    # ! ALGORITHM 4.3
    @classmethod
    def EulerAnglesFromDCM(cls, Q : np.ndarray) -> np.ndarray:
        """Direction Cosine Matrix --> Euler Angles

        Args:
            Q (np.ndarray): Direction Cosine Matrix

        Returns:
            np.ndarray: Euler Angles
        """
        
        # * 1. Precession angle
        
        phi = np.arctan2(Q[2,0], -Q[2,1])
        
        if phi < 0: phi += 2 * np.pi
        
        # * 2. Nutation angle
        
        theta = np.arccos(Q[2,2])
        
        # * 3. Spin angle
        
        psi = np.arctan2(Q[0,2], Q[1,2])
        
        if psi < 0: psi += 2 * np.pi
        
        # * 4. Euler angles
        
        return np.array([phi, theta, psi])
    
    @classmethod
    def DCMFromEulerAngles(cls, phi : float, theta : float, psi : float) -> np.ndarray:
        """Euler Angles --> Direction Cosine Matrix

        Args:
            phi (float): Precession angle
            theta (float): Nutation angle
            psi (float): Spin angle

        Returns:
            np.ndarray: Direction Cosine Matrix
        """
        
        Q_11 = -np.sin(phi) * np.cos(theta) * np.sin(psi) + np.cos(phi) * np.cos(psi)
        Q_12 = +np.cos(phi) * np.cos(theta) * np.sin(psi) + np.sin(phi) * np.cos(psi)
        Q_13 = +np.sin(theta) * np.sin(psi)
        
        Q_21 = -np.sin(phi) * np.cos(theta) * np.cos(psi) - np.cos(phi) * np.sin(psi)
        Q_22 = +np.cos(phi) * np.cos(theta) * np.cos(psi) - np.sin(phi) * np.sin(psi)
        Q_23 = +np.sin(theta) * np.cos(psi)
        
        Q_31 = +np.sin(phi) * np.sin(theta)
        Q_32 = -np.cos(phi) * np.sin(theta)
        Q_33 = +np.cos(theta)
        
        Q = np.array([[Q_11, Q_12, Q_13], [Q_21, Q_22, Q_23], [Q_31, Q_32, Q_33]])
        
        return Q

    # ! SECTION 9.10
    
    # ! ALGORITHM 4.4
    @classmethod
    def YawPitchRollAnglesFromDCM(cls, Q : np.ndarray) -> np.ndarray:
        """Direction Cosine Matrix --> Yaw-Pitch-Roll Angles

        Args:
            Q (np.ndarray): Direction Cosine Matrix

        Returns:
            np.ndarray: Yaw-Pitch-Roll Angles
        """
        
        # * 1. Precession angle
        
        phi = np.arctan2(Q[0,1], Q[0,0])
        
        if phi < 0: phi += 2 * np.pi
        
        # * 2. Nutation angle
        
        theta = np.arcsin(-Q[0,2])
        
        # * 3. Spin angle
        
        psi = np.arctan2(Q[1,2], Q[2,2])
        
        if psi < 0: psi += 2 * np.pi
        
        # * 4. Euler angles
        
        return np.array([phi, theta, psi])
    
    @classmethod
    def DCMFromYawPitchRollAngles(cls, phi : float, theta : float, psi : float) -> np.ndarray:
        """Yaw-Pitch-Roll Angles --> Direction Cosine Matrix

        Args:
            phi (float): Yaw angle
            theta (float): Pitch angle
            psi (float): Roll angle

        Returns:
            np.ndarray: Direction Cosine Matrix
        """
        
        Q_11 = +np.cos(phi) * np.cos(theta)
        Q_12 = +np.sin(phi) * np.cos(theta)
        Q_13 = -np.sin(theta)
        
        Q_21 = +np.cos(phi) * np.sin(theta) * np.sin(psi) - np.sin(phi) * np.cos(psi)
        Q_22 = +np.sin(phi) * np.sin(theta) * np.sin(psi) + np.cos(phi) * np.cos(psi)
        Q_23 = +np.cos(theta) * np.sin(psi)
        
        Q_31 = +np.cos(phi) * np.sin(theta) * np.cos(psi) + np.sin(phi) * np.sin(psi)
        Q_32 = +np.sin(phi) * np.sin(theta) * np.cos(psi) - np.cos(phi) * np.sin(psi)
        Q_33 = +np.cos(theta) * np.cos(psi)
        
        Q = np.array([[Q_11, Q_12, Q_13], [Q_21, Q_22, Q_23], [Q_31, Q_32, Q_33]])
        
        return Q

    # ! SECTION 9.11
    
    # ! ALGORITHM 9.1
    @classmethod
    def DCMFromQuaternions(cls, q : np.ndarray) -> np.ndarray:
        """Quaternions --> Direction Cosine Matrix

        Args:
            q (np.ndarray): Quaternions

        Returns:
            np.ndarray: Direction Cosine Matrix
        """
        
        q_1, q_2, q_3, q_4 = q
        
        Q_11 = q_1**2 - q_2**2 - q_3**2 + q_4**2
        Q_12 = 2 * (q_1 * q_2 + q_3 * q_4)
        Q_13 = 2 * (q_1 * q_3 - q_2 * q_4)
        
        Q_21 = 2 * (q_1 * q_2 - q_3 * q_4)
        Q_22 = -q_1**2 + q_2**2 - q_3**2 + q_4**2
        Q_23 = 2 * (q_2 * q_3 + q_1 * q_4)
        
        Q_31 = 2 * (q_1 * q_3 + q_2 * q_4)
        Q_32 = 2 * (q_2 * q_3 - q_1 * q_4)
        Q_33 = -q_1**2 - q_2**2 + q_3**2 + q_4**2
        
        Q = np.array([[Q_11, Q_12, Q_13], [Q_21, Q_22, Q_23], [Q_31, Q_32, Q_33]])
        
        return Q
    
    # ! ALGORITHM 9.2
    @classmethod
    def QuaternionsFromDCM(cls, Q : np.ndarray) -> np.ndarray:
        """Direction Cosine Matrix --> Quaternions

        Args:
            Q (np.ndarray): Direction Cosine Matrix

        Returns:
            np.ndarray: Quaternions
        """
        
        # * 1. Symmetric Matrix
        
        K_11 = Q[0,0] - Q[1,1] - Q[2,2]
        K_12 = Q[1,0] + Q[0,1]
        K_13 = Q[2,0] + Q[0,2]
        K_14 = Q[1,2] - Q[2,1]
        
        K_21 = Q[1,0] + Q[0,1]
        K_22 = -Q[0,0] + Q[1,1] - Q[2,2]
        K_23 = Q[2,1] + Q[1,2]
        K_24 = Q[2,0] - Q[0,2]
        
        K_31 = Q[2,0] + Q[0,2]
        K_32 = Q[2,1] + Q[1,2]
        K_33 = -Q[0,0] - Q[1,1] + Q[2,2]
        K_34 = Q[0,1] - Q[1,0]
        
        K_41 = Q[1,2] - Q[2,1]
        K_42 = Q[2,0] - Q[0,2]
        K_43 = Q[0,1] - Q[1,0]
        K_44 = Q[0,0] + Q[1,1] + Q[2,2]
        
        K = 1/3 * np.array([[K_11, K_12, K_13, K_14], [K_21, K_22, K_23, K_24], [K_31, K_32, K_33, K_34], [K_41, K_42, K_43, K_44]])
        
        # * 2. Eigenvalue Problem
        
        l, v = linalg.eig(K)
        
        index = np.argmax(l)
        
        q = v[:, index]
        
        return q
    
if __name__ == '__main__':
    
    print('EXAMPLE 9.17\n')
    print(np.rad2deg(RigidBodyDynamics.EulerAnglesFromDCM(np.array([[-0.32175, +0.89930, -0.29620],
                                                                    [+0.57791, -0.061275, -0.81380],
                                                                    [-0.75000, -0.43301, -0.5000]]))))
    print(RigidBodyDynamics.DCMFromEulerAngles(np.deg2rad(300), np.deg2rad(120), np.deg2rad(200)))
    
    print(np.rad2deg(RigidBodyDynamics.YawPitchRollAnglesFromDCM(np.array([[-0.32175, +0.89930, -0.29620],
                                                                           [+0.57791, -0.061275, -0.81380],
                                                                           [-0.75000, -0.43301, -0.5000]]))))
    print(RigidBodyDynamics.DCMFromYawPitchRollAngles(np.deg2rad(109.69), np.deg2rad(17.230), np.deg2rad(238.43)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 9.22\n')
    print(RigidBodyDynamics.QuaternionsFromDCM(np.array([[+0, +0, -1],
                                                         [+0.93969, +0.342020, +0],
                                                         [0.34202, -0.93969, +0]])))
    print(RigidBodyDynamics.DCMFromQuaternions(np.array([0.40558, 0.57923, -0.40558, 0.57923])))
    print('-' * 40, '\n')
    
    print('PROVA\n')
    y_0 = np.array([0.1, 0, 0, np.deg2rad(99), np.deg2rad(60), np.deg2rad(10)])
    RigidBodyDynamics.integrateAttitudeDynamics(y_0, 0, 100, show=True)
    print('-' * 40, '\n')