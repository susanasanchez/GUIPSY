#!/usr/bin/env python
from gipsy import *

init()

# Syntax: x = userreal(keyword="INPUT=", message=None, default=0, defval=0.0, nmax=1)
# example 1: All arguments are default

x = userreal()
anyout( str(x) )


# example 2: Specify everything

x = userreal(keyword="NUMBER2=", message="Give one value: [10.3]", 
             default=1, defval=10.3, nmax=1 )
anyout( str(x) )


# example 3: Specify everything, but in fixed order so that you can omit
# the argument names

x = userreal("NUMBER3=", "Give one value: [10.3]", 1, 10.3, 1 )
anyout( str(x) )


# example 4: Get a list of n numbers. Now 'x' is a list so you can
# index the individual numbers


x = userreal("NUMBER4=", "Give max. 10 values", 1, (1.3), 10 )
anyout( str(x) )
anyout( "Number = %f" % x[0] )


# example 5: Get a list of n numbers. with defaults

x = userreal("NUMBER5=", "Give max. 10 values", 1, (1,2,3,4), 10 )
anyout( str(x) )
anyout( "First Number = %f" % x[0] )

finis()
      
