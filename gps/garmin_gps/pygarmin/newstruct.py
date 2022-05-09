#!/usr/bin/env python
"""
   newstruct

   Very quickly hacked layer over the struct module to handle
   null-terminated strings.

   In the format string, an 's' is interpreted as a null-terminated
   string, rather than a string of length 1.

   This is released under the Gnu General Public Licence. A copy of
   this can be found at http://www.opensource.org/licenses/gpl-license.html

   (c) 2000 James A. H. Skillen <jahs@jahs.net>

"""

from struct import *
import struct


import re

START = re.compile("^[ ]*[@=<>!]")
TOKEN = re.compile("[ ]*([0-9]*)([xcbBhHiIlLfdspP])")

def pack(fmt, *args):
    endian, tokens = _parse(fmt)
    fmt = [ endian ]
    args = list(args)
    for i in range(len(tokens)):
        if isinstance(args[i], str): args[i] = args[i].encode()
        if tokens[i][1] == "s" and tokens[i][0] == "":
            if isinstance(args[i], str):
                args[i] = args[i].encode()
            if isinstance(args[i], dict):
                args[i] = str(args[i]).encode()
            args[i] = args[i] + b"\000"
            tokens[i][0] = str(len(args[i]))
        fmt.append(''.join(tokens[i]))
    args.insert(0, ''.join(fmt))
    return struct.pack(*args)

def _parse(fmt):
    if START.match(fmt) is not None:
        endian = fmt[0]
        fmt = fmt[1:]
    else:
        endian = "@"
    tokens = []
    while fmt != "":
        m = TOKEN.match(fmt)
        if m is None:
            raise error("bad char in struct format")
        tokens.append(list(m.groups()))
        fmt = fmt[m.end():]
    return (endian, tokens)

def unpack(fmt, string):
    endian, tokens = _parse(fmt)
    unpacked = []
    buffer = [ endian ]
    for i in range(len(tokens)):
        if tokens[i][1] == "s" and tokens[i][0] == "":
            if len(buffer) > 1:
                format = ''.join(buffer)
                size = struct.calcsize(format)
                unpacked = unpacked + list(struct.unpack(format, string[:size]))
                string = string[size:]
                buffer = [ endian ]
            index = string.find(b'\x00')
            unpacked.append(string[:index])
            string = string[index+1:]
        else:
            buffer.append(''.join(tokens[i]))
    if len(buffer) > 1:
        format = ''.join(buffer)
        size = struct.calcsize(format)
        unpacked = unpacked + list(struct.unpack(format, string[:size]))
    return tuple(unpacked)

def calcsize(fmt):
    endian, tokens = _parse(fmt)
    for num, type in tokens:
        if type == "s" and num == "":
            return None  # FIXME hehe - we don't know the length...
    return struct.calcsize(fmt)
