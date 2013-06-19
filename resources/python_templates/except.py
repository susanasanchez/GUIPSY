#!/usr/bin/env python
from gipsy import *

init()

name = usertext(message="Set name")

try:
   s = Set(name)
except GipsyError, msg:
   error(4,str(msg))

del s

finis()
