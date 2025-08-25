"""Card and Deck classes for UNO game."""

from typing import List, Optional
import random
from enum import Enum


class CardColor(Enum):
    """UNO card colors."""
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    WILD = "wild"


class CardType(Enum):
    """UNO card types."""
    NUMBER = "number"
    ACTION = "action"
    WILD = "wild"


class Card:
    """Represents a single UNO card."""
    
    def __init__(self, color: CardColor, value: str, card_type: CardType):
        """Initialize a UNO card.
        
        Args:
            color: The card color
            value: The card value ('0'-'9', 'skip', 'reverse', 'draw_two', 'wild', 'wild_draw_four')
            card_type: The type of card (number, action, wild)
        """
        self.color = color
        self.value = value
        self.card_type = card_type
    
    def can_play_on(self, other_card: 'Card') -> bool:
        """Check if this card can be played on another card.
        
        Args:
            other_card: The card to check against
            
        Returns:
            True if this card can be played on the other card
        """
        # Wild cards can always be played
        if self.card_type == CardType.WILD:
            return True
        
        # Must match color or value
        return (self.color == other_card.color or 
                self.value == other_card.value)
    
    def is_action_card(self) -> bool:
        """Check if this is an action card."""
        return self.card_type in [CardType.ACTION, CardType.WILD]
    
    def get_points(self) -> int:
        """Get the point value of this card for scoring."""
        if self.value.isdigit():
            return int(self.value)
        elif self.value in ['skip', 'reverse', 'draw_two']:
            return 20
        elif self.value in ['wild', 'wild_draw_four']:
            return 50
        return 0
    
    def __str__(self) -> str:
        """String representation of the card."""
        if self.card_type == CardType.WILD:
            return f"Wild {self.value.replace('_', ' ').title()}"
        return f"{self.color.value.title()} {self.value.replace('_', ' ').title()}"
    
    def __repr__(self) -> str:
        """Detailed representation of the card."""
        return f"Card({self.color}, {self.value}, {self.card_type})"
    
    def __eq__(self, other) -> bool:
        """Check equality with another card."""
        if not isinstance(other, Card):
            return False
        return (self.color == other.color and 
                self.value == other.value and 
                self.card_type == other.card_type)


class Deck:
    """Represents a deck of UNO cards."""
    
    def __init__(self):
        """Initialize a standard UNO deck."""
        self.cards: List[Card] = []
        self.discard_pile: List[Card] = []
        self._create_standard_deck()
        self.shuffle()
    
    def _create_standard_deck(self) -> None:
        """Create a standard 108-card UNO deck."""
        # Number cards (0-9) for each color
        for color in [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]:
            # One 0 card per color
            self.cards.append(Card(color, "0", CardType.NUMBER))
            
            # Two of each number 1-9 per color
            for number in range(1, 10):
                self.cards.append(Card(color, str(number), CardType.NUMBER))
                self.cards.append(Card(color, str(number), CardType.NUMBER))
            
            # Two of each action card per color
            for action in ['skip', 'reverse', 'draw_two']:
                self.cards.append(Card(color, action, CardType.ACTION))
                self.cards.append(Card(color, action, CardType.ACTION))
        
        # Wild cards (4 of each)
        for _ in range(4):
            self.cards.append(Card(CardColor.WILD, "wild", CardType.WILD))
            self.cards.append(Card(CardColor.WILD, "wild_draw_four", CardType.WILD))
    
    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)
    
    def deal_card(self) -> Optional[Card]:
        """Deal one card from the deck.
        
        Returns:
            A card from the deck, or None if deck is empty
        """
        if not self.cards:
            self._reshuffle_from_discard()
        
        if self.cards:
            return self.cards.pop()
        return None
    
    def deal_hand(self, size: int = 7) -> List[Card]:
        """Deal a hand of cards.
        
        Args:
            size: Number of cards to deal
            
        Returns:
            List of cards
        """
        hand = []
        for _ in range(size):
            card = self.deal_card()
            if card:
                hand.append(card)
        return hand
    
    def add_to_discard(self, card: Card) -> None:
        """Add a card to the discard pile.
        
        Args:
            card: Card to add to discard pile
        """
        self.discard_pile.append(card)
    
    def get_top_discard(self) -> Optional[Card]:
        """Get the top card from the discard pile.
        
        Returns:
            The top discard card, or None if empty
        """
        return self.discard_pile[-1] if self.discard_pile else None
    
    def _reshuffle_from_discard(self) -> None:
        """Reshuffle discard pile back into deck, keeping top card."""
        if len(self.discard_pile) <= 1:
            return
        
        # Keep the top card in discard pile
        top_card = self.discard_pile.pop()
        
        # Move rest to deck and shuffle
        self.cards.extend(self.discard_pile)
        self.discard_pile = [top_card]
        self.shuffle()
    
    def cards_remaining(self) -> int:
        """Get number of cards remaining in deck."""
        return len(self.cards)
    
    def is_empty(self) -> bool:
        """Check if deck is empty."""
        return len(self.cards) == 0 and len(self.discard_pile) <= 1
