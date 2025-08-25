<!--
INSTRUCTIONS FOR ARCHITECTURE DOCUMENT (FREESTYLE):
- Document high-level system architecture and context
- Focus on system boundaries, external interfaces, and key components
- Include technology decisions with rationale
- Keep it concise but comprehensive enough for new team members
- Update as architecture evolves during development
-->

# CLI UNO Game Architecture

## System Overview

A single-player CLI UNO card game built in Python using Object-Oriented design. The system provides classical UNO gameplay against a rule-based AI opponent, featuring ASCII art cards and a boss key for stealth gaming during meetings.

## System Context

**Primary User:** Meeting attendees seeking discreet entertainment
**External Interfaces:**
- Terminal/Console (input/output)
- Operating System (Windows, macOS, Linux)
- Keyboard input (game controls + boss key)

**No External Dependencies:**
- No network connectivity required
- No file persistence needed
- Self-contained Python application

## High-Level Architecture

**Architectural Pattern:** Object-Oriented with clear separation of concerns

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Game Engine   │◄──►│  Display Layer  │◄──►│  Input Handler  │
│                 │    │                 │    │                 │
│ • Game Logic    │    │ • ASCII Art     │    │ • User Input    │
│ • Rule Engine   │    │ • Terminal UI   │    │ • Boss Key      │
│ • State Mgmt    │    │ • Fake Terminal │    │ • Validation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Data Models   │
                    │                 │
                    │ • Card          │
                    │ • Deck          │
                    │ • Player        │
                    │ • GameState     │
                    └─────────────────┘
```

## Technology Decisions

- **Language:** Python 3.8+ - Cross-platform, rich ecosystem, rapid development
- **Terminal Library:** `rich` - Beautiful ASCII art, colors, cross-platform terminal handling
- **Input Handling:** `keyboard` - Global hotkey detection for boss key functionality
- **Architecture:** Object-Oriented - Maintainable, extensible, clear separation of concerns
- **Dependencies:** Minimal external libraries for easy deployment and compatibility

## Key Components

### Game Engine (`UnoGame`)
- **Purpose:** Core game logic, rule enforcement, turn management
- **Responsibilities:** 
  - Initialize and manage game state
  - Enforce UNO rules and card play validation
  - Coordinate between players and manage turns
  - Handle game flow (start, play, end)

### Player Classes (`HumanPlayer`, `AIPlayer`)
- **Purpose:** Represent different player types with their behaviors
- **Responsibilities:**
  - Manage player hand and actions
  - `HumanPlayer`: Handle user input and display choices
  - `AIPlayer`: Implement rule-based decision making

### Card System (`Card`, `Deck`)
- **Purpose:** Represent UNO cards and deck management
- **Responsibilities:**
  - `Card`: Store card properties (color, value, type)
  - `Deck`: Shuffle, deal, draw cards, manage discard pile

### Display Manager (`DisplayManager`)
- **Purpose:** Handle all terminal output and ASCII art rendering
- **Responsibilities:**
  - Render ASCII art cards and game board
  - Display game state and player information
  - Handle boss key fake terminal output (ps command simulation)
  - Manage terminal clearing and formatting
- **Boss Key Implementation:** Generate realistic `ps` command output with system processes

### Input Handler (`InputHandler`)
- **Purpose:** Process user input and boss key detection
- **Responsibilities:**
  - Capture and validate user moves
  - Detect boss key (space bar) activation
  - Handle menu navigation and game controls

### AI Engine (`SimpleAI`)
- **Purpose:** Rule-based computer opponent decision making
- **Responsibilities:**
  - Analyze current game state
  - Select optimal card to play using simple rules
  - Handle special card strategy (Wild cards, action cards)

## Data Flow

1. **Game Initialization:** `UnoGame` creates players, deck, and initial state
2. **Turn Loop:** Game alternates between human and AI player turns
3. **Human Turn:** `InputHandler` → `HumanPlayer` → `UnoGame` → `DisplayManager`
4. **AI Turn:** `AIPlayer` → `SimpleAI` → `UnoGame` → `DisplayManager`
5. **Boss Key:** `InputHandler` detects space → `DisplayManager` shows fake terminal
6. **Game End:** Win condition triggers score calculation and restart option

## Deployment Architecture

**Single File Deployment:**
- Main executable: `uno_game.py`
- All classes in separate modules for organization
- Package as standalone Python script or executable
- No installation required - just run with Python 3.8+

**Dependencies:**
```
rich>=10.0.0      # Terminal formatting and colors
keyboard>=0.13.0  # Boss key detection
```

## Security Architecture

**Minimal Security Concerns:**
- No network communication
- No file system access beyond standard Python
- Boss key provides "stealth mode" for meeting contexts
- Input validation prevents crashes from invalid user input

## Quality Attributes

**Performance:**
- Target: <2 second startup time
- Memory: <50MB RAM usage
- Responsive turn-based gameplay

**Maintainability:**
- Object-oriented design for easy extension
- Clear separation of concerns
- Comprehensive docstrings and type hints

**Usability:**
- Intuitive ASCII art interface
- Clear input prompts and error messages
- Quick boss key activation (space bar)

**Compatibility:**
- Python 3.8+ on Windows, macOS, Linux
- Standard terminal sizes (80x24 minimum)
- Works in various terminal emulators
