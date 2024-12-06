"""Look for bare [link] tags and convert then to [link](link).
        
The annoying part about this is that we don't want to process this
inside verbatim blocks, so we hack a parser of sorts.
"""
from flask import Flask
from wikmd.config import WikmdConfig


def _find_exact(line, char, count):
    c = 0
    found = 0
    while c < len(line):
        if line[c] == char:
            found += 1
        elif found == count:
            return c - 1
        else:
            found = 0
        c += 1
    if found == count:
        return c - 1
    return -1

def process_md(md: str) -> str:
    in_verbatim = False
    tick_count = 0
    lines = md.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        # skip verbatim blocks with four spaces or >
        if line.startswith('    ') or line.lstrip().startswith('>'):
            continue
        # check for ending backtick verbatim block
        if tick_count:
            if line.lstrip().startswith('`' * tick_count):
                tick_count = 0
                # whether we found it or not, skip this line
            continue
        c = 0
        link_start = -1
        while c < len(line):
            # check for a verbatim
            if line[c] == '`':
                # slurp opening ticks
                tc = 0
                while c < len(line) and line[c] == '`':
                    tc += 1
                    c += 1
                    # lookahead for closing ticks
                n = _find_exact(line[c:], '`', tc)
                if n == -1:
                    if tc > 2:
                        # it was start of a ``` block
                        tick_count = tc
                        break
                    # it was a lone ` or ``
                    continue
                # advance to closing ticks and continue
                c += n
                continue
                
            # check for links
            if line[c] == '[':
                # slurp opening [
                tc = 0
                while line[c] == '[' and c < len(line):
                    tc += 1
                    c += 1
                # lookahead for closing ]
                n = _find_exact(line[c:], ']', tc)
                if n == -1:
                    # didn't find it
                    continue
                start = c
                c += n
                # if it was 1, do link manipulation
                if tc == 1 and (
                        # doesn't have following paren
                        (len(line) < c+2 or line[c+1] != '(') and
                        # is not empty brackets
                        n>0):
                    line = line[:c+1] + '(' + line[start:c] + ')' + line[c+1:]
                    c += n + 2

            # nothing, advance
            c += 1
        lines[i] = line
    return '\n'.join(lines)

class Plugin:
    def get_plugin_name(self) -> str:
        return "quick_links"

    def process_md_before_html_convert(self, md: str) -> str:
        return process_md(md)

    def __init__(self, flask_app: Flask, config: WikmdConfig, web_dep):
        self.name = "quick_links"
        self.plugname = "quick_links"
        self.flask_app = flask_app
        self.config = config
        self.web_dep = web_dep
    
                    
# TODO: test this, ugh
                    
                
