#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════╗
║                    AXIMA CLI v4.0                          ║
║         Zero-Parameter Intelligence Terminal               ║
║                                                           ║
║  Math • Physics • Explain • Brain • Voice • 15 Languages  ║
╚═══════════════════════════════════════════════════════════╝

Usage:
  python3 axima_cli.py              → Interactive mode
  python3 axima_cli.py "query"      → Single query mode
  echo "query" | python3 axima_cli.py  → Pipe mode
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'python'))

from axima import get_axima


# ═══════════════════════════════════════════════════════════
# COLORS (ANSI)
# ═══════════════════════════════════════════════════════════

class C:
    BOLD = '\033[1m'
    DIM = '\033[2m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    RED = '\033[31m'
    BLUE = '\033[34m'
    RESET = '\033[0m'


# ═══════════════════════════════════════════════════════════
# CLI ENGINE
# ═══════════════════════════════════════════════════════════

class AximaCLI:
    """Interactive AXIMA terminal."""

    def __init__(self):
        self.ax = get_axima()
        self.mode = "deep"
        self.voice = "nova"
        self.emotion = "neutral"
        self.history = []
        self.running = True

    def run(self):
        """Main loop."""
        self._banner()

        # Single query from args
        if len(sys.argv) > 1:
            query = ' '.join(sys.argv[1:])
            self._handle(query)
            return

        # Pipe mode
        if not sys.stdin.isatty():
            for line in sys.stdin:
                line = line.strip()
                if line:
                    self._handle(line)
            return

        # Interactive mode
        while self.running:
            try:
                prompt = f"{C.CYAN}axima{C.RESET} {C.DIM}({self.mode}){C.RESET} {C.GREEN}>{C.RESET} "
                text = input(prompt)
                if text.strip():
                    self._handle(text.strip())
            except (KeyboardInterrupt, EOFError):
                print(f"\n{C.DIM}Goodbye.{C.RESET}")
                break

    def _handle(self, text: str):
        """Handle a single input."""
        # Commands start with /
        if text.startswith('/'):
            self._command(text)
            return

        # Process with AXIMA
        result = self.ax.process(text, mode=self.mode)
        self.history.append((text, result))
        self._display(result)

    def _command(self, cmd: str):
        """Handle slash commands."""
        parts = cmd.lower().split()
        command = parts[0]

        if command in ('/q', '/quit', '/exit'):
            self.running = False
            print(f"{C.DIM}Goodbye.{C.RESET}")

        elif command == '/help':
            self._help()

        elif command == '/mode':
            if len(parts) > 1:
                modes = ['one-line', 'bullets', 'steps', 'deep', 'expert', 'simple', 'teach', 'exam']
                if parts[1] in modes:
                    self.mode = parts[1]
                    print(f"  {C.GREEN}Mode set to: {self.mode}{C.RESET}")
                else:
                    print(f"  Modes: {', '.join(modes)}")
            else:
                print(f"  Current mode: {C.BOLD}{self.mode}{C.RESET}")

        elif command == '/voice':
            if len(parts) > 1:
                voices = self.ax.voices()
                if parts[1] in voices:
                    self.voice = parts[1]
                    print(f"  {C.GREEN}Voice: {self.voice}{C.RESET}")
                else:
                    print(f"  Voices: {', '.join(voices)}")
            else:
                print(f"  Current voice: {C.BOLD}{self.voice}{C.RESET}")

        elif command == '/emotion':
            if len(parts) > 1:
                emotions = ['neutral', 'happy', 'sad', 'angry', 'fear', 'surprise', 'disgust', 'tender']
                if parts[1] in emotions:
                    self.emotion = parts[1]
                    print(f"  {C.GREEN}Emotion: {self.emotion}{C.RESET}")
                else:
                    print(f"  Emotions: {', '.join(emotions)}")
            else:
                print(f"  Current emotion: {C.BOLD}{self.emotion}{C.RESET}")

        elif command == '/speak':
            text = ' '.join(parts[1:]) if len(parts) > 1 else "Hello world"
            print(f"  {C.DIM}Generating speech...{C.RESET}")
            audio = self.ax.speak(text, voice=self.voice, emotion=self.emotion)
            if audio:
                # Save to file
                import wave, struct
                path = '/tmp/axima_speak.wav'
                with wave.open(path, 'w') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(22050)
                    data = b''.join(struct.pack('<h', int(max(-1,min(1,s))*32767)) for s in audio)
                    wf.writeframes(data)
                dur = len(audio) / 22050
                print(f"  {C.GREEN}Generated: {dur:.1f}s → {path}{C.RESET}")
            else:
                print(f"  {C.RED}Failed to generate speech{C.RESET}")

        elif command == '/brain':
            if len(parts) > 1 and parts[1] == 'load':
                # Load a file
                filepath = ' '.join(parts[2:])
                if os.path.exists(filepath):
                    with open(filepath) as f:
                        content = f.read()
                    self.ax.load_brain(content, os.path.basename(filepath))
                    print(f"  {C.GREEN}Loaded: {filepath}{C.RESET}")
                else:
                    print(f"  {C.RED}File not found: {filepath}{C.RESET}")
            elif len(parts) > 1 and parts[1] == 'add':
                text = ' '.join(parts[2:])
                if text:
                    self.ax.load_brain(text, "CLI Input")
                    print(f"  {C.GREEN}Added to brain{C.RESET}")
            else:
                print(f"  /brain load <file> — Load document")
                print(f"  /brain add <text>  — Add text directly")

        elif command == '/lang':
            from multilingual import MultilingualEngine
            e = MultilingualEngine()
            if len(parts) > 1:
                r = e.process(' '.join(parts[1:]))
                print(f"  Detected: {C.BOLD}{r.language}{C.RESET} | intent={r.intent} | topic=\"{r.topic}\"")
            else:
                print(f"  Supported: te hi ta es fr de pt ar ja ko ru bn kn ml en (15 languages)")

        elif command == '/history':
            if not self.history:
                print(f"  {C.DIM}No history yet{C.RESET}")
            else:
                for i, (q, r) in enumerate(self.history[-10:], 1):
                    print(f"  {C.DIM}{i}.{C.RESET} {q[:50]} → [{r.source}]")

        elif command == '/clear':
            os.system('clear' if os.name != 'nt' else 'cls')
            self._banner()

        elif command == '/stats':
            print(f"  {C.BOLD}AXIMA v4.0{C.RESET}")
            print(f"  Mode: {self.mode} | Voice: {self.voice} | Emotion: {self.emotion}")
            print(f"  History: {len(self.history)} queries")
            print(f"  Languages: 15 | Voices: 8 | Emotions: 8")
            print(f"  Engines: Math + Physics + ACES + Brain + Voice")

        else:
            print(f"  {C.RED}Unknown command. Type /help{C.RESET}")

    def _display(self, result):
        """Display a response beautifully."""
        # Language badge
        lang_badge = f"{C.MAGENTA}[{result.language}]{C.RESET}" if result.language != 'en' else ""
        source_badge = f"{C.BLUE}[{result.source}]{C.RESET}"

        print()
        if lang_badge:
            print(f"  {lang_badge} {source_badge}")
        else:
            print(f"  {source_badge}")
        print()

        # Answer
        for line in result.answer.split('\n'):
            if line.strip():
                # Highlight formulas
                if '=' in line and any(c.isalpha() for c in line):
                    print(f"  {C.YELLOW}{line}{C.RESET}")
                # Highlight steps
                elif line.strip()[0:1].isdigit() and '.' in line[:3]:
                    print(f"  {C.GREEN}{line}{C.RESET}")
                # Highlight bullets
                elif line.strip().startswith(('•', '→', '📖', '💡', '⚠️', '✅')):
                    print(f"  {C.CYAN}{line}{C.RESET}")
                else:
                    print(f"  {line}")
            else:
                print()
        print()

    def _banner(self):
        """Show welcome banner."""
        print(f"""
{C.BOLD}{C.CYAN}╔═══════════════════════════════════════════════════════╗
║                    AXIMA CLI v4.0                      ║
║        Zero-Parameter Intelligence Terminal            ║
╠═══════════════════════════════════════════════════════╣
║  Ask anything in 15 languages. Type /help for commands ║
╚═══════════════════════════════════════════════════════╝{C.RESET}
""")

    def _help(self):
        """Show help."""
        print(f"""
  {C.BOLD}COMMANDS:{C.RESET}
    /mode <mode>       Set explanation mode
                       (one-line|bullets|steps|deep|expert|simple|teach|exam)
    /voice <name>      Set voice (atlas|nova|spark|sage|aria|echo|storm|whisper)
    /emotion <name>    Set emotion (neutral|happy|sad|angry|fear|surprise|tender)
    /speak <text>      Generate speech audio
    /brain load <file> Load document for Q&A
    /brain add <text>  Add knowledge directly
    /lang <text>       Detect language of text
    /history           Show recent queries
    /stats             Show system info
    /clear             Clear screen
    /help              This help
    /quit              Exit

  {C.BOLD}JUST TYPE:{C.RESET}
    gravity ante enti          → Telugu auto-detected
    solve x^2 + 2x + 1 = 0    → Math solver
    explain photosynthesis     → ACES explanation
    que es la fuerza           → Spanish auto-detected
    gravity kya hai bro        → Hindi casual

  {C.BOLD}SUPPORTS:{C.RESET}
    15 languages • 8 explanation modes • 8 voices • 8 emotions
    Math solver • Physics engine • ACES explainer • Brain Q&A
""")


# ═══════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    cli = AximaCLI()
    cli.run()
