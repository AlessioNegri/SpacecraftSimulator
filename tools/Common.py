import os
import sys
import math
import numpy as np

from datetime import datetime, timedelta

sys.path.append(os.path.dirname(__file__))

def wrap_to_2pi(x : float) -> float:
    """Wraps the angle in the range 0 - 2 PI

    Args:
        x (float): angle

    Returns:
        float: Wrapped angle
    """

    return np.remainder(x, 2 * np.pi if x > 0 else - 2 * np.pi)

def wrap_to360deg(x : float) -> float:
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
        
def daterange_length(start : datetime, end : datetime, step : int = 1) -> int:
    """Length of the daterange

    Args:
        start (datetime): Start datetime
        end (datetime): End datetime
        step (int, optional): Step for date range. Defaults to 1.

    Yields:
        Generator: Generator[Any, Any, None]
    """
    
    return math.ceil(int((end - start).days + 1) / step)

def print_progress_bar(iteration : int,
                     total : int,
                     prefix : str = '',
                     suffix : str = '',
                     decimals : int = 1,
                     length : int = 100,
                     fill : str = '*',
                     printEnd : str = '\r') -> None:
    """Call in a loop to create terminal progress bar

    Args:
        iteration (int): Current iteration
        total (int): Total iterations
        prefix (str, optional): Prefix string. Defaults to ''.
        suffix (str, optional): Suffix string. Defaults to ''.
        decimals (int, optional): Positive number of decimals in percent complete. Defaults to 1.
        length (int, optional): Character length of bar. Defaults to 100.
        fill (str, optional): Bar fill character. Defaults to '*'.
        printEnd (str, optional): End character (e.g. '\r', '\r\n'). Defaults to '\r'.
    """    
    
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration / float(total)))
    
    filledLength = int(length * iteration // total)
    
    bar = fill * filledLength + '-' * (length - filledLength)
    
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    
    if iteration == total: print()

def extrema(x : np.ndarray, movingwindowsize : int = 1, movingwindow : bool = False) -> list:
    """Translation of the extrema.m matlab function to python.

    Args:
        x (np.ndarray): Signal for which you need to find local maximum and minimums
        movingwindowsize (int, optional): Unused. Defaults to 1.
        movingwindow (bool, optional): Unused. Defaults to False.

    Returns:
        list: [ arrays of local maximum and minimum values,  indices of the maximum and minimum values ]
    """
    
    xmax = xmin = imax = imin = np.array([])
    
    if x.ndim != 1: raise TypeError('Input is not an 1D array')
    
    nt = len(x)

    inan = np.array(np.where(np.isnan(x))).flatten()
    indx = np.arange(0, nt)


    if len(inan) > 0:
        
        x = np.delete(x, inan)
        
        indx = np.delete(indx, inan)
        
        nt = len(x)
        
    dx = np.diff(x)

    a = np.array(np.where(dx != 0)).flatten()
    
    lm = np.array(np.where(np.diff(a) != 1)) + 1
    
    d = a[lm] - a[lm - 1]
    
    a[lm] = a[lm] - np.floor(d / 2)
    
    a = np.append(a, np.array([nt - 1]))
    
    
    xa = x[a]
    
    b = (np.diff(xa) > 0)
    
    xb = np.diff(b + 0)
    
    imax = np.array(np.where(xb == -1)) + 1
    
    imin = np.array(np.where(xb == +1)) + 1
    
    imax = a[imax]
    
    imin = a[imin]
    
    imax = imax.flatten()
    
    imin = imin.flatten()
    
    nmaxi = len(imax)
    
    nmini = len(imin)
    
    if nmaxi == 0 and nmini == 0:
        
        if x[0] > x[nt]:
            
            xmax = x[0]
            imax = indx[0]
            xmin = x[nt]
            imin = indx[nt]
            
        elif x[0] < x[nt]:
            
            xmax = x[nt]
            imax = indx[nt]
            xmin = x[0]
            imin = indx[0]
            
        return [xmax, xmin, imax, imin]

    if nmaxi == 0:
        
        imax[:2] = [1, nt]
        
    elif nmini == 0:
        
        imin[:2] = [1, nt]
        
    else:
        
        if imax[0] < imin[0]:
            
            imin = np.append(np.array([1]), imin)
            
        else:
            
            imax = np.append(np.array([1]), imax)

        if imax[-1] > imin[-1]:
            
            imin = np.append(imin, np.array([nt - 1]))
            
        else:
            
            imax = np.append(imax, np.array([nt - 1]))

    xmax = x[imax]
    xmin = x[imin]

    if len(inan) > 0:
        
        imax = indx[imax]
        imin = indx[imin]

    imax = np.reshape(imax, np.shape(xmax))
    imin = np.reshape(imin, np.shape(xmin))

    inmax = np.argsort(-xmax)
    xmax = xmax[inmax]
    imax = imax[inmax]
    inmin = np.argsort(xmin)
    xmin = np.sort(xmin)
    imin = imin[inmin]
    
    imaxSort = imax.argsort()
    iminSort = imin.argsort()
    
    xmax = xmax[imaxSort[::-1]]
    xmin = xmin[iminSort[::-1]]
    imax = imax[imaxSort[::-1]]
    imin = imin[iminSort[::-1]]

    return [xmax, xmin, imax, imin]