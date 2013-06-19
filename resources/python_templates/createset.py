#!/usr/bin/env python
from gipsy import *

init()

name = usertext(message="Set name")

s = Set(name, create=True)      # Mode 'create' creates a new set

s.extend("RA",   10, 5)         # Create an axis. Parameters: Name, length, origin
s.extend("DEC",  15, 4)
s.extend("FREQ",  0,  3)

i = s.image                     # Now you can create its data
anyout( str(s.slo) )
anyout( str(s.shi) )

i[:] = range(5)                 # Fill with numbers

x = i[1,:,]                     # Get a slice

anyout(str(x))
anyout(str(x.shape))

del s

finis()
