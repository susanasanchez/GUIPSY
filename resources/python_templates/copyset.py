#!/usr/bin/env python
from gipsy import *

init()
setin = Set(usertext("INSET=", "Set, subset:"))
anyout("flo= %s, fhi= %s" % (setin.slo, setin.shi))

# Prepare to enter a box

boxmes = 'Enter box in '
for k in setin.axperm('inside'):
    boxmes += str(setin.axname(k)) + ' '
boxmes += '   [entire subset]'
b = usertext("BOX=", boxmes, defval='', default=1)
setin.setbox(b)
anyout( "blo=%s bhi=%s" % (setin.blo,setin.bhi) )

outname = usertext("OUTSET=", "Name of output set: ")
setout=setin.copy( outname )

userexpr = usertext("EXPR=", "Enter expression f(x,y,data): ")

# Start to loop over all subsets. You need both the coordinate words 
# of the input set and the output set.

for s in range( len(setin.subsets) ):
   Min  = setin.subimage(setin.subsets[s])
   Mout = setout.subimage(setout.subsets[s])

   for y in range(setin.blo[1],setin.bhi[1]+1):
      iy = y - setin.blo[1]
      for x in range(setin.blo[0],setin.bhi[0]+1):
         ix = x - setin.blo[0]
         data = Min[iy,ix]
         Min[iy,ix] = eval(userexpr)

   Mout[:] = Min                     # Copy subset data to output set
   setout.wminmax(setout.subsets[s]) # Update header items DATAMIN,DATAMAX,NBLANK

setout.whistory()                    # Save history to header
del setin
del setout

finis()
