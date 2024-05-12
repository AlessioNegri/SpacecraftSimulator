import os
import sys

sys.path.append(os.path.dirname(__file__))

import numpy as np
import numpy.linalg as linalg

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import mpl_toolkits.mplot3d.art3d as art3d

import seaborn as sbn

from scipy.optimize import newton
from scipy.integrate import solve_ivp

from dataclasses import dataclass, field

from enum import IntEnum

from PIL import Image

from datetime import datetime

from AstronomicalData import *

#sbn.set_style('whitegrid')

class CustomException(Exception):
    
    def __init__(self, m : str): self.message = m
    
    def __str__(self): return '>>> ' + self.message

@dataclass
class RESULT:
    t       : np.ndarray
    r_x     : np.ndarray
    r_y     : np.ndarray
    r_z     : np.ndarray
    v_x     : np.ndarray
    v_y     : np.ndarray
    v_z     : np.ndarray
    m       : np.ndarray
    success : bool = False

def wrapTo2Pi(x : float) -> float:
    """Wraps the angle in the range 0 - 2 PI

    Args:
        x (float): angle

    Returns:
        float: Wrapped angle
    """

    return np.remainder(x, 2 * np.pi if x > 0 else - 2 * np.pi)

def wrapTo360Deg(x : float) -> float:
    """Wraps the angle in the range 0 - 360 degrees

    Args:
        x (float): angle

    Returns:
        float: Wrapped angle
    """

    return np.remainder(x, 360 if x > 0 else -360)