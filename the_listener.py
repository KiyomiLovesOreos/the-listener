#!/usr/bin/env python3
"""
The Listener - A cosmic horror survival game
"""
import os
import sys
import random
import time
import shutil
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    INVERT = '\033[7m'
    END = '\033[0m'
    
    @staticmethod
    def glitch():
        """Return a random glitch color"""
        return random.choice([Colors.RED, Colors.MAGENTA, Colors.CYAN])
    
    @staticmethod
    def sanity_color(sanity: int) -> str:
        """Return color based on sanity level"""
        if sanity >= 70:
            return Colors.GREEN
        elif sanity >= 40:
            return Colors.YELLOW
        else:
            return Colors.RED

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class GameMode(Enum):
    TERMINAL = "terminal"
    EXPLORATION = "exploration"

@dataclass
class Signal:
    frequency: float
    strength: int
    noise_level: int
    content_type: str
    decoded_content: str
    value: int

@dataclass
class Player:
    x: int
    y: int
    direction: Direction
    credits: int
    sanity: int
    current_mode: GameMode

@dataclass
class Resources:
    power: int
    oxygen: int
    water_filters: int
    food_cartridges: int
    repair_parts: int

class Station:
    def __init__(self):
        # Larger station layout (20x20 grid)
        # 0 = floor, 1 = wall, 2 = door, 3 = terminal, 4 = generator, 5 = storage
        self.layout = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 5, 5, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.tiles = {
            0: ".",
            1: "#",
            2: "D",
            3: "T",
            4: "G",
            5: "S"
        }

    def get_tile(self, x: int, y: int) -> int:
        if 0 <= y < len(self.layout) and 0 <= x < len(self.layout[0]):
            return self.layout[y][x]
        return 1

    def is_walkable(self, x: int, y: int) -> bool:
        tile = self.get_tile(x, y)
        return tile in [0, 2, 3, 4, 5]

