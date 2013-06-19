#!/usr/bin/env python
from gipsy import *

init()

# example 1: Repeat over user input until program agrees with input
# The reject shows a message and cancels the keyword input so it can
# be entered again

ok = False
keyword = "NUMBER1="
while not ok:
   x = userreal(keyword, "Enter a number:", 0, 0, 1)   
   anyout( str(x) )
   if x >= 0 :
      ok = True
   else:
      reject( keyword, "Negative value not allowed" )


# example 2: Repeat over user input. Cancel the keyword.
# Note that we are using the default value for the keyword because
# we did not specify the parameter keyword=

attempt = 1
while True:
   v = userreal(nmax=1, default=1, message='Enter number (attempt %d):'% attempt)
   anyout(str(v))
   cancel()
   attempt += 1

finis()
