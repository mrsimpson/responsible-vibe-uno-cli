# Changelog

All notable changes to the CLI UNO Game project.

## [1.0.0] - 2025-08-25

### Added
- Complete UNO card game implementation with all 108 cards
- Beautiful ASCII art card designs with suit symbols (♦♠♣♥★)
- Strategic AI opponent with intelligent decision-making
- Rich terminal graphics with professional layouts and panels
- Cross-platform compatibility (Windows, macOS, Linux)
- Graceful fallback when rich library is not installed
- Multiple game versions (main and minimal)
- Complete UNO rules implementation including:
  - Number cards (0-9) in four colors
  - Action cards (Skip, Reverse, Draw Two)
  - Wild cards (Wild, Wild Draw Four)
  - Proper color and number matching
  - Automatic UNO calls
  - Win condition detection
- Smart AI strategy with color preference and strategic timing
- Hand display with card numbering for easy selection
- Game state display showing top card, deck size, and player info
- Multi-game sessions with game counter
- Comprehensive error handling and input validation

### Technical Features
- Object-oriented architecture with clean separation of concerns
- Modular design with separate components for cards, players, game logic, and display
- Rich library integration with fallback to basic terminal output
- Strategic AI with multiple decision factors
- Complete deck management with shuffling and reshuffling
- Proper game state management including turn order and penalties

### Game Versions
- **Single Version** (`uno.py`): Complete game with rich graphics and automatic fallback

### Documentation
- Comprehensive README with installation and gameplay instructions
- Installation guide with troubleshooting
- Architecture overview and component descriptions
- Complete feature list and system requirements
