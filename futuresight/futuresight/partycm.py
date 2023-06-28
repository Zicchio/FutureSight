"""Tools to evaluate party composition"""

from enum import Enum
from typing import TypeAlias

# _CM_T is Class Member Type, wich is an integer from 0b0 (0) to 0b1111 (15)
_CM_T: TypeAlias = int

# List of all possible class members
_N: _CM_T = 0
_F: _CM_T = 1
_R: _CM_T = 2
_W: _CM_T = 4
_C: _CM_T = 8
_FR = _F | _R
_FW = _F | _W
_FC = _F | _C
_RW = _R | _W
_RC = _R | _C
_WC = _W | _C
_FRW = _F | _R | _W
_FRC = _F | _R | _C
_FWC = _F | _W | _C
_RWC = _R | _W | _C
_FRWC = _F | _R | _W | _C


def hw(x: int) -> int:
    """hamming weight function"""
    w = 0
    while x > 0:
        w += x & 1
        x = x >> 1
    return w


# Array of hamming weight of all possible party members
_cw_weight: list[int] = [hw(i) for i in range(16)]


def pm_reduce(pm: list[_CM_T]) -> list[_CM_T]:
    """Removes unecessary party """
    if len(pm) == 0:
        return pm
    # TODO: devo verificare a mano che l'algoritmo sia corretto.
    return pm
