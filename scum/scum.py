#!/usr/bin/env python

from src.main import MainGUI, START_PATH, TABS_PATH
import os
import signal

def main():
    os.system('stty -ixon') # disable XOFF to accept Ctrl-S
    # instantiate it!
    main = MainGUI()
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    status = main.display()
    os.system('stty ixon') # re-enable XOFF!
    if status == 'failure':
        with open(TABS_PATH, 'w') as f:
            f.write(START_PATH + '\n')
            f.write('False')

#if __name__=="__main__":
#    main()


