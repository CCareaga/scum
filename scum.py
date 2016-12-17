#!/usr/bin/env python

from src.main import MainGUI
import os
import signal

def main():
    os.system('stty -ixon') # disable XOFF to accept Ctrl-S
    # instantiate it!
    main = MainGUI()
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    main.display()
    os.system('stty ixon') # re-enable XOFF!

main()
