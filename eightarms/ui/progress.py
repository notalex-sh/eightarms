import sys
from .colors import Colors

# EPIC spinner (thanks chatgpt)

class ProgressSpinner:
    
    def __init__(self):
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.current = 0
        self.total = 0
        self.processed = 0
    
    def set_total(self, total: int):
        self.total = total
        self.processed = 0
    
    def increment(self):
        self.processed += 1
        self.update()
    
    def update(self):
        if self.total == 0:
            return
        
        spinner_char = self.spinner_chars[self.processed % len(self.spinner_chars)]
        progress_color = Colors.CYAN
        count_color = Colors.YELLOW
        
        sys.stdout.write(
            f'\r{progress_color}{spinner_char} {Colors.WHITE}Searching through '
            f'{count_color}{self.processed}/{self.total}{Colors.WHITE} commit patches...{Colors.RESET}'
        )
        sys.stdout.flush()
    
    def finish(self):
        if self.total > 0:
            sys.stdout.write(f'\r{Colors.GREEN}✓ Analysed {Colors.YELLOW}{self.processed}{Colors.GREEN} patches{Colors.RESET}' + ' ' * 20 + '\n')
            sys.stdout.flush()
        else:
            print()