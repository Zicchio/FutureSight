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
    such as Oracle of Mul Daya, Nalia  or Gaelia.
    Unique enumerable qualities (like being being the specific members of a
    party) are also supported.
    """

    card_id: int
    has_qual: bool
    unique_qual: int = 0
    cmc: int = -1  # mana value of the card - currently unused


@dataclass
class MagicDeck:
    """Class that represents a magic deck as a list of cards. List element
    indexed by zero is bottom of the deck.
    Not using a queue as it is overkill.
    """

    cards: list[MagicCard]
    rng: np.random.Generator

    def size(self) -> int:
        """return current decks size"""
        return len(self.cards)

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
        if self.size() == 0:
            raise EmptyDeckException("library is empty")
        return self.cards[-1]

    def move_to_bottom(self) -> None:
        """move the top card of you library to bottom"""
        if self.size() <= 1:  # empty and 1 size library don't move anything around
            return
        card = self.cards.pop()
        self.add_cards(card, to_bottom=True)

    def play_a_card(self) -> MagicCard:
        """look and remove the top card of you library"""
        if self.size() == 0:
            raise EmptyDeckException("library is empty")
        return self.cards.pop()

    def scry1(self) -> bool:
        """look at the top of library and, if it does not have the desired
        quality, move it to bottom.
        Te function returns True if it moved a card to the bottom, False
        otherwise.
        """
        if self.size() <= 1:
            return False
        card = self.observe_a_card()
        if not card.has_qual:
            self.move_to_bottom()
            return True
        return False
