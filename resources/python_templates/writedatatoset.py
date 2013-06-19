#!/usr/bin/env python
from gipsy import *

init()

name = usertext(message="Set name")

s = Set(name, write=True)

i = s.image

val = userreal("value=", "Enter value to fill set")
anyout( str(val) )

# Entire set is set to this value
i[:] = val

del s
finis()
