#!/usr/bin/env python

import urwid
import os
import re
import signal
import string
from src.modules import *

import pygments.util
from pygments.lexers import guess_lexer_for_filename, get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.lexers.python import PythonLexer, Python3Lexer
from pygments.token import Token
from pygments.filter import Filter
from pygments.styles import get_style_by_name

from pkg_resources import resource_filename

RE_WORD = re.compile(r'\w+')
RE_NOT_WORD = re.compile(r'\W+')

CONFIG_PATH = os.path.abspath(resource_filename('src.resources', 'config.txt'))
HELP_PATH = os.path.abspath(resource_filename('src.resources', 'help.txt'))
TABS_PATH = os.path.abspath(resource_filename('src.resources', 'tabs.dat'))
START_PATH = os.path.abspath(resource_filename('src.resources', 'start_up.txt'))

CONFIG = {
    'short_to_rgb': {  # color look-up table for 8-bit to RGB hex
        # Primary 3-bit (8 colors). Unique representation!
        '00': '000000', '01': '800000', '02': '008000', '03': '808000', '04': '000080',
        '05': '800080', '06': '008080', '07': 'c0c0c0',
        # Equivalent "bright" versions of original 8 colors.
        '08': '808080', '09': 'ff0000', '10': '00ff00', '11': 'ffff00', '12': '0000ff',
        '13': 'ff00ff', '14': '00ffff', '15': 'ffffff',
        # Strictly ascending.
        '16': '000000', '17': '00005f', '18': '000087', '19': '0000af', '20': '0000d7',
        '21': '0000ff', '22': '005f00', '23': '005f5f', '24': '005f87', '25': '005faf',
        '26': '005fd7', '27': '005fff', '28': '008700', '29': '00875f', '30': '008787',
        '31': '0087af', '32': '0087d7', '33': '0087ff', '34': '00af00', '35': '00af5f',
        '36': '00af87', '37': '00afaf', '38': '00afd7', '39': '00afff', '40': '00d700',
        '41': '00d75f', '42': '00d787', '43': '00d7af', '44': '00d7d7', '45': '00d7ff',
        '46': '00ff00', '47': '00ff5f', '48': '00ff87', '49': '00ffaf', '50': '00ffd7',
        '51': '00ffff', '52': '5f0000', '53': '5f005f', '54': '5f0087', '55': '5f00af',
        '56': '5f00d7', '57': '5f00ff','58': '5f5f00', '59': '5f5f5f', '60': '5f5f87',
        '61': '5f5faf', '62': '5f5fd7', '63': '5f5fff', '64': '5f8700', '65': '5f875f',
        '66': '5f8787', '67': '5f87af', '68': '5f87d7', '69': '5f87ff', '70': '5faf00',
        '71': '5faf5f', '72': '5faf87', '73': '5fafaf', '74': '5fafd7', '75': '5fafff',
        '76': '5fd700', '77': '5fd75f', '78': '5fd787', '79': '5fd7af', '80': '5fd7d7',
        '81': '5fd7ff', '82': '5fff00', '83': '5fff5f', '84': '5fff87', '85': '5fffaf',
        '86': '5fffd7', '87': '5fffff', '88': '870000', '89': '87005f', '90': '870087',
        '91': '8700af', '92': '8700d7', '93': '8700ff', '94': '875f00', '95': '875f5f',
        '96': '875f87', '97': '875faf', '98': '875fd7', '99': '875fff', '100': '878700',
        '101': '87875f', '102': '878787', '103': '8787af', '104': '8787d7',
        '105': '8787ff', '106': '87af00', '107': '87af5f', '108': '87af87',
        '109': '87afaf', '110': '87afd7', '111': '87afff', '112': '87d700',
        '113': '87d75f', '114': '87d787', '115': '87d7af', '116': '87d7d7',
        '117': '87d7ff', '118': '87ff00', '119': '87ff5f', '120': '87ff87',
        '121': '87ffaf', '122': '87ffd7', '123': '87ffff', '124': 'af0000',
        '125': 'af005f', '126': 'af0087', '127': 'af00af', '128': 'af00d7',
        '129': 'af00ff', '130': 'af5f00', '131': 'af5f5f', '132': 'af5f87',
        '133': 'af5faf', '134': 'af5fd7', '135': 'af5fff', '136': 'af8700',
        '137': 'af875f', '138': 'af8787', '139': 'af87af', '140': 'af87d7',
        '141': 'af87ff', '142': 'afaf00', '143': 'afaf5f', '144': 'afaf87',
        '145': 'afafaf', '146': 'afafd7', '147': 'afafff', '148': 'afd700',
        '149': 'afd75f', '150': 'afd787', '151': 'afd7af', '152': 'afd7d7',
        '153': 'afd7ff', '154': 'afff00', '155': 'afff5f', '156': 'afff87',
        '157': 'afffaf', '158': 'afffd7', '159': 'afffff', '160': 'd70000',
        '161': 'd7005f', '162': 'd70087', '163': 'd700af', '164': 'd700d7',
        '165': 'd700ff', '166': 'd75f00', '167': 'd75f5f', '168': 'd75f87',
        '169': 'd75faf', '170': 'd75fd7', '171': 'd75fff', '172': 'd78700',
        '173': 'd7875f', '174': 'd78787', '175': 'd787af', '176': 'd787d7',
        '177': 'd787ff', '178': 'd7af00', '179': 'd7af5f', '180': 'd7af87',
        '181': 'd7afaf', '182': 'd7afd7', '183': 'd7afff', '184': 'd7d700',
        '185': 'd7d75f', '186': 'd7d787', '187': 'd7d7af', '188': 'd7d7d7',
        '189': 'd7d7ff', '190': 'd7ff00', '191': 'd7ff5f', '192': 'd7ff87',
        '193': 'd7ffaf', '194': 'd7ffd7', '195': 'd7ffff', '196': 'ff0000',
        '197': 'ff005f', '198': 'ff0087', '199': 'ff00af', '200': 'ff00d7',
        '201': 'ff00ff', '202': 'ff5f00', '203': 'ff5f5f', '204': 'ff5f87',
        '205': 'ff5faf', '206': 'ff5fd7', '207': 'ff5fff', '208': 'ff8700',
        '209': 'ff875f', '210': 'ff8787', '211': 'ff87af', '212': 'ff87d7',
        '213': 'ff87ff', '214': 'ffaf00', '215': 'ffaf5f', '216': 'ffaf87',
        '217': 'ffafaf', '218': 'ffafd7', '219': 'ffafff', '220': 'ffd700',
        '221': 'ffd75f', '222': 'ffd787', '223': 'ffd7af', '224': 'ffd7d7',
        '225': 'ffd7ff', '226': 'ffff00', '227': 'ffff5f', '228': 'ffff87',
        '229': 'ffffaf', '230': 'ffffd7', '231': 'ffffff',
        # Gray-scale range.
        '232': '080808', '233': '121212', '234': '1c1c1c', '235': '262626',
        '236': '303030', '237': '3a3a3a', '238': '444444', '239': '4e4e4e',
        '240': '585858', '241': '626262', '242': '6c6c6c', '243': '767676',
        '244': '808080', '245': '8a8a8a', '246': '949494', '247': '9e9e9e',
        '248': 'a8a8a8', '249': 'b2b2b2', '250': 'bcbcbc', '251': 'c6c6c6',
        '252': 'd0d0d0', '253': 'dadada', '254': 'e4e4e4', '255': 'eeeeee',
        },

        'header':['header', 'white', 'dark gray', 'bold'],
        'browse':['browse', 'black', 'light gray'],
        'footer':['footer', 'white', 'dark gray', 'bold'],
        'key':['key', 'white', 'dark blue', 'default'],
        'selected':['selected', 'white', 'dark blue', 'bold'],
        'flagged':['flagged', 'black', 'dark green', 'bold'],
        'focus':['focus', 'light gray', 'dark blue', 'standout'],
        'flagged focus':['flagged focus', 'yellow', 'dark cyan', ('bold','standout','underline')],

        'style':'monokai',

        'open':'ctrl o',
        'save':'ctrl s',
        'find':'ctrl f',
        'undo':'ctrl q',
        'delline':'ctrl d',
        'prevtab':'meta page up',
        'nexttab':'meta page down',
        'closetab':'ctrl w',
        'terminal':'ctrl g',
        'linenum':'ctrl n',
        'layout':'f1',
        'config':'f5',
        'exit':'ctrl x'
    }

