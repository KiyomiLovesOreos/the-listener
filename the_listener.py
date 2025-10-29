#!/usr/bin/env python3
"""
The Listener - A cosmic horror survival game
"""
import os
import sys
import random
import time
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
        # Simple station layout (10x10 grid)
        # 0 = floor, 1 = wall, 2 = door, 3 = terminal, 4 = generator, 5 = storage
        self.layout = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 3, 0, 2, 0, 0, 4, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 2, 1, 1, 1, 1, 2, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 5, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
        
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_separator(self, char="═"):
        print(Colors.GRAY + char * 70 + Colors.END)

    def print_box_header(self, text: str):
        padding = (68 - len(text)) // 2
        print(Colors.CYAN + "╔" + "═" * 68 + "╗" + Colors.END)
        print(Colors.CYAN + "║" + " " * padding + Colors.BOLD + text + Colors.END + Colors.CYAN + " " * (68 - padding - len(text)) + "║" + Colors.END)
        print(Colors.CYAN + "╚" + "═" * 68 + "╝" + Colors.END)

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
        print(f"\n{Colors.CYAN}[ENTERING EXPLORATION MODE]{Colors.END}")
        print(f"{Colors.DIM}Use WASD to move, Q to return to terminal{Colors.END}")
        time.sleep(1)
        self.player.current_mode = GameMode.EXPLORATION
        self.render_exploration()

    def render_exploration(self):
        # Calculate view based on player direction
        view_distance = 5
        dx, dy = self.get_direction_vector()
        
        self.clear_screen()
        self.print_box_header("EXPLORATION MODE")
        
        print(f"\n{Colors.BLUE}Position:{Colors.END} {Colors.CYAN}({self.player.x}, {self.player.y}){Colors.END} │ "
              f"{Colors.BLUE}Facing:{Colors.END} {Colors.YELLOW}{self.player.direction.name}{Colors.END}")
        self.print_separator()
        
        # Render first-person view with color
        print("\n")
        for dist in range(view_distance, 0, -1):
            look_x = self.player.x + dx * dist
            look_y = self.player.y + dy * dist
            
            tile = self.station.get_tile(look_x, look_y)
            tile_char = self.station.tiles.get(tile, "#")
            
            # Create perspective effect
            width = (view_distance - dist + 1) * 2
            padding = " " * ((view_distance * 2) - width)
            
            # Color based on tile type and sanity
            if tile == 1:  # Wall
                wall_color = Colors.GRAY if self.player.sanity > 50 else Colors.glitch()
                display = wall_color + tile_char * width + Colors.END
            else:
                display = " " * width
            
            # Add glitch at low sanity
            if self.player.sanity < 30 and random.random() < 0.1:
                display = Colors.RED + random.choice(self.glitch_chars) * width + Colors.END
            
            print(padding + display)
        
        print(f"\n{Colors.CYAN}{'═' * 20}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}    [  YOU  ]{Colors.END}")
        print(f"{Colors.CYAN}{'═' * 20}{Colors.END}")
        
        # Show what's at current location
        current_tile = self.station.get_tile(self.player.x, self.player.y)
        if current_tile == 3:
            print(f"\n{Colors.GREEN}> You are at the TERMINAL. Press Q to use it.{Colors.END}")
        elif current_tile == 4:
            print(f"\n{Colors.YELLOW}> You are at the GENERATOR.{Colors.END}")
        elif current_tile == 5:
            print(f"\n{Colors.CYAN}> You are at STORAGE.{Colors.END}")
        
        # Random creepy messages at low sanity
        if self.player.sanity < 40 and random.random() < 0.15:
            messages = [
                f"{Colors.GRAY}...something moved in the shadows...{Colors.END}",
                f"{Colors.GRAY}...the walls feel closer than before...{Colors.END}",
                f"{Colors.GRAY}...did you hear that?...{Colors.END}"
            ]
            print(f"\n{random.choice(messages)}")
        
        print(f"\n{Colors.DIM}Controls: W=Forward, S=Backward, A=Turn Left, D=Turn Right, Q=Exit{Colors.END}")

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
            
            cmd = input("\n> ").strip().lower()
            
            if cmd == 'w':
                self.move_player(forward=True)
            elif cmd == 's':
                self.move_player(forward=False)
            elif cmd == 'a':
                self.turn_player(clockwise=False)
            elif cmd == 'd':
                self.turn_player(clockwise=True)
            elif cmd == 'q':
                self.player.current_mode = GameMode.TERMINAL
                print(f"\n{Colors.CYAN}[RETURNING TO TERMINAL MODE]{Colors.END}")
                time.sleep(1)
                return
            elif cmd == 'help':
                print(f"\n{Colors.YELLOW}W=Forward, S=Backward, A=Turn Left, D=Turn Right, Q=Exit{Colors.END}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")
            else:
                print(f"\n{Colors.RED}> Invalid command. Type 'help' for controls.{Colors.END}")
                time.sleep(1)

    def help_command(self):
        self.print_box_header("AVAILABLE COMMANDS")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Terminal Operations:{Colors.END}")
        print(f"  {Colors.YELLOW}scan{Colors.END}          - Scan for signals")
        print(f"  {Colors.YELLOW}analyze <n>{Colors.END}   - Analyze signal at index n")
        print(f"  {Colors.YELLOW}decode{Colors.END}        - Decode current signal")
        print(f"  {Colors.YELLOW}submit{Colors.END}        - Submit decoded signal for credits")
        print(f"  {Colors.YELLOW}status{Colors.END}        - Show detailed status")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Navigation:{Colors.END}")
        print(f"  {Colors.YELLOW}explore{Colors.END}       - Enter exploration mode")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}System:{Colors.END}")
        print(f"  {Colors.YELLOW}help{Colors.END}          - Show this help")
        print(f"  {Colors.YELLOW}exit/quit{Colors.END}     - Exit the game")

    def process_command(self, cmd: str):
        parts = cmd.strip().lower().split()
        if not parts:
            return
        
        command = parts[0]
        args = parts[1:]
        
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
        elif command == 'explore':
            self.explore_command()
            if self.player.current_mode == GameMode.EXPLORATION:
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
            self.clear_screen()
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
            cmd = input(f"\n{Colors.CYAN}>{Colors.END} ").strip()
            
            if cmd:
                self.process_command(cmd)
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")
                
                # Daily resource consumption
                if random.random() < 0.1:
                    self.resources.power = max(0, self.resources.power - 1)
                    self.resources.oxygen = max(0, self.resources.oxygen - 1)

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
