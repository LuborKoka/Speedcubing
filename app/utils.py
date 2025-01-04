import copy
import math, re
from decimal import Decimal
from typing import List
from uuid import UUID
import numpy as np

from app.constants import CUBES
from app.model.solution import Solution
from app.types.averages import AverageDetails


def timestr_to_float(time_str: str):
    """
    Converts a time string (formatted as mm:ss or ss.sss) into a float representing the total number of seconds.

    Args:
        time_str (str): The time string to convert. The string can be in the format "mm:ss", "mm:ss.sss", or "ss.sss".

    Returns:
        float: The total time in seconds as a float, or None if the input string is invalid.
    """
    time_str = time_str.replace(',', '.')

    match = re.match(r'^(?:([1-5]?[0-9]):)?([0-5]?[0-9])(\.[0-9]{1,3})?$', time_str)
    if not match:
        return None
    
    minutes = 60 * int(match.group(1)) if match.group(1) is not None else 0

    
    seconds = match.group(2) 
    seconds += match.group(3) if match.group(3) is not None else ''
    seconds = float(seconds)

    return minutes + seconds


def float_to_timestr(val: float | None):
    """
    Converts a float representing time in seconds into a formatted time string.

    Args:
        val (float | None): The time in seconds to convert.

    Returns:
        str: A formatted time string in the format "mm:ss" or "ss.sss", where "min" or "s" is appended depending on the value.
    """
    if val is None:
        return '--:--.--'

    minutes = math.floor(val / 60)
    seconds = val - (60 * minutes)

    minutes_str = f'{minutes}:' if minutes > 0 else ''
    return f'{minutes_str}{"0" if minutes > 0 and seconds < 10 else ""}{Decimal(seconds):.2f}{"min" if minutes > 0 else "s"}'


def get_avg_of(n: int, solutions: List[Solution], omit_best_worst: bool = False) -> AverageDetails:
    """
    Calculates the average of the `time` attribute for the given list of `solutions`.

    The function either calculates the mean of all times or the mean of the times after omitting the best and worst.

    Args:
        n (int): The number of solutions to consider. If there are fewer than `n` solutions, None is returned.
        solutions (List[Solution]): A list of `Solution` objects that have a `time` attribute.
        omit_best_worst (bool): Whether to calculate the mean of all times (True) or omit the best and worst times before calculating the mean (False).

    Returns:
        float: The average time (mean), or None if there are fewer than `n` solutions.
    """
    if len(solutions) < n:
        return {
            'time_str': float_to_timestr(None),
            'time': None,
            'solutions': None
        }

    times = np.array([s.time for s in solutions[:n]])
    
    if not omit_best_worst:
        avg = np.mean(times)
    else:
        sorted_times = np.sort(times)[1:-1]
        avg = np.mean(sorted_times)
    
    return {
        'time_str': float_to_timestr(avg),
        'time': avg,
        'solutions': solutions[:n]
    }



def is_valid_uuid(uuid_to_test: str, version=4):
    """
    Check if uuid_to_test is a valid UUID.
    
     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}
    
     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.
    
     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
        return str(uuid_obj) == uuid_to_test
    except ValueError:
        return False
    

def get_cubes(puzzle: str):
    cubes = copy.deepcopy(CUBES)
    next((cube for cube in cubes if cube['puzzle'] == puzzle), None)['status'] = 'active'

    return cubes