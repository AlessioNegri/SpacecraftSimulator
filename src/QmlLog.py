import PySide6.QtCore as qtCore

class QmlLog(qtCore.QObject):
    """Class to manage the console.log from qml javascript in python
    """
    
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
        
        print('qml: ' + message)