from stdafx import *
from AstronomicalData import *

# ! CHAPTER 8 - Interplanetary Trajectories
class InterplanetaryTrajectories:
    
    def __init__(self) -> None: pass
    
    # ! SECTION 8.3
    
    @classmethod
    def SynodicPeriod(cls, departurePlanet : CelestialBody, arrivalPlanet : CelestialBody) -> float:
        """Calculates the Synodic Period for an interplanetary transfer

        Args:
            departurePlanet (CelestialBody): Departure planet
            arrivalPlanet (CelestialBody): Arrival planet

        Returns:
            float: Synodic period
        """
        
        # * 1. Mean motions
        
        n_1 = 2 * np.pi / AstronomicalData.SiderealOrbitalPeriod(departurePlanet)
        n_2 = 2 * np.pi / AstronomicalData.SiderealOrbitalPeriod(arrivalPlanet)
        
        # * 2. Synodic period
        
        T_syn = 2 * np.pi / np.abs(n_2 - n_1)
        
        return T_syn
    
    @classmethod
    def WaitTime(cls, departurePlanet : CelestialBody, arrivalPlanet : CelestialBody) -> list:
        """Calculates the wait time for an interplanetary transfer

        Args:
            departurePlanet (CelestialBody): Departure planet
            arrivalPlanet (CelestialBody): Arrival planet

        Returns:
            list: [Wait time, initial phase angle, final phase angle
        """
        
        # * 1. Transfer ellipse
        
        mu_sun  = AstronomicalData.GravitationalParameter(CelestialBody.SUN)
        R_1     = AstronomicalData.SemiMajorAxis(departurePlanet)
        R_2     = AstronomicalData.SemiMajorAxis(arrivalPlanet)
        n_1     = 2 * np.pi / AstronomicalData.SiderealOrbitalPeriod(departurePlanet)
        n_2     = 2 * np.pi / AstronomicalData.SiderealOrbitalPeriod(arrivalPlanet)
        
        t_12 = np.pi / np.sqrt(mu_sun) * ((R_1 + R_2) / 2)**(3/2)
        
        # * 2. Initial phase angle bewteen planets (departure trip)
        
        phi_0 = np.pi - n_2 * t_12
        
        # * 3. Final phase angle at planet arrival (departure trip)
        
        phi_f = np.pi - n_1 * t_12
        
        # * 4. Initial phase angle bewteen planets (return trip)
        
        phi_0 = - phi_f
        
        # * 5. Wait time
        
        t_wait = -1
        
        N = 0
        
        while t_wait < 0:
            
            t_wait = (-2 * phi_f - 2 * np.pi * N) / (n_2 - n_1) if (n_1 > n_2) else (-2 * phi_f + 2 * np.pi * N) / (n_2 - n_1)
            
            N += 1
        
        return [t_wait, phi_0, phi_f]

if __name__ == '__main__':
    
    print('EXAMPLE 8.1\n')
    print(InterplanetaryTrajectories.SynodicPeriod(CelestialBody.EARTH, CelestialBody.MARS) / 86400)
    print('-' * 40, '\n')
    
    print('EXAMPLE 8.2\n')
    print(InterplanetaryTrajectories.WaitTime(CelestialBody.EARTH, CelestialBody.MARS))
    print('-' * 40, '\n')
    
    print('EXAMPLE 8.3\n')
    print(AstronomicalData.SphereOfInfluence(CelestialBody.EARTH) / 6378)
    print(AstronomicalData.SphereOfInfluence(CelestialBody.MOON))
    print('-' * 40, '\n')