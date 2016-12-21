import urwid

class ToggleTerm(urwid.Terminal):
    def __init__(self, display):
        super().__init__(None)
        self.display = display

    def keypress(self, size, key):
        ret = super().keypress(size, key)
        if key == self.display.config['terminal']:
            self.display.toggle_term()
        return ret
