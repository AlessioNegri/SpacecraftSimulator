""" Utility.py: List of utility functions """

__author__      = "Alessio Negri"
__license__     = "LGPL v3"
__maintainer__  = "Alessio Negri"

import numpy as np

from decimal import Decimal, ROUND_DOWN

def format(x : float, format : str = '1.000000', deg : bool = False) -> float:
    """Formats a float with a given precision

    Args:
        x (float): Number
        format (str, optional): Precision format. Defaults to '1.000'.
        deg (bool, optional): True for converting rad to deg. Defaults to False.

    Returns:
        float: Formatted number
    """
    
    if deg: x = np.rad2deg(x)
    
    return float(Decimal.from_float(x).quantize(Decimal(format), rounding=ROUND_DOWN))

def singleton(cls, *args, **kw):
    """Decorator for singleton classes

    Returns:
        : class instance
    """
    
    instances = {}
     
    def _singleton(*args, **kw):
         
        if cls not in instances:
            
             instances[cls] = cls(*args, **kw)
             
        return instances[cls]
    
    return _singleton