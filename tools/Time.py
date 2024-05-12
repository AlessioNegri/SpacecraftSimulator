import os
import sys

sys.path.append(os.path.dirname(__file__))

from stdafx import *

class DirectionType(IntEnum):
    
    MEAN_ANOMALY_TO_TIME = 0
    TIME_TO_MEAN_ANOMALY = 1

# ! CHAPTER 3 - Orbital Position as a Function of Time
class Time():
    
    mu = AstronomicalData.GravitationalParameter(CelestialBody.EARTH)
    
    def __init__(self) -> None: pass
    
    @classmethod
    def setCelestialBody(cls, celestialBody : CelestialBody) -> None:
        """Sets the current celectial body

        Args:
            celestialBody (CelestialBody): Celestial body
        """
        
        cls.mu = AstronomicalData.GravitationalParameter(celestialBody)
    
    # ! SECTION 3.3
    
    @classmethod
    def calculateCircularOrbit(cls, direction : DirectionType, T : float, **kwargs) -> float:
        """Calculates the time / mean anomaly for a circular orbit

        Args:
            direction (DirectionType): MEAN_ANOMALY_TO_TIME - TIME_TO_MEAN_ANOMALY
            T (float): Orbital period
        
        Kwargs:
            theta (float): True anomaly (MEAN_ANOMALY_TO_TIME)
            t (float): Time (TIME_TO_MEAN_ANOMALY)

        Returns:
            float: Mean anomaly / time
        """
        
        if direction == DirectionType.MEAN_ANOMALY_TO_TIME and 'theta'  not in kwargs: raise CustomException('theta not defined')
        if direction == DirectionType.TIME_TO_MEAN_ANOMALY and 't'      not in kwargs: raise CustomException('t not defined')
        
        if direction == DirectionType.MEAN_ANOMALY_TO_TIME:
            
            theta = kwargs.get('theta')
            
            # * 1.
            
            return theta / (2 * np.pi) * T
        
        else:
            
            t = kwargs.get('t')
            
            # * 1.
            
            return (2 * np.pi) / T * t
    
    # ! SECTION 3.4
    
    # ! ALGORITHM 3.1
    @classmethod
    def calculateEllipticalOrbit(cls, direction : DirectionType, T : float, e : float, **kwargs) -> float:
        """Calculates the time / mean anomaly for an elliptical orbit

        Args:
            direction (DirectionType): MEAN_ANOMALY_TO_TIME - TIME_TO_MEAN_ANOMALY
            T (float): Orbital period
            e (float): Eccentricity
            
        Kwargs:
            theta (float): True anomaly (MEAN_ANOMALY_TO_TIME)
            t (float): Time (TIME_TO_MEAN_ANOMALY)

        Returns:
            float: Mean anomaly / time
        """
        
        if direction == DirectionType.MEAN_ANOMALY_TO_TIME and 'theta'  not in kwargs: raise CustomException('theta not defined')
        if direction == DirectionType.TIME_TO_MEAN_ANOMALY and 't'      not in kwargs: raise CustomException('t not defined')
        
        if direction == DirectionType.MEAN_ANOMALY_TO_TIME:
            
            theta = kwargs.get('theta')
            
            # * 1.
            
            E = 2 * np.arctan(np.sqrt((1 - e) / (1 + e)) * np.tan(theta / 2))
            
            # * 2.
            
            M_e = E - e * np.sin(E)
            
            # * 3.
            
            return M_e / (2 * np.pi) * T
        
        else:
            
            t = kwargs.get('t')
            
            # * 1.
            
            M_e = (2 * np.pi) / T * t
            
            f = lambda E, e, M_e: E - e * np.sin(E) - M_e
            
            df = lambda E, e, M_e: 1 - e * np.cos(E)
            
            E0 = (M_e + 0.5 * e) if M_e < np.pi else (M_e - 0.5 * e)
            
            # * 2.
            
            E = newton(f, E0, df, args=(e, M_e))
            
            # * 3.
            
            theta = 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2))
            
            return theta if theta > 0 else (theta + 2 * np.pi)
    
    # ! SECTION 3.5
    
    @classmethod
    def calculateParabolicOrbit(cls, direction : DirectionType, h : float, **kwargs) -> float:
        """Calculates the time / mean anomaly for a parabolic orbit

        Args:
            direction (DirectionType): MEAN_ANOMALY_TO_TIME - TIME_TO_MEAN_ANOMALY
            h (float): Angular momentum
        
        Kwargs:
            theta (float): True anomaly (MEAN_ANOMALY_TO_TIME)
            t (float): Time (TIME_TO_MEAN_ANOMALY)

        Returns:
            float: Mean anomaly / time
        """
        
        if direction == DirectionType.MEAN_ANOMALY_TO_TIME and 'theta'  not in kwargs: raise CustomException('theta not defined')
        if direction == DirectionType.TIME_TO_MEAN_ANOMALY and 't'      not in kwargs: raise CustomException('t not defined')
        
        if direction == DirectionType.MEAN_ANOMALY_TO_TIME:
            
            theta = kwargs.get('theta')
            
            # * 1.
        
            M_p = 1/2 * np.tan(theta / 2) + 1/6 * np.tan(theta / 2)**3
            
            # * 2.
            
            return M_p * h**3 / cls.mu**2
        
        else:
            
            t = kwargs.get('t')
            
            # * 1.
            
            M_p = cls.mu**2 / h**3 * t
            
            # * 2.
            
            return 2 * np.arctan( (3 * M_p + np.sqrt((3 * M_p)**2 + 1))**(1/3) - (3 * M_p + np.sqrt((3 * M_p)**2 + 1))**(-1/3) )
    
    # ! SECTION 3.6
    
    # ! ALGORITHM 3.2
    @classmethod
    def calculateHyperbolicOrbit(cls, direction : DirectionType, h : float, e : float, analyze : bool = False, **kwargs) -> float:
        """Calculates the time / mean anomaly for a parabolic orbit

        Args:
            direction (DirectionType): MEAN_ANOMALY_TO_TIME - TIME_TO_MEAN_ANOMALY
            h (float): Angular momentum
            e (float): Eccentricity
            analyze(bool): True for showing the plot for initial root estimate. Defaults to False.
            
        Kwargs:
            theta (float): True anomaly (MEAN_ANOMALY_TO_TIME)
            t (float): Time (TIME_TO_MEAN_ANOMALY)

        Returns:
            float: Mean anomaly / time
        """
        
        if direction == DirectionType.MEAN_ANOMALY_TO_TIME and 'theta'  not in kwargs: raise CustomException('theta not defined')
        if direction == DirectionType.TIME_TO_MEAN_ANOMALY and 't'      not in kwargs: raise CustomException('t not defined')
        
        if direction == DirectionType.MEAN_ANOMALY_TO_TIME:
            
            theta = kwargs.get('theta')
            
            # * 1.
            
            F = 2 * np.arctanh(np.sqrt((e - 1) / (e + 1)) * np.tan(theta / 2))
            
            # * 2.
            
            M_h = e * np.sinh(F) - F
            
            # * 3.
            
            return M_h * h**3 / cls.mu**2 * (e**2 - 1)**(-3/2)
        
        else:
            
            t = kwargs.get('t')
            
            # * 1.
            
            M_h = cls.mu**2 / h**3 * (e**2 - 1)**(3/2) * t
            
            if analyze:
            
                F = np.linspace(0, 6, 1000)
                
                plt.figure()
                plt.semilogy(F, 2.7696 * np.sinh(F) - F)
                plt.semilogy(F, M_h * np.ones(np.size(F)))
                plt.grid(True)
                plt.xlabel('$F$')
                plt.ylabel('$M_h$')
                plt.show()
            
            # * 2.
            
            f = lambda F, e, M_h: e * np.sinh(F) - F - M_h
            
            df = lambda F, e, M_h: e * np.cosh(F) - 1
            
            F = newton(f, 3.45, df, args=(e, M_h))
            
            # * 3.
            
            theta = 2 * np.arctan(np.sqrt((e + 1) / (e - 1)) * np.tanh(F / 2))
            
            # * 4.
            
            return theta if theta > 0 else (theta + 2 * np.pi)
    
