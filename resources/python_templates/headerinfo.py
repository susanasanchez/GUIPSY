#!/usr/bin/env python
from gipsy import *

init()

s = Set(usertext(message="Setname"), write=True)

dim = s.naxis
anyout( "Dimension of set: %d" % dim )

# Get coordinate words of first data point in set and of the last one
lo, hi = s.range(0)

# Print the axis name and the range in grids for all the axes in the set
for i in range(dim):
   anyout("%s: from %d to %d" % (s.axname(i), s.grid(i, lo), s.grid(i, hi)))

# Print the value of a header item (at set level)
t = s[0, 'INSTRUME']
anyout( str(t) )


s[0, 'OBSERVER'] = 'Me'        # Change the value of a header item.
s['TEMPHEAD'] = None           # Delete item 'TEMPHEAD' on set level (=0)

del s                          # Close the set

finis()
