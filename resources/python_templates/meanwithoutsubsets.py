#!/usr/bin/env python
from gipsy import *

init()                  # Contact Hermes

# Get the name of the GIPSY set by prompting with a default keyword INPUT=
name = usertext(message="Set name")

s = Set(name)           # Create set object s

i = s.image             # Extract the image part of the set object

k = i.shape[0]          # Length of first element = last axis

# Loop over all subsets
for j in range(0,k):
   m = i[j]             # Extract a subset along the last axis. Note that
                        # i[j] is an abbreviation of the array slice i[j,:,:]
   me = m.mean()        # Get the mean of this subset

   anyout( "mean of channel "+str(j)+" = "+str(me) )


del s                   # Release the object

finis()                 # Disconnect Hermes
