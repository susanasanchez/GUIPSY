#!/usr/bin/env python
from gipsy import *

init()

while True:
   input = usertext("SET=", "Set, (subsets)")
   cancel("SET=")
   s = Set(input)
   anyout("set opened with: %s" % s.spec)
   anyout("set name       : %s" % s.name)
   anyout("subsets        : %s" % str(s.subsets))
   anyout("axperm         : %s" % str(s.axperm()))
   anyout("Axis in fixed order of set:" )

   for ax in s.axes():
      anyout( "Name = %-10s from %5d to %5d  grid 0 is %10g %-10s" % (
        ax.name, ax.slo, ax.shi, ax.crval, ax.cunit ) )

   anyout("Axis in order of user input:" )
   for a in s.axes( True, 'inside' ):
      anyout( "%s (subset axis)" % a.name )

   for a in s.axes( True, 'outside' ):
      anyout( "%s (repeat axis)" % a.name )

   del s

finis()
