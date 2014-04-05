#!/usr/local/bin/python

usage = """
    Reads an input CSS file and prints the CSS as a greyscale version

    Usage:
    chmod +x grey.py
    ./grey.py in.css
    """

import sys
import json
import re

def greyscale(css):
    # fetch all html colour names
    colours = []
    with open('colours.json') as json_data:
        colours = json.load(json_data)

    # not very safe pattern... might capture inside css values
    colour_names_pattern = "(%s)(?!\w)" % '|'.join(colours.keys())
    colour_names_regex = re.compile(colour_names_pattern)

    # replace colour names with hex values
    def replName(m):
        colour = m.group(1)
        return colours[colour]['hex']
    css = re.sub(colour_names_pattern, replName, css, flags=re.I)

    # we only want 6 digit hex values, convert the others
    css = re.sub("#([a-f\d])([a-f\d])([a-f\d])(?![a-f\d])", r"#\1\1\2\2\3\3", css, flags=re.I)

    # now turn all colours to greyscale
    def replHex(m):
        r = int(m.group(1), 16)
        g = int(m.group(2), 16)
        b = int(m.group(3), 16)

        grey = (r+g+b)/3
        return "#%s%s%s" % tuple([hex(grey)[2:4]]*3)
    css = re.sub("#([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})", replHex, css, flags=re.I)

    return css

if __name__ == "__main__":

    if len(sys.argv) <= 1:
        exit(usage)

    with open(sys.argv[1]) as f:
        css = f.read()
        print(greyscale(css))
