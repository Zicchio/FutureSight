from typing import Optional
from tqdm import tqdm

import numpy as np
from futuresight.types import MagicCard, MagicDeck, FSGameOutcome, FSGameParams


def create_m_n_deck(m: int, n: int) -> MagicDeck:
    """Create a Magic the Gathering deck where m out of n cards have the desired propriety"""
    if m > n:
        raise ValueError(
            f"cannot create a deck where m={m} card out of n={n} have the desired propriety"
        )
    if m == 0 and n == 0:
        return MagicDeck([])
    qual_cards = [MagicCard(i, True) for i in range(m)]  # card with quality
    noqual_cards = [MagicCard(i, False)
                    for i in range(m, n)]  # cards without quality
    return MagicDeck(qual_cards + noqual_cards)


def fs_round_action(deck: MagicDeck, max_plays: int, max_scries: int) -> int:
    """Future sight round action.
    Play of to max_draws from the top of the library. If you see a brick,
    perfmorm up to max scries.
    """
    avail_cards = max_plays  # number of cards that I can still play
    avail_scries = max_scries  # number of scries I can take this round
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


def simulate_fs_deck(
    deck: MagicDeck,
    max_plays: int,
    max_scries: int,
    rounds: Optional[int] = None,
) -> FSGameOutcome:
    """Simulate how many cards a future sight effect will draw on a set deck.
    Each round, play up to max_plays cards from top of library, whith up to
    max_scries available if you see bricks.
    The game will end as soon as the number of rounds finishes or the deck is
    empty.

    Returns:
        FSGameOutcome: Result of the game
    """
    real_rounds = 0
    virtual_draws: list[int] = []
    # Play the game until the library is empty of the rounds are over
    while deck.decksize() > 0:
        deck.play_a_card()  # cards you draw in a turn
        real_rounds += 1
        if (rounds is not None) and (real_rounds > rounds):
            break
        round_draws = fs_round_action(deck, max_plays, max_scries)
        virtual_draws.append(round_draws)
    if real_rounds > 0:
        avg_draws = sum(virtual_draws) / real_rounds
    else:
        avg_draws = 0
    return FSGameOutcome(rounds=real_rounds, virtual_draws=virtual_draws, dpr=avg_draws)


def simulate_fs_game(
    game: FSGameParams,
    rounds: Optional[int] = None,
    seed: Optional[int] = None,
    max_scries: int = 0,
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
    rng = np.random.default_rng(seed)
    deck = create_m_n_deck(game.m, game.n)
    deck.shuffle(rng)
    # Remove init_hand_size cards from the top of the library
    if init_hand_size > 0:
        for _ in range(init_hand_size):
            if deck.decksize() == 0:
                break
            deck.play_a_card()
    return simulate_fs_deck(
        deck,
        game.round_max,
        max_scries,
        rounds=rounds,
    )


def simulate_n_fs_games(
    game: FSGameParams,
    n: int,
    rounds: Optional[int] = None,
    init_hand_size: int = 0,
    quiet: bool = True,
) -> tuple[float, list[int]]:
    """Take the average of simulating N future sight games.
    This can be slow for big values of N. Set quiet = False to showcase
    a progress bar.

    Returns:
        - float: average number of card drawn in each game.
        - list[int]: distribution with the number of draws.
    """
    ratio = 0
    draws_dist = [0 for _ in range(game.round_max+1)]
    for i in tqdm(range(n), disable=quiet):
        outcome = simulate_fs_game(
            game, rounds, seed=i, init_hand_size=init_hand_size)
        ratio += outcome.dpr
        for v in outcome.virtual_draws:
            draws_dist[v] += 1
    return ratio / n, draws_dist
