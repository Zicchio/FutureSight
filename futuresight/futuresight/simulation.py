from typing import Optional, NamedTuple

import numpy as np
from futuresight.types import MagicCard, MagicDeck

class FutureSightResult(NamedTuple):
    rounds: int
    virtual_draws: int
    dpr: float # average draw per round


def create_m_n_deck(m: int, n: int, seed: int = 0) -> MagicDeck:
    """Create a Magic the Gathering deck where m out of n cards have the desired propriety"""
    if m > n:
        raise ValueError(
            f"cannot create a deck where m={m} card out of n={n} have the desired propriety"
        )
    rng = np.random.default_rng(seed)
    if m == 0 and n == 0:
        return MagicDeck([], rng=rng)
    qual_cards = [MagicCard(i, True) for i in range(m)]  # card with quality
    noqual_cards = [MagicCard(i, False) for i in range(m, n)]  # cards without quality
    return MagicDeck(qual_cards + noqual_cards, rng=rng)


def fs_round_action(deck: MagicCard, max_cards: int = 1, num_scries: int = 0) -> int:
    """Future sight round action.
    Play of to max_draws from the top of the library if they have 
    """


def simulate_fs_game(
    m: int, n: int, rounds: int, seed: Optional[int] = None, init_hand_size: int = 0
) -> tuple[int, float]:
    """Simulate future sight game initialize a deck with where m
    out of n cards satisfy the desider future sight propriety.
    The game will go on until r rounds are performed, or the deck is empty
    (which ever comes first).
    
    For a deterministic procedure procedure, set a seed.
    For a more accurate data, you "exclude" the first init_hand_size cards
    from the deck. 
    """
    deck = create_m_n_deck(m, n, seed)
    deck.shuffle()
    real_rounds = 0
    virtual_draws = 0
    if init_hand_size > 0:
        # pop up ti initi_hand size from deck
        for _ in range(init_hand_size):
            if deck.size() == 0:
                break
            deck.play_a_card()
    for r in rounds:
        if deck.size() == 0:
            break
        real_rounds += 1
        