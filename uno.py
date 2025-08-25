#!/usr/bin/env python3
"""
🎮 CLI UNO Game - Beautiful Edition!
Combines rich terminal graphics with pure UNO fun.
"""

import random
import os
import sys
import time

# Try to import rich for beautiful display
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.text import Text
    from rich.table import Table
    from rich.align import Align
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Rich library not found. Install with: pip install rich")
    print("   Falling back to basic display...")

class UnoCard:
    def __init__(self, color, value):
        self.color = color  # 'R', 'B', 'G', 'Y', 'W' (wild)
        self.value = value  # '0'-'9', 'S' (skip), 'R' (reverse), 'D' (draw), 'W' (wild), 'F' (wild draw four)
    
    def __str__(self):
        colors = {'R': 'Red', 'B': 'Blue', 'G': 'Green', 'Y': 'Yellow', 'W': 'Wild'}
        values = {'S': 'Skip', 'R': 'Reverse', 'D': 'Draw Two', 'W': 'Wild', 'F': 'Wild Draw Four'}
        
        color_name = colors.get(self.color, self.color)
        value_name = values.get(self.value, self.value)
        
        return f"{color_name} {value_name}"
    
    def get_ascii_art(self):
        """Get ASCII art for the card."""
        symbols = {
            'R': '♦', 'B': '♠', 'G': '♣', 'Y': '♥', 'W': '★',
            'S': '⊘', 'R': '↻', 'D': '+2', 'F': '+4'
        }
        
        symbol = symbols.get(self.value, self.value)
        if self.value.isdigit():
            symbol = self.value
        
        color_symbol = symbols.get(self.color, '•')
        
        return f"┌─────┐\n│{self.color} {symbol:<2} │\n│  {color_symbol}  │\n│ {symbol:>2} {self.color}│\n└─────┘"
    
    def get_rich_art(self):
        """Get rich-formatted ASCII art."""
        if not RICH_AVAILABLE:
            return self.get_ascii_art()
        
        color_styles = {
            'R': "bold red",
            'B': "bold blue", 
            'G': "bold green",
            'Y': "bold yellow",
            'W': "bold magenta"
        }
        
        art = self.get_ascii_art()
        style = color_styles.get(self.color, "white")
        return f"[{style}]{art}[/{style}]"
    
    def can_play_on(self, other_card, current_color=None):
        if self.color == 'W':  # Wild cards can always be played
            return True
        
        effective_color = current_color if current_color else other_card.color
        return self.color == effective_color or self.value == other_card.value

class UnoDeck:
    def __init__(self):
        self.cards = []
        self.discard = []
        self._create_deck()
        self.shuffle()
    
    def _create_deck(self):
        colors = ['R', 'B', 'G', 'Y']
        
        # Number cards (108 total)
        for color in colors:
            self.cards.append(UnoCard(color, '0'))  # One 0 per color
            for num in '123456789':
                self.cards.append(UnoCard(color, num))  # Two of each 1-9
                self.cards.append(UnoCard(color, num))
            
            # Action cards (two of each per color)
            for action in ['S', 'R', 'D']:
                self.cards.append(UnoCard(color, action))
                self.cards.append(UnoCard(color, action))
        
        # Wild cards (4 of each)
        for _ in range(4):
            self.cards.append(UnoCard('W', 'W'))
            self.cards.append(UnoCard('W', 'F'))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, count=1):
        dealt = []
        for _ in range(count):
            if self.cards:
                dealt.append(self.cards.pop())
            elif len(self.discard) > 1:
                # Reshuffle discard pile
                top_card = self.discard.pop()
                self.cards.extend(self.discard)
                self.discard = [top_card]
                self.shuffle()
                if self.cards:
                    dealt.append(self.cards.pop())
        return dealt

class UnoPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def add_cards(self, cards):
        self.hand.extend(cards)
    
    def play_card(self, index):
        if 0 <= index < len(self.hand):
            return self.hand.pop(index)
        return None
    
    def get_valid_cards(self, top_card, current_color=None):
        return [i for i, card in enumerate(self.hand) 
                if card.can_play_on(top_card, current_color)]

