# VERY BUGGY AS OF NOW

# The Listener

A cosmic horror survival game inspired by *Voices of the Void*. You are a lone operator in a remote observatory, processing deep space signals while navigating the physical station in a stunning ASCII terminal interface.

## Installation

No dependencies required - uses only Python standard library!

```bash
python3 the_listener.py
```

## Visual Features

✨ **Full ANSI Color Support** - Beautiful, atmospheric terminal interface
- Color-coded status indicators (green/yellow/red based on levels)
- Distinct signal type colors
- Syntax-highlighted commands and prompts
- Atmospheric box-drawing characters

🎭 **Sanity-Based Visual Effects**
- Text glitches and corruption at low sanity
- Screen flickers with disturbing messages
- Color aberrations when reality breaks down
- Visual distortions in exploration mode

🔊 **Simulated Audio Feedback**
- Terminal bell alerts for critical events
- Descriptive ambient sound logs
- Creepy auditory hallucinations at low sanity

🎨 **Professional UI Design**
- ASCII art title screen
- Animated loading sequences
- Styled headers and separators
- Immersive first-person exploration rendering

## How to Play

### Terminal Mode (Default)
Process deep space signals to earn credits:
- `scan` - Scan for signals (with animated progress)
- `analyze <n>` - Analyze signal at index n  
- `decode` - Decode current signal content (affects sanity!)
- `submit` - Submit decoded signal for credits

### Exploration Mode
Navigate the station in first-person ASCII view:
- `explore` - Enter exploration mode
- **W** - Move forward
- **S** - Move backward
- **A** - Turn left (90°)
- **D** - Turn right (90°)
- **Q** - Return to terminal

### Survival
Monitor your color-coded resources:
- **Sanity**: Decreases when decoding disturbing signals (GREEN→YELLOW→RED)
- **Power**: Used by terminal operations
- **Oxygen**: Consumed while moving
- **Supplies**: Water filters, food, repair parts

## Game Features

### 💀 Horror Mechanics
- **6 Signal Types**: Data streams, voices, coordinates, blueprints, warnings, unknown
- **Dynamic Sanity System**: 
  - Visual glitches and text corruption
  - Screen flickers with horror messages
  - Unreliable interface at low sanity
  - Creepy ambient sounds
- **Atmospheric Events**: System malfunctions, strange noises, unauthorized access alerts

### 🎮 Gameplay
- **Signal Processing**: Scan → Analyze → Decode → Submit workflow
- **Station Exploration**: Navigate between Terminal, Generator, and Storage
- **Resource Management**: Balance power, oxygen, and supplies
- **Random Events**: Malfunctions, anomalies, and mysterious occurrences

### 🎨 Visual Design
- Color-coded UI elements for instant readability
- Animated text sequences (scanning, decoding, transmitting)
- Box-drawing characters for professional appearance
- Perspective-based first-person rendering
- Glitch effects that intensify with low sanity

## Commands

- `help` - Show all commands (color-coded)
- `status` - Detailed status report with formatting
- `exit` or `quit` - Exit game

## Tips

1. Start by scanning for signals
2. Analyze them to check quality before decoding
3. **Watch the colors** - they indicate danger levels
4. High-noise signals are harder to decode but may be valuable
5. Monitor your sanity - some signal types are more disturbing
6. At low sanity, don't trust what you see...
7. Use exploration mode to check station systems
8. Watch your oxygen when exploring!
9. Listen for audio cues (terminal bell) on critical events

## Game Over Conditions

- Sanity reaches 0% (accompanied by visual/audio effects)
- Oxygen depleted
- Power failure

## Technical Features

- Pure Python 3 (standard library only)
- ANSI escape sequences for colors and effects
- Terminal bell character (\a) for audio feedback
- Box-drawing Unicode characters
- Smooth animations and transitions
- Dynamic text corruption algorithms

---

⚠️ **Warning**: Contains flashing text effects and terminal bell sounds. May not be suitable for those sensitive to such effects.

Stay alert, operator. The void is listening...
