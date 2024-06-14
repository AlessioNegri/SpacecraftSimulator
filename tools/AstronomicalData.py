import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))

from enum import IntEnum

class CelestialBody(IntEnum):
    
    SUN     = 0
    MERCURY = 1
    VENUS   = 2
    EARTH   = 3
    MOON    = 4
    MARS    = 5
    JUPITER = 6
    SATURN  = 7
    URANUS  = 8
    NEPTUNE = 9
    PLUTO   = 10

class Planet(IntEnum):
    
    MERCURY = 0
    VENUS   = 1
    EARTH   = 2
    MARS    = 3
    JUPITER = 4
    SATURN  = 5
    URANUS  = 6
    NEPTUNE = 7
    PLUTO   = 8
    
def celestialBodyFromPlanet(planet : Planet) -> CelestialBody:
    """Converts the Planet enum to the CelestialBody enum

    Args:
        planet (Planet): Planet

    Returns:
        CelestialBody: Celestial body
    """
    
    match (planet):
        
        case Planet.MERCURY:    return CelestialBody.MERCURY
        case Planet.VENUS:      return CelestialBody.VENUS
        case Planet.EARTH:      return CelestialBody.EARTH
        case Planet.MARS:       return CelestialBody.MARS
        case Planet.JUPITER:    return CelestialBody.JUPITER
        case Planet.SATURN:     return CelestialBody.SATURN
        case Planet.URANUS:     return CelestialBody.URANUS
        case Planet.NEPTUNE:    return CelestialBody.NEPTUNE
        case Planet.PLUTO:      return CelestialBody.PLUTO
        case _:                 return CelestialBody.EARTH

    
def celestialBodyFromIndex(index : int) -> CelestialBody:
    """Converts the index to the CelestialBody enum

    Args:
        index (int): Index

    Returns:
        CelestialBody: Celestial body
    """
    
    match (index):
            
        case 0:  return CelestialBody.SUN
        case 1:  return CelestialBody.MERCURY
        case 2:  return CelestialBody.VENUS
        case 3:  return CelestialBody.EARTH
        case 4:  return CelestialBody.MOON
        case 5:  return CelestialBody.MARS
        case 6:  return CelestialBody.JUPITER
        case 7:  return CelestialBody.SATURN
        case 8:  return CelestialBody.URANUS
        case 9:  return CelestialBody.NEPTUNE
        case 10: return CelestialBody.PLUTO
        case _:  return CelestialBody.EARTH
        
def indexFromCelestialBody(celestialBody : CelestialBody) -> int:
    """Converts the CelestialBody enum to the index

    Args:
        celestialBody (CelestialBody): Celestial body

    Returns:
        int: Index
    """
    
    match (celestialBody):
        
        case CelestialBody.SUN:     return 0
        case CelestialBody.MERCURY: return 1
        case CelestialBody.VENUS:   return 2
        case CelestialBody.EARTH:   return 3
        case CelestialBody.MOON:    return 4
        case CelestialBody.MARS:    return 5
        case CelestialBody.JUPITER: return 6
        case CelestialBody.SATURN:  return 7
        case CelestialBody.URANUS:  return 8
        case CelestialBody.NEPTUNE: return 9
        case CelestialBody.PLUTO:   return 10
        case _:                     return 3

def planetFromIndex(index : int) -> Planet:
    """Converts the index to the Planet enum

    Args:
        index (int): Index

    Returns:
        Planet: Planet
    """
    
    match (index):
            
        case 0: return Planet.MERCURY
        case 1: return Planet.VENUS
        case 2: return Planet.EARTH
        case 3: return Planet.MARS
        case 4: return Planet.JUPITER
        case 5: return Planet.SATURN
        case 6: return Planet.URANUS
        case 7: return Planet.NEPTUNE
        case 8: return Planet.PLUTO
        case _: return Planet.EARTH
        
def indexFromPlanet(planet : Planet) -> int:
    """Converts the Planet enum to the index

    Args:
        planet (Planet): Planet

    Returns:
        int: Index
    """
    
    match (planet):
        
        case Planet.MERCURY: return 0
        case Planet.VENUS:   return 1
        case Planet.EARTH:   return 2
        case Planet.MARS:    return 3
        case Planet.JUPITER: return 4
        case Planet.SATURN:  return 5
        case Planet.URANUS:  return 6
        case Planet.NEPTUNE: return 7
        case Planet.PLUTO:   return 8
        case _:              return 2