if __name__ == '__main__':
    
    print('EXAMPLE\n')
    print(Time.calculateCircularOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=10000, theta=np.deg2rad(120)))
    print(np.rad2deg(Time.calculateCircularOrbit(DirectionType.TIME_TO_MEAN_ANOMALY, T=10000, t=3333.333333333333)))
    print('-' * 40, '\n')
    
    
    print('EXAMPLE 3.1\n')
    print(Time.calculateEllipticalOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, T=18834, e=0.37255, theta=np.deg2rad(120)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 3.2\n')
    print(np.rad2deg(Time.calculateEllipticalOrbit(DirectionType.TIME_TO_MEAN_ANOMALY, T=18834, e=0.37255, t=10800)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 3.4\n')
    print(Time.calculateParabolicOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, h=79720, theta=np.deg2rad(144.75)) / 3600)
    print(np.rad2deg(Time.calculateParabolicOrbit(DirectionType.TIME_TO_MEAN_ANOMALY, h=79720, t=6 * 3600)))
    print('-' * 40, '\n')
    
    print('EXAMPLE 3.5\n')
    print(Time.calculateHyperbolicOrbit(DirectionType.MEAN_ANOMALY_TO_TIME, h=100170, e=2.7696, theta=np.deg2rad(100)))
    print(np.rad2deg(Time.calculateHyperbolicOrbit(DirectionType.TIME_TO_MEAN_ANOMALY, h=100170, e=2.7696, t=3 * 3600 + 4141.45, analyze=True)))
    print('-' * 40, '\n')