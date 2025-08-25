"""Input handler for UNO game with boss key functionality."""

import threading
import time
from typing import List, Optional, Callable
from ..models.card import Card, CardColor
from ..models.player import Player


class InputHandler:
    """Handles user input and boss key detection."""
    
    def __init__(self, display_manager):
        """Initialize input handler.
        
        Args:
            display_manager: The display manager instance
        """
        self.display_manager = display_manager
        self.boss_key_active = False
        self.boss_key_callback: Optional[Callable] = None
        self._keyboard_available = False
        self._setup_keyboard()
    
    def _setup_keyboard(self) -> None:
        """Set up keyboard monitoring for boss key."""
        try:
            # Try to import and use keyboard library safely
            import keyboard
            
            # Test if keyboard library works without crashing
            keyboard.is_pressed('shift')  # Simple test
            
            self._keyboard_available = True
            print("✅ Boss key enabled! Press SPACE to hide the game.")
            
            # Set up boss key (space bar) detection
            keyboard.on_press_key('space', self._on_boss_key_pressed)
            
        except ImportError:
            print("⚠️  Boss key disabled: keyboard library not installed.")
            print("   Install with: pip install keyboard")
            self._keyboard_available = False
        except Exception as e:
            print(f"⚠️  Boss key disabled: {e}")
            print("   Continuing without boss key functionality...")
            self._keyboard_available = False
    
    def _on_boss_key_pressed(self, event) -> None:
        """Handle boss key press event.
        
        Args:
            event: Keyboard event
        """
        if not self.boss_key_active:
            self.boss_key_active = True
            self.display_manager.show_boss_screen()
            
            # Wait for any key to return to game
            self._wait_for_return_key()
    
    def _wait_for_return_key(self) -> None:
        """Wait for any key press to return from boss mode."""
        def wait_thread():
            try:
                if self._keyboard_available:
                    import keyboard
                    while self.boss_key_active:
                        event = keyboard.read_event()
                        if event.event_type == keyboard.KEY_DOWN and event.name != 'space':
                            self.boss_key_active = False
                            self.display_manager.exit_boss_mode()
                            break
                        time.sleep(0.1)
                else:
                    # Fallback: wait for Enter in terminal
                    input()  # Wait for Enter key
                    self.boss_key_active = False
                    self.display_manager.exit_boss_mode()
            except:
                # Fallback: wait for Enter in terminal
                try:
                    input()  # Wait for Enter key
                except:
                    pass
                self.boss_key_active = False
                self.display_manager.exit_boss_mode()
        
        # Run in separate thread to not block main game
        thread = threading.Thread(target=wait_thread, daemon=True)
        thread.start()
    
    def get_player_move(self, player: Player, valid_cards: List[Card], 
                       top_card: Card) -> Optional[tuple]:
        """Get player's move choice.
        
        Args:
            player: The player making the move
            valid_cards: List of valid cards to play
            top_card: Current top card
            
        Returns:
            Tuple of (action, card_index, wild_color) or None for draw
            Actions: 'play', 'draw', 'quit'
        """
        if self.boss_key_active:
            return None
        
        while True:
            try:
                # Show available options
                self._show_move_options(valid_cards)
                
                # Get user input
                prompt = "Enter your choice (1-9 to play card, D to draw, Q to quit"
                if self._keyboard_available:
                    prompt += ", SPACE for boss key"
                prompt += "): "
                
                choice = self.display_manager.prompt_input(prompt).strip().upper()
                
                if self.boss_key_active:
                    return None
                
                # Handle quit
                if choice == 'Q':
                    return ('quit', None, None)
                
                # Handle draw
                if choice == 'D':
                    return ('draw', None, None)
                
                # Handle card selection
                if choice.isdigit():
                    card_index = int(choice) - 1
                    
                    if 0 <= card_index < len(player.hand):
                        selected_card = player.hand[card_index]
                        
                        # Check if card is valid
                        if selected_card in valid_cards:
                            # Handle wild card color selection
                            wild_color = None
                            if selected_card.card_type.value == "wild":
                                wild_color = self._get_wild_color_choice()
                                if wild_color is None:  # User cancelled
                                    continue
                            
                            return ('play', card_index, wild_color)
                        else:
                            self.display_manager.show_error(
                                f"Cannot play {selected_card}. It doesn't match the top card."
                            )
                    else:
                        self.display_manager.show_error(
                            f"Invalid card number. Choose 1-{len(player.hand)}."
                        )
                else:
                    self.display_manager.show_error(
                        "Invalid input. Enter a number (1-9), D to draw, or Q to quit."
                    )
                
            except KeyboardInterrupt:
                return ('quit', None, None)
            except Exception as e:
                self.display_manager.show_error(f"Input error: {e}")
    
    def _show_move_options(self, valid_cards: List[Card]) -> None:
        """Show available move options to the player.
        
        Args:
            valid_cards: List of valid cards that can be played
        """
        if not valid_cards:
            self.display_manager.show_message(
                "No valid cards to play. You must draw a card.", 
                "warning"
            )
        else:
            card_list = ", ".join([f"{i+1}: {card}" for i, card in enumerate(valid_cards)])
            self.display_manager.show_message(
                f"Valid cards: {card_list}", 
                "info"
            )
    
    def _get_wild_color_choice(self) -> Optional[CardColor]:
        """Get color choice for wild card.
        
        Returns:
            Chosen CardColor or None if cancelled
        """
        color_options = {
            'R': CardColor.RED,
            'B': CardColor.BLUE, 
            'G': CardColor.GREEN,
            'Y': CardColor.YELLOW
        }
        
        while True:
            if self.boss_key_active:
                return None
            
            choice = self.display_manager.prompt_input(
                "Choose color for wild card (R/B/G/Y): "
            ).strip().upper()
            
            if choice in color_options:
                return color_options[choice]
            elif choice == '':
                return None  # Cancel
            else:
                self.display_manager.show_error(
                    "Invalid color. Choose R (Red), B (Blue), G (Green), or Y (Yellow)."
                )
    
    def get_yes_no_input(self, prompt: str) -> bool:
        """Get yes/no input from user.
        
        Args:
            prompt: The prompt message
            
        Returns:
            True for yes, False for no
        """
        while True:
            if self.boss_key_active:
                return False
            
            choice = self.display_manager.prompt_input(
                f"{prompt} (y/n): "
            ).strip().lower()
            
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                self.display_manager.show_error("Please enter 'y' for yes or 'n' for no.")
    
    def wait_for_key(self, message: str = "Press any key to continue...") -> None:
        """Wait for any key press.
        
        Args:
            message: Message to display
        """
        if self.boss_key_active:
            return
        
        try:
            # Always use input() for reliability
            input(f"{message} (Press Enter)")
        except:
            pass
    
    def cleanup(self) -> None:
        """Clean up keyboard hooks."""
        try:
            if self._keyboard_available:
                import keyboard
                keyboard.unhook_all()
        except:
            pass
    
    def is_boss_key_available(self) -> bool:
        """Check if boss key functionality is available.
        
        Returns:
            True if boss key is available
        """
        return self._keyboard_available
