class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
    	self.impl = _GetchUnix()

    def __call__(self): 
        char = self.impl()
        if char == '\x03':
            raise KeyboardInterrupt
        elif char == '\x04':
            raise EOFError
        return char

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSANOW, old_settings)
        return ch
        
getch = _Getch()