class Game:
    def __init__(self):
        self.player = Player(x=2, y=2, direction=Direction.NORTH, 
                           credits=100, sanity=100, current_mode=GameMode.TERMINAL)
        self.resources = Resources(power=100, oxygen=100, water_filters=10,
                                  food_cartridges=10, repair_parts=5)
        self.station = Station()
        self.current_signal: Optional[Signal] = None
        self.scanned_signals: List[Signal] = []
        self.day = 1
        self.running = True
        self.discovered_signals = 0
        self.glitch_chars = ['░', '▒', '▓', '█', '▄', '▀', '■', '□', '▪', '▫', '§', '¶', '†', '‡', '∴', '∵', '◊', '○', '●', '◘', '◙']
        self.corruption_chars = ['§', 'µ', '¿', '¶', '†', '‡', '∞', '≈', '∴', '∵', '◊']
        self.zalgo_marks = ['̃', '̀', '́', '̂', '̄', '̆', '̇', '̈', '̊', '̋', '̌', '̐', '̒']
        self.light_flicker_frame = 0
        self.terminal_history = []
        self.max_history = 100
        
    def clear_screen(self):
        """Clear screen - now just used for special effects"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def get_terminal_size(self):
        """Get terminal dimensions"""
        size = shutil.get_terminal_size((80, 24))
        return size.columns, size.lines

    def print_separator(self, char="═"):
        cols, _ = self.get_terminal_size()
        width = min(cols, 100)
        print(Colors.GRAY + char * width + Colors.END)

    def print_box_header(self, text: str):
        cols, _ = self.get_terminal_size()
        width = min(cols - 4, 96)
        padding = (width - len(text)) // 2
        print(Colors.CYAN + "╔" + "═" * width + "╗" + Colors.END)
        print(Colors.CYAN + "║" + " " * padding + Colors.BOLD + text + Colors.END + Colors.CYAN + " " * (width - padding - len(text)) + "║" + Colors.END)
        print(Colors.CYAN + "╚" + "═" * width + "╝" + Colors.END)

    def glitch_text(self, text: str) -> str:
        """Apply glitch effects to text based on sanity"""
        if self.player.sanity >= 70:
            return text
        
        glitch_chance = (100 - self.player.sanity) / 200
        result = []
        
        for char in text:
            if random.random() < glitch_chance:
                result.append(Colors.glitch() + random.choice(self.glitch_chars) + Colors.END)
            else:
                result.append(char)
        
        return ''.join(result)

    def screen_flicker(self):
        """Cause a brief visual glitch"""
        if self.player.sanity < 40 and random.random() < 0.15:
            self.clear_screen()
            glitch_messages = [
                "T̷H̴E̸Y̵ ̴A̶R̴E̷ ̸W̶A̶T̷C̸H̷I̶N̵G̴",
                "░▒▓█ SIGNAL CORRUPTED █▓▒░",
                "DO NOT TRUST THE CONSOLE",
                "YOU ARE NOT ALONE",
                "◊◊◊ LISTENING... LISTENING... ◊◊◊",
                "ERROR: REALITY.SYS NOT FOUND"
            ]
            print("\n" * 10)
            print(Colors.RED + Colors.BLINK + Colors.BOLD + random.choice(glitch_messages).center(70) + Colors.END)
            print("\a")  # Bell sound
            time.sleep(0.3)
            self.clear_screen()

    def print_status(self):
        # Check for screen flicker before drawing UI
        self.screen_flicker()
        
        sanity_col = Colors.sanity_color(self.player.sanity)
        power_col = Colors.sanity_color(self.resources.power)
        o2_col = Colors.sanity_color(self.resources.oxygen)
        
        status_line = f"{Colors.BLUE}Day{Colors.END} {Colors.YELLOW}{self.day}{Colors.END} │ "
        status_line += f"{Colors.BLUE}Credits{Colors.END} {Colors.YELLOW}{self.credits}{Colors.END} │ "
        status_line += f"{Colors.BLUE}Sanity{Colors.END} {sanity_col}{self.player.sanity}%{Colors.END} │ "
        status_line += f"{Colors.BLUE}Mode{Colors.END} {Colors.CYAN}{self.player.current_mode.value}{Colors.END}"
        
        resource_line = f"{Colors.BLUE}Power{Colors.END} {power_col}{self.resources.power}%{Colors.END} │ "
        resource_line += f"{Colors.BLUE}O2{Colors.END} {o2_col}{self.resources.oxygen}%{Colors.END} │ "
        resource_line += f"{Colors.BLUE}Supplies{Colors.END} {Colors.WHITE}W:{self.resources.water_filters} F:{self.resources.food_cartridges} R:{self.resources.repair_parts}{Colors.END}"
        
        print(self.glitch_text(status_line))
        print(self.glitch_text(resource_line))
        self.print_separator()

    @property
    def credits(self):
        return self.player.credits

    def generate_signal(self) -> Signal:
        frequencies = [1420.4, 2800.0, 3300.5, 4500.2, 5200.8, 6100.3]
        content_types = ["data_stream", "voice", "coordinates", "blueprint", "warning", "unknown"]
        
        freq = random.choice(frequencies)
        strength = random.randint(20, 100)
        noise = random.randint(10, 80)
        ctype = random.choice(content_types)
        
        contents = {
            "data_stream": self.generate_data_content(),
            "voice": self.generate_voice_content(),
            "coordinates": self.generate_coords_content(),
            "blueprint": self.generate_blueprint_content(),
            "warning": self.generate_warning_content(),
            "unknown": self.generate_unknown_content()
        }
        
        value = max(10, strength - noise // 2)
        
        return Signal(freq, strength, noise, ctype, contents[ctype], value)

    def generate_data_content(self) -> str:
        data = [
            "Binary sequence detected: 01001000 01000101 01001100 01010000",
            "Telemetry data from Sector 7-G. All systems nominal. Wait... additional data appended.",
            "Scientific log entry #4782: The readings are impossible. We shouldn't be seeing this.",
            "Astronomical data corrupted. Stars in wrong positions. Constellations altered."
        ]
        return random.choice(data)

    def generate_voice_content(self) -> str:
        voices = [
            "[Static]... can you hear... [static]... they're coming... [signal lost]",
            "Help us. We've been here so long. Don't let them find you.",
            "Hello? Is anyone there? I'm trapped in... [interference]... observatory...",
            "You shouldn't be listening. STOP. Turn it off. Turn it ALL off.",
            "The void speaks to those who listen. Will you answer?",
            "[Breathing sounds] ...behind you... [laughter] ...always watching..."
        ]
        return random.choice(voices)

    def generate_coords_content(self) -> str:
        coords = [
            "Coordinates: 23h 17m 12s, -45° 32' 18\". Location: Unknown Deep Space.",
            "Star chart detected. WARNING: Constellations do not match any known patterns.",
            "Navigation data: Destination coordinates lead to empty space. Or do they?",
            "Orbital mechanics data. Calculating trajectory... Impact in [REDACTED] days."
        ]
        return random.choice(coords)

    def generate_blueprint_content(self) -> str:
        blueprints = [
            "Schematic decoded: Unknown device. Purpose unclear. Materials: Available on station.",
            "Construction plans for... something. The design hurts to look at.",
            "Blueprint fragments: Assembly instructions in unknown language.",
            "Technical diagram: Device components already in your storage room."
        ]
        return random.choice(blueprints)

    def generate_warning_content(self) -> str:
        warnings = [
            "ALERT: Containment breach detected at facility [COORDINATES DELETED]",
            "EVACUATION NOTICE: All personnel must leave immediately. This is not a drill.",
            "WARNING: Do not trust the signals. Do not trust the voices. Do not trust yourself.",
            "EMERGENCY BROADCAST: If you receive this message, you are already dead."
        ]
        return random.choice(warnings)

    def generate_unknown_content(self) -> str:
        unknown = [
            "[INCOMPREHENSIBLE SOUNDS] ...ṫ̶̻h̵͉̔e̶̝̾ ̸̣̈v̶̰̈́o̵̰̅i̵̳̐d̶̰̈́ ̷̣̈́l̶̰̾i̸̦̓s̶̰̈́t̷̰̊e̵̬̊n̵̢̛s̶̰̈́...",
            "Signal structure unknown. Origin: Beyond observable universe.",
            "Content cannot be parsed. Your mind cannot process this information safely.",
            "̸̱͝W̷̘̾Ë̵́͜ ̴̰̾A̷̘̾R̷̘͝E̵̬͝ ̵̝̾C̵̱͠O̷̰͝M̶̙͝I̷̱̾N̵̰̾G̶̱͝"
        ]
        return random.choice(unknown)

    def animate_loading(self, text: str, duration: float = 1.0):
        """Animated loading text"""
        steps = int(duration / 0.2)
        for i in range(steps):
            dots = "." * ((i % 3) + 1)
            print(f"\r{Colors.CYAN}{text}{dots}   {Colors.END}", end='', flush=True)
            time.sleep(0.2)
        print()

    def scan_command(self):
        print(f"\n{Colors.CYAN}[SCANNING FREQUENCIES]{Colors.END}")
        self.animate_loading("Scanning", 1.0)
        
        signal_count = random.randint(1, 3)
        self.scanned_signals = [self.generate_signal() for _ in range(signal_count)]
        
        print(f"\n{Colors.GREEN}✓ Found {signal_count} signal(s):{Colors.END}")
        for i, sig in enumerate(self.scanned_signals):
            strength_col = Colors.GREEN if sig.strength > 60 else Colors.YELLOW if sig.strength > 30 else Colors.RED
            noise_col = Colors.GREEN if sig.noise_level < 30 else Colors.YELLOW if sig.noise_level < 60 else Colors.RED
            print(f"  {Colors.BOLD}[{i}]{Colors.END} Freq: {Colors.CYAN}{sig.frequency}{Colors.END} MHz │ "
                  f"Strength: {strength_col}{sig.strength}%{Colors.END} │ "
                  f"Noise: {noise_col}{sig.noise_level}%{Colors.END}")
        
        print(f"\n{Colors.DIM}Use 'analyze <index>' to examine a signal.{Colors.END}")
        self.resources.power -= random.randint(1, 3)

    def analyze_command(self, args: List[str]):
        if not args:
            print(f"{Colors.YELLOW}Usage: analyze <signal_index>{Colors.END}")
            return
        
        try:
            idx = int(args[0])
            if idx < 0 or idx >= len(self.scanned_signals):
                print(f"{Colors.RED}Invalid signal index. Available: 0-{len(self.scanned_signals)-1}{Colors.END}")
                return
            
            self.current_signal = self.scanned_signals[idx]
            print(f"\n{Colors.CYAN}[ANALYZING SIGNAL {idx}]{Colors.END}")
            self.animate_loading("Analyzing", 1.0)
            
            print(f"\n{Colors.BLUE}Frequency:{Colors.END} {Colors.CYAN}{self.current_signal.frequency}{Colors.END} MHz")
            
            strength_col = Colors.GREEN if self.current_signal.strength > 60 else Colors.YELLOW if self.current_signal.strength > 30 else Colors.RED
            print(f"{Colors.BLUE}Signal Strength:{Colors.END} {strength_col}{self.current_signal.strength}%{Colors.END}")
            
            noise_col = Colors.GREEN if self.current_signal.noise_level < 30 else Colors.YELLOW if self.current_signal.noise_level < 60 else Colors.RED
            print(f"{Colors.BLUE}Noise Level:{Colors.END} {noise_col}{self.current_signal.noise_level}%{Colors.END}")
            
            type_col = Colors.YELLOW if self.current_signal.content_type in ["warning", "unknown"] else Colors.WHITE
            print(f"{Colors.BLUE}Content Type:{Colors.END} {type_col}{self.current_signal.content_type.upper()}{Colors.END}")
            
            quality = 'CLEAN' if self.current_signal.noise_level < 30 else 'MODERATE' if self.current_signal.noise_level < 60 else 'POOR'
            quality_col = Colors.GREEN if quality == 'CLEAN' else Colors.YELLOW if quality == 'MODERATE' else Colors.RED
            print(f"\n{Colors.BLUE}Quality:{Colors.END} {quality_col}{quality}{Colors.END}")
            
            print(f"\n{Colors.DIM}Use 'decode' to extract the signal content.{Colors.END}")
            
            self.resources.power -= 2
            
        except ValueError:
            print(f"{Colors.RED}Invalid index. Must be a number.{Colors.END}")

    def decode_command(self):
        if not self.current_signal:
            print(f"{Colors.RED}No signal selected. Use 'analyze <index>' first.{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}[DECODING SIGNAL]{Colors.END}")
        self.animate_loading("Decoding", 1.5)
        
        # Content color based on type
        content_colors = {
            "data_stream": Colors.CYAN,
            "voice": Colors.YELLOW,
            "coordinates": Colors.GREEN,
            "blueprint": Colors.BLUE,
            "warning": Colors.RED + Colors.BOLD,
            "unknown": Colors.MAGENTA + Colors.BOLD
        }
        
        content_col = content_colors.get(self.current_signal.content_type, Colors.WHITE)
        
        print(f"\n{Colors.CYAN}╔{'═' * 68}╗{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END} {Colors.BOLD}DECODED CONTENT{Colors.END}" + " " * 52 + f"{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╠{'═' * 68}╣{Colors.END}")
        
        # Apply glitch to decoded content at low sanity
        decoded = self.glitch_text(self.current_signal.decoded_content)
        
        # Wrap text to fit in box
        max_width = 66
        words = decoded.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        
        for line in lines:
            padding = max_width - len(line)
            print(f"{Colors.CYAN}║{Colors.END} {content_col}{line}{Colors.END}{' ' * padding} {Colors.CYAN}║{Colors.END}")
        
        print(f"{Colors.CYAN}╚{'═' * 68}╝{Colors.END}")
        
        # Sanity impact based on content type
        sanity_loss = {
            "data_stream": 1,
            "voice": 3,
            "coordinates": 2,
            "blueprint": 2,
            "warning": 5,
            "unknown": 8
        }
        
        loss = sanity_loss.get(self.current_signal.content_type, 2)
        self.player.sanity = max(0, self.player.sanity - loss)
        
        if loss > 3:
            print(f"\n{Colors.RED}[Your hands are shaking... -{loss} sanity]{Colors.END}")
            print("\a")  # Bell sound for high sanity loss
        
        # Add creepy sounds at low sanity
        if self.player.sanity < 50 and random.random() < 0.3:
            self.trigger_sound_log()
        
        print(f"\n{Colors.DIM}Use 'submit' to send this signal for analysis and earn credits.{Colors.END}")
        self.resources.power -= 3

    def trigger_sound_log(self):
        """Generate creepy auditory descriptions"""
        sounds = [
            f"{Colors.GRAY}[LOG]: A faint scratching sound is heard from inside the walls.{Colors.END}",
            f"{Colors.GRAY}[LOG]: The low hum of life support seems to form words before returning to normal.{Colors.END}",
            f"{Colors.GRAY}[LOG]: Three distinct, slow knocks echo from the exterior hull.{Colors.END}",
            f"{Colors.GRAY}[LOG]: A sound like breathing comes through the ventilation system.{Colors.END}",
            f"{Colors.GRAY}[LOG]: The lights flicker. Did something move in the corner?{Colors.END}",
            f"{Colors.GRAY}[LOG]: A voice whispers your name. The station AI reports no anomalies.{Colors.END}",
            f"{Colors.GRAY}[LOG]: The generator's rhythm changes. It sounds almost... deliberate.{Colors.END}",
            f"{Colors.GRAY}[LOG]: Metal groans throughout the station. No structural damage detected.{Colors.END}"
        ]
        print(f"\n{random.choice(sounds)}")
        if random.random() < 0.5:
            print("\a")  # Occasional beep

    def submit_command(self):
        if not self.current_signal:
            print(f"{Colors.RED}No decoded signal to submit.{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}[SUBMITTING TO CENTRAL COMMAND]{Colors.END}")
        self.animate_loading("Transmitting", 1.0)
        
        credits_earned = self.current_signal.value
        self.player.credits += credits_earned
        self.discovered_signals += 1
        
        print(f"\n{Colors.GREEN}✓ Signal submitted successfully!{Colors.END}")
        print(f"{Colors.BLUE}Credits earned:{Colors.END} {Colors.YELLOW}+{credits_earned}{Colors.END}")
        print(f"{Colors.BLUE}Total credits:{Colors.END} {Colors.YELLOW}{self.player.credits}{Colors.END}")
        
        self.current_signal = None
        self.scanned_signals = []
        
        # Random event chance
        if random.random() < 0.2:
            self.trigger_random_event()

    def trigger_random_event(self):
        events = [
            (f"{Colors.RED}⚠ Power fluctuation detected!{Colors.END}", lambda: setattr(self.resources, 'power', max(20, self.resources.power - 15)), True),
            (f"{Colors.RED}⚠ Oxygen scrubber malfunction!{Colors.END}", lambda: setattr(self.resources, 'oxygen', max(30, self.resources.oxygen - 10)), True),
            (f"{Colors.YELLOW}⚠ Strange noise from the corridor...{Colors.END}", lambda: setattr(self.player, 'sanity', max(0, self.player.sanity - 5)), False),
            (f"{Colors.YELLOW}⚠ System alert: Unauthorized access attempt detected.{Colors.END}", lambda: setattr(self.player, 'sanity', max(0, self.player.sanity - 3)), False),
            (f"{Colors.GREEN}✓ System diagnostics complete. All nominal.{Colors.END}", lambda: None, False),
        ]
        
        event_msg, event_func, is_critical = random.choice(events)
        print(f"\n{event_msg}")
        event_func()
        
        if is_critical:
            print("\a\a")  # Double beep for critical events

    def status_command(self):
        self.print_box_header("STATION STATUS")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Operator Status:{Colors.END}")
        print(f"  {Colors.BLUE}Credits:{Colors.END} {Colors.YELLOW}{self.player.credits}{Colors.END}")
        
        sanity_col = Colors.sanity_color(self.player.sanity)
        print(f"  {Colors.BLUE}Sanity:{Colors.END} {sanity_col}{self.player.sanity}%{Colors.END}")
        print(f"  {Colors.BLUE}Signals Discovered:{Colors.END} {Colors.WHITE}{self.discovered_signals}{Colors.END}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Life Support:{Colors.END}")
        power_col = Colors.sanity_color(self.resources.power)
        print(f"  {Colors.BLUE}Power:{Colors.END} {power_col}{self.resources.power}%{Colors.END}")
        
        o2_col = Colors.sanity_color(self.resources.oxygen)
        print(f"  {Colors.BLUE}Oxygen:{Colors.END} {o2_col}{self.resources.oxygen}%{Colors.END}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Supplies:{Colors.END}")
        print(f"  {Colors.BLUE}Water Filters:{Colors.END} {Colors.WHITE}{self.resources.water_filters}{Colors.END}")
        print(f"  {Colors.BLUE}Food Cartridges:{Colors.END} {Colors.WHITE}{self.resources.food_cartridges}{Colors.END}")
        print(f"  {Colors.BLUE}Repair Parts:{Colors.END} {Colors.WHITE}{self.resources.repair_parts}{Colors.END}")
        
        print(f"\n{Colors.BLUE}Current Day:{Colors.END} {Colors.YELLOW}{self.day}{Colors.END}")

    def explore_command(self):
        # Check if player is at a terminal
        current_tile = self.station.get_tile(self.player.x, self.player.y)
        if current_tile != 3:
            print(f"\n{Colors.RED}You must be at a Terminal (T) to access the command interface.{Colors.END}")
            print(f"{Colors.DIM}Use 'explore' to navigate the station, or 'map' to see terminal locations.{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}[ENTERING EXPLORATION MODE]{Colors.END}")
        print(f"{Colors.DIM}Use WASD to move, Q to return to terminal{Colors.END}")
        time.sleep(1)
        self.player.current_mode = GameMode.EXPLORATION
        self.render_exploration()

    def apply_corruption(self, char: str) -> str:
        """Apply corruption effects to characters based on sanity"""
        if self.player.sanity >= 70:
            return char
        
        corruption_chance = (100 - self.player.sanity) / 400
        
        if random.random() < corruption_chance:
            corrupted = random.choice(self.corruption_chars)
            # Add zalgo marks for severe corruption
            if self.player.sanity < 30 and random.random() < 0.3:
                corrupted += random.choice(self.zalgo_marks)
            return Colors.RED + corrupted + Colors.END
        
        return char
    
    def render_exploration(self):
        """Render full-screen ASCII FPS-style exploration view with true 3D perspective"""
        cols, lines = self.get_terminal_size()
        view_distance = 8
        dx, dy = self.get_direction_vector()
        
        self.clear_screen()
        
        # Light flicker simulation
        self.light_flicker_frame = (self.light_flicker_frame + 1) % 10
        is_light_on = self.light_flicker_frame < 7 or self.player.sanity > 60
        light_intensity = 1.0 if is_light_on else 0.3
        
        # Calculate available space for rendering
        view_lines = lines - 4
        
        # Split screen into ceiling, walls, and floor
        ceiling_lines = view_lines // 3
        wall_lines = view_lines // 3
        floor_lines = view_lines - ceiling_lines - wall_lines
        
        output_lines = []
        
        # RENDER CEILING (looking up perspective)
        for i in range(ceiling_lines):
            line_chars = []
            
            # Ceiling gets darker towards edges
            depth = i / ceiling_lines
            
            if depth < 0.3:
                # Near ceiling - show details
                for x in range(cols):
                    edge_dist = min(x, cols - x) / cols
                    if random.random() < 0.02 and edge_dist > 0.1:
                        line_chars.append(Colors.DIM + random.choice(['-', '|', '·', '.']) + Colors.END)
                    else:
                        line_chars.append(Colors.DIM + '.' + Colors.END)
            else:
                # Farther ceiling
                for x in range(cols):
                    if random.random() < 0.005:
                        line_chars.append(Colors.DIM + '.' + Colors.END)
                    else:
                        line_chars.append(' ')
            
            # Add corruption at edges for low sanity
            if self.player.sanity < 50 and random.random() < 0.05:
                if len(line_chars) > 0:
                    line_chars[0] = Colors.RED + random.choice(self.corruption_chars) + Colors.END
                if len(line_chars) > 1:
                    line_chars[-1] = Colors.RED + random.choice(self.corruption_chars) + Colors.END
            
            output_lines.append(''.join(line_chars))
        
        # RENDER WALLS (main 3D perspective view)
        for i in range(wall_lines):
            # Calculate which distance slice we're looking at
            # Middle of screen = closest, edges = farthest
            view_progress = i / wall_lines
            dist = int(view_distance * (1 - view_progress)) + 1
            
            if dist > view_distance:
                dist = view_distance
            
            look_x = self.player.x + dx * dist
            look_y = self.player.y + dy * dist
            
            # Check surrounding tiles
            perp_dx, perp_dy = -dy, dx
            left_tile = self.station.get_tile(look_x + perp_dx, look_y + perp_dy)
            right_tile = self.station.get_tile(look_x - perp_dx, look_y - perp_dy)
            center_tile = self.station.get_tile(look_x, look_y)
            
            # Perspective calculation - narrower at far distances
            perspective_factor = (view_distance - dist + 1) / (view_distance + 1)
            wall_width = max(8, int(cols * 0.15 * perspective_factor))
            center_gap = cols - (2 * wall_width)
            
            if center_gap < 10:
                center_gap = 10
                wall_width = (cols - center_gap) // 2
            
            # Distance-based lighting
            distance_fade = 1.0 - (dist / view_distance)
            brightness = distance_fade * light_intensity
            
            line_chars = []
            
            # LEFT WALL - rendered with depth
            if left_tile == 1:
                for w in range(wall_width):
                    # Create depth gradient from edge to center
                    depth_factor = w / wall_width
                    
                    if brightness > 0.7:
                        if depth_factor < 0.3:
                            wall_char = '█'
                        elif depth_factor < 0.6:
                            wall_char = '▓'
                        else:
                            wall_char = '▒'
                    elif brightness > 0.4:
                        if depth_factor < 0.5:
                            wall_char = '▓'
                        else:
                            wall_char = '▒'
                    elif brightness > 0.2:
                        wall_char = '▒'
                    else:
                        wall_char = '░'
                    
                    # Add structural details
                    if random.random() < 0.08 and depth_factor > 0.4:
                        wall_char = random.choice(['|', ':', '║'])
                    
                    wall_color = Colors.GREEN if self.player.sanity > 50 else Colors.glitch()
                    line_chars.append(self.apply_corruption(wall_color + wall_char + Colors.END))
            else:
                # Empty space - show darkness gradient
                for w in range(wall_width):
                    depth_factor = w / wall_width
                    if depth_factor > 0.7 and random.random() < 0.02:
                        line_chars.append(Colors.DIM + '░' + Colors.END)
                    else:
                        line_chars.append(' ')
            
            # CENTER - what's ahead
            center_chars = []
            
            if center_tile == 1:  # Wall ahead - render with texture
                wall_color = Colors.GREEN if self.player.sanity > 50 else Colors.glitch()
                
                for c in range(center_gap):
                    # Create texture based on position
                    horizontal_pos = c / center_gap
                    
                    # Add depth and texture
                    if brightness > 0.8:
                        # Close wall - high detail
                        if (c + i) % 4 == 0:
                            fill_char = '#'
                        elif random.random() < 0.15:
                            fill_char = random.choice(['#', '▓', '|', '-'])
                        else:
                            fill_char = '█'
                    elif brightness > 0.5:
                        fill_char = '▓' if random.random() < 0.7 else '#'
                    elif brightness > 0.3:
                        fill_char = '▒'
                    else:
                        fill_char = '░'
                    
                    center_chars.append(self.apply_corruption(wall_color + fill_char + Colors.END))
                    
            elif center_tile == 2:  # Door - render with perspective
                door_width = int(center_gap * perspective_factor * 0.5)
                door_width = max(4, min(door_width, center_gap - 4))
                side_space = (center_gap - door_width) // 2
                
                # Left wall section
                wall_color = Colors.GREEN if self.player.sanity > 50 else Colors.glitch()
                for _ in range(side_space):
                    center_chars.append(wall_color + '#' + Colors.END)
                
                # Door itself
                if dist <= 2:
                    # Close door - show detail
                    center_chars.append(Colors.CYAN + Colors.BOLD + '╔' + Colors.END)
                    for d in range(door_width - 2):
                        if d == door_width // 2:
                            center_chars.append(Colors.CYAN + '█' + Colors.END)  # Handle
                        else:
                            center_chars.append(Colors.CYAN + '║' + Colors.END)
                    center_chars.append(Colors.CYAN + Colors.BOLD + '╗' + Colors.END)
                elif dist <= 4:
                    # Medium distance
                    for _ in range(door_width):
                        center_chars.append(Colors.CYAN + '▓' + Colors.END)
                else:
                    # Far door
                    for _ in range(door_width):
                        center_chars.append(Colors.CYAN + '▒' + Colors.END)
                
                # Right wall section
                for _ in range(center_gap - side_space - door_width):
                    center_chars.append(wall_color + '#' + Colors.END)
                    
            elif center_tile == 3:  # Terminal
                if dist <= 4:
                    term_width = int(center_gap * perspective_factor * 0.4)
                    term_width = max(6, min(term_width, center_gap - 4))
                    side_space = (center_gap - term_width) // 2
                    
                    for _ in range(side_space):
                        center_chars.append(' ')
                    
                    # Terminal display
                    if dist <= 2:
                        center_chars.append(Colors.GREEN + Colors.BOLD + '[' + Colors.END)
                        for t in range(term_width - 2):
                            if t % 3 == 0:
                                center_chars.append(Colors.GREEN + Colors.BOLD + 'T' + Colors.END)
                            else:
                                center_chars.append(Colors.GREEN + '▓' + Colors.END)
                        center_chars.append(Colors.GREEN + Colors.BOLD + ']' + Colors.END)
                    else:
                        for _ in range(term_width):
                            center_chars.append(Colors.GREEN + '▓' + Colors.END)
                    
                    for _ in range(center_gap - side_space - term_width):
                        center_chars.append(' ')
                else:
                    for _ in range(center_gap):
                        center_chars.append(Colors.GREEN + '░' + Colors.END)
                        
            elif center_tile == 4:  # Generator - with glowing effect
                if dist <= 4:
                    gen_width = int(center_gap * perspective_factor * 0.5)
                    gen_width = max(8, min(gen_width, center_gap - 4))
                    side_space = (center_gap - gen_width) // 2
                    
                    for _ in range(side_space):
                        center_chars.append(' ')
                    
                    # Generator core
                    if dist <= 2:
                        center_chars.append(Colors.RED + Colors.BOLD + '◄' + Colors.END)
                        for g in range(gen_width - 2):
                            if random.random() < 0.4:
                                glow = random.choice(['█', '▓', '▒'])
                            else:
                                glow = '▓'
                            center_chars.append(Colors.RED + glow + Colors.END)
                        center_chars.append(Colors.RED + Colors.BOLD + '►' + Colors.END)
                    else:
                        for _ in range(gen_width):
                            center_chars.append(Colors.RED + '▓' + Colors.END)
                    
                    for _ in range(center_gap - side_space - gen_width):
                        center_chars.append(' ')
                else:
                    for _ in range(center_gap):
                        center_chars.append(Colors.RED + '░' + Colors.END)
                        
            elif center_tile == 5:  # Storage
                if dist <= 4:
                    stor_width = int(center_gap * perspective_factor * 0.4)
                    stor_width = max(6, min(stor_width, center_gap - 4))
                    side_space = (center_gap - stor_width) // 2
                    
                    for _ in range(side_space):
                        center_chars.append(' ')
                    
                    for _ in range(stor_width):
                        center_chars.append(Colors.MAGENTA + random.choice(['▓', '▒', '█']) + Colors.END)
                    
                    for _ in range(center_gap - side_space - stor_width):
                        center_chars.append(' ')
                else:
                    for _ in range(center_gap):
                        center_chars.append(Colors.MAGENTA + '░' + Colors.END)
            else:
                # Empty corridor
                for _ in range(center_gap):
                    center_chars.append(' ')
            
            line_chars.extend(center_chars)
            
            # RIGHT WALL - mirror of left with depth
            if right_tile == 1:
                for w in range(wall_width):
                    # Create depth gradient from center to edge
                    depth_factor = (wall_width - w) / wall_width
                    
                    if brightness > 0.7:
                        if depth_factor < 0.3:
                            wall_char = '█'
                        elif depth_factor < 0.6:
                            wall_char = '▓'
                        else:
                            wall_char = '▒'
                    elif brightness > 0.4:
                        if depth_factor < 0.5:
                            wall_char = '▓'
                        else:
                            wall_char = '▒'
                    elif brightness > 0.2:
                        wall_char = '▒'
                    else:
                        wall_char = '░'
                    
                    # Add structural details
                    if random.random() < 0.08 and depth_factor > 0.4:
                        wall_char = random.choice(['|', ':', '║'])
                    
                    wall_color = Colors.GREEN if self.player.sanity > 50 else Colors.glitch()
                    line_chars.append(self.apply_corruption(wall_color + wall_char + Colors.END))
            else:
                # Empty space - darkness gradient
                for w in range(wall_width):
                    depth_factor = (wall_width - w) / wall_width
                    if depth_factor > 0.7 and random.random() < 0.02:
                        line_chars.append(Colors.DIM + '░' + Colors.END)
                    else:
                        line_chars.append(' ')
            
            # Add screen edge corruption at low sanity
            if self.player.sanity < 50:
                if len(line_chars) > 0 and random.random() < 0.1:
                    line_chars[0] = Colors.RED + random.choice(self.corruption_chars) + Colors.END
                if len(line_chars) > 1 and random.random() < 0.1:
                    line_chars[-1] = Colors.RED + random.choice(self.corruption_chars) + Colors.END
            
            output_lines.append(''.join(line_chars[:cols]))
        
        # RENDER FLOOR (looking down perspective)
        for i in range(floor_lines):
            line_chars = []
            
            # Floor gets closer to center as we go down
            depth = i / floor_lines
            floor_width = int(cols * (0.3 + depth * 0.4))
            side_margin = (cols - floor_width) // 2
            
            # Left darkness
            for _ in range(side_margin):
                if random.random() < 0.01:
                    line_chars.append(Colors.DIM + '░' + Colors.END)
                else:
                    line_chars.append(' ')
            
            # Floor tiles
            for f in range(floor_width):
                horizontal_pos = f / floor_width
                
                if depth > 0.7:
                    # Close floor
                    if (f + i) % 5 == 0:
                        line_chars.append(Colors.DIM + ',' + Colors.END)
                    elif random.random() < 0.05:
                        line_chars.append(Colors.DIM + '.' + Colors.END)
                    else:
                        line_chars.append(Colors.DIM + ' ' + Colors.END)
                elif depth > 0.4:
                    # Medium floor
                    if random.random() < 0.03:
                        line_chars.append(Colors.DIM + '.' + Colors.END)
                    else:
                        line_chars.append(' ')
                else:
                    # Far floor
                    if random.random() < 0.01:
                        line_chars.append(Colors.DIM + '·' + Colors.END)
                    else:
                        line_chars.append(' ')
            
            # Right darkness
            for _ in range(cols - side_margin - floor_width):
                if random.random() < 0.01:
                    line_chars.append(Colors.DIM + '░' + Colors.END)
                else:
                    line_chars.append(' ')
            
            # Corruption at edges
            if self.player.sanity < 50 and random.random() < 0.05:
                if len(line_chars) > 0:
                    line_chars[0] = Colors.RED + random.choice(self.corruption_chars) + Colors.END
                if len(line_chars) > 1:
                    line_chars[-1] = Colors.RED + random.choice(self.corruption_chars) + Colors.END
            
            output_lines.append(''.join(line_chars))
        
        # Print all lines
        for line in output_lines:
            print(line)
        
        # Status bar with retro terminal aesthetic
        print(Colors.GREEN + "─" * cols + Colors.END)
        
        current_tile = self.station.get_tile(self.player.x, self.player.y)
        location_text = ""
        location_hint = ""
        
        if current_tile == 3:
            location_text = f"{Colors.GREEN}{Colors.BOLD}[TERMINAL]{Colors.END}"
            location_hint = f"{Colors.GREEN}Press Q to access terminal interface{Colors.END}"
        elif current_tile == 4:
            location_text = f"{Colors.RED}{Colors.BOLD}[GENERATOR]{Colors.END}"
            location_hint = f"{Colors.YELLOW}Power hums through the machinery{Colors.END}"
        elif current_tile == 5:
            location_text = f"{Colors.MAGENTA}{Colors.BOLD}[STORAGE]{Colors.END}"
            location_hint = f"{Colors.CYAN}Supplies stored here{Colors.END}"
        else:
            location_text = f"{Colors.WHITE}[CORRIDOR]{Colors.END}"
            location_hint = ""
        
        status = f"{Colors.GREEN}> {location_text} {Colors.DIM}│{Colors.END} "
        status += f"{Colors.GREEN}POS:{Colors.END}{self.player.x:02d},{self.player.y:02d} {Colors.DIM}│{Colors.END} "
        status += f"{Colors.GREEN}DIR:{Colors.END}{self.player.direction.name[0]} {Colors.DIM}│{Colors.END} "
        status += f"{Colors.GREEN}O2:{Colors.END}{self.resources.oxygen}%"
        
        print(status)
        
        if location_hint:
            print(location_hint)
        
        # Sanity effects
        if self.player.sanity < 40 and random.random() < 0.2:
            messages = [
                f"{Colors.RED}...{random.choice(self.corruption_chars)}...something moved...{Colors.END}",
                f"{Colors.RED}...the walls breathe...{Colors.END}",
                f"{Colors.RED}...{random.choice(self.corruption_chars)}...you hear whispers...{Colors.END}",
                f"{Colors.RED}...you are not alone...{random.choice(self.corruption_chars)}{Colors.END}"
            ]
            print(f"\n{random.choice(messages)}")
        
        print(f"\n{Colors.DIM}[W]FWD [S]BACK [A]LEFT [D]RIGHT [M]MAP [Q]TERM{Colors.END}")

    def get_direction_vector(self) -> Tuple[int, int]:
        vectors = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0)
        }
        return vectors[self.player.direction]

    def move_player(self, forward: bool = True):
        dx, dy = self.get_direction_vector()
        if not forward:
            dx, dy = -dx, -dy
        
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        if self.station.is_walkable(new_x, new_y):
            self.player.x = new_x
            self.player.y = new_y
            self.resources.oxygen -= 1
            
            # Random sounds while exploring
            if self.player.sanity < 60 and random.random() < 0.1:
                self.trigger_sound_log()
        else:
            print(f"\n{Colors.RED}> You can't move that way!{Colors.END}")
            time.sleep(0.5)

    def turn_player(self, clockwise: bool = True):
        direction_order = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        current_idx = direction_order.index(self.player.direction)
        
        if clockwise:
            new_idx = (current_idx + 1) % 4
        else:
            new_idx = (current_idx - 1) % 4
        
        self.player.direction = direction_order[new_idx]

    def handle_exploration_input(self):
        while self.player.current_mode == GameMode.EXPLORATION:
            self.render_exploration()
            
            cmd = input(f"\n{Colors.CYAN}>{Colors.END} ").strip().lower()
            
            if cmd == 'w':
                self.move_player(forward=True)
            elif cmd == 's':
                self.move_player(forward=False)
            elif cmd == 'a':
                self.turn_player(clockwise=False)
            elif cmd == 'd':
                self.turn_player(clockwise=True)
            elif cmd == 'm':
                self.map_command()
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")
            elif cmd == 'q':
                # Check if at terminal
                current_tile = self.station.get_tile(self.player.x, self.player.y)
                if current_tile == 3:
                    self.player.current_mode = GameMode.TERMINAL
                    print(f"\n{Colors.GREEN}[ACCESSING TERMINAL INTERFACE]{Colors.END}")
                    time.sleep(0.8)
                    return
                else:
                    print(f"\n{Colors.RED}> No terminal access from this location. Find a Terminal (T) first.{Colors.END}")
                    time.sleep(1)
            elif cmd == 'help':
                print(f"\n{Colors.YELLOW}W=Forward, S=Backward, A=Turn Left, D=Turn Right, M=Map, Q=Terminal{Colors.END}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")
            else:
                print(f"\n{Colors.RED}> Invalid command. Use 'help' for controls.{Colors.END}")
                time.sleep(0.5)

    def help_command(self):
        self.print_box_header("AVAILABLE COMMANDS")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Terminal Operations:{Colors.END}")
        print(f"  {Colors.YELLOW}scan{Colors.END}          - Scan for signals")
        print(f"  {Colors.YELLOW}analyze <n>{Colors.END}   - Analyze signal at index n")
        print(f"  {Colors.YELLOW}decode{Colors.END}        - Decode current signal")
        print(f"  {Colors.YELLOW}submit{Colors.END}        - Submit decoded signal for credits")
        print(f"  {Colors.YELLOW}status{Colors.END}        - Show detailed status")
        print(f"  {Colors.YELLOW}clear{Colors.END}         - Clear terminal history")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Station Management:{Colors.END}")
        print(f"  {Colors.YELLOW}repair <sys>{Colors.END}  - Repair system (power/oxygen)")
        print(f"  {Colors.YELLOW}rest{Colors.END}          - Rest to restore sanity")
        print(f"  {Colors.YELLOW}inventory{Colors.END}     - Show inventory and supplies")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Navigation:{Colors.END}")
        print(f"  {Colors.YELLOW}explore{Colors.END}       - Enter exploration mode")
        print(f"  {Colors.YELLOW}map{Colors.END}           - Show station map")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}System:{Colors.END}")
        print(f"  {Colors.YELLOW}help{Colors.END}          - Show this help")
        print(f"  {Colors.YELLOW}exit/quit{Colors.END}     - Exit the game")
    
    def clear_command(self):
        """Clear terminal history"""
        self.terminal_history = []
        self.clear_screen()
        print(f"{Colors.GREEN}Terminal history cleared.{Colors.END}\n")
    
    def repair_command(self, args: List[str]):
        """Repair station systems"""
        if not args:
            print(f"{Colors.YELLOW}Usage: repair <power|oxygen>{Colors.END}")
            print(f"{Colors.DIM}Repair parts available: {self.resources.repair_parts}{Colors.END}")
            return
        
        system = args[0].lower()
        if system not in ['power', 'oxygen']:
            print(f"{Colors.RED}Invalid system. Use: power or oxygen{Colors.END}")
            return
        
        if self.resources.repair_parts < 1:
            print(f"{Colors.RED}Not enough repair parts!{Colors.END}")
            return
        
        self.resources.repair_parts -= 1
        
        if system == 'power':
            old_power = self.resources.power
            self.resources.power = min(100, self.resources.power + 30)
            print(f"\n{Colors.CYAN}[REPAIRING POWER SYSTEM]{Colors.END}")
            self.animate_loading("Repairing", 1.5)
            print(f"{Colors.GREEN}✓ Power restored: {old_power}% → {self.resources.power}%{Colors.END}")
        else:
            old_oxygen = self.resources.oxygen
            self.resources.oxygen = min(100, self.resources.oxygen + 30)
            print(f"\n{Colors.CYAN}[REPAIRING OXYGEN SYSTEM]{Colors.END}")
            self.animate_loading("Repairing", 1.5)
            print(f"{Colors.GREEN}✓ Oxygen restored: {old_oxygen}% → {self.resources.oxygen}%{Colors.END}")
    
    def rest_command(self):
        """Rest to restore sanity"""
        if self.resources.water_filters < 1 or self.resources.food_cartridges < 1:
            print(f"{Colors.RED}Not enough supplies to rest! Need: 1 water filter, 1 food cartridge{Colors.END}")
            return
        
        self.resources.water_filters -= 1
        self.resources.food_cartridges -= 1
        
        print(f"\n{Colors.CYAN}[RESTING]{Colors.END}")
        self.animate_loading("Resting", 2.0)
        
        old_sanity = self.player.sanity
        self.player.sanity = min(100, self.player.sanity + 20)
        
        print(f"{Colors.GREEN}✓ You feel more stable{Colors.END}")
        print(f"{Colors.BLUE}Sanity restored: {old_sanity}% → {self.player.sanity}%{Colors.END}")
        
        self.day += 1
        self.resources.power = max(0, self.resources.power - 5)
        self.resources.oxygen = max(0, self.resources.oxygen - 5)
    
    def inventory_command(self):
        """Show detailed inventory"""
        self.print_box_header("INVENTORY")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Currency:{Colors.END}")
        print(f"  {Colors.YELLOW}Credits:{Colors.END} {self.player.credits}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Supplies:{Colors.END}")
        print(f"  {Colors.BLUE}Water Filters:{Colors.END} {self.resources.water_filters}")
        print(f"  {Colors.BLUE}Food Cartridges:{Colors.END} {self.resources.food_cartridges}")
        print(f"  {Colors.BLUE}Repair Parts:{Colors.END} {self.resources.repair_parts}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Statistics:{Colors.END}")
        print(f"  {Colors.BLUE}Signals Discovered:{Colors.END} {self.discovered_signals}")
        print(f"  {Colors.BLUE}Days Survived:{Colors.END} {self.day}")
    
    def map_command(self):
        """Display station map"""
        self.print_box_header("STATION MAP")
        
        print(f"\n{Colors.DIM}Legend: @ = You, # = Wall, . = Floor, D = Door, T = Terminal, G = Generator, S = Storage{Colors.END}\n")
        
        for y, row in enumerate(self.station.layout):
            line = ""
            for x, tile in enumerate(row):
                if x == self.player.x and y == self.player.y:
                    line += Colors.YELLOW + "@" + Colors.END
                else:
                    tile_char = self.station.tiles[tile]
                    if tile == 1:
                        line += Colors.GRAY + tile_char + Colors.END
                    elif tile == 2:
                        line += Colors.CYAN + tile_char + Colors.END
                    elif tile == 3:
                        line += Colors.GREEN + tile_char + Colors.END
                    elif tile == 4:
                        line += Colors.RED + tile_char + Colors.END
                    elif tile == 5:
                        line += Colors.MAGENTA + tile_char + Colors.END
                    else:
                        line += Colors.DIM + tile_char + Colors.END
            print("  " + line)
        
        print(f"\n{Colors.BLUE}Position:{Colors.END} ({self.player.x}, {self.player.y})")

    def process_command(self, cmd: str):
        parts = cmd.strip().lower().split()
        if not parts:
            return
        
        command = parts[0]
        args = parts[1:]
        
        # Check if at terminal for most commands
        current_tile = self.station.get_tile(self.player.x, self.player.y)
        terminal_only_commands = ['scan', 'analyze', 'decode', 'submit', 'status', 'repair', 'rest', 'inventory']
        
        if command in terminal_only_commands and current_tile != 3:
            print(f"\n{Colors.RED}⚠ ERROR: Terminal access required{Colors.END}")
            print(f"{Colors.YELLOW}You must be at a Terminal location to use this command.{Colors.END}")
            print(f"{Colors.DIM}Use 'explore' to navigate to a terminal, or 'map' to see locations.{Colors.END}")
            return
        
        if command in ['exit', 'quit']:
            self.running = False
            print(f"\n{Colors.CYAN}[SHUTTING DOWN SYSTEMS...]{Colors.END}")
            print(f"{Colors.YELLOW}Stay safe out there, operator.{Colors.END}")
        elif command == 'scan':
            self.scan_command()
        elif command == 'analyze':
            self.analyze_command(args)
        elif command == 'decode':
            self.decode_command()
        elif command == 'submit':
            self.submit_command()
        elif command == 'status':
            self.status_command()
        elif command == 'clear':
            self.clear_command()
        elif command == 'repair':
            self.repair_command(args)
        elif command == 'rest':
            self.rest_command()
        elif command == 'inventory':
            self.inventory_command()
        elif command == 'map':
            self.map_command()
        elif command == 'explore':
            # Exploration can be accessed from anywhere
            if self.player.current_mode == GameMode.TERMINAL:
                print(f"\n{Colors.CYAN}[ENTERING EXPLORATION MODE]{Colors.END}")
                print(f"{Colors.DIM}Navigate to terminals to access commands{Colors.END}")
                time.sleep(1)
                self.player.current_mode = GameMode.EXPLORATION
                self.render_exploration()
                self.handle_exploration_input()
        elif command == 'help':
            self.help_command()
        else:
            print(f"{Colors.RED}Unknown command: {command}. Type 'help' for available commands.{Colors.END}")

    def show_title_screen(self):
        """Display ASCII art title screen"""
        self.clear_screen()
        title = f"""{Colors.CYAN}{Colors.BOLD}
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║  ████████╗██╗  ██╗███████╗    ██╗     ██╗███████╗████████╗███████╗ ║
║  ╚══██╔══╝██║  ██║██╔════╝    ██║     ██║██╔════╝╚══██╔══╝██╔════╝ ║
║     ██║   ███████║█████╗      ██║     ██║███████╗   ██║   █████╗   ║
║     ██║   ██╔══██║██╔══╝      ██║     ██║╚════██║   ██║   ██╔══╝   ║
║     ██║   ██║  ██║███████╗    ███████╗██║███████║   ██║   ███████╗ ║
║     ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝╚══════╝   ╚═╝   ╚══════╝ ║
║                           ███╗   ██╗███████╗██████╗                ║
║                           ████╗  ██║██╔════╝██╔══██╗               ║
║                           ██╔██╗ ██║█████╗  ██████╔╝               ║
║                           ██║╚██╗██║██╔══╝  ██╔══██╗               ║
║                           ██║ ╚████║███████╗██║  ██║               ║
║                           ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝               ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
{Colors.END}"""
        print(title)
        
        print(f"\n{Colors.GRAY}You are alone in a remote observatory, processing deep space signals.{Colors.END}")
        print(f"{Colors.GRAY}Strange things are happening. The signals... they're changing you.{Colors.END}")
        print(f"\n{Colors.YELLOW}Type 'help' for available commands.{Colors.END}")
        print(f"\n{Colors.RED}{Colors.DIM}⚠ Warning: Contains flashing text effects and bell sounds{Colors.END}")
        input(f"\n{Colors.GREEN}Press Enter to begin...{Colors.END}")

    def run(self):
        self.show_title_screen()
        
        while self.running:
            # Don't clear screen - let it scroll like Linux terminal
            print()  # Add spacing
            self.print_status()
            
            # Check game over conditions
            if self.player.sanity <= 0:
                print(f"\n{Colors.RED}{Colors.BOLD}[YOUR MIND SHATTERS]{Colors.END}")
                print(f"\n{Colors.MAGENTA}The voices win. You are one with the void now.{Colors.END}")
                print(f"\n{Colors.RED}{'═' * 25} GAME OVER {'═' * 25}{Colors.END}")
                print("\a\a\a")
                break
            
            if self.resources.oxygen <= 0:
                print(f"\n{Colors.RED}{Colors.BOLD}[OXYGEN DEPLETED]{Colors.END}")
                print(f"\n{Colors.GRAY}You gasp for air that isn't there...{Colors.END}")
                print(f"\n{Colors.RED}{'═' * 25} GAME OVER {'═' * 25}{Colors.END}")
                print("\a\a\a")
                break
            
            if self.resources.power <= 0:
                print(f"\n{Colors.RED}{Colors.BOLD}[TOTAL POWER FAILURE]{Colors.END}")
                print(f"\n{Colors.GRAY}The lights go out. Something moves in the darkness.{Colors.END}")
                print(f"\n{Colors.RED}{'═' * 25} GAME OVER {'═' * 25}{Colors.END}")
                print("\a\a\a")
                break
            
            print(f"\n{Colors.GREEN}TERMINAL READY{Colors.END}")
            cmd = input(f"{Colors.CYAN}>{Colors.END} ").strip()
            
            if cmd:
                self.process_command(cmd)
                
                # Daily resource consumption
                if random.random() < 0.1:
                    self.resources.power = max(0, self.resources.power - 1)
                    self.resources.oxygen = max(0, self.resources.oxygen - 1)

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
