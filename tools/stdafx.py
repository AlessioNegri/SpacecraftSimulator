import os
import sys

sys.path.append(os.path.dirname(__file__))

import math
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

from datetime import datetime, timedelta, date

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

def daterange(start : datetime, end : datetime, step : int = 1):
    """Function to loop dates

    Args:
        start (datetime): Start datetime
        end (datetime): End datetime
        step (int, optional): Step for date range. Defaults to 1.

    Yields:
        Generator: Generator[Any, Any, None]
    """
    
    for day in range(0, int((end - start).days + 1), step):
        
        yield start + timedelta(day)
        
def daterangeLength(start : datetime, end : datetime, step : int = 1) -> int:
    """Length of the daterange

    Args:
        start (datetime): Start datetime
        end (datetime): End datetime
        step (int, optional): Step for date range. Defaults to 1.

    Yields:
        Generator: Generator[Any, Any, None]
    """
    
    return math.ceil(int((end - start).days + 1) / step)

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '*', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()