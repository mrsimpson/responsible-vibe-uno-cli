# 🎮 CLI UNO Game

A beautiful command-line UNO card game with ASCII art graphics and strategic AI opponent. Play the classic card game right in your terminal with gorgeous visuals and smooth gameplay.

![Python](https://img.shields.io/badge/Python-3.8+-green) ![Platform](https://img.shields.io/badge/Platform-CLI-blue) ![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

### 🎯 Core Gameplay
- **Complete UNO Rules**: All 108 cards with proper game mechanics
- **Strategic AI Opponent**: Smart computer player with intelligent decision-making
- **Beautiful ASCII Art**: Colorful card designs with suit symbols (♦♠♣♥★)
- **Cross-Platform**: Works on Windows, macOS, and Linux terminals

### 🎨 Visual Interface
- **Rich Terminal Graphics**: Professional layouts with panels and borders
- **Color-Coded Cards**: Red, Blue, Green, Yellow, and Wild cards
- **Smart Fallback**: Works with or without rich library installed
- **Hand Display**: Clear card numbering for easy selection
- **Game Board**: Shows current state, top card, and player information

### 🤖 AI Features
- **Strategic Decision Making**: AI prefers color matches, uses action cards wisely
- **Wild Card Intelligence**: Chooses colors based on hand composition
- **Difficulty Scaling**: Challenging but fair gameplay

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd demo-responsible-vibe-uno
   ```

2. **Install dependencies (optional for enhanced graphics):**
   ```bash
   pip install rich
   ```

3. **Run the game:**
   ```bash
   python uno.py
   ```

### System Requirements
- Python 3.8 or higher
- Terminal with color support (recommended)
- `rich` library for enhanced graphics (optional - game works without it)

## 🎮 How to Play

### Game Controls
- **1-9**: Select and play a card from your hand
- **D**: Draw a card from the deck
- **Q**: Quit the game

### UNO Rules
- Match the top card by **color** or **number**
- **Action Cards**:
  - **Skip**: Next player loses their turn
  - **Reverse**: Changes direction (acts like Skip in 2-player)
  - **Draw Two**: Next player draws 2 cards and loses turn
- **Wild Cards**:
  - **Wild**: Choose any color
  - **Wild Draw Four**: Choose color, next player draws 4 cards
- **UNO Call**: Automatically called when you have one card left
- **Winning**: First player to play all cards wins!

### Sample Gameplay
```
🎮 BEAUTIFUL UNO 🎮
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Game #1 | Turn: You                    🎮 BEAUTIFUL UNO 🎮                    Deck: 85 cards │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
┌──────── Game Board ─────────┐┌──────────────────── You's Hand ────────────────────────────────┐
│ Top Card:                   ││  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│                             ││  │R 7  │ │B 3  │ │G ⊘  │ │Y 1  │ │W ★  │ │B +2 │ │R 9  │     │
│ ┌─────┐                     ││  │  ♦  │ │  ♠  │ │  ♣  │ │  ♥  │ │  ★  │ │  ♠  │ │  ♦  │     │
│ │Y 5  │                     ││  │  7 R│ │  3 B│ │  ⊘ G│ │  1 Y│ │  ★ W│ │ +2 B│ │  9 R│     │
│ │  ♥  │                     ││  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘     │
│ │  5 Y│                     ││     1       2       3       4       5       6       7        │
│ └─────┘                     ││                                                              │
└─────────────────────────────┘└──────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                    Commands: 1-9 Play card • D Draw • Q Quit                               │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🏗️ Architecture

### Project Structure
```
demo-responsible-vibe-uno/
├── uno.py                   # Main game with rich graphics and fallback
├── requirements.txt         # Optional dependencies for enhanced graphics
├── INSTALL.md              # Installation guide
├── CHANGELOG.md            # Version history
└── README.md               # This file
```

### Key Components
- **UnoCard**: Card representation with ASCII art rendering
- **UnoDeck**: Standard 108-card UNO deck with shuffling
- **UnoPlayer**: Player management and hand operations
- **BeautifulUnoGame**: Main game engine with rich terminal interface

## 🎯 Game Features

### 🌟 Single Version (`uno.py`) - Complete Experience
- ✅ Rich terminal graphics with professional layouts
- ✅ ASCII art cards with colors
- ✅ Strategic AI opponent
- ✅ Graceful fallback if rich library not installed
- ✅ Works everywhere Python runs

## 🤖 AI Strategy

The computer opponent uses intelligent decision-making:

### Decision Priority
1. **Color Matches**: Prefers matching colors over numbers
2. **Number Matches**: Plays matching numbers when no color match
3. **Action Cards**: Uses strategically based on game state
4. **Wild Cards**: Conserves for optimal timing

### Smart Features
- **Hand Analysis**: Chooses wild colors based on remaining cards
- **Opponent Awareness**: Plays more aggressively when you have few cards
- **Strategic Timing**: Saves powerful cards for the right moment

## 🛠️ Development

### Running the Game
```bash
python uno.py
```

### Dependencies
- **rich**: Terminal formatting and colors (optional)
- **Python 3.8+**: Core requirement

### Compatibility
- **Windows**: Command Prompt, PowerShell
- **macOS**: Terminal app
- **Linux**: Standard terminal emulators
- **Fallback**: Works without any external libraries

## 🏆 Game Statistics

- **108 UNO Cards**: Complete standard deck
- **4 Colors**: Red, Blue, Green, Yellow
- **8 Wild Cards**: 4 Wild + 4 Wild Draw Four
- **Strategic AI**: Makes intelligent decisions
- **Cross-Platform**: Works everywhere Python runs

## 🎉 Enjoy Your UNO Game!

A beautiful, feature-complete UNO implementation that brings the classic card game to your terminal with style. Perfect for quick games, learning Python game development, or just having fun!

**Features:**
- 🎨 Gorgeous ASCII art cards
- 🤖 Challenging AI opponent  
- 🎮 Smooth terminal gameplay
- 🌈 Beautiful colors and layouts
- 🏆 Complete UNO rule implementation

---

*Built with ❤️ for terminal game enthusiasts*
