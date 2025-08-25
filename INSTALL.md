# 🎮 CLI UNO Game - Installation Guide

## Quick Start

### Enhanced Experience (Recommended)
```bash
# Install the rich library for enhanced graphics
pip install rich

# Run the game
python uno.py
```

### Basic Installation
```bash
# No dependencies needed - works with any Python 3.8+
python uno.py
```

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Terminal**: Any terminal with color support (recommended)

## Installation Methods

### Method 1: Direct Download
1. Download the game files
2. Extract to a folder
3. Open terminal in that folder
4. Run `python uno.py`

### Method 2: Git Clone
```bash
git clone <repository-url>
cd demo-responsible-vibe-uno
python uno.py
```

## Dependencies

### Required
- **Python 3.8+**: Core requirement

### Optional
- **rich**: Enhanced terminal graphics
  ```bash
  pip install rich
  ```

## Troubleshooting

### "Command not found: python"
Try using `python3` instead:
```bash
python3 uno.py
```

### "Module not found: rich"
The game works without rich - it will automatically use basic graphics:
```bash
python uno.py  # Works with or without rich
```

### Colors not showing
- Ensure your terminal supports colors
- Try a different terminal application
- The game will work without colors

## Verification

Test your installation:
```bash
python -c "print('Python works!')"
python uno.py
```

You should see the UNO game title screen.

## Getting Help

If you encounter issues:
1. Check Python version: `python --version`
2. Ensure you're in the correct directory
3. Check file permissions
4. The game automatically adapts to your system

Enjoy playing UNO! 🎉
