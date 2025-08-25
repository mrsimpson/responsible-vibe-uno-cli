"""Player classes for UNO game."""

from typing import List, Optional
from abc import ABC, abstractmethod
from .card import Card, CardColor


class Player(ABC):
    """Abstract base class for UNO players."""
    
    def __init__(self, name: str):
        """Initialize a player.
        
        Args:
            name: Player's name
        """
        self.name = name
        self.hand: List[Card] = []
        self.has_called_uno = False
    
    def add_card(self, card: Card) -> None:
        """Add a card to the player's hand.
        
        Args:
            card: Card to add
        """
        self.hand.append(card)
    
    def remove_card(self, card: Card) -> bool:
        """Remove a card from the player's hand.
        
        Args:
            card: Card to remove
            
        Returns:
            True if card was removed, False if not found
        """
        try:
            self.hand.remove(card)
            return True
        except ValueError:
            return False
    
    def get_valid_cards(self, top_card: Card) -> List[Card]:
        """Get all valid cards that can be played on the top card.
        
        Args:
            top_card: The current top card of the discard pile
            
        Returns:
            List of playable cards
        """
        return [card for card in self.hand if card.can_play_on(top_card)]
    
    def has_cards(self) -> bool:
        """Check if player has any cards."""
        return len(self.hand) > 0
    
    def card_count(self) -> int:
        """Get number of cards in hand."""
        return len(self.hand)
    
    def should_call_uno(self) -> bool:
        """Check if player should call UNO (has exactly one card)."""
        return len(self.hand) == 1
    
    def call_uno(self) -> None:
        """Call UNO."""
        self.has_called_uno = True
    
    def reset_uno_call(self) -> None:
        """Reset UNO call status."""
        self.has_called_uno = False
    
    def get_hand_points(self) -> int:
        """Calculate total points in hand for scoring."""
        return sum(card.get_points() for card in self.hand)
    
    @abstractmethod
    def choose_card(self, top_card: Card) -> Optional[Card]:
        """Choose a card to play.
        
        Args:
            top_card: The current top card
            
        Returns:
            Card to play, or None if cannot play
        """
        pass
    
    @abstractmethod
    def choose_wild_color(self) -> CardColor:
        """Choose a color when playing a wild card.
        
        Returns:
            The chosen color
        """
        pass
    
    def __str__(self) -> str:
        """String representation of the player."""
        return f"{self.name} ({len(self.hand)} cards)"


class HumanPlayer(Player):
    """Human player implementation."""
    
    def __init__(self, name: str = "Player"):
        """Initialize a human player."""
        super().__init__(name)
    
    def choose_card(self, top_card: Card, opponent: Player = None, 
                   game_state: dict = None) -> Optional[Card]:
        """Choose a card to play (will be handled by UI).
        
        This method is a placeholder - actual card selection
        will be handled by the InputHandler in the UI layer.
        
        Args:
            top_card: The current top card
            opponent: Opponent player (unused for human)
            game_state: Game state (unused for human)
            
        Returns:
            None (UI will handle the selection)
        """
        # This will be implemented in the UI layer
        return None
    
    def choose_wild_color(self, opponent: Player = None) -> CardColor:
        """Choose a color for wild card (will be handled by UI).
        
        Args:
            opponent: Opponent player (unused for human)
            
        Returns:
            CardColor (UI will handle the selection)
        """
        # This will be implemented in the UI layer
        return CardColor.RED


class AIPlayer(Player):
    """AI player implementation with enhanced strategic AI."""
    
    def __init__(self, name: str = "Computer", difficulty: str = "medium"):
        """Initialize an AI player.
        
        Args:
            name: Player name
            difficulty: AI difficulty (easy, medium, hard)
        """
        super().__init__(name)
        self.difficulty = difficulty
        self._ai_engine = None
    
    def _get_ai_engine(self):
        """Lazy load AI engine to avoid circular imports."""
        if self._ai_engine is None:
            from ..engine.ai_engine import SimpleAI
            self._ai_engine = SimpleAI(self.difficulty)
        return self._ai_engine
    
    def choose_card(self, top_card: Card, opponent: Player = None, 
                   game_state: dict = None) -> Optional[Card]:
        """Choose a card to play using enhanced AI strategy.
        
        Args:
            top_card: The current top card
            opponent: The opponent player (for strategic decisions)
            game_state: Current game state information
            
        Returns:
            Card to play, or None if cannot play
        """
        valid_cards = self.get_valid_cards(top_card)
        
        if not valid_cards:
            return None
        
        # Use enhanced AI if opponent and game state provided
        if opponent and game_state:
            ai_engine = self._get_ai_engine()
            return ai_engine.choose_best_card(
                self, valid_cards, top_card, opponent, game_state
            )
        
        # Fallback to simple strategy
        return self._simple_card_choice(valid_cards, top_card)
    
    def _simple_card_choice(self, valid_cards: List[Card], top_card: Card) -> Card:
        """Simple card selection strategy (fallback).
        
        Args:
            valid_cards: Valid cards to choose from
            top_card: Current top card
            
        Returns:
            Selected card
        """
        # Separate cards by type for strategic selection
        color_matches = []
        number_matches = []
        action_cards = []
        wild_cards = []
        
        for card in valid_cards:
            if card.card_type.value == "wild":
                wild_cards.append(card)
            elif card.color == top_card.color:
                if card.card_type.value == "action":
                    action_cards.append(card)
                else:
                    color_matches.append(card)
            elif card.value == top_card.value:
                number_matches.append(card)
        
        # Priority 1: Color matches (non-action)
        if color_matches:
            return color_matches[0]
        
        # Priority 2: Number matches
        if number_matches:
            return number_matches[0]
        
        # Priority 3: Action cards (use strategically)
        if action_cards:
            # Prefer Skip and Reverse over Draw Two
            skip_reverse = [c for c in action_cards if c.value in ['skip', 'reverse']]
            if skip_reverse:
                return skip_reverse[0]
            return action_cards[0]
        
        # Priority 4: Wild cards (last resort)
        if wild_cards:
            # Prefer regular Wild over Wild Draw Four
            regular_wilds = [c for c in wild_cards if c.value == 'wild']
            if regular_wilds:
                return regular_wilds[0]
            return wild_cards[0]
        
        return valid_cards[0]
    
    def choose_wild_color(self, opponent: Player = None) -> CardColor:
        """Choose a color for wild card using enhanced strategy.
        
        Args:
            opponent: Opponent player for strategic decisions
            
        Returns:
            The chosen color
        """
        # Use enhanced AI if opponent provided
        if opponent:
            ai_engine = self._get_ai_engine()
            return ai_engine.choose_wild_color_strategic(self, opponent)
        
        # Fallback to simple strategy
        return self._simple_color_choice()
    
    def _simple_color_choice(self) -> CardColor:
        """Simple color selection strategy (fallback).
        
        Returns:
            Selected color
        """
        # Count colors in hand (excluding wilds)
        color_counts = {
            CardColor.RED: 0,
            CardColor.BLUE: 0,
            CardColor.GREEN: 0,
            CardColor.YELLOW: 0
        }
        
        for card in self.hand:
            if card.color in color_counts:
                color_counts[card.color] += 1
        
        # Return the most common color, or red if tie/no cards
        if not any(color_counts.values()):
            return CardColor.RED
        
        return max(color_counts, key=color_counts.get)
