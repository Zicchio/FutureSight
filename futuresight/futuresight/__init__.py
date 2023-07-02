"""
Module FutureSight merges Magic the Gathering and Python to obtain numberical
 data on conditional future sight games.
A conditional future sight game is a game where you have a card that lets you
 play the top card of you library as long as it has a certain quality X.
The target of the simulation is to provide an answere tot he following 
 question: "on average: how many cards per round can I play?".

Practical example include
 - "How many cards per round an Oracle of Mul Daya plays in my deck?"
 
"""

from futuresight.types import FSGameParams, FSGameOutcome
from futuresight.simulation import simulate_fs_game, simulate_n_fs_games

__version__ = "0.1.0"
