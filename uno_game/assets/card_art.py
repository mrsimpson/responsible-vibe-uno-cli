"""ASCII art templates and rendering for UNO cards."""

from typing import Dict, List
from ..models.card import Card, CardColor, CardType


class CardArtist:
    """Handles ASCII art rendering for UNO cards."""
    
    # Color mappings for rich console
    COLOR_STYLES = {
        CardColor.RED: "bold red",
        CardColor.BLUE: "bold blue", 
        CardColor.GREEN: "bold green",
        CardColor.YELLOW: "bold yellow",
        CardColor.WILD: "bold magenta"
    }
    
    # Symbols for different card types
    SYMBOLS = {
        # Numbers use the number itself
        "skip": "⊘",
        "reverse": "↻", 
        "draw_two": "+2",
        "wild": "★",
        "wild_draw_four": "+4"
    }
    
    def __init__(self):
        """Initialize the card artist."""
        pass
    
    def get_card_art(self, card: Card, width: int = 7, height: int = 5) -> List[str]:
        """Generate ASCII art for a card.
        
        Args:
            card: The card to render
            width: Width of the card in characters
            height: Height of the card in characters
            
        Returns:
            List of strings representing the card art
        """
        # Get card display elements
        color_char = self._get_color_char(card.color)
        symbol = self._get_symbol(card.value)
        
        # Create the card template
        lines = []
        
        # Top border
        lines.append("┌" + "─" * (width - 2) + "┐")
        
        # Top line with color and symbol
        top_content = f"{color_char} {symbol}"
        padding = width - 2 - len(top_content)
        lines.append("│" + top_content + " " * padding + "│")
        
        # Middle lines with center symbol
        for i in range(height - 4):
            center_symbol = self._get_center_symbol(card)
            center_padding = (width - 2 - len(center_symbol)) // 2
            line_content = " " * center_padding + center_symbol + " " * (width - 2 - center_padding - len(center_symbol))
            lines.append("│" + line_content + "│")
        
        # Bottom line with inverted color and symbol
        bottom_content = f"{symbol} {color_char}"
        padding = width - 2 - len(bottom_content)
        lines.append("│" + " " * padding + bottom_content + "│")
        
        # Bottom border
        lines.append("└" + "─" * (width - 2) + "┘")
        
        return lines
    
    def get_colored_card_art(self, card: Card, width: int = 7, height: int = 5) -> str:
        """Generate colored ASCII art for a card using rich markup.
        
        Args:
            card: The card to render
            width: Width of the card
            height: Height of the card
            
        Returns:
            Rich markup string for colored display
        """
        lines = self.get_card_art(card, width, height)
        color_style = self.COLOR_STYLES.get(card.color, "white")
        
        # Wrap each line in color markup
        colored_lines = [f"[{color_style}]{line}[/{color_style}]" for line in lines]
        return "\n".join(colored_lines)
    
    def get_hand_display(self, cards: List[Card], max_width: int = 80) -> str:
        """Display a hand of cards in a row.
        
        Args:
            cards: List of cards to display
            max_width: Maximum width for the display
            
        Returns:
            Rich markup string showing all cards
        """
        if not cards:
            return "[dim]No cards[/dim]"
        
        card_width = 7
        spacing = 1
        cards_per_row = min(len(cards), (max_width + spacing) // (card_width + spacing))
        
        result_lines = []
        
        # Process cards in rows
        for row_start in range(0, len(cards), cards_per_row):
            row_cards = cards[row_start:row_start + cards_per_row]
            
            # Get all card arts for this row
            card_arts = [self.get_card_art(card) for card in row_cards]
            
            # Combine cards horizontally
            for line_idx in range(5):  # 5 lines per card
                line_parts = []
                for i, card in enumerate(row_cards):
                    color_style = self.COLOR_STYLES.get(card.color, "white")
                    colored_line = f"[{color_style}]{card_arts[i][line_idx]}[/{color_style}]"
                    line_parts.append(colored_line)
                
                result_lines.append(" " * spacing + (" " * spacing).join(line_parts))
            
            # Add card numbers below each card
            if len(row_cards) > 1:
                number_line = " " * spacing
                for i, _ in enumerate(row_cards):
                    card_num = str(row_start + i + 1).center(card_width)
                    number_line += f"[dim]{card_num}[/dim]" + " " * spacing
                result_lines.append(number_line)
            
            # Add spacing between rows
            if row_start + cards_per_row < len(cards):
                result_lines.append("")
        
        return "\n".join(result_lines)
    
    def get_game_board(self, top_card: Card, current_color: CardColor = None) -> str:
        """Display the game board with top card.
        
        Args:
            top_card: The current top card
            current_color: Current color (for wild cards)
            
        Returns:
            Rich markup string for the game board
        """
        lines = []
        
        # Title
        lines.append("[bold]🎮 UNO Game Board[/bold]")
        lines.append("")
        
        # Current top card
        lines.append("[bold]Top Card:[/bold]")
        lines.append(self.get_colored_card_art(top_card))
        
        # Show current color if different (wild cards)
        if current_color and current_color != top_card.color:
            color_style = self.COLOR_STYLES.get(current_color, "white")
            lines.append(f"[bold]Current Color: [{color_style}]{current_color.value.title()}[/{color_style}][/bold]")
        
        return "\n".join(lines)
    
    def _get_color_char(self, color: CardColor) -> str:
        """Get single character representation of color.
        
        Args:
            color: The card color
            
        Returns:
            Single character for the color
        """
        return {
            CardColor.RED: "R",
            CardColor.BLUE: "B", 
            CardColor.GREEN: "G",
            CardColor.YELLOW: "Y",
            CardColor.WILD: "W"
        }.get(color, "?")
    
    def _get_symbol(self, value: str) -> str:
        """Get symbol representation for card value.
        
        Args:
            value: The card value
            
        Returns:
            Symbol to display on card
        """
        if value.isdigit():
            return value
        return self.SYMBOLS.get(value, value[:2].upper())
    
    def _get_center_symbol(self, card: Card) -> str:
        """Get center symbol for the card.
        
        Args:
            card: The card
            
        Returns:
            Center symbol to display
        """
        if card.color == CardColor.RED:
            return "♦"
        elif card.color == CardColor.BLUE:
            return "♠"
        elif card.color == CardColor.GREEN:
            return "♣"
        elif card.color == CardColor.YELLOW:
            return "♥"
        elif card.color == CardColor.WILD:
            return "★"
        return "•"
    
    def get_card_back(self, width: int = 7, height: int = 5) -> str:
        """Get ASCII art for card back.
        
        Args:
            width: Card width
            height: Card height
            
        Returns:
            Rich markup for card back
        """
        lines = []
        
        # Top border
        lines.append("┌" + "─" * (width - 2) + "┐")
        
        # Fill with pattern
        for i in range(height - 2):
            if i == (height - 2) // 2:
                content = "UNO".center(width - 2)
            else:
                content = "░" * (width - 2)
            lines.append("│" + content + "│")
        
        # Bottom border
        lines.append("└" + "─" * (width - 2) + "┘")
        
        colored_lines = [f"[bold blue]{line}[/bold blue]" for line in lines]
        return "\n".join(colored_lines)