class BeautifulUnoGame:
    def __init__(self):
        self.deck = UnoDeck()
        self.player = UnoPlayer("You")
        self.computer = UnoPlayer("Computer")
        self.top_card = None
        self.current_color = None
        self.current_player = self.player
        self.direction = 1
        self.draw_count = 0
        self.game_number = 1
        
        if RICH_AVAILABLE:
            self.console = Console()
        
    def setup(self):
        # Deal 7 cards to each player
        self.player.add_cards(self.deck.deal(7))
        self.computer.add_cards(self.deck.deal(7))
        
        # Set initial top card (not wild or action)
        while True:
            card = self.deck.deal(1)[0]
            if card.color != 'W' and card.value.isdigit():
                self.top_card = card
                self.current_color = card.color
                break
            else:
                self.deck.cards.append(card)
                self.deck.shuffle()
    
    def clear_screen(self):
        if RICH_AVAILABLE:
            self.console.clear()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_title_screen(self):
        """Display title screen."""
        self.clear_screen()
        
        if RICH_AVAILABLE:
            title_art = """
    ██╗   ██╗███╗   ██╗ ██████╗ 
    ██║   ██║████╗  ██║██╔═══██╗
    ██║   ██║██╔██╗ ██║██║   ██║
    ██║   ██║██║╚██╗██║██║   ██║
    ╚██████╔╝██║ ╚████║╚██████╔╝
     ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ 
            """
            
            title_panel = Panel(
                Align.center(title_art),
                title="[bold red]CLI UNO Game[/bold red]",
                subtitle="[dim]Terminal card game[/dim]",
                border_style="bright_blue"
            )
            
            self.console.print(title_panel)
            self.console.print("\n[bold green]🎮 Ready to play![/bold green]")
        else:
            print("🎮 CLI UNO GAME 🎮")
            print("=" * 30)
            print("Terminal card game")
            print("🎮 Ready to play!")
    
    def display_game_rich(self):
        """Display game with rich formatting."""
        self.clear_screen()
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        # Header with game info
        header_table = Table.grid(padding=1)
        header_table.add_column(justify="left")
        header_table.add_column(justify="center") 
        header_table.add_column(justify="right")
        
        header_table.add_row(
            f"[bold]Game #{self.game_number} | Turn: {self.current_player.name}[/bold]",
            "[bold blue]🎮 UNO GAME 🎮[/bold blue]",
            f"[dim]Deck: {len(self.deck.cards)} cards[/dim]"
        )
        
        layout["header"].update(Panel(header_table, border_style="blue"))
        
        # Main area split between board and hand
        layout["main"].split_row(
            Layout(name="board", ratio=1),
            Layout(name="hand", ratio=2)
        )
        
        # Game board with top card
        board_content = f"[bold]Top Card:[/bold]\n\n{self.top_card.get_rich_art()}"
        
        if self.current_color and self.top_card.color == 'W':
            color_styles = {'R': 'red', 'B': 'blue', 'G': 'green', 'Y': 'yellow'}
            color_names = {'R': 'Red', 'B': 'Blue', 'G': 'Green', 'Y': 'Yellow'}
            style = color_styles.get(self.current_color, 'white')
            name = color_names.get(self.current_color, 'Unknown')
            board_content += f"\n\n[bold]Current Color:[/bold]\n[{style}]{name}[/{style}]"
        
        layout["board"].update(Panel(board_content, title="[bold]Game Board[/bold]", border_style="green"))
        
        # Player hand
        hand_content = self._get_rich_hand_display()
        computer_info = f"Computer: {len(self.computer.hand)} cards"
        if len(self.computer.hand) == 1:
            computer_info += " [bold red]- UNO![/bold red]"
        
        hand_title = f"[bold]{self.player.name}'s Hand[/bold] | {computer_info}"
        layout["hand"].update(Panel(hand_content, title=hand_title, border_style="yellow"))
        
        # Footer with controls
        footer_text = "[dim]Commands: [bold]1-9[/bold] Play card • [bold]D[/bold] Draw • [bold]Q[/bold] Quit[/dim]"
        layout["footer"].update(Panel(Align.center(footer_text), border_style="dim"))
        
        self.console.print(layout)
    
    def display_game_basic(self):
        """Display game with basic formatting."""
        self.clear_screen()
        print("🎮 CLI UNO GAME 🎮")
        print("=" * 40)
        print(f"🎯 Game #{self.game_number} | Current Player: {self.current_player.name}")
        print("=" * 40)
        
        # Show top card
        print("📋 TOP CARD:")
        print(self.top_card.get_ascii_art())
        
        if self.current_color and self.top_card.color == 'W':
            colors = {'R': '🔴 Red', 'B': '🔵 Blue', 'G': '🟢 Green', 'Y': '🟡 Yellow'}
            print(f"\n🌈 Current Color: {colors[self.current_color]}")
        
        print(f"\n📦 Cards in deck: {len(self.deck.cards)}")
        print(f"🤖 Computer has {len(self.computer.hand)} cards", end="")
        
        if len(self.computer.hand) == 1:
            print(" - 🚨 UNO!")
        else:
            print()
        
        print("\n" + "="*40)
        print("🃏 YOUR HAND:")
        print("="*40)
        
        for i, card in enumerate(self.player.hand):
            print(f"{i+1:2d}. {card}")
        
        if len(self.player.hand) == 1:
            print("\n🎉 UNO! You have one card left!")
        
        print("\n" + "="*40)
    
    def _get_rich_hand_display(self):
        """Get rich formatted hand display."""
        if not self.player.hand:
            return "[dim]No cards[/dim]"
        
        # Display cards in a grid
        cards_per_row = min(len(self.player.hand), 4)
        result_lines = []
        
        for row_start in range(0, len(self.player.hand), cards_per_row):
            row_cards = self.player.hand[row_start:row_start + cards_per_row]
            
            # Get individual card arts (without rich formatting first)
            card_arts = [card.get_ascii_art().split('\n') for card in row_cards]
            
            # Get color styles for each card
            color_styles = {
                'R': "bold red",
                'B': "bold blue", 
                'G': "bold green",
                'Y': "bold yellow",
                'W': "bold magenta"
            }
            
            # Combine cards horizontally with proper coloring
            for line_idx in range(5):  # 5 lines per card
                line_parts = []
                for i, card_lines in enumerate(card_arts):
                    card = row_cards[i]
                    style = color_styles.get(card.color, "white")
                    colored_line = f"[{style}]{card_lines[line_idx]}[/{style}]"
                    line_parts.append(colored_line)
                result_lines.append(" ".join(line_parts))
            
            # Add card numbers
            number_line = ""
            for i, _ in enumerate(row_cards):
                card_num = str(row_start + i + 1).center(7)
                number_line += f"[dim]{card_num}[/dim] "
            result_lines.append(number_line)
            
            # Add spacing between rows
            if row_start + cards_per_row < len(self.player.hand):
                result_lines.append("")
        
        return "\n".join(result_lines)
    
    def display_game(self):
        """Display game using best available method."""
        if RICH_AVAILABLE:
            self.display_game_rich()
        else:
            self.display_game_basic()
    
    def get_player_move(self):
        valid_indices = self.player.get_valid_cards(self.top_card, self.current_color)
        
        if not valid_indices:
            self.show_message("❌ No valid cards! You must draw a card...", "warning")
            self.wait_for_key("Press Enter to draw...")
            drawn = self.deck.deal(1)
            if drawn:
                self.player.add_cards(drawn)
                self.show_message(f"📥 You drew: {drawn[0]}", "info")
                # Check if drawn card can be played
                new_valid = self.player.get_valid_cards(self.top_card, self.current_color)
                if len(new_valid) > len(valid_indices):
                    play = input(f"✨ You can play the drawn card! Play it? (y/n): ").lower()
                    if play == 'y':
                        return len(self.player.hand) - 1, None
            return None, None
        
        self.show_message(f"✅ Valid cards: {[i+1 for i in valid_indices]}", "info")
        
        while True:
            try:
                choice = self.prompt_input("🎯 Enter card number (1-9), D to draw, Q to quit: ").strip().upper()
                
                if choice == 'Q':
                    return "quit", None
                
                if choice == 'D':
                    drawn = self.deck.deal(1)
                    if drawn:
                        self.player.add_cards(drawn)
                        self.show_message(f"📥 You drew: {drawn[0]}", "info")
                    return None, None
                
                if choice.isdigit():
                    index = int(choice) - 1
                    if index in valid_indices:
                        card = self.player.hand[index]
                        wild_color = None
                        
                        if card.color == 'W':
                            self.show_message("🌈 Choose a color for your wild card:", "info")
                            while True:
                                color = self.prompt_input("Choose color (R/B/G/Y): ").upper()
                                if color in ['R', 'B', 'G', 'Y']:
                                    wild_color = color
                                    break
                                self.show_message("❌ Invalid color! Choose R, B, G, or Y.", "error")
                        
                        return index, wild_color
                    else:
                        self.show_message("❌ Invalid card! Choose from valid cards.", "error")
                else:
                    self.show_message("❌ Invalid input! Enter a number (1-9), D, or Q.", "error")
            
            except (ValueError, IndexError):
                self.show_message("❌ Invalid input! Enter a number, D, or Q.", "error")
    
    def computer_move(self):
        valid_indices = self.computer.get_valid_cards(self.top_card, self.current_color)
        
        if not valid_indices:
            drawn = self.deck.deal(1)
            if drawn:
                self.computer.add_cards(drawn)
                self.show_message("🤖 Computer drew a card", "info")
                # Check if can play drawn card
                new_valid = self.computer.get_valid_cards(self.top_card, self.current_color)
                if len(new_valid) > len(valid_indices):
                    index = len(self.computer.hand) - 1
                    card = self.computer.hand[index]
                    wild_color = None
                    if card.color == 'W':
                        wild_color = random.choice(['R', 'B', 'G', 'Y'])
                    return index, wild_color
            return None, None
        
        # Smart AI strategy
        color_matches = [i for i in valid_indices if self.computer.hand[i].color == self.current_color and self.computer.hand[i].color != 'W']
        number_matches = [i for i in valid_indices if self.computer.hand[i].value == self.top_card.value and self.computer.hand[i].color != 'W']
        action_cards = [i for i in valid_indices if self.computer.hand[i].value in ['S', 'R', 'D'] and self.computer.hand[i].color != 'W']
        wild_cards = [i for i in valid_indices if self.computer.hand[i].color == 'W']
        
        # Strategy: color match > number match > action cards > wild cards
        if color_matches:
            best_index = color_matches[0]
        elif number_matches:
            best_index = number_matches[0]
        elif action_cards:
            best_index = action_cards[0]
        else:
            best_index = valid_indices[0]
        
        card = self.computer.hand[best_index]
        wild_color = None
        if card.color == 'W':
            # Choose most common color in hand
            colors = {'R': 0, 'B': 0, 'G': 0, 'Y': 0}
            for c in self.computer.hand:
                if c.color in colors:
                    colors[c.color] += 1
            wild_color = max(colors, key=colors.get) if any(colors.values()) else 'R'
        
        return best_index, wild_color
    
    def play_card(self, player, index, wild_color=None):
        card = player.play_card(index)
        if card:
            self.deck.discard.append(self.top_card)
            self.top_card = card
            
            if card.color == 'W':
                self.current_color = wild_color
                if card.value == 'F':  # Wild Draw Four
                    self.draw_count += 4
            else:
                self.current_color = card.color
                if card.value == 'D':  # Draw Two
                    self.draw_count += 2
            
            self.show_message(f"✨ {player.name} played: {card}", "success")
            if wild_color:
                colors = {'R': '🔴 Red', 'B': '🔵 Blue', 'G': '🟢 Green', 'Y': '🟡 Yellow'}
                self.show_message(f"🌈 New color: {colors[wild_color]}", "info")
            
            return True
        return False
    
    def handle_draw_penalty(self, player):
        if self.draw_count > 0:
            drawn = self.deck.deal(self.draw_count)
            player.add_cards(drawn)
            self.show_message(f"💥 {player.name} draws {self.draw_count} penalty cards!", "warning")
            self.draw_count = 0
            return True
        return False
    
    def switch_player(self):
        self.current_player = self.computer if self.current_player == self.player else self.player
    
    def show_message(self, message, style="info"):
        """Show a message with appropriate styling."""
        if RICH_AVAILABLE:
            styles = {
                "info": ("blue", "Info"),
                "warning": ("yellow", "Warning"), 
                "success": ("green", "Success"),
                "error": ("red", "Error")
            }
            
            color, title = styles.get(style, ("blue", "Info"))
            panel = Panel(message, title=f"[bold {color}]{title}[/bold {color}]", border_style=color)
            self.console.print(panel)
        else:
            print(f"{message}")
    
    def prompt_input(self, message):
        """Prompt for input with styling."""
        if RICH_AVAILABLE:
            return self.console.input(f"[bold cyan]{message}[/bold cyan]")
        else:
            return input(f"{message}")
    
    def wait_for_key(self, message="Press Enter to continue..."):
        """Wait for key press."""
        input(f"{message}")
    
    def play(self):
        self.show_title_screen()
        self.show_message("✨ Features: ASCII cards, strategic AI, complete UNO rules", "info")
        self.show_message("🏆 Ready to play UNO!", "success")
        self.wait_for_key("Press Enter to start your UNO adventure...")
        
        while True:
            self.setup()
            
            self.show_message(f"🎯 Starting Game #{self.game_number}!", "success")
            self.wait_for_key("Press Enter to begin...")
            
            # Game loop
            while True:
                self.display_game()
                
                # Handle draw penalties
                if self.handle_draw_penalty(self.current_player):
                    self.wait_for_key("Press Enter to continue...")
                    self.switch_player()
                    continue
                
                # Check for winner
                if len(self.player.hand) == 0:
                    self.clear_screen()
                    self.show_message("🎉 CONGRATULATIONS! YOU WIN! 🏆", "success")
                    self.show_message(f"Game #{self.game_number} completed!", "info")
                    break
                elif len(self.computer.hand) == 0:
                    self.clear_screen()
                    self.show_message("🤖 Computer wins this round!", "warning")
                    self.show_message("Better luck next time!", "info")
                    break
                
                # Get move
                if self.current_player == self.player:
                    result = self.get_player_move()
                    if result == ("quit", None):
                        self.show_message("👋 Thanks for playing UNO!", "info")
                        return
                    index, wild_color = result
                else:
                    self.show_message("🤖 Computer is thinking...", "info")
                    time.sleep(1.5)
                    index, wild_color = self.computer_move()
                
                # Play card if valid move
                if index is not None:
                    self.play_card(self.current_player, index, wild_color)
                    self.wait_for_key("Press Enter to continue...")
                
                self.switch_player()
            
            # Game over - show final scores
            self.show_message(f"📊 Final Score - Game #{self.game_number}:", "info")
            self.show_message(f"Your cards left: {len(self.player.hand)}", "info")
            self.show_message(f"Computer cards left: {len(self.computer.hand)}", "info")
            
            play_again = input("\n🎮 Play another game? (y/n): ").lower()
            if play_again != 'y':
                break
            
            # Reset for next game
            self.game_number += 1
            self.deck = UnoDeck()
            self.player.hand = []
            self.computer.hand = []
            self.current_player = self.player
            self.draw_count = 0
        
        self.show_message("🎉 Thanks for playing CLI UNO!", "success")
        self.show_message("🏆 You're a UNO champion!", "success")

def main():
    """Main function."""
    try:
        game = BeautifulUnoGame()
        game.play()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing CLI UNO!")
        print("🏆 Keep playing UNO!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
