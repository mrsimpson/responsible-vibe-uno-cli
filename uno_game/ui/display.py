"""Display manager for UNO game using rich library."""

import os
import time
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich.align import Align

from ..models.card import Card, CardColor
from ..models.player import Player
from ..assets.card_art import CardArtist


class DisplayManager:
    """Manages all display output for the UNO game."""
    
    def __init__(self):
        """Initialize the display manager."""
        self.console = Console()
        self.card_artist = CardArtist()
        self.boss_mode = False
        self._original_screen = ""
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_title_screen(self) -> None:
        """Display the game title screen."""
        self.clear_screen()
        
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
            subtitle="[dim]Press SPACE for boss key • Perfect for boring meetings[/dim]",
            border_style="bright_blue"
        )
        
        self.console.print(title_panel)
        self.console.print("\n[bold green]🎮 Starting game...[/bold green]")
    
    def show_game_state(self, game_info: dict, current_player: Player, 
                       top_card: Card, current_color: Optional[CardColor] = None) -> None:
        """Display the current game state.
        
        Args:
            game_info: Game information dictionary
            current_player: The current player
            top_card: Current top card
            current_color: Current effective color
        """
        if self.boss_mode:
            return
        
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
            f"[bold]Turn: {game_info['current_player']}[/bold]",
            "[bold blue]🎮 UNO GAME 🎮[/bold blue]",
            f"[dim]Cards left: {game_info['deck_cards']}[/dim]"
        )
        
        layout["header"].update(Panel(header_table, border_style="blue"))
        
        # Main area split between board and hand
        layout["main"].split_row(
            Layout(name="board", ratio=1),
            Layout(name="hand", ratio=2)
        )
        
        # Game board
        board_content = self.card_artist.get_game_board(top_card, current_color)
        layout["board"].update(Panel(board_content, title="[bold]Game Board[/bold]", border_style="green"))
        
        # Player hand
        hand_content = self._get_hand_display(current_player)
        layout["hand"].update(Panel(hand_content, title=f"[bold]{current_player.name}'s Hand[/bold]", border_style="yellow"))
        
        # Footer with controls
        footer_text = "[dim]Commands: [bold]1-9[/bold] Play card • [bold]D[/bold] Draw • [bold]Q[/bold] Quit • [bold]SPACE[/bold] Boss key[/dim]"
        layout["footer"].update(Panel(Align.center(footer_text), border_style="dim"))
        
        self.console.print(layout)
    
    def show_player_hand(self, player: Player, show_numbers: bool = True) -> None:
        """Display a player's hand.
        
        Args:
            player: The player whose hand to show
            show_numbers: Whether to show card numbers for selection
        """
        if not player.hand:
            self.console.print("[dim]No cards in hand[/dim]")
            return
        
        hand_display = self.card_artist.get_hand_display(player.hand)
        self.console.print(hand_display)
    
    def _get_hand_display(self, player: Player) -> str:
        """Get formatted hand display for a player.
        
        Args:
            player: The player
            
        Returns:
            Formatted hand display string
        """
        if not player.hand:
            return "[dim]No cards[/dim]"
        
        return self.card_artist.get_hand_display(player.hand)
    
    def show_card_played(self, player: Player, card: Card) -> None:
        """Show animation/message when a card is played.
        
        Args:
            player: Player who played the card
            card: Card that was played
        """
        if self.boss_mode:
            return
        
        card_art = self.card_artist.get_colored_card_art(card)
        
        panel = Panel(
            Align.center(f"{player.name} played:\n\n{card_art}"),
            title="[bold green]Card Played![/bold green]",
            border_style="green"
        )
        
        self.console.print(panel)
        time.sleep(1.5)  # Brief pause to show the played card
    
    def show_draw_cards(self, player: Player, cards: List[Card], reason: str = "") -> None:
        """Show when a player draws cards.
        
        Args:
            player: Player drawing cards
            cards: Cards drawn
            reason: Reason for drawing (penalty, no moves, etc.)
        """
        if self.boss_mode:
            return
        
        message = f"{player.name} drew {len(cards)} card(s)"
        if reason:
            message += f" ({reason})"
        
        self.console.print(f"[yellow]{message}[/yellow]")
    
    def show_uno_call(self, player: Player) -> None:
        """Show UNO call animation.
        
        Args:
            player: Player calling UNO
        """
        if self.boss_mode:
            return
        
        uno_text = Text("🎉 UNO! 🎉", style="bold red blink")
        panel = Panel(
            Align.center(f"{player.name} calls\n{uno_text}"),
            title="[bold red]UNO CALLED![/bold red]",
            border_style="red"
        )
        
        self.console.print(panel)
        time.sleep(2)
    
    def show_winner(self, winner: Player, final_scores: dict) -> None:
        """Display game winner and final scores.
        
        Args:
            winner: The winning player
            final_scores: Dictionary of player scores
        """
        if self.boss_mode:
            return
        
        self.clear_screen()
        
        winner_text = f"""
    🏆 WINNER: {winner.name.upper()} 🏆
    
    🎉 Congratulations! 🎉
        """
        
        # Create scores table
        scores_table = Table(title="Final Scores")
        scores_table.add_column("Player", style="bold")
        scores_table.add_column("Cards Left", justify="center")
        scores_table.add_column("Points", justify="center")
        
        for player_name, score_info in final_scores.items():
            scores_table.add_row(
                player_name,
                str(score_info.get('cards_left', 0)),
                str(score_info.get('points', 0))
            )
        
        winner_panel = Panel(
            Align.center(winner_text),
            title="[bold green]GAME OVER[/bold green]",
            border_style="green"
        )
        
        self.console.print(winner_panel)
        self.console.print(scores_table)
    
    def show_boss_screen(self) -> None:
        """Display fake terminal output for boss key."""
        self.boss_mode = True
        self.clear_screen()
        
        # Generate fake ps output
        fake_processes = [
            "  PID TTY           TIME CMD",
            "    1 ??         0:01.23 /sbin/launchd",
            "   47 ??         0:00.12 /usr/sbin/syslogd",
            "   48 ??         0:00.45 /usr/libexec/UserEventAgent (System)",
            "   51 ??         0:00.23 /System/Library/PrivateFrameworks/Uninstall.framework/Resources/uninstalld",
            "   52 ??         0:00.34 /usr/sbin/cfprefsd daemon",
            "   54 ??         0:00.12 /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/CarbonCore.framework/Versions/A/Support/fseventsd",
            "   56 ??         0:00.67 /usr/sbin/distnoted daemon",
            "   58 ??         0:00.23 /usr/libexec/configd",
            "   59 ??         0:00.45 /System/Library/CoreServices/powerd.bundle/powerd",
            "   61 ??         0:00.12 /usr/libexec/logd",
            "   63 ??         0:00.34 /usr/libexec/keybagd -t 15",
            "   65 ??         0:00.23 /System/Library/PrivateFrameworks/MediaRemote.framework/Support/mediaremoted",
            "   67 ??         0:00.45 /usr/sbin/systemstats --daemon",
            "   69 ??         0:00.12 /usr/libexec/coreduetd",
            "   71 ??         0:00.34 /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mds",
            "   73 ??         0:00.23 /usr/bin/python3 /usr/local/bin/build_monitor.py",
            "   75 ??         0:00.45 /usr/libexec/nsurlsessiond",
            "   77 ??         0:00.12 /System/Library/PrivateFrameworks/CloudKitDaemon.framework/Support/cloudd",
            "   79 ??         0:00.34 /usr/libexec/trustd --agent",
            "   81 ??         0:00.23 /System/Library/Frameworks/Security.framework/Versions/A/Resources/CloudKeychainProxy.bundle/Contents/MacOS/CloudKeychainProxy",
            "   83 ??         0:00.45 /usr/libexec/secd",
            "   85 ??         0:00.12 /System/Library/PrivateFrameworks/CoreSymbolication.framework/coresymbolicationd",
            "   87 ??         0:00.34 /usr/libexec/lsd",
            "   89 ??         0:00.23 /System/Library/CoreServices/launchservicesd",
            "   91 ??         0:00.45 /usr/libexec/runningboardd",
            "   93 ??         0:00.12 /usr/libexec/mobileassetd",
        ]
        
        for line in fake_processes:
            print(line)
        
        # Add cursor
        print("$ ", end="", flush=True)
    
    def exit_boss_mode(self) -> None:
        """Exit boss mode and return to game."""
        self.boss_mode = False
    
    def show_error(self, message: str) -> None:
        """Display an error message.
        
        Args:
            message: Error message to display
        """
        if self.boss_mode:
            return
        
        error_panel = Panel(
            message,
            title="[bold red]Error[/bold red]",
            border_style="red"
        )
        self.console.print(error_panel)
    
    def show_message(self, message: str, style: str = "info") -> None:
        """Display a general message.
        
        Args:
            message: Message to display
            style: Style of message (info, warning, success)
        """
        if self.boss_mode:
            return
        
        styles = {
            "info": ("blue", "Info"),
            "warning": ("yellow", "Warning"), 
            "success": ("green", "Success"),
            "error": ("red", "Error")
        }
        
        color, title = styles.get(style, ("blue", "Info"))
        
        panel = Panel(
            message,
            title=f"[bold {color}]{title}[/bold {color}]",
            border_style=color
        )
        self.console.print(panel)
    
    def prompt_input(self, message: str) -> str:
        """Prompt for user input.
        
        Args:
            message: Prompt message
            
        Returns:
            User input string
        """
        if self.boss_mode:
            return ""
        
        return self.console.input(f"[bold cyan]{message}[/bold cyan] ")
    
    def show_loading(self, message: str = "Loading...") -> None:
        """Show loading message.
        
        Args:
            message: Loading message
        """
        if self.boss_mode:
            return
        
        with self.console.status(f"[bold green]{message}[/bold green]"):
            time.sleep(1)