class AstronomicalData():
    
    G = 6.6743015e-20 # ? Universal Gravitational Constant [km^3 / kg s^2]
    
    AU = 149_597_870.707 # ? Astronimical Unit [km]
    
    c = 299_792_458 # ? Speed of Light [m / s]
    
    S_0 = 5.670e-8 * 5777**4 # ? Radiated power intensity from the Sun photosphere [W / m**2]
    
    R_0 = 696000 # ? Photosphere radius [km]
    
    def __init__(self) -> None: pass
    
    @classmethod
    def EquatiorialRadius(cls, celestialBody : CelestialBody) -> float:
        """Equatorial Radius

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: R_E [km]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 696_300
            case CelestialBody.MERCURY: return 2_439.700
            case CelestialBody.VENUS:   return 6_051.800
            case CelestialBody.EARTH:   return 6_378.137
            case CelestialBody.MOON:    return 1_738.100
            case CelestialBody.MARS:    return 3_396.200
            case CelestialBody.JUPITER: return 71_492
            case CelestialBody.SATURN:  return 60_268
            case CelestialBody.URANUS:  return 25_559
            case CelestialBody.NEPTUNE: return 24_764
            case CelestialBody.PLUTO:   return 1_188.300
            case _:                     return 0
    
    @classmethod
    def Flattening(cls, celestialBody : CelestialBody) -> float:
        """Flattening

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: f []
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0.000_050
            case CelestialBody.MERCURY: return 0.000_900
            case CelestialBody.VENUS:   return 0.000_000
            case CelestialBody.EARTH:   return 1 / 298.257_222_101 # 0.003_352_811
            case CelestialBody.MOON:    return 0.001_200
            case CelestialBody.MARS:    return 0.005_890
            case CelestialBody.JUPITER: return 0.064_870
            case CelestialBody.SATURN:  return 0.097_960
            case CelestialBody.URANUS:  return 0.022_900
            case CelestialBody.NEPTUNE: return 0.017_100
            case CelestialBody.PLUTO:   return 0.010_000
            case _:                     return 0
    
    @classmethod
    def SecondZonalHarmonics(cls, celestialBody : CelestialBody) -> float:
        """Second Zonal Harmonics

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: J_2 []
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0
            case CelestialBody.MERCURY: return 60e-6
            case CelestialBody.VENUS:   return 4.458e-6
            case CelestialBody.EARTH:   return 1.08263e-3
            case CelestialBody.MOON:    return 202.7e-6
            case CelestialBody.MARS:    return 1.96045e-3
            case CelestialBody.JUPITER: return 14.736e-3
            case CelestialBody.SATURN:  return 16.298e-3
            case CelestialBody.URANUS:  return 3.34343e-3
            case CelestialBody.NEPTUNE: return 3.411e-3
            case CelestialBody.PLUTO:   return 0
            case _:                     return 0
    
    @classmethod
    def SiderealOrbitalPeriod(cls, celestialBody : CelestialBody) -> float:
        """Sidereal Orbital Period

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: T [s]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0
            case CelestialBody.MERCURY: return     87.969_100_000 * 86400
            case CelestialBody.VENUS:   return    224.701_000_000 * 86400
            case CelestialBody.EARTH:   return    365.256_363_004 * 86400
            case CelestialBody.MOON:    return     27.321_661_000 * 86400
            case CelestialBody.MARS:    return    686.980_000_000 * 86400
            case CelestialBody.JUPITER: return  4_332.590_000_000 * 86400
            case CelestialBody.SATURN:  return 10_755.700_000_000 * 86400
            case CelestialBody.URANUS:  return 30_688.500_000_000 * 86400
            case CelestialBody.NEPTUNE: return 60_195.000_000_000 * 86400
            case CelestialBody.PLUTO:   return 90_560.000_000_000 * 86400
            case _:                     return 0
            
    @classmethod
    def AngularVelocity(cls, celestialBody : CelestialBody) -> float:
        """Angular Velocity

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: omega [rad / s]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0
            case CelestialBody.MERCURY: return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody)
            case CelestialBody.VENUS:   return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody)
            case CelestialBody.EARTH:   return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody)
            case CelestialBody.MOON:    return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody)
            case CelestialBody.MARS:    return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody)
            case CelestialBody.JUPITER: return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody)
            case CelestialBody.SATURN:  return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody)
            case CelestialBody.URANUS:  return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody)
            case CelestialBody.NEPTUNE: return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody)
            case CelestialBody.PLUTO:   return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody)
            case _:                     return 0
    
    @classmethod
    def GroundTrackAngularVelocity(cls, celestialBody : CelestialBody) -> float:
        """Ground Track Angular Velocity

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: omega [rad / s]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0
            case CelestialBody.MERCURY: return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody) + 2 * np.pi / 86400
            case CelestialBody.VENUS:   return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody) + 2 * np.pi / 86400
            case CelestialBody.EARTH:   return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody) + 2 * np.pi / 86400
            case CelestialBody.MOON:    return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody) + 2 * np.pi / 86400
            case CelestialBody.MARS:    return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody) + 2 * np.pi / 86400
            case CelestialBody.JUPITER: return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody) + 2 * np.pi / 86400
            case CelestialBody.SATURN:  return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody) + 2 * np.pi / 86400
            case CelestialBody.URANUS:  return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody) + 2 * np.pi / 86400
            case CelestialBody.NEPTUNE: return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody) + 2 * np.pi / 86400
            case CelestialBody.PLUTO:   return 2 * np.pi / cls.SiderealOrbitalPeriod(celestialBody) + 2 * np.pi / 86400
            case _:                     return 0
    
    @classmethod
    def Mass(cls, celestialBody : CelestialBody) -> float:
        """Mass

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: m [kg]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 1.9885e30
            case CelestialBody.MERCURY: return 3.3011e23
            case CelestialBody.VENUS:   return 4.8675e24
            case CelestialBody.EARTH:   return 5.972168e24
            case CelestialBody.MOON:    return 7.342e22
            case CelestialBody.MARS:    return 6.4171e23
            case CelestialBody.JUPITER: return 1.8982e27
            case CelestialBody.SATURN:  return 5.6834e26
            case CelestialBody.URANUS:  return 8.6810e25
            case CelestialBody.NEPTUNE: return 1.02409e26
            case CelestialBody.PLUTO:   return 1.303e22
            case _:                     return 0
    
    @classmethod
    def Gravity(cls, celestialBody : CelestialBody, km : bool = False) -> float:
        """Gravity

        Args:
            celestialBody (CelestialBody): Celestial body
            km (bool, optional): True for gravity in [km / s^2]. Defaults to False.

        Returns:
            float: g [m / s^2]
        """
        
        conversion = 1e-3 if km else 1
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 274 * conversion
            case CelestialBody.MERCURY: return 3.700 * conversion
            case CelestialBody.VENUS:   return 8.870 * conversion
            case CelestialBody.EARTH:   return 9.806_650 * conversion
            case CelestialBody.MOON:    return 1.622 * conversion
            case CelestialBody.MARS:    return 3.720_760 * conversion
            case CelestialBody.JUPITER: return 24.790 * conversion
            case CelestialBody.SATURN:  return 10.440 * conversion
            case CelestialBody.URANUS:  return 8.690 * conversion
            case CelestialBody.NEPTUNE: return 11.150 * conversion
            case CelestialBody.PLUTO:   return 0.620 * conversion
            case _:                     return 0 * conversion
    
    @classmethod
    def SphereOfInfluence(cls, celestialBody : CelestialBody) -> float:
        """Sphere Of Influence

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: SOI [km]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0
            case CelestialBody.MERCURY: return cls.SemiMajorAxis(celestialBody) * (cls.Mass(celestialBody) / cls.Mass(CelestialBody.SUN))**(2/5)
            case CelestialBody.VENUS:   return cls.SemiMajorAxis(celestialBody) * (cls.Mass(celestialBody) / cls.Mass(CelestialBody.SUN))**(2/5)
            case CelestialBody.EARTH:   return cls.SemiMajorAxis(celestialBody) * (cls.Mass(celestialBody) / cls.Mass(CelestialBody.SUN))**(2/5)
            case CelestialBody.MOON:    return cls.SemiMajorAxis(celestialBody) * (cls.Mass(celestialBody) / cls.Mass(CelestialBody.EARTH))**(2/5)
            case CelestialBody.MARS:    return cls.SemiMajorAxis(celestialBody) * (cls.Mass(celestialBody) / cls.Mass(CelestialBody.SUN))**(2/5)
            case CelestialBody.JUPITER: return cls.SemiMajorAxis(celestialBody) * (cls.Mass(celestialBody) / cls.Mass(CelestialBody.SUN))**(2/5)
            case CelestialBody.SATURN:  return cls.SemiMajorAxis(celestialBody) * (cls.Mass(celestialBody) / cls.Mass(CelestialBody.SUN))**(2/5)
            case CelestialBody.URANUS:  return cls.SemiMajorAxis(celestialBody) * (cls.Mass(celestialBody) / cls.Mass(CelestialBody.SUN))**(2/5)
            case CelestialBody.NEPTUNE: return cls.SemiMajorAxis(celestialBody) * (cls.Mass(celestialBody) / cls.Mass(CelestialBody.SUN))**(2/5)
            case CelestialBody.PLUTO:   return cls.SemiMajorAxis(celestialBody) * (cls.Mass(celestialBody) / cls.Mass(CelestialBody.SUN))**(2/5)
            case _:                     return 0
    
    @classmethod
    def SemiMajorAxis(cls, celestialBody : CelestialBody) -> float:
        """Semi-major axis

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: a [km]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0
            case CelestialBody.MERCURY: return 0.387_098 * cls.AU
            case CelestialBody.VENUS:   return 0.723_332 * cls.AU
            case CelestialBody.EARTH:   return 149_598_023
            case CelestialBody.MOON:    return 0.002_570 * cls.AU
            case CelestialBody.MARS:    return 1.523_680_550 * cls.AU
            case CelestialBody.JUPITER: return 5.203_800 * cls.AU
            case CelestialBody.SATURN:  return 9.582_600 * cls.AU
            case CelestialBody.URANUS:  return 19.191_260 * cls.AU
            case CelestialBody.NEPTUNE: return 30.070 * cls.AU
            case CelestialBody.PLUTO:   return 39.482 * cls.AU
            case _:                     return 0
    
    @classmethod
    def Eccentricity(cls, celestialBody : CelestialBody) -> float:
        """Eccentricity

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: e []
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0
            case CelestialBody.MERCURY: return 0.205_630
            case CelestialBody.VENUS:   return 0.006_772
            case CelestialBody.EARTH:   return 0.016_708_600
            case CelestialBody.MOON:    return 0.054_900
            case CelestialBody.MARS:    return 0.093_400
            case CelestialBody.JUPITER: return 0.048_900
            case CelestialBody.SATURN:  return 0.056_500
            case CelestialBody.URANUS:  return 0.047_170
            case CelestialBody.NEPTUNE: return 0.008_678
            case CelestialBody.PLUTO:   return 0.2488
            case _:                     return 0
    
    @classmethod
    def Inclination(cls, celestialBody : CelestialBody) -> float:
        """Inclination

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: i [rad]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0
            case CelestialBody.MERCURY: return np.deg2rad(7.005)
            case CelestialBody.VENUS:   return np.deg2rad(3.394_58)
            case CelestialBody.EARTH:   return np.deg2rad(0.00)
            case CelestialBody.MOON:    return np.deg2rad(5.145)
            case CelestialBody.MARS:    return np.deg2rad(1.850)
            case CelestialBody.JUPITER: return np.deg2rad(1.303)
            case CelestialBody.SATURN:  return np.deg2rad(2.485)
            case CelestialBody.URANUS:  return np.deg2rad(0.773)
            case CelestialBody.NEPTUNE: return np.deg2rad(1.770)
            case CelestialBody.PLUTO:   return np.deg2rad(17.16)
            case _:                     return 0
    
    @classmethod
    def RightAscensionAscendingNode(cls, celestialBody : CelestialBody) -> float:
        """Right Ascension of the Ascending Node

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: Omega [rad]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0
            case CelestialBody.MERCURY: return np.deg2rad(48.331)
            case CelestialBody.VENUS:   return np.deg2rad(76.680)
            case CelestialBody.EARTH:   return np.deg2rad(-11.260_640)
            case CelestialBody.MOON:    return np.deg2rad(0)
            case CelestialBody.MARS:    return np.deg2rad(49.578_540)
            case CelestialBody.JUPITER: return np.deg2rad(100.464)
            case CelestialBody.SATURN:  return np.deg2rad(113.665)
            case CelestialBody.URANUS:  return np.deg2rad(74.006)
            case CelestialBody.NEPTUNE: return np.deg2rad(131.783)
            case CelestialBody.PLUTO:   return np.deg2rad(110.299)
            case _:                     return 0
    
    @classmethod
    def ArgumentPerihelion(cls, celestialBody : CelestialBody) -> float:
        """Argument of Perihelion

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: omega [rad]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 0
            case CelestialBody.MERCURY: return np.deg2rad(29.124)
            case CelestialBody.VENUS:   return np.deg2rad(54.884)
            case CelestialBody.EARTH:   return np.deg2rad(114.207_830)
            case CelestialBody.MOON:    return np.deg2rad(0)
            case CelestialBody.MARS:    return np.deg2rad(286.500)
            case CelestialBody.JUPITER: return np.deg2rad(273.867)
            case CelestialBody.SATURN:  return np.deg2rad(339.392)
            case CelestialBody.URANUS:  return np.deg2rad(96.998_857)
            case CelestialBody.NEPTUNE: return np.deg2rad(273.187)
            case CelestialBody.PLUTO:   return np.deg2rad(113.834)
            case _:                     return 0
    
    @classmethod
    def GravitationalParameter(cls, celestialBody : CelestialBody) -> float:
        """Gravitational Parameter

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            float: Gravitational Parameter [km^3 / s^2]
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return 132_712_440_018.9
            case CelestialBody.MERCURY: return 22032.9
            case CelestialBody.VENUS:   return 324_859.9
            case CelestialBody.EARTH:   return 398_600.441_88
            case CelestialBody.MOON:    return 4_904.869_59
            case CelestialBody.MARS:    return 42_828.372
            case CelestialBody.JUPITER: return 126_686_534.9
            case CelestialBody.SATURN:  return 37_931_187.9
            case CelestialBody.URANUS:  return 5_793_939.9
            case CelestialBody.NEPTUNE: return 6_836_529.9
            case CelestialBody.PLUTO:   return 871.9
            case _:                     return 0

    @classmethod
    def Texture(cls, celestialBody : CelestialBody) -> str:
        """Texture

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            str: Texture path
        """
        
        match (celestialBody):
            
            case CelestialBody.SUN:     return './tools/texture/Sun.png'
            case CelestialBody.MERCURY: return './tools/texture/Mercury.jpg'
            case CelestialBody.VENUS:   return './tools/texture/Venus.jpg'
            case CelestialBody.EARTH:   return './tools/texture/Earth.jpg'
            case CelestialBody.MOON:    return './tools/texture/Moon.jpg'
            case CelestialBody.MARS:    return './tools/texture/Mars.jpg'
            case CelestialBody.JUPITER: return './tools/texture/Jupiter.jpg'
            case CelestialBody.SATURN:  return './tools/texture/Saturn.jpg'
            case CelestialBody.URANUS:  return './tools/texture/Uranus.jpg'
            case CelestialBody.NEPTUNE: return './tools/texture/Neptune.jpg'
            case CelestialBody.PLUTO:   return './tools/texture/Earth.jpg'
            case _:                     return './tools/texture/Earth.jpg'
    
    @classmethod
    def PlanetaryOrbitalElementsAndRates(cls, celestialBody : CelestialBody) -> list:
        """Planetary Orbital Elements & Rates

        Args:
            celestialBody (CelestialBody): Celestial body

        Returns:
            list: [Orbital Elements, Orbital Elements Rates]
        """
        
        orbital_elements = dict(a=0.0, e=0.0, i=0.0, Omega=0.0, bomega=0.0, L=0.0)
        
        orbital_elements_rates = dict(a=0.0, e=0.0, i=0.0, Omega=0.0, bomega=0.0, L=0.0)
        
        match (celestialBody):
            
            case CelestialBody.SUN:
                
                return [orbital_elements, orbital_elements_rates]
            
            case CelestialBody.MERCURY:
                
                # ? 0.38709893 0.20563069 7.00487 48.33167 77.45645 252.25084
                
                orbital_elements['a']               = 0.38709927
                orbital_elements['e']               = 0.20563593
                orbital_elements['i']               = 7.00497902
                orbital_elements['Omega']           = 48.33076593
                orbital_elements['bomega']          = 77.45779628
                orbital_elements['L']               = 252.25032350
                
                # ? 0.00000066 0.00002527 -23.51 -446.30 573.57 538101628.29 (arcsec)
                
                orbital_elements_rates['a']         = 0.00000037
                orbital_elements_rates['e']         = 0.00001906
                orbital_elements_rates['i']         = -0.00594749
                orbital_elements_rates['Omega']     = -0.12534081
                orbital_elements_rates['bomega']    = 0.16047689
                orbital_elements_rates['L']         = 149472.67411175
                
            case CelestialBody.VENUS:
                
                # ? 0.72333199 0.00677323 3.39471 76.68069 131.53298 181.97973
                
                orbital_elements['a']               = 0.72333566
                orbital_elements['e']               = 0.00677672
                orbital_elements['i']               = 3.39467605
                orbital_elements['Omega']           = 76.67984255
                orbital_elements['bomega']          = 131.60246717
                orbital_elements['L']               = 181.97909950
                
                # ? 0.00000092 -0.00004938 -2.86 -996.89 -108.80 210664136.06 (arcsec)
                
                orbital_elements_rates['a']         = 0.00000390
                orbital_elements_rates['e']         = -0.00004107
                orbital_elements_rates['i']         = -0.00078890
                orbital_elements_rates['Omega']     = -0.27769418
                orbital_elements_rates['bomega']    = 0.00268329
                orbital_elements_rates['L']         = 58517.81538729
            
            case CelestialBody.EARTH:
                
                # ? 1.00000011 0.01671022 0.00005 -11.26064 102.94719 100.46435
                
                orbital_elements['a']               = 1.00000261
                orbital_elements['e']               = 0.01671123
                orbital_elements['i']               = -0.00001531 # !
                orbital_elements['Omega']           = 0.0 # !
                orbital_elements['bomega']          = 102.93768193
                orbital_elements['L']               = 100.46457166
                
                # ? -0.00000005 -0.00003804 -46.94 -18228.25 1198.28 129597740.63 (arcsec)
                
                orbital_elements_rates['a']         = 0.00000562
                orbital_elements_rates['e']         = -0.00004932
                orbital_elements_rates['i']         = -0.01294668
                orbital_elements_rates['Omega']     = 0.0
                orbital_elements_rates['bomega']    = 0.32327364
                orbital_elements_rates['L']         = 35999.37244981
                
            case CelestialBody.MARS:
                
                # ? 1.52366231 0.09341233 1.85061 49.57854 336.04084 355.45332
                
                orbital_elements['a']               = 1.52371034
                orbital_elements['e']               = 0.09339410
                orbital_elements['i']               = 1.84969142
                orbital_elements['Omega']           = 49.55953891
                orbital_elements['bomega']          = 360 - 23.94362959 # !
                orbital_elements['L']               = 360 - 4.55343205 # !
                
                # ? -0.00007221 0.00011902 -25.47 -1020.19 1560.78 68905103.78 (arcsec)
                
                orbital_elements_rates['a']         = 0.0001847
                orbital_elements_rates['e']         = 0.00007882
                orbital_elements_rates['i']         = -0.00813131
                orbital_elements_rates['Omega']     = -0.29257343
                orbital_elements_rates['bomega']    = 0.44441088
                orbital_elements_rates['L']         = 19140.30268499
            
            case CelestialBody.JUPITER:
                
                # ? 5.20336301 0.04839266 1.30530 100.55615 14.75385 34.40438
                
                orbital_elements['a']               = 5.20288700
                orbital_elements['e']               = 0.04838624
                orbital_elements['i']               = 1.30439695
                orbital_elements['Omega']           = 100.47390909
                orbital_elements['bomega']          = 14.72847983
                orbital_elements['L']               = 34.39644501
                
                # ? 0.00060737 -0.00012880 -4.15 1217.17 839.93 10925078.35 (arcsec)
                
                orbital_elements_rates['a']         = -0.00011607
                orbital_elements_rates['e']         = 0.00013253
                orbital_elements_rates['i']         = -0.00183714
                orbital_elements_rates['Omega']     = 0.20469106
                orbital_elements_rates['bomega']    = 0.21252668
                orbital_elements_rates['L']         = 3034.74612775
                
            case CelestialBody.SATURN:
                
                # ? 9.53707032 0.05415060 2.48446 113.71504 92.43194 49.94432
                
                orbital_elements['a']               = 9.53667594
                orbital_elements['e']               = 0.05386179
                orbital_elements['i']               = 2.48599187
                orbital_elements['Omega']           = 113.66242448
                orbital_elements['bomega']          = 92.59887831
                orbital_elements['L']               = 49.95424423
                
                # ? -0.00301530 -0.00036762 6.11 -1591.05 -1948.89 4401052.95 (arcsec)
                
                orbital_elements_rates['a']         = -0.00125060
                orbital_elements_rates['e']         = -0.00050991
                orbital_elements_rates['i']         = 0.00193609
                orbital_elements_rates['Omega']     = -0.28867794
                orbital_elements_rates['bomega']    = -0.41897216
                orbital_elements_rates['L']         = 1222.49362201
            
            case CelestialBody.URANUS:
                
                # ? 19.19126393 0.04716771 0.76986 74.22988 170.96424 313.23218
                
                orbital_elements['a']               = 19.18916464
                orbital_elements['e']               = 0.04725744
                orbital_elements['i']               = 0.77263783
                orbital_elements['Omega']           = 74.01692503
                orbital_elements['bomega']          = 170.95427630
                orbital_elements['L']               = 313.23810451
                
                # ? 0.00152025 -0.00019150 -2.09 -1681.4 1312.56 1542547.79 (arcsec)
                
                orbital_elements_rates['a']         = -0.00196176
                orbital_elements_rates['e']         = -0.00004397
                orbital_elements_rates['i']         = -0.00242939
                orbital_elements_rates['Omega']     = 0.04240589
                orbital_elements_rates['bomega']    = 0.40805281
                orbital_elements_rates['L']         = 424.48202785
                
            case CelestialBody.NEPTUNE:
                
                # ? 30.06896348 0.00858587 1.76917 131.72169 44.97135 304.88003
                
                orbital_elements['a']               = 30.06992276
                orbital_elements['e']               = 0.00859048
                orbital_elements['i']               = 1.77004347
                orbital_elements['Omega']           = 131.78422574
                orbital_elements['bomega']          = 44.96476227
                orbital_elements['L']               = 360 - 55.12002969 # !
                
                # ? -0.00125196 0.00002514 -3.64 -151.25 -844.43 786449.21 (arcsec)
                
                orbital_elements_rates['a']         = 0.00026291
                orbital_elements_rates['e']         = 0.00005105
                orbital_elements_rates['i']         = 0.00035372
                orbital_elements_rates['Omega']     = -0.00508664
                orbital_elements_rates['bomega']    = -0.32241464
                orbital_elements_rates['L']         = 218.45945325
                
            case CelestialBody.PLUTO:
                
                # ? 39.48168677 0.24880766 17.14175 110.30347 224.06676 238.92881
                
                orbital_elements['a']               = 39.48211675
                orbital_elements['e']               = 0.24882730
                orbital_elements['i']               = 17.14001206
                orbital_elements['Omega']           = 110.30393684
                orbital_elements['bomega']          = 224.06891629
                orbital_elements['L']               = 238.92903833
                
                # ? -0.00076912 0.00006465 11.07 -37.33 -132.25 522747.90 (arcsec)
                
                orbital_elements_rates['a']         = -0.00031596
                orbital_elements_rates['e']         = 0.00005170
                orbital_elements_rates['i']         = 0.00004818
                orbital_elements_rates['Omega']     = -0.01183482
                orbital_elements_rates['bomega']    = -0.04062942
                orbital_elements_rates['L']         = 145.20780515
        
        return [orbital_elements, orbital_elements_rates]

if __name__ == '__main__':
    
    print(AstronomicalData.GravitationalParameter(CelestialBody.EARTH))
    print(AstronomicalData.AngularVelocity(CelestialBody.EARTH))
    print(AstronomicalData.GroundTrackAngularVelocity(CelestialBody.EARTH))