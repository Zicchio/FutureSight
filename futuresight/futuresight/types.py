from dataclasses import dataclass, field

import numpy as np


class MagicDeckException(Exception):
    pass


class EmptyDeckException(MagicDeckException):
    pass


@dataclass(frozen=True)
class MagicCard:
    """Simple class to represent a magic the gathering card that might or might
    not have a specified quality used to check conditional future sight effects,
    such as Oracle of Mul Daya, Nalia  or Gaelia
    """

    card_id: int
    has_qual: bool


@dataclass
class MagicDeck:
    """Class that represents a magic deck as a list of cards. List element
    indexed by zero is bottom of the deck.
    Not using a queue as it is overkill.
    """

    cards: list[MagicCard]
    rng: np.random.Generator

    def add_cards(self, card: MagicCard, to_bottom: bool = False):
        """add a magic card to a deck (optionally: to bottom of library"""
        if to_bottom:
            self.cards.insert(0, MagicCard)
        self.cards.append(card)

    def shuffle(self):
        """shuffle the deck"""
        self.rng.shuffle(self.cards)

    def observe_a_card(self) -> MagicCard:
        """look at the top card of you library"""
        if len(self.cards) == 0:
            raise EmptyDeckException("library is empty")
        return self.cards[-1]

    def move_to_bottom(self) -> None:
        """move the top card of you library to bottom"""
        if len(self.cards) <= 1:  # empty and 1 size library don't move anything around
            return
        card = self.cards.pop()
        self.add_cards(card, to_bottom=True)

    def play_a_card(self) -> MagicCard:
        """look and remove the top card of you library"""
        if len(self.cards) == 0:
            raise EmptyDeckException("library is empty")
        return self.cards.pop()

    def scry1(self) -> None:
        """look at the top of library and, if it does not have the desired
        quality, move it to bottom
        """
        if len(self.cards) <= 1:
            return
        card = self.observe_a_card()
        if not card.has_qual:
            self.move_to_bottom()


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
