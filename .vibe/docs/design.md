<!--
INSTRUCTIONS FOR DESIGN DOCUMENT (FREESTYLE):
- Document technical implementation details in whatever format works best
- Focus on what to build and how to build it well
- Include key decisions, patterns, and implementation guidance
- Consider including testing approach, error handling, and performance
- Reference architecture document for high-level context
- Keep it practical and actionable for developers
-->

# CLI UNO Game - Detailed Design

## Architecture Reference

See [Architecture Document](./architecture.md) for high-level system context and architecture decisions.

## Implementation Overview

The CLI UNO game will be implemented as a Python package with 8 core classes following Object-Oriented principles. The implementation prioritizes simplicity, maintainability, and the specific "stealth gaming" requirements for meeting contexts.

## Project Structure

```
uno_game/
├── main.py              # Entry point and main game loop
├── models/
│   ├── __init__.py
│   ├── card.py          # Card and Deck classes
│   ├── player.py        # HumanPlayer and AIPlayer classes
│   └── game_state.py    # Game state management
├── engine/
│   ├── __init__.py
│   ├── game_engine.py   # UnoGame class
│   └── ai_engine.py     # SimpleAI class
├── ui/
│   ├── __init__.py
│   ├── display.py       # DisplayManager class
│   └── input_handler.py # InputHandler class
├── assets/
│   └── card_art.py      # ASCII art templates
└── requirements.txt     # Dependencies
```

## Key Design Decisions

### 1. Card Representation
```python
class Card:
    def __init__(self, color: str, value: str, card_type: str):
        self.color = color      # 'red', 'blue', 'green', 'yellow', 'wild'
        self.value = value      # '0'-'9', 'skip', 'reverse', 'draw_two', 'wild', 'wild_draw_four'
        self.card_type = card_type  # 'number', 'action', 'wild'
```

### 2. ASCII Art Card Design
Cards will be 7x5 character blocks:
```
┌─────┐
│ R 7 │  # Red 7
│  ♦  │
│ 7 R │
└─────┘

┌─────┐
│ B ⊘ │  # Blue Skip
│  ⊘  │
│ ⊘ B │
└─────┘
```

### 3. Boss Key Implementation
- Space bar detection using `keyboard` library
- Fake `ps` output with realistic process names:
  - System processes (kernel_task, launchd, etc.)
  - Development tools (python, node, git)
  - Common applications (chrome, slack, etc.)
- Return to game on any other key press

### 4. AI Decision Rules (Priority Order)
1. **Must Play**: If forced to play (after drawing)
2. **Color Match**: Prefer matching current color
3. **Number Match**: Play matching numbers if no color match
4. **Action Cards**: Use strategically (Skip when ahead, Draw Two when behind)
5. **Wild Cards**: Save for when no other options, choose most common color in hand

## Implementation Details

### Game Flow State Machine
```
START → DEAL_CARDS → PLAYER_TURN → [BOSS_KEY] → AI_TURN → CHECK_WIN → [RESTART|END]
                         ↑                                      ↓
                         └──────── CONTINUE_GAME ←─────────────┘
```

### Class Specifications

#### Card Class
```python
class Card:
    COLORS = ['red', 'blue', 'green', 'yellow', 'wild']
    VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
              'skip', 'reverse', 'draw_two', 'wild', 'wild_draw_four']
    
    def can_play_on(self, other_card: 'Card') -> bool:
        # Implementation logic for UNO rules
    
    def get_ascii_art(self) -> str:
        # Return 7x5 ASCII representation
```

#### Deck Class
```python
class Deck:
    def __init__(self):
        self.cards = self._create_standard_deck()  # 108 cards
        self.discard_pile = []
    
    def _create_standard_deck(self) -> List[Card]:
        # Create standard UNO deck (108 cards)
    
    def shuffle(self):
        # Shuffle remaining cards
    
    def deal_hand(self, size: int = 7) -> List[Card]:
        # Deal initial hand
```

#### DisplayManager Class
```python
class DisplayManager:
    def __init__(self):
        self.console = Console()  # rich Console
        self.boss_mode = False
    
    def show_game_state(self, game_state):
        # Display current game board
    
    def show_boss_screen(self):
        # Display fake ps output
    
    def get_card_art(self, card: Card) -> str:
        # Return ASCII art for card
```

#### InputHandler Class
```python
class InputHandler:
    def __init__(self, display_manager):
        self.display_manager = display_manager
        self._setup_boss_key()
    
    def _setup_boss_key(self):
        keyboard.on_press_key('space', self._boss_key_pressed)
    
    def get_player_move(self, valid_moves) -> int:
        # Get and validate player input
```

### Testing Strategy

#### Unit Tests
- Card logic and UNO rule validation
- AI decision-making algorithms
- ASCII art rendering

#### Integration Tests
- Game flow from start to finish
- Boss key functionality
- Cross-platform terminal compatibility

#### Manual Testing
- Play complete games to verify fun factor
- Test boss key in different terminals
- Verify ASCII art readability

### Error Handling

#### Input Validation
- Invalid card selections → Show error and re-prompt
- Non-numeric input → Clear error message
- Boss key during input → Preserve game state

#### System Errors
- Terminal resize → Graceful redraw
- Keyboard library issues → Fallback to basic input
- Rich library errors → Fallback to plain text

### Performance Considerations

#### Startup Time
- Lazy loading of ASCII art templates
- Minimal imports in main.py
- Pre-compiled regex patterns

#### Memory Usage
- Efficient card representation
- Clear unused game states
- Minimal string concatenation

### Development Milestones

#### Milestone 1: Core Game Logic (40% complete)
- Card and Deck classes
- Basic UNO rule validation
- Simple text-based gameplay

#### Milestone 2: ASCII Art Interface (70% complete)
- DisplayManager with rich integration
- ASCII card art rendering
- Improved game state display

#### Milestone 3: AI and Boss Key (90% complete)
- SimpleAI implementation
- Boss key functionality with fake ps output
- InputHandler with keyboard integration

#### Milestone 4: Polish and Testing (100% complete)
- Cross-platform testing
- Performance optimization
- Documentation and packaging

## Development Guidelines

### Code Style
- Follow PEP 8 conventions
- Use type hints for all public methods
- Comprehensive docstrings for classes and methods
- Maximum line length: 88 characters (Black formatter)

### Dependencies
- Minimize external dependencies
- Pin versions in requirements.txt
- Graceful degradation if optional libraries unavailable

### Git Workflow
- Feature branches for each major component
- Commit messages following conventional commits
- Regular integration testing

### Documentation
- README with installation and usage
- Inline code documentation
- Architecture decision records for major choices
