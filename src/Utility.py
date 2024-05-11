import os
import sys
import numpy as np

from decimal import Decimal, ROUND_DOWN

sys.path.append(os.path.dirname(__file__))

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