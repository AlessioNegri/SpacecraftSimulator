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

class AstronomicalData():
    
    G = 6.6743015e-20 # ? Universal Gravitational Constant [km^3 / kg s^2]
    
    AU = 149_597_870.707 # ? Astronimical Unit [km]
    
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

if __name__ == '__main__':
    
    print(AstronomicalData.GravitationalParameter(CelestialBody.EARTH))
    print(AstronomicalData.AngularVelocity(CelestialBody.EARTH))
    print(AstronomicalData.GroundTrackAngularVelocity(CelestialBody.EARTH))