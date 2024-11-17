""" QmlLog.py: Javascript console for QML """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import PySide6.QtCore as qtCore

from termcolor import cprint

class QmlLog(qtCore.QObject):
    """Class to manage the javascript console function from qml in python"""
    
    # --- METHODS 
    
    def __init__(self) -> None:
        """Constructor
        """
        
        qtCore.QObject.__init__(self)
    
    @qtCore.Slot(str)
    def log(self, message : str = '') -> None:
        """Writes in python the console.log from qml javascript

        Args:
            message (str, optional): Message to display. Defaults to ''.
        """
        
        cprint('qml: ' + message, 'green')
    
    @qtCore.Slot(str)
    def warn(self, message : str = '') -> None:
        """Writes in python the console.warn from qml javascript

        Args:
            message (str, optional): Message to display. Defaults to ''.
        """
        
        cprint('qml: ' + message, 'yellow')
    
    @qtCore.Slot(str)
    def error(self, message : str = '') -> None:
        """Writes in python the console.error from qml javascript

        Args:
            message (str, optional): Message to display. Defaults to ''.
        """
        
        cprint('qml: ' + message, 'red')