CONFIG['rgb_to_short'] = {v: k for k, v in CONFIG['short_to_rgb'].items()}

# all the possible widgets that can be defined in the config
palette_items = ['header', 'flagged focus', 'key', 'footer', 'focus', 'selected', 'flagged', 'browse']
text_options = ['bold', 'underline', 'standout']

def read_config():
    counter = 0
    new_config = CONFIG # make a copy of the default config
    with open(CONFIG_PATH, 'r') as f:
        lines = [x.strip('\n') for x in f.readlines()] # strip any unempty lines

    for line in lines:
        counter += 1
        if line.strip() and line.lstrip()[0] != '#': # skip lines with '#' at beginning
            split = line.split(':') # break the line into two parts item and attributes
            item = split[0].strip()
            if item in palette_items: # if this line is a palette line
                attribs = split[1].strip().split(",")
                try: # try creating an urwid attr spec
                    a = urwid.AttrSpec(attribs[0].strip(), attribs[1].strip(), colors=256)
                    if attribs[2] not in text_options:
                        attribs[2] = ''
                    new_config[item] = [item]+[a.foreground, a.background, attribs[2]] # add this to the new config
                except:
                    print("error on line" + str(counter))
            else: # this line isn't a palette lime
                if item in new_config: # if this item exists in config dict
                    new_config[item] = split[1].strip() # redefine it in the dict

    return new_config

def strip_fname(fname):
    # This function gets only the name of the file, without the path
    peices = fname.split("/")
    return peices[-1]

def strip_path(fname):
    peices = os.path.abspath(fname).split("/")
    return "/".join(peices[0:-1])

def rgb_to_short(rgb, mapping):
    """Find the closest xterm-256 approximation to the given RGB value."""
    # Thanks to Micah Elliott (http://MicahElliott.com) for colortrans.py
    rgb = rgb.lstrip('#') if rgb.startswith('#') else rgb
    incs = (0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff)
    # Break 6-char RGB code into 3 integer vals.
    parts = [int(h, 16) for h in re.split(r'(..)(..)(..)', rgb)[1:4]]
    res = []
    for part in parts:
        i = 0
        while i < len(incs)-1:
            s, b = incs[i], incs[i+1]  # smaller, bigger
            if s <= part <= b:
                s1 = abs(s - part)
                b1 = abs(b - part)
                if s1 < b1: closest = s
                else: closest = b
                res.append(closest)
                break
            i += 1
    res = ''.join([ ('%02.x' % i) for i in res ])
    equiv = mapping[res]
    return equiv, res

