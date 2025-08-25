"""Game state management for UNO game."""

from typing import List, Optional
from enum import Enum
from .card import Card, CardColor
from .player import Player


class GameDirection(Enum):
    """Direction of play."""
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


class GamePhase(Enum):
    """Current phase of the game."""
    SETUP = "setup"
    PLAYING = "playing"
    FINISHED = "finished"


class GameState:
    """Manages the current state of the UNO game."""
    
    def __init__(self, players: List[Player]):
        """Initialize game state.
        
        Args:
            players: List of players in the game
        """
        self.players = players
        self.current_player_index = 0
        self.direction = GameDirection.CLOCKWISE
        self.phase = GamePhase.SETUP
        self.top_card: Optional[Card] = None
        self.current_color: Optional[CardColor] = None  # For wild cards
        self.draw_count = 0  # For stacking Draw Two/Draw Four cards
        self.winner: Optional[Player] = None
        self.game_over = False
    
    def get_current_player(self) -> Player:
        """Get the current player.
        
        Returns:
            The player whose turn it is
        """
        return self.players[self.current_player_index]
    
    def get_next_player(self) -> Player:
        """Get the next player without advancing turn.
        
        Returns:
            The next player in turn order
        """
        next_index = self._get_next_player_index()
        return self.players[next_index]
    
    def advance_turn(self) -> None:
        """Advance to the next player's turn."""
        self.current_player_index = self._get_next_player_index()
        
        # Reset UNO call status for all players except current
        for i, player in enumerate(self.players):
            if i != self.current_player_index:
                player.reset_uno_call()
    
    def _get_next_player_index(self) -> int:
        """Calculate the next player index based on direction.
        
        Returns:
            Index of the next player
        """
        if self.direction == GameDirection.CLOCKWISE:
            return (self.current_player_index + 1) % len(self.players)
        else:
            return (self.current_player_index - 1) % len(self.players)
    
    def reverse_direction(self) -> None:
        """Reverse the direction of play."""
        if self.direction == GameDirection.CLOCKWISE:
            self.direction = GameDirection.COUNTERCLOCKWISE
        else:
            self.direction = GameDirection.CLOCKWISE
    
    def skip_next_player(self) -> None:
        """Skip the next player's turn."""
        self.advance_turn()  # Skip one player
        self.advance_turn()  # Move to the player after the skipped one
        # Go back one so advance_turn() in main loop works correctly
        if self.direction == GameDirection.CLOCKWISE:
            self.current_player_index = (self.current_player_index - 1) % len(self.players)
        else:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def set_top_card(self, card: Card) -> None:
        """Set the top card of the discard pile.
        
        Args:
            card: The new top card
        """
        self.top_card = card
        
        # If it's a wild card, keep the chosen color
        if card.card_type.value != "wild":
            self.current_color = card.color
    
    def set_wild_color(self, color: CardColor) -> None:
        """Set the color for a wild card.
        
        Args:
            color: The chosen color
        """
        self.current_color = color
    
    def get_effective_color(self) -> Optional[CardColor]:
        """Get the effective color for card matching.
        
        For wild cards, returns the chosen color.
        For regular cards, returns the card's color.
        
        Returns:
            The effective color for matching
        """
        return self.current_color
    
    def add_draw_count(self, count: int) -> None:
        """Add to the draw count for stacking draw cards.
        
        Args:
            count: Number of cards to add to draw count
        """
        self.draw_count += count
    
    def reset_draw_count(self) -> None:
        """Reset the draw count."""
        self.draw_count = 0
    
    def check_winner(self) -> Optional[Player]:
        """Check if any player has won (no cards left).
        
        Returns:
            The winning player, or None if no winner yet
        """
        for player in self.players:
            if not player.has_cards():
                self.winner = player
                self.game_over = True
                self.phase = GamePhase.FINISHED
                return player
        return None
    
    def is_game_over(self) -> bool:
        """Check if the game is over.
        
        Returns:
            True if game is finished
        """
        return self.game_over
    
    def start_game(self) -> None:
        """Start the game (move from setup to playing phase)."""
        self.phase = GamePhase.PLAYING
    
    def get_game_info(self) -> dict:
        """Get current game information for display.
        
        Returns:
            Dictionary with current game state info
        """
        return {
            'current_player': self.get_current_player().name,
            'direction': 'Clockwise' if self.direction == GameDirection.CLOCKWISE else 'Counterclockwise',
            'top_card': str(self.top_card) if self.top_card else 'None',
            'effective_color': self.current_color.value if self.current_color else 'None',
            'draw_count': self.draw_count,
            'phase': self.phase.value,
            'players': [{'name': p.name, 'cards': p.card_count()} for p in self.players]
        }
