#!/usr/bin/env python
from gipsy import *

init()

input = usertext("SET=", "Set, (subsets)")
s = Set(input)

ndim = s.ndims( subset=True )
x = userdble( "GRIDS=", "Enter position in subset (%d numbers): " % ndim, nmax=ndim )
anyout( "grid = %s" % str(x) )

axnames = ''
for a in s.axes( True, 'inside' ):
   axnames += a.name + '(s) '

for a in s.axes( True, 'outside' ):
   axnames += a.name + '(r) '

anyout( axnames )

for cword in s.subsets:
   p = s.tophys( x, cword, 'inside' )
   po = s.tophys( x, cword, 'outside' )

   #  Get the grids of the position of the subset on the repeat axes
   #  Method 1, use axis permutation array and grid() method
   #  st = ''
   #  for k in s.axperm('outside'):
   #     st += str(s.grid(k,cword))+ ' '

   # Method 2, use the axes() method for this subset. The repeat axes
   # need a coordinate word.
   st = ''
   for a in s.axes( cword, 'outside' ):
       st += str(a.blo) + ' '


   anyout( "%s repeat: (%s)=%s" % (str(p), st, str(po)) )

del s


finis()