# since this is a multi-tab editor, there are a lot of peices of info that need to be stored for each tab
# instead of keeping a bunch of dicts to key the data we need, we can just have one dict and key up an
# object that has all the data we need
#
# DATA:
#       file content
#       cursor pos
#       undo stack
#
class TabInfo(object):
    def __init__(self, display):
        self.display = display
        self.lines = []
        self.cursor = [0, 0]
        self.undo = UndoStack(self.display)

class UndoStack(object):
    def __init__(self, display):
        self.items = []
        self.display = display

    def undo(self):
        # this method undoes the last action from the undo stack. This could be a character added, deleted, a line
        # added, a line combined with the previous or the next. It is pretty ugly becuase there are quite a bit of special
        # cases to take into consideration like pressing delete at the end of a line, or backspace at the beginning of
        # a line. It works though!
        if self.items == []:
            return
        item = self.items.pop(-1)
        # item[0] = keys, item[1] = position, item[2] = change

        self.display.listbox.set_focus(item[1][0])
        self.display.listbox.focus.set_edit_pos(item[1][1])

        if item[2]: # something deleted, so add
            if item[0] == 'backspace': # backspace at beginning of line or del at end
                self.display.listbox.set_focus(item[1][0])
                self.display.listbox.focus.set_edit_pos(item[1][1])
                self.display.listbox.do_enter()
                self.items.pop(-1)
                return
            elif item[0][-1] == '\n': # if ctrl d is pressed (delete line)
                text = TextLine(item[0][:-1], self.display)
                self.display.listbox.lines.insert(item[1][0], text)
                self.display.line_nums.add()
            else: # this is just a normal backspace
                self.display.listbox.focus.insert_text(item[0])

        else: # something added so delete!
            if item[0] == 'enter': # undo an enter press
                self.display.listbox.set_focus(item[1][0]+1)
                self.display.listbox.combine_previous()
                return
            # otherwise undo a normal character deletion
            old_text = self.display.listbox.focus.edit_text
            index = int(item[0])
            #self.display.loop.process_input(['backspace'])
            if index != len(old_text):
                new_text = old_text[:index-1] + old_text[index:]
            else:
                new_text = old_text[:index-1]

            self.display.listbox.focus.set_edit_text(new_text)

    def log(self, keys, position, change):
        #keys: text to insert, or un-insert
        #position: where to place or take out text
        #change: if removed this is 1 (backspace, delete), if added this is 0 (keypress)
        new_item = [keys, position, change]
        self.items.append(new_item)

class FindField(urwid.Edit):
    def __init__(self, display, **kwargs):
        super().__init__("find: ", **kwargs)
        self.display = display
        self.index = 0
        self.line = 0
        self.last = 0
        self.on_line = []
        self.history = []

    def goto(self, word, current):
        # this method is some crazy sh*t, I wrote it and I still am not quite sure how it works...
        # but since it works, I will not mess with it :-)
        found = False
        if self.history == [] or self.history[-1] != (self.line, self.index):
            self.history.append((self.line, self.index))

        if len(self.on_line) > 0:
            self.index = self.on_line.pop(0)

        else:
            for line in self.display.listbox.lines[current[0]:]:
                if word in line.edit_text:
                    for m in re.finditer(word, line.edit_text):
                        self.on_line.append(m.start())

                    self.index = self.on_line.pop(0)

                    self.last = self.line
                    self.line = self.display.listbox.lines.index(line)
                    found = True
                    break
        if not found:
            self.history.pop(-1)
            return

        self.display.top.set_focus('body')
        self.display.listbox.lines[self.line].set_edit_pos(self.index)
        self.display.listbox.set_focus(self.line)
        self.display.update_line_numbers()

    def handle_key(self, key):
        # this is where all the keypress for the find bar happen, I don't use the keypress method
        # becuase we are never actually focused on the find bar, we are always focused on the text
        # editor. We grab the key presses from the text editor and manually feed them into the find
        # bar, and running each function according to the keypress we get

        if key in string.printable: # if the key press was a printable character
            # we are searching for a new string so we clear everyhting and find the first occurence
            self.on_line = []
            self.insert_text(key)
            self.goto(self.edit_text, (0,0))
            self.history = []

        if key == self.display.config['find']: # if ctrl+f is pressed again stop finding
            self.display.top.contents['footer'] = (self.display.foot_col, None)
            self.set_edit_text("")
            self.on_line = []
            if self.display.layout:
                self.display.top.contents['footer'] = (self.display.status, None)
            else:
                for file in self.display.file_names:
                    # since these files are already open, the list box won't repopulate
                    # but the tabs will be re-drawn!
                    self.display.listbox.populate(file)

            self.display.listbox.set_focus(self.line)
            self.display.finding = False
            #self.display.update_line_numbers()
            return

        if key == 'right': # go to the next occurence of the search string
            if len(self.edit_text) > 0:
                self.goto(self.edit_text, (self.line+1, self.index+1))
                self.display.update_line_numbers(cfrom='above')

        if key == 'left': # go to the previous occurence of the search string
            if len(self.history) > 0: # if there is a previous one to go to
                previous = self.history.pop(-1)
                self.last = self.line
                self.line, self.index = previous[0], previous[1]
                self.display.listbox.lines[self.line].set_edit_pos(self.index)
                self.display.listbox.set_focus(self.line)
                self.display.update_line_numbers(cfrom='below')
            else: # we are at the first occurence so ensure that nothing wonky happens
                self.on_line = []
                self.goto(self.edit_text, (0,0))
                self.history = []
                return

        if key == 'backspace': # this means we are starting a new search
            self.on_line = []
            self.set_edit_text(self.edit_text[:-1]) # get the string wihtout the last letter
            self.goto(self.edit_text, (0, 0))
            self.history = []

        self.display.listbox.lines[self.line].set_edit_pos(self.index)
        self.display.listbox.set_focus(self.line)
        self.display.update_line_numbers()

