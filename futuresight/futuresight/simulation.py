from typing import Optional

import numpy as np
from futuresight.types import MagicCard, MagicDeck, FSGameOutcome, FSGameParams


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


def fs_round_action(deck: MagicDeck, game: FSGameParams) -> int:
    """Future sight round action.
    Play of to max_draws from the top of the library if they have
    """
    avail_cards = game.round_max  # number of cards that I can still play
    avail_scries = game.scry_max  # number of scries I can take this round
    played_cards = 0
    while (deck.decksize() > 0) and (avail_cards > 0):
        topcard = deck.observe_a_card()
        if topcard.has_qual:
            # the top card can be casted
            deck.play_a_card()
            played_cards += 1
            avail_cards -= 1
        elif avail_scries > 0:
            # the top card cannot be casted, but I can scry
            deck.scry1()
            avail_scries -= 1
        else:
            # QUIT when top card is a brick and I don't have any scries left
            break
    return played_cards


def simulate_fs_game(
    game: FSGameParams,
    rounds: Optional[int] = None,
    seed: Optional[int] = None,
    init_hand_size: int = 0,
) -> FSGameOutcome:
    """Simulate future sight game initialize a deck with where m
    out of n cards satisfy the desider future sight propriety.
    The game will go on until r rounds are performed, or the deck is empty
    (which ever comes first).

    For a deterministic procedure procedure, set a seed.
    For a more accurate data, you "exclude" the first init_hand_size cards
    from the deck.
    """
    deck = create_m_n_deck(game.m, game.n, seed)
    deck.shuffle()
    real_rounds = 0
    virtual_draws = 0
    # Remove init_hand_size cards from the top of the library
    if init_hand_size > 0:
        for _ in range(init_hand_size):
            if deck.decksize() == 0:
                break
            deck.play_a_card()
    # Play the game until the library is empty of the rounds are over
    while deck.decksize() > 0:
        deck.play_a_card()  # cards you draw in a turn
        real_rounds += 1
        if (rounds is not None) and (real_rounds > rounds):
            break
        virtual_draws += fs_round_action(deck, game)
    avg_draws = virtual_draws / real_rounds
    return FSGameOutcome(rounds=real_rounds, virtual_draws=virtual_draws, dpr=avg_draws)
