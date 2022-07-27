from dataclasses import dataclass, field


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
    cards: list[MagicCard]

    def add_cards(self, card: MagicCard):
        """add a magic card to a deck"""
        self.cards.append(card)
    
    def shuffle(self):
        """shuffle the deck"""
        


def create_m_n_deck(m: int, n: int) -> MagicDeck:
    """Create a Magic the Gathering deck where m out of n cards have the desired propriety"""
    if m > n:
        raise ValueError(
            f"cannot create a deck where m={m} card out of n={n} have the desired propriety"
        )
    if m == 0 and n == 0:
        return MagicDeck()
    qual_cards = [MagicCard(i, True) for i in range(m)] # card with quality
    noqual_cards = [MagicCard(i, False) for i in range(m, n)] # cards without quality
    return MagicDeck(qual_cards+noqual_cards)