class TextLine(urwid.Edit):
    def __init__(self, text, display, tabsize=4, **kwargs):
        super().__init__(edit_text=text.expandtabs(4), wrap='clip', **kwargs)
        self.display = display
        self.tab = tabsize
        self.tokens = []
        self.attribs = []
        self.parsed = False
        self.original = text

    def get_text(self):
        etext = self.get_edit_text()
        # this is done to ensure that parsing is only done if the line is selected and altered
        if not self.parsed or (self.display.listbox.focus == self and self.edit_text != self.original):
            self.parsed = True
            # get the new tokens and return them
            self.tokens = self.display.listbox.get_tokens(self.edit_text)
            self.attribs = [(tok, len(s)) for tok, s in self.tokens]
            self.original = self.edit_text

        return etext, self.attribs

    def get_tabsize(self, pos):
        mod = pos % self.tab
        size = self.tab - mod
        if size == 0:
            return self.tab
        return size

    def keypress(self, size, key):
        # this function updates the status bar and implements tab behaviour
        if self.display.finding:
            ret = self.display.finder.handle_key(key)
            return

        ret = super().keypress(size, key)

        if key == 'tab':
            lb = self.display.listbox
            pos = lb.focus.edit_pos
            tabsize = self.get_tabsize(pos)
            for i in range(1, tabsize+1):
                cur_tab = self.display.tab_info[self.display.listbox.fname]
                cur_tab.undo.log(pos+i, [lb.focus_position, lb.focus.edit_pos], 0)
            self.insert_text(' ' * tabsize)

        return ret

# the line numbers to the left of the editor window is actually a listbox of its own
# it is placed next to the main editor listbox in a column container like so:
# __________________________________
# |    Urwid Column container      |
# ----------------------------------
# |1| text                         |
# |2| text                         |
#
# to simulate scrolling I simply set the focus of the line number list box
# to the same focus position as the main editor window. Unfortunately the
# line numbers are copyable so if you try to copy multiple lines they will be
# copied as well :/ so I made them togglable!

class LineNumbers(urwid.ListBox):
    def __init__(self, display):
        self.display = display
        self.numbers = [] # this is the list the listbox uses
        super().__init__(self.numbers) # instantiate the parent class with the list
        self._selectable = False # can't be selectable!
        self.width = 1 # this tells how wide to make the line num column
        # since the line numbers aren't selectable we simulate them being selected
        # by changing their color. this field is used to save the last number that
        # was highlighted in order to unhighlight it
        self.previous  = 1

    # each time the user switches tabs the line numbers need to be cleared and
    # repopulated. For some reason this is the way this has to be done...
    def clear(self):
        self.previous = 1
        for _ in range(0, len(self.numbers)):
            self.sub()

    # this populates the line number listbox , it takes a list as an arg,
    # but it really only needs a length.. it calls clear then
    # it calls  add a bunch to create the new line num
    def populate(self, lines):
        if not self.display.show_lnums:
            return
        self.clear()
        self.width = 1
        for i in range(0, len(lines)):
            self.add()

    # this method is called when a new number needs to be added. if the new number is
    # a digit longer than the last then the column width is increased!
    def add(self):
        self.numbers.append(urwid.Text(str(len(self.numbers)+1) + '| ', align='right'))
        if len(str(len(self.numbers)-1)) > self.width:
            self.width += 1
            new_col = urwid.Columns([(self.width+2, self.display.line_nums), self.display.listbox], focus_column=1)
            self.display.top.contents['body'] = (new_col, None)

    # this method simply deletes a line from the end of the line numbers
    # note: we have to check that we didnt delete the last line or we get an index out of bounds!
    def sub(self):
        if self.display.listbox.focus_position == len(self.numbers)-1:
            self.previous = len(self.numbers)-2
        self.numbers.pop(-1)

