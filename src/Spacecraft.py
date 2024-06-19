import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml

from Utility import format, singleton

"""
m_0_changed     = qtCore.Signal()
def get_m_0(self):      return format(self._m_0)
def set_m_0(self, m_0 : float):     self._m_0 = m_0; self.m_0_changed.emit()
m_0     = qtCore.Property(float, get_m_0, set_m_0, notify=m_0_changed)

---

@qtCore.Property(float)
def initial_mass(self): return self._initial_mass

@initial_mass.setter
def initial_mass(self, val : float): self._initial_mass = val
"""

@singleton
class Spacecraft(qtCore.QObject):
    """This class describes the properties and parameters of a Spacecraft
    """
    
    # ! PROPERTIES
    
    # ? Initial Mass [kg]
    
    @qtCore.Property(float)
    def initial_mass(self): return format(self._initial_mass)

    @initial_mass.setter
    def initial_mass(self, val : float): self._initial_mass = val
    
    # ? Mass [kg]
    
    @qtCore.Property(float)
    def mass(self): return format(self._mass)

    @mass.setter
    def mass(self, val : float): self._mass = val
    
    # ? Specific Impulse [s]
    
    @qtCore.Property(float)
    def specific_impulse(self): return format(self._specific_impulse)

    @specific_impulse.setter
    def specific_impulse(self, val : float): self._specific_impulse = val
    
    # ? Thrust [N]
    
    @qtCore.Property(float)
    def thrust(self): return format(self._thrust)

    @thrust.setter
    def thrust(self, val : float): self._thrust = val
    
    # ! CONSTRUCTOR
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__Spacecraft", self)
        
        self._initial_mass      : float = 2000.0
        self._mass              : float = 2000.0
        self._specific_impulse  : float = 300.0
        self._thrust            : float = 10e3
    
    # ! METHODS
    
    def reset(self) -> None:
        """Resets the spacecraft parameters
        """
        
        self._mass = self._initial_mass
    
    def update_mass(self, consumed_mass : float) -> None:
        """Updates the current mass subtracting the consumed one

        Args:
            consumed_mass (float): Consumed mass [kg]
        """
        
        if self._mass >= consumed_mass:
        
            self._mass -= consumed_mass