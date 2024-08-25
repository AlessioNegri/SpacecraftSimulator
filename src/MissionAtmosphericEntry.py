import PySide6.QtCore as qtCore
import PySide6.QtQml as qtQml
import FigureCanvas as fc
import numpy as np
import matplotlib.pyplot as plt

from tools.AtmosphericEntry import AtmosphericEntry

class MissionAtmosphericEntry(qtCore.QObject):
    
    def __init__(self, engine : qtQml.QQmlApplicationEngine) -> None:
        
        """Constructor

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        qtCore.QObject.__init__(self)
        
        engine.rootContext().setContextProperty("__MissionAtmosphericEntry", self)
        
        # * Figure Canvas
        
        self.figure = fc.FigureCanvas()
        
        # * Context properties
        
        engine.rootContext().setContextProperty("__AtmosphericEntryFigure", self.figure)
    
    # - PUBLIC 
    
    def setUpdateWithCanvas(self, engine : qtQml.QQmlApplicationEngine) -> None:
        
        """Connects all the QML figures with the backend model

        Args:
            engine (qtQml.QQmlApplicationEngine): QML engine
        """
        
        win = engine.rootObjects()[0]
        
        self.figure.updateWithCanvas(win.findChild(qtCore.QObject, "AtmosphericEntryFigure"), win.findChild(qtCore.QObject, "AtmosphericEntryFigureParent"), rows=2, cols=3)
    
    # - SLOTS 
    
    @qtCore.Slot()
    def simulate(self) -> None:
        
        """Simulates the atmospheric entry mission
        """
        
        # - Simulation 
        
        AtmosphericEntry.setCapsuleParameters(0, 300, 0, 0, 1.096, 0.341)
        
        result = AtmosphericEntry.integrateAtmosphericEntry(np.array([12.6161, np.deg2rad(-9), 120, 0, 26.27]), t_f=3000)
        
        V       = result['y'][0, :]
        gamma   = result['y'][1, :]
        r       = result['y'][2, :]
        x       = result['y'][3, :]
        m       = result['y'][4, :]
        t       = result['t']
        
        C       = (1.7415 * 1e-4 * 1 / np.sqrt(AtmosphericEntry.R_N))
        q_t_c   = np.array([C * np.sqrt(1.225 * np.exp(-(r[i] - AtmosphericEntry.R_E) / AtmosphericEntry.H)) * (V[i] * 1e3)**3 for i in range(0, len(t))])
        a       = np.array([(V[i] - V[i - 1]) / (t[i] - t[i - 1]) for i in range(1, len(t))])
        
        
        # - Plot 
        
        t = t / 60
        
        self.figure.resetCanvas()
        
        self.figure.figure.suptitle(f"$V_e = {V[0]}\;\;km/s$   $\gamma_e = {np.rad2deg(gamma[0])}\;\;°$   $z_e = {r[0] - AtmosphericEntry.R_E}\;\;km$   $R_N = {AtmosphericEntry.R_N}\;\;m$   $V_f = {V[-1] * 1e3}$")
            
        self.figure.axes[0,0].set_xlabel("Time [$s$]")
        self.figure.axes[0,0].set_ylabel("$V$ [$km / s$]")
        self.figure.axes[0,0].grid()
        self.figure.axes[0,0].plot(t, V, color='#FFCC80')
        
        self.figure.axes[0,1].set_xlabel("Time [$s$]")
        self.figure.axes[0,1].set_ylabel("$\gamma$ [°]")
        self.figure.axes[0,1].grid()
        self.figure.axes[0,1].plot(t, gamma * 180 / np.pi, color='#90CAF9')
        
        self.figure.axes[0,2].set_xlabel("Downrange distance $x$ [$km$]")
        self.figure.axes[0,2].set_ylabel("$z$ [$km$]")
        self.figure.axes[0,2].grid()
        self.figure.axes[0,2].plot(x, r - AtmosphericEntry.R_E, color='#CE93D8')
        
        self.figure.axes[1,0].set_xlabel("$V$ [$km / s$]")
        self.figure.axes[1,0].set_ylabel("$z$ [$km$]")
        self.figure.axes[1,0].grid()
        self.figure.axes[1,0].plot(V, r - AtmosphericEntry.R_E, color='#F48FB1')
        
        self.figure.axes[1,1].set_xlabel("Time [$s$]")
        self.figure.axes[1,1].set_ylabel("$q_{t,c}$ [$W / cm^2$]")
        self.figure.axes[1,1].grid()
        self.figure.axes[1,1].plot(t, q_t_c * 1e-4, color='#E6EE9C')
        
        self.figure.axes[1,2].set_xlabel("Time [$s$]")
        self.figure.axes[1,2].set_ylabel("$dV/dt\;\;(g_E)$")
        self.figure.axes[1,2].grid()
        self.figure.axes[1,2].plot(t[1:], a / AtmosphericEntry.g_E, color='#80CBC4')
        
        self.figure.redrawCanvas()