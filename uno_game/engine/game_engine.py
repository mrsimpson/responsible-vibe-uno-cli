"""Main game engine for UNO game."""

from typing import List, Optional, Tuple
from ..models.card import Card, Deck, CardColor, CardType
from ..models.player import Player, HumanPlayer, AIPlayer
from ..models.game_state import GameState, GamePhase


class UnoGame:
    """Main UNO game engine that manages game flow and rules."""
    
    def __init__(self):
        """Initialize the UNO game."""
        self.deck: Optional[Deck] = None
        self.game_state: Optional[GameState] = None
        self.human_player: Optional[HumanPlayer] = None
        self.ai_player: Optional[AIPlayer] = None
    
    def setup_game(self, human_name: str = "Player", ai_name: str = "Computer") -> None:
        """Set up a new game.
        
        Args:
            human_name: Name for the human player
            ai_name: Name for the AI player
        """
        # Create players
        self.human_player = HumanPlayer(human_name)
        self.ai_player = AIPlayer(ai_name)
        
        # Create deck and game state
        self.deck = Deck()
        self.game_state = GameState([self.human_player, self.ai_player])
        
        # Deal initial hands
        self.human_player.hand = self.deck.deal_hand(7)
        self.ai_player.hand = self.deck.deal_hand(7)
        
        # Set initial top card (must not be a wild or action card)
        self._set_initial_top_card()
        
        # Start the game
        self.game_state.start_game()
    
    def _set_initial_top_card(self) -> None:
        """Set the initial top card, ensuring it's not wild or action."""
        while True:
            card = self.deck.deal_card()
            if card and card.card_type == CardType.NUMBER:
                self.deck.add_to_discard(card)
                self.game_state.set_top_card(card)
                break
            elif card:
                # Put action/wild cards back in deck
                self.deck.cards.append(card)
                self.deck.shuffle()
    
    def can_play_card(self, player: Player, card: Card) -> bool:
        """Check if a player can play a specific card.
        
        Args:
            player: The player attempting to play
            card: The card to play
            
        Returns:
            True if the card can be played
        """
        if card not in player.hand:
            return False
        
        # Check if card can be played on current top card
        top_card = self.game_state.top_card
        if not top_card:
            return False
        
        # For wild cards, always playable
        if card.card_type == CardType.WILD:
            return True
        
        # Check color match (considering wild card color)
        effective_color = self.game_state.get_effective_color()
        if card.color == effective_color:
            return True
        
        # Check value match
        if card.value == top_card.value:
            return True
        
        return False
    
    def play_card(self, player: Player, card: Card, chosen_color: Optional[CardColor] = None) -> bool:
        """Attempt to play a card.
        
        Args:
            player: The player playing the card
            card: The card to play
            chosen_color: Color choice for wild cards
            
        Returns:
            True if card was successfully played
        """
        if not self.can_play_card(player, card):
            return False
        
        # Remove card from player's hand
        player.remove_card(card)
        
        # Add to discard pile
        self.deck.add_to_discard(card)
        self.game_state.set_top_card(card)
        
        # Handle wild cards
        if card.card_type == CardType.WILD:
            if chosen_color:
                self.game_state.set_wild_color(chosen_color)
            else:
                # AI chooses color automatically
                if isinstance(player, AIPlayer):
                    color = player.choose_wild_color()
                    self.game_state.set_wild_color(color)
        
        # Apply card effects
        self._apply_card_effects(card)
        
        # Check for UNO call
        if player.should_call_uno():
            player.call_uno()
        
        # Check for winner
        self.game_state.check_winner()
        
        return True
    
    def _apply_card_effects(self, card: Card) -> None:
        """Apply the effects of a played card.
        
        Args:
            card: The card that was played
        """
        if card.value == 'skip':
            self.game_state.skip_next_player()
        elif card.value == 'reverse':
            # In 2-player game, reverse acts like skip
            self.game_state.reverse_direction()
            self.game_state.skip_next_player()
        elif card.value == 'draw_two':
            self.game_state.add_draw_count(2)
            self.game_state.skip_next_player()
        elif card.value == 'wild_draw_four':
            self.game_state.add_draw_count(4)
            self.game_state.skip_next_player()
    
    def draw_cards(self, player: Player, count: int = 1) -> List[Card]:
        """Make a player draw cards from the deck.
        
        Args:
            player: The player drawing cards
            count: Number of cards to draw
            
        Returns:
            List of cards drawn
        """
        drawn_cards = []
        for _ in range(count):
            card = self.deck.deal_card()
            if card:
                player.add_card(card)
                drawn_cards.append(card)
        return drawn_cards
    
    def handle_draw_penalty(self, player: Player) -> List[Card]:
        """Handle draw penalty from Draw Two/Draw Four cards.
        
        Args:
            player: The player who must draw
            
        Returns:
            List of cards drawn
        """
        draw_count = self.game_state.draw_count
        if draw_count > 0:
            drawn_cards = self.draw_cards(player, draw_count)
            self.game_state.reset_draw_count()
            return drawn_cards
        return []
    
    def get_valid_moves(self, player: Player) -> List[Card]:
        """Get all valid cards a player can play.
        
        Args:
            player: The player to check
            
        Returns:
            List of playable cards
        """
        return [card for card in player.hand if self.can_play_card(player, card)]
    
    def must_draw(self, player: Player) -> bool:
        """Check if player must draw cards (no valid moves).
        
        Args:
            player: The player to check
            
        Returns:
            True if player must draw
        """
        return len(self.get_valid_moves(player)) == 0
    
    def advance_turn(self) -> None:
        """Advance to the next player's turn."""
        self.game_state.advance_turn()
    
    def get_current_player(self) -> Player:
        """Get the current player.
        
        Returns:
            The player whose turn it is
        """
        return self.game_state.get_current_player()
    
    def is_game_over(self) -> bool:
        """Check if the game is over.
        
        Returns:
            True if game is finished
        """
        return self.game_state.is_game_over()
    
    def get_winner(self) -> Optional[Player]:
        """Get the winner of the game.
        
        Returns:
            The winning player, or None if game not finished
        """
        return self.game_state.winner
    
    def get_game_info(self) -> dict:
        """Get current game information.
        
        Returns:
            Dictionary with game state information
        """
        info = self.game_state.get_game_info()
        info['deck_cards'] = self.deck.cards_remaining()
        info['discard_cards'] = len(self.deck.discard_pile)
        return info
    
    def restart_game(self) -> None:
        """Restart the game with the same players."""
        if self.human_player and self.ai_player:
            self.setup_game(self.human_player.name, self.ai_player.name)