class TextList(urwid.ListBox):
    def __init__(self, display):
        self.display = display
        self.lines = []
        super().__init__(self.lines)
        self.fname = ' '
        self.short_name = ' '
        self.lexer = None
        self.config = self.display.config

    def populate(self, fname):
        # this function populates the TextList and creates a new tabs
        # The same Textlist is used for each tab but when tabs are switched the
        # contents of the tab are grabbed from the files TabInfo instance
        if fname not in self.display.file_names:
            # grab the lines from the file and strip the newline char
            # then iterate through and create a new TextLine object for each line
            try:
                with open(fname) as f:
                    content = [x.strip('\n') for x in f.readlines()]
            except:
                self.redraw_tabs()
                return

            # the short name is the file name without a path
            self.short_name = strip_fname(fname)
            self.display.file_names.append(fname)
            new_lines = []

            # grab the lines from the file and strip the newline char
            # Then iterate through and create a new TextLine object for each line
            for line in content:
                text = TextLine(line, self.display)
                new_lines.append(text)

            # if the file is empty then add one empty line so it can be displayed
            if len(new_lines) < 1:
                text = TextLine(' ', self.display)
                new_lines.append(text)

            # create a new tab (button widget) with the correct attributes
            self.display.cur_tab = self.display.tab_info[fname] = TabInfo(self.display)
            new_tab_info = self.display.tab_info[fname]
            new_tab_info.lines = new_lines
            new_tab_info.undo = UndoStack(self.display)
            new_tab_info.cursor = (0, 0)

            self.display.line_nums.populate(new_lines)
            button = urwid.Button(self.short_name)
            button._label.align = 'center'
            attrib = urwid.AttrMap(button, 'footer')
            self.display.tabs.append(attrib)
            # switch to the new tab
            self.switch_tabs(fname)
        else:
            self.display.line_nums.populate(self.lines)
        self.redraw_tabs()

    def redraw_tabs(self):
         # this is done to ensure that the bottom bar is re-drawn after opening files
        foot_col = urwid.Columns(self.display.tabs)
        foot = urwid.AttrMap(foot_col, 'footer')
        if self.display.layout:
            self.display.top.contents['header'] = (foot, None)
        else:
            self.display.top.contents['footer'] = (foot, None)

    def delete_tab(self, fname):
        files = self.display.file_names
        # make sure there is more than one file open
        if len(files) > 1:
            index = files.index(fname)
            if index < len(files)-1: # if not last in list
                new_name = files[index+1]
            else: # if last file in list
                new_name = files[index-1]
            # delete file and contents from master lists
            #del self.display.tab_info[fname]
            del files[index]
            del self.display.tabs[index]
            # reset the footer with new tab amount
            foot_col = urwid.Columns(self.display.tabs)
            foot = urwid.AttrMap(foot_col, 'footer')
            if self.display.layout:
                self.display.top.contents['header'] = (foot, None)
            else:
                self.display.top.contents['footer'] = (foot, None)

            self.switch_tabs(new_name)
            del self.display.tab_info[fname]

    def get_lexer(self):
        # this function gets the lexer depending on the files name
        try:
            lexer = get_lexer_for_filename(self.short_name)
        except pygments.util.ClassNotFound:
            lexer = TextLexer()

        lexer.add_filter('tokenmerge')

        return lexer

    def switch_tabs(self, fname):
        # this method switches to a tab according to the provided filename
        if self.fname != fname: # make sure we aren't already on this tab
            cur_tab_info = self.display.cur_tab
            if self.fname != ' ':
                cur_tab_info = self.display.tab_info[self.fname]
                cur_tab_info.lines[:] = self.lines
                try:
                    line = self.focus_position
                    col = self.focus.edit_pos
                    cur_tab_info.cursor = (line, col)
                except:
                    cur_tab_info.cursor = (0, 0)
            index = self.display.file_names.index(fname)
            tabs = self.display.tabs
            if self.fname != ' ': #hopefully ensures all lines are saved when switching tabs
                cur_tab_info.lines[:] = self.lines
            # change tab colors depending on current index
            for i in range(0, len(tabs)):
                if i != index:
                    tabs[i].set_attr_map({None:'footer'})
                else:
                    tabs[i].set_attr_map({None:'selected'})
            # re-assign the current path and filename
            self.fname = fname
            new_tab_info = self.display.tab_info[self.fname]
            self.short_name = strip_fname(fname)
            # repopulate the lines list from the line dict in the main class
            self.lines[:] = new_tab_info.lines
            self.display.line_nums.populate(self.lines[:])
            self.display.top.set_focus('body')
            self.lexer = self.get_lexer()
            self.set_focus(new_tab_info.cursor[0])
            self.focus.set_edit_pos(new_tab_info.cursor[1])
            self.display.update_line_numbers()
            self.display.cur_tab = new_tab_info
        else:
            # not really needed since no mouse support :/
            self.display.top.set_focus('body')
            return

    def do_enter(self):
        lead = self.get_leading()
        self.split_focus(self.focus_position)
        #text = self.focus.edit_text.strip()
        self.display.line_nums.add()
        self.display.loop.process_input(['down'])
        #if text != "":
        #   self.focus.set_edit_pos(lead)
        #   self.focus.set_edit_text(' ' * lead  + self.focus.edit_text)

    def get_leading(self):
        #get the leading whitespace of a line!
        line = self.lines[self.focus_position]
        return len(self.focus.edit_text) - len(self.focus.edit_text.lstrip())

    def get_tokens(self, text):
        # this function returns the tokens for the provided text
        return list(self.lexer.get_tokens(text))

    def get_line(self, position):
        # gets the TextLine object at the given position
        # I don't think I use this anywhere
        if position < 0:
            return None

        elif len(self.lines) > position:
            return self.lines[position]

    def next(self, index):
        # get the line after the current position
        return self.get_line(index+1)

    def previous(self, index):
        # get the line after the current position
        return self.get_line(index-1)

    def combine_previous(self):
        # combine the line with the one before it (used with backspace)
        prev = self.previous(self.focus_position)
        if prev is None:
            return

        focus = self.focus
        f_pos = self.focus_position

        p_length = len(prev.edit_text)
        # don't mess with this, it is slightly magic, but it works!
        prev.set_edit_text(prev.edit_text + focus.edit_text)
        self.display.loop.process_input(['up'])
        self.focus.set_edit_pos(p_length)
        del self.lines[self.focus_position+1]

    def combine_next(self):
        # combine the line with the one after it (used with delete)
        below = self.next(self.focus_position)
        if below is None:
            return
        self.focus.set_edit_text(self.focus.text + below.text)
        del self.lines[self.focus_position+1]

    def split_focus(self, index):
        # split the current line at the cursor position (when enter is pressed)
        focus = self.lines[index]
        position = focus.edit_pos
        # make a new edit for split half of the line
        new_edit = TextLine(focus.text[position:], self.display)
        focus.set_edit_text(focus.text[:position])
        self.focus.set_edit_pos(0)
        # insert the newline at the correct index
        self.lines.insert(index+1, new_edit)

    def del_line(self):
        pos = self.focus_position
        del self.lines[pos]
        self.focus.set_edit_pos(0)

    def save_file(self):
        # this function is used to save the current file.
        with open(self.fname, 'w') as f:
            for line in self.lines:
                f.write(line.edit_text.rstrip()+'\n')

        if self.short_name == 'config.txt':
            self.display.configure()
            self.display.register_palette()
            self.display.loop.screen.clear()
            self.display.update_top_bar()

    def keypress(self, size, key):
        # this function implements all the keypress behaviour of the text editor window
        # some of the keypress strings are grabbed from the config becuase they are customizable
        cur_tab = self.display.tab_info[self.fname]
        bkey, dkey = '', ''
        pos = 0
        if self.lines != []:
            if len(self.focus.edit_text) > 0:
                pos = self.focus.edit_pos
                bkey = self.focus.edit_text[pos-1]
                if pos < len(self.focus.edit_text):
                    dkey = self.focus.edit_text[pos]

        ret = super().keypress(size, key)
        if self.display.finding:
            return

        if key in string.printable:
            pos = self.focus.edit_pos
            cur_tab.undo.log(pos, [self.focus_position, self.focus.edit_pos], 0)

        if key == 'down' or key == 'up' or key == 'page down' or key == 'page up':
            # we need to set the correct coming_from attribute or the line numbers won't
            # scroll correctly
            if key == 'down' or key == 'page down':
                cfrom = 'above'
            else:
                cfrom = 'below'
            self.display.update_line_numbers(cfrom=cfrom)

        elif key == 'backspace':
            cur_tab.undo.log(bkey, [self.focus_position, self.focus.edit_pos], 1)

        elif key == 'delete':
            cur_tab.undo.log(dkey, [self.focus_position, self.focus.edit_pos], 1)

        elif key == 'enter':
            cur_tab.undo.log('enter', [self.focus_position, self.focus.edit_pos], 0)
            self.do_enter()
        # the next two conditionals use regex to create the Ctrl+arrow behaviour
        elif key == "ctrl right" or key == "meta right":
            line = self.focus
            xpos = line.edit_pos
            if xpos == len(line.edit_text) and self.focus_position != len(self.lines)-1:
                self.set_focus(self.focus_position+1)
                line.set_edit_pos(0)
                return

            re_word = RE_WORD
            m = re_word.search(line.edit_text or "", xpos)
            word_pos = len(line.edit_text) if m is None else m.end()
            line.set_edit_pos(word_pos)

        elif key == "ctrl left" or key == "meta left":
            line = self.focus
            xpos = line.edit_pos
            if xpos == 0 and self.focus_position != 0:
                self.set_focus(self.focus_position-1)
                line.set_edit_pos(len(line.edit_text))
                return
            re_word = RE_WORD
            starts = [m.start() for m in re_word.finditer(line.edit_text or "", 0, xpos)]
            word_pos = 0 if len(starts) == 0 else starts[-1]
            line.set_edit_pos(word_pos)

        elif key == "ctrl backspace":
            line = self.focus
            xpos = line.edit_pos

            starts = [m.start() for m in RE_WORD.finditer(line.edit_text or "", 0, xpos)]
            word_pos = 0 if len(starts) == 0 else starts[-1]
            line.set_edit_text(line.edit_text[word_pos:xpos])

        # this elif moves to the next tab and if user is on the last tab goes to the frst
        elif key == self.config['nexttab']:
            index = self.display.file_names.index(self.fname)
            if index + 1 < len(self.display.file_names):
                next_index = index + 1
            else:
                next_index = 0

            self.switch_tabs(self.display.file_names[next_index])
            self.display.cur_tab = self.display.tab_info[self.fname]

        elif key == self.config['prevtab']:
            index = self.display.file_names.index(self.fname)
            if index - 1 >= 0:
                next_index = index - 1
            else:
                next_index = -1

            self.switch_tabs(self.display.file_names[next_index])
            self.display.cur_tab = self.display.tab_info[self.fname]

        # this elif closes the current tab
        elif key == self.config['closetab']:
            self.delete_tab(self.fname)
            self.display.save_tabs()
        # this elif saves the current tab
        elif key == self.config['save']:
            self.save_file()

        return ret

