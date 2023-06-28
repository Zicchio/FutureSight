import argparse
from typing import NamedTuple

from futuresight.simulation import simulate_n_fs_games
from futuresight.types import FSGameParams

DEFAULT_SEED = 20220610
DEFAULT_TRIALS = 10_000
DEFAULT_HPT = 1


class ProgArgs(NamedTuple):
    decksize: int
    numhits: int
    hpt: int
    t: int
    seed: int


def parse_args() -> ProgArgs:
    parser = argparse.ArgumentParser(
        prog="futuresight",
        description="Program FutureSight is tool designed for Magic: The Gathering that produces stats about the number of card that a conditional future sight effect can yield in a game.",
    )
    parser.add_argument("decksize", type=int, help="Size of the MTG")
    parser.add_argument("numhits", type=int,
                        help="number of card (in the deck) that can be played from the top of the deck")
    parser.add_argument("--hpt", type=int, default=DEFAULT_HPT,
                        help=f"maximum number of cards that can be played from top of deck per turn, defaults to {DEFAULT_HPT}")
    parser.add_argument("--t", type=int, default=DEFAULT_TRIALS,
                        help=f"numbers of simulations to run, defaults to {DEFAULT_TRIALS}")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help=f"seed to recreate a simulation, defaults to {DEFAULT_SEED}")
    args_ns = parser.parse_args()
    return ProgArgs(**vars(args_ns))


def main_cli():
    args = parse_args()
    print("Starting simulaztions")
    game = FSGameParams(
        args.numhits,
        args.decksize,
        args.hpt,
        0
    )
    outcome = simulate_n_fs_games(game, args.t, quiet=False)
    print(f"Result: {outcome} card per turn")
