"""Main game loop for CLI UNO game."""

import time
import sys
from typing import Optional

from .engine.game_engine import UnoGame
from .ui.display import DisplayManager
from .ui.input_handler import InputHandler
from .models.card import CardColor
from .models.player import HumanPlayer, AIPlayer


class UnoGameController:
    """Main game controller that orchestrates the UNO game."""
    
    def __init__(self):
        """Initialize the game controller."""
        self.game = UnoGame()
        self.display = DisplayManager()
        self.input_handler = InputHandler(self.display)
        self.running = True
    
    def start_game(self) -> None:
        """Start and run the main game loop."""
        try:
            self._show_welcome()
            self._setup_game()
            self._main_game_loop()
        except KeyboardInterrupt:
            self.display.show_message("Game interrupted by user.", "info")
        except Exception as e:
            self.display.show_error(f"Unexpected error: {e}")
        finally:
            self._cleanup()
    
    def _show_welcome(self) -> None:
        """Show welcome screen and game info."""
        self.display.show_title_screen()
        time.sleep(2)
        
        # Show boss key info if available
        if self.input_handler.is_boss_key_available():
            self.display.show_message(
                "🕵️ Boss key enabled! Press SPACE to hide the game instantly.", 
                "success"
            )
        else:
            self.display.show_message(
                "⚠️ Boss key not available (keyboard library not installed).", 
                "warning"
            )
        
        self.input_handler.wait_for_key("Press any key to start...")
    
    def _setup_game(self) -> None:
        """Set up a new game."""
        # Get player names (optional)
        human_name = "Player"
        ai_name = "Computer"
        
        # Set up the game
        self.game.setup_game(human_name, ai_name)
        
        self.display.show_message("Game setup complete! Let's play UNO!", "success")
        time.sleep(1)
    
    def _main_game_loop(self) -> None:
        """Main game loop."""
        while self.running and not self.game.is_game_over():
            try:
                current_player = self.game.get_current_player()
                
                # Show current game state
                self._display_game_state()
                
                # Handle player turn
                if isinstance(current_player, HumanPlayer):
                    self._handle_human_turn(current_player)
                else:
                    self._handle_ai_turn(current_player)
                
                # Check for winner
                if self.game.is_game_over():
                    self._show_game_over()
                    break
                
                # Advance to next turn
                self.game.advance_turn()
                
                # Small delay for readability
                time.sleep(0.5)
                
            except Exception as e:
                self.display.show_error(f"Error during game: {e}")
                break
    
    def _display_game_state(self) -> None:
        """Display the current game state."""
        if self.input_handler.boss_key_active:
            return
        
        current_player = self.game.get_current_player()
        top_card = self.game.game_state.top_card
        current_color = self.game.game_state.get_effective_color()
        game_info = self.game.get_game_info()
        
        self.display.show_game_state(game_info, current_player, top_card, current_color)
    
    def _handle_human_turn(self, player: HumanPlayer) -> None:
        """Handle human player's turn.
        
        Args:
            player: The human player
        """
        # Handle draw penalty first
        if self.game.game_state.draw_count > 0:
            penalty_cards = self.game.handle_draw_penalty(player)
            self.display.show_draw_cards(
                player, penalty_cards, 
                f"penalty ({self.game.game_state.draw_count} cards)"
            )
            self.input_handler.wait_for_key()
            return
        
        # Get valid moves
        valid_cards = self.game.get_valid_moves(player)
        top_card = self.game.game_state.top_card
        
        # Check if player must draw
        if not valid_cards:
            drawn_cards = self.game.draw_cards(player, 1)
            self.display.show_draw_cards(player, drawn_cards, "no valid moves")
            
            # Check if drawn card can be played
            if drawn_cards:
                new_valid_cards = self.game.get_valid_moves(player)
                if drawn_cards[0] in new_valid_cards:
                    play_drawn = self.input_handler.get_yes_no_input(
                        f"You drew {drawn_cards[0]}. Do you want to play it?"
                    )
                    if play_drawn:
                        self._play_card(player, drawn_cards[0])
            return
        
        # Get player's move
        move_result = self.input_handler.get_player_move(player, valid_cards, top_card)
        
        if not move_result:
            return  # Boss key activated or other interruption
        
        action, card_index, wild_color = move_result
        
        if action == 'quit':
            self.running = False
            return
        elif action == 'draw':
            drawn_cards = self.game.draw_cards(player, 1)
            self.display.show_draw_cards(player, drawn_cards, "player choice")
        elif action == 'play' and card_index is not None:
            card_to_play = player.hand[card_index]
            self._play_card(player, card_to_play, wild_color)
    
    def _handle_ai_turn(self, player: AIPlayer) -> None:
        """Handle AI player's turn.
        
        Args:
            player: The AI player
        """
        # Show AI thinking
        self.display.show_message(f"{player.name} is thinking...", "info")
        time.sleep(1)  # Simulate thinking time
        
        # Handle draw penalty first
        if self.game.game_state.draw_count > 0:
            penalty_cards = self.game.handle_draw_penalty(player)
            self.display.show_draw_cards(
                player, penalty_cards, 
                f"penalty ({len(penalty_cards)} cards)"
            )
            self.input_handler.wait_for_key()
            return
        
        # Get AI's choice
        top_card = self.game.game_state.top_card
        opponent = self.game.human_player
        game_info = self.game.get_game_info()
        
        chosen_card = player.choose_card(top_card, opponent, game_info)
        
        if chosen_card:
            # AI chooses wild color if needed
            wild_color = None
            if chosen_card.card_type.value == "wild":
                wild_color = player.choose_wild_color(opponent)
            
            self._play_card(player, chosen_card, wild_color)
        else:
            # AI must draw
            drawn_cards = self.game.draw_cards(player, 1)
            self.display.show_draw_cards(player, drawn_cards, "no valid moves")
            
            # Check if AI can play the drawn card
            if drawn_cards:
                new_top_card = self.game.game_state.top_card
                if self.game.can_play_card(player, drawn_cards[0]):
                    wild_color = None
                    if drawn_cards[0].card_type.value == "wild":
                        wild_color = player.choose_wild_color(opponent)
                    
                    self.display.show_message(
                        f"{player.name} plays the drawn card!", "info"
                    )
                    self._play_card(player, drawn_cards[0], wild_color)
        
        self.input_handler.wait_for_key()
    
    def _play_card(self, player, card, wild_color: Optional[CardColor] = None) -> None:
        """Play a card for a player.
        
        Args:
            player: The player playing the card
            card: The card to play
            wild_color: Color choice for wild cards
        """
        success = self.game.play_card(player, card, wild_color)
        
        if success:
            self.display.show_card_played(player, card)
            
            # Show wild color choice
            if wild_color:
                self.display.show_message(
                    f"{player.name} chose {wild_color.value} as the new color!", 
                    "info"
                )
            
            # Check for UNO call
            if player.should_call_uno() and player.has_called_uno:
                self.display.show_uno_call(player)
        else:
            self.display.show_error(f"Could not play {card}")
    
    def _show_game_over(self) -> None:
        """Show game over screen."""
        winner = self.game.get_winner()
        
        if winner:
            # Calculate final scores
            final_scores = {}
            for player in [self.game.human_player, self.game.ai_player]:
                final_scores[player.name] = {
                    'cards_left': player.card_count(),
                    'points': player.get_hand_points()
                }
            
            self.display.show_winner(winner, final_scores)
        
        # Ask if player wants to play again
        if self.input_handler.get_yes_no_input("Would you like to play again?"):
            self.game.restart_game()
            self._main_game_loop()
        else:
            self.running = False
    
    def _cleanup(self) -> None:
        """Clean up resources."""
        self.input_handler.cleanup()
        self.display.show_message("Thanks for playing UNO! 🎮", "success")


def main():
    """Main entry point for the UNO game."""
    try:
        controller = UnoGameController()
        controller.start_game()
    except Exception as e:
        print(f"Failed to start game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