class MainGUI(object):
    def __init__(self):
        # set up all the empty lists, dicts and strings needed
        # also create the widgets that will be used later
        self.cwd = os.getcwd()
        self.tab_info = {}
        self.file_names = []
        self.palette = []
        self.tabs = []
        self.cur_tab = None

        self.finding = False
        self.show_term = False
        self.show_lnums = True

        self.state = ''
        self.rows = 0

        # this variable represents the UI layout. if this value is False
        # then the tabs are on bottom and status is on top. when this value
        # is True then the layout is switched!
        self.layout = False

        self.configure()

        self.stext = ('header', ['SCUM   ',
                                    ('key', 'ESC'), ' Help ',
                                    ('key', 'ctrl s'), ' Save ',
                                    ('key', 'ctrl o'), ' Open ',
                                    ('key', 'ctrl x'), ' Exit'  ])

        self.openfile_stext = ('header', ['Open File: Arrows to navigate ',
                                    ('key', 'Space'), ' Select ',
                                    ('key', 'Enter'), ' Open '])
        # editor state GUI
        self.bbar = urwid.Text('')

        self.tbar = urwid.Text(self.stext)
        self.tbar_text = self.tbar.text
        self.status = urwid.AttrMap(self.tbar, 'header')

        self.listbox = TextList(self)
        urwid.AttrMap(self.listbox, 'body')

        self.line_nums = LineNumbers(self)
        self.body_col = urwid.Columns([(3, self.line_nums), self.listbox], focus_column=1)

        self.foot_col = urwid.Columns(self.tabs)
        self.foot = urwid.AttrMap(self.foot_col, 'footer')

        self.finder = FindField(self)
        self.fedit = urwid.AttrMap(self.finder, 'footer')

        # openfile state GUI
        self.new_files = []
        self.openfile_top = urwid.Text(self.openfile_stext)
        self.oftbar = urwid.AttrMap(self.openfile_top, 'header')

        self.browser = urwid.TreeListBox(urwid.TreeWalker(DirectoryNode(self.cwd, self)))
        self.browser.offset_rows = 1
        urwid.AttrWrap(self.browser, 'browse')

        self.openfile_bottom = urwid.Text(' ')
        self.ofbbar = urwid.AttrWrap(self.openfile_bottom, 'footer')

        self.top = urwid.Frame(self.body_col, header=self.status, footer=self.foot_col)
        self.update_top_bar()

        self.state = 'editor'

        self.term = ToggleTerm(self)
        self.termbox = urwid.LineBox(self.term)

        self.pile = urwid.Pile([self.top])
        self.open_tabs()

        if len(self.tabs) == 0:
            self.listbox.populate(START_PATH)

    def display(self):
        # this method starts the main loop and such
        self.loop = urwid.MainLoop(self.pile,
                                   self.palette,
                                   handle_mouse = False,
                                   unhandled_input = self.keypress,
                                   pop_ups = True)
        self.loop.screen.set_terminal_properties(colors=256)
        self.register_palette()

        self.term.main_loop = self.loop
        try:
            self.loop.run()
        except:
            return 'failure'

        with open(TABS_PATH, 'a') as f:
            f.write(str(self.layout))

        return 'exit'

    def configure(self):
        # this method is run to re-parse the config and set the palette
        self.config = read_config()

        self.style = get_style_by_name(self.config['style'])

        for item in palette_items:
            self.palette.append(tuple(self.config[item]))

    def update_top_bar(self):
        self.stext = ('header', ['SCUM   ',
                        ('key', 'ESC'), ' Help ',
                        ('key', self.config['save']), ' Save ',
                        ('key', self.config['open']), ' Open ',
                        ('key', self.config['exit']), ' Exit'  ])

        self.tbar = urwid.Text(self.stext)
        self.status = urwid.AttrMap(self.tbar, 'header')

        self.top.contents['header'] = (self.status, None)

    def update_status(self):
        # this method is runs to update the top bar depending on the current state
        col, self.rows = self.loop.screen.get_cols_rows()

        selected = ''
        for f in self.new_files:
            selected += strip_fname(f) + ' | '
        extra = col - len(selected) - 1
        self.ofbbar.set_text(selected)

    def update_line_numbers(self, cfrom=None):
        if self.show_lnums:
            focus_pos = self.listbox.focus_position
            lnums = self.line_nums
            lnums.set_focus(focus_pos, coming_from=cfrom)
            foc = lnums.numbers[focus_pos]

            prev = lnums.numbers[lnums.previous]
            lnums.numbers[lnums.previous] = urwid.Text(prev.text, align='right')

            lnums.numbers[focus_pos] = urwid.AttrWrap(foc, 'key')
            lnums.previous = focus_pos

    def switch_states(self, state):
        # this method is run to switch states, it reassigns what content is in the Frame
        if state == 'editor':
            self.top.contents['header'] = (self.status, None)
            self.top.contents['body'] = (self.body_col, None)
            self.top.contents['footer'] = (self.foot_col, None)
            if self.layout:
                self.top.contents['footer'] = (self.status, None)
                self.top.contents['header'] = (self.foot_col, None)

        elif state == 'openfile':
            path = strip_path(self.listbox.fname)
            self.browser = urwid.TreeListBox(urwid.TreeWalker(DirectoryNode(path, self)))
            self.top.contents['header'] = (self.oftbar, None)
            self.top.contents['body'] = (self.browser, None)
            self.top.contents['footer'] = (self.ofbbar, None)
            self.ofbbar.set_text('')

        self.state = state

    def toggle_line_numbers(self):
        self.show_lnums = not self.show_lnums
        if self.show_lnums:
            self.line_nums.populate(self.listbox.lines)
            lns = urwid.AttrMap(self.line_nums, 'body')
            self.body_col = urwid.Columns([(self.line_nums.width+2, lns), self.listbox], focus_column=1)
        else:
            self.body_col.contents.pop(0)
        self.top.contents['body'] = (self.body_col, None)

    def toggle_term(self):
        self.show_term = not self.show_term
        if self.show_term:
            cols, rows = self.loop.screen.get_cols_rows()
            height = min(25, rows/2)
            pile = self.pile
            pile.contents.append((self.termbox, pile.options(height_type='given', height_amount=height)))
            pile.focus_position = 1
            self.term.main_loop = self.loop
        else:
            self.pile.contents.pop(-1)

    def toggle_layout(self):
        self.layout = not self.layout
        content = self.top.contents
        content['header'], content['footer'] = content['footer'], content['header']

    def open_tabs(self):
        # this method reads the saved tabs from the data file and opens the files on start up
        with open(TABS_PATH, 'r') as f:
            lines = [line.strip('\n') for line in f.readlines()]
        if len(lines) == 0:
            with open(TABS_PATH, 'w') as f:
                f.write(START_PATH + '\n')
                f.write('False')
            self.listbox.populate(START_PATH)

        for line in lines:
            if line != lines[-1]:
                self.listbox.populate(line)
            else:
                if line == 'True':
                    self.toggle_layout()

        self.save_tabs()

    def save_tabs(self):
        # this method is run whenever a tab is opened or closed, it writes
        # the current open file names to a data file to be read on start up
        with open(TABS_PATH, 'w') as f:
            for tab in self.file_names:
                f.write(tab + '\n')

    def keypress(self, k):
        # this method handles any keypresses that are unhandled by other widgets
        foc = self.top.focus_position
        # these conditionals will only be run if other widgets didnt handle them already, if right
        # or left keypresses go unhandled we know we are at the beginning or end of a line
        if k == 'left':
            self.loop.process_input(['up'])
            self.listbox.focus.set_edit_pos(len(self.listbox.focus.edit_text))

        elif k == 'right' and self.state != 'openfile':
            self.loop.process_input(['down'])
            self.listbox.focus.set_edit_pos(0)

        elif k == 'backspace':
            # Right here we run combine_previous() to combine the
            # current text line with the one prior. This function
            # returns the length of the previous line. We have to wait to set the edit_pos
            # because self.loop.process_input changes the edit_pos
            if self.listbox.focus_position != 0:
                self.line_nums.sub()
            self.listbox.combine_previous()
            self.cur_tab.undo.log('backspace', [self.listbox.focus_position, self.listbox.focus.edit_pos], 1)

        elif k == 'delete':
            self.listbox.combine_next()
            self.cur_tab.undo.log('backspace', [self.listbox.focus_position, self.listbox.focus.edit_pos], 1)

        # this keypress opens up the configuration file so it can be edited
        elif k == self.config['config']:
            self.listbox.populate(CONFIG_PATH)

        # this keypress saves the changes of the config file and updates everything

        elif k == self.config['delline']:
            if self.listbox.focus_position == 0 and len(self.listbox.lines) == 1:
                self.listbox.focus.set_edit_text('')
                return

            self.cur_tab.undo.log(self.listbox.focus.edit_text+'\n', [self.listbox.focus_position, 0], 1)
            self.line_nums.sub()
            self.listbox.del_line()

        elif k == self.config['layout']:
            self.toggle_layout()

        elif k == self.config['linenum']:
            self.toggle_line_numbers()

        elif k == self.config['terminal']:
            self.toggle_term()

        elif k == self.config['open']:
            self.new_files = []
            self.browser = urwid.TreeListBox(urwid.TreeWalker(DirectoryNode(self.cwd, self)))
            self.browser.offset_rows = 1
            self.switch_states('openfile')

        # this keypress only registers when enter is pressed in the open file state, otherwise the
        # editor would have handled it. This means we need to open the selected files if there are any
        # and set the state back to editor mode

        elif k == 'enter':
            if self.state == 'openfile':
                self.switch_states('editor')
                if len(self.new_files) > 0:
                    for fname in self.new_files:
                        self.listbox.populate(fname)
                else:
                    self.listbox.populate(self.file_names[0])

                self.new_files = []
                self.save_tabs()

        elif k == self.config['find']:
            self.finding = True
            self.top.contents['footer'] = (self.fedit, None)

        elif k == self.config['undo']:
            self.cur_tab.undo.undo()
            self.update_line_numbers()

        elif k == 'ctrl x':
            # get outta here!
            raise urwid.ExitMainLoop()

        # user needs help... so give them this help file I guess.
        elif k == 'esc':
            self.listbox.populate(HELP_PATH)

    def register_palette(self):
        """Converts pygmets style to urwid palatte"""
        default = 'default'
        palette = list(self.palette)
        mapping = CONFIG['rgb_to_short']
        for tok in self.style.styles.keys():
            for t in tok.split()[::-1]:
                st = self.style.styles[t]
                if '#' in st:
                    break
            if '#' not in st:
                st = ''
            st = st.split()
            st.sort()   # '#' comes before '[A-Za-z0-9]'
            if len(st) == 0:
                c = default
            elif st[0].startswith('bg:'):
                c = default
            elif len(st[0]) == 7:
                c = 'h' + rgb_to_short(st[0][1:], mapping)[0]
            elif len(st[0]) == 4:
                c = 'h' + rgb_to_short(st[0][1]*2 + st[0][2]*2 + st[0][3]*2, mapping)[0]
            else:
                c = default
            a = urwid.AttrSpec(c, default, colors=256)
            row = (tok, default, default, default, a.foreground, default)
            palette.append(row)
        self.loop.screen.register_palette(palette)